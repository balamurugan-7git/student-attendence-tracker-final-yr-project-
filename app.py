from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database Helper
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Login Required Decorator
def login_required(role=None):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please login first.', 'warning')
                return redirect(url_for('login'))
            if role and session.get('role') != role:
                flash('Access denied.', 'error')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return wrapper

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password)).fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user['user_id']
            session['name'] = user['name']
            session['role'] = user['role']
            flash(f"Welcome back, {user['name']}!", 'success')
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid email or password.", 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = 'student' # Default role
        
        conn = get_db_connection()
        try:
            conn.execute("INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)", 
                         (name, email, password, role))
            conn.commit()
            flash("Registration successful! Please login.", 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Email already exists.", 'error')
        finally:
            conn.close()
            
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required()
def dashboard():
    conn = get_db_connection()
    if session['role'] == 'admin':
        exams = conn.execute("SELECT * FROM exams").fetchall()
        users_count = conn.execute("SELECT COUNT(*) FROM users WHERE role='student'").fetchone()[0]
        exams_count = len(exams)
        return render_template('admin.html', exams=exams, users_count=users_count, exams_count=exams_count)
    else:
        exams = conn.execute("SELECT * FROM exams").fetchall()
        results = conn.execute("SELECT r.*, e.exam_name FROM results r JOIN exams e ON r.exam_id = e.exam_id WHERE r.user_id = ?", 
                               (session['user_id'],)).fetchall()
        return render_template('dashboard.html', exams=exams, results=results)

@app.route('/take_exam/<int:exam_id>')
@login_required('student')
def take_exam(exam_id):
    conn = get_db_connection()
    exam = conn.execute("SELECT * FROM exams WHERE exam_id = ?", (exam_id,)).fetchone()
    questions = conn.execute("SELECT * FROM questions WHERE exam_id = ?", (exam_id,)).fetchall()
    conn.close()
    
    if not questions:
        flash("No questions found for this exam.", 'warning')
        return redirect(url_for('dashboard'))
    
    # Randomize questions for different students
    import random
    questions_list = list(questions)
    random.shuffle(questions_list)
        
    return render_template('exam.html', exam=exam, questions=questions_list)

@app.route('/submit_exam', methods=['POST'])
@login_required('student')
def submit_exam():
    exam_id = request.form.get('exam_id')
    user_id = session['user_id']
    
    conn = get_db_connection()
    questions = conn.execute("SELECT * FROM questions WHERE exam_id = ?", (exam_id,)).fetchall()
    
    score = 0
    total_marks = 0 # This could also be pulled from the exam table
    
    for q in questions:
        answer = request.form.get(f"question_{q['question_id']}")
        if answer == q['correct_answer']:
            score += 1
    
    # Store result
    conn.execute("INSERT INTO results (user_id, exam_id, score) VALUES (?, ?, ?)", 
                 (user_id, exam_id, score))
    conn.commit()
    conn.close()
    
    return redirect(url_for('view_result', exam_id=exam_id, score=score))

@app.route('/view_result')
@login_required('student')
def view_result():
    exam_id = request.args.get('exam_id')
    score = request.args.get('score')
    conn = get_db_connection()
    exam = conn.execute("SELECT * FROM exams WHERE exam_id = ?", (exam_id,)).fetchone()
    conn.close()
    return render_template('result.html', exam=exam, score=score)

@app.route('/certificate/<int:exam_id>/<int:score>')
@login_required('student')
def certificate(exam_id, score):
    conn = get_db_connection()
    exam = conn.execute("SELECT * FROM exams WHERE exam_id = ?", (exam_id,)).fetchone()
    conn.close()
    return render_template('certificate.html', exam=exam, score=score, name=session['name'])

@app.route('/admin/attendance')
@login_required('admin')
def admin_attendance():
    conn = get_db_connection()
    # Join results with users and exams to show who took what and when
    attendance = conn.execute("""
        SELECT r.date, u.name as student_name, u.email, e.exam_name, r.score, e.total_marks
        FROM results r
        JOIN users u ON r.user_id = u.user_id
        JOIN exams e ON r.exam_id = e.exam_id
        ORDER BY r.date DESC
    """).fetchall()
    conn.close()
    return render_template('attendance.html', attendance=attendance)

# Admin Routes
@app.route('/admin/add_exam', methods=['POST'])
@login_required('admin')
def add_exam():
    name = request.form['exam_name']
    duration = request.form['duration']
    total_marks = request.form['total_marks']
    
    conn = get_db_connection()
    conn.execute("INSERT INTO exams (exam_name, duration, total_marks) VALUES (?, ?, ?)", 
                 (name, duration, total_marks))
    conn.commit()
    conn.close()
    flash("Exam added successfully!", 'success')
    return redirect(url_for('dashboard'))

@app.route('/admin/add_question', methods=['POST'])
@login_required('admin')
def add_question():
    exam_id = request.form['exam_id']
    question = request.form['question']
    opt_a = request.form['option_a']
    opt_b = request.form['option_b']
    opt_c = request.form['option_c']
    opt_d = request.form['option_d']
    correct = request.form['correct_answer']
    
    conn = get_db_connection()
    conn.execute("INSERT INTO questions (exam_id, question, option_a, option_b, option_c, option_d, correct_answer) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                 (exam_id, question, opt_a, opt_b, opt_c, opt_d, correct))
    conn.commit()
    conn.close()
    flash("Question added successfully!", 'success')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
