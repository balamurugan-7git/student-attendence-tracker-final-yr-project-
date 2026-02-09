import sqlite3

def seed():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Add a Data Analytics exam
    cursor.execute("INSERT INTO exams (exam_name, duration, total_marks) VALUES (?, ?, ?)", 
                   ('Data Analytics Fundamentals', 15, 50))
    exam_id = cursor.lastrowid
    
    # Add High-Quality Data Analytics questions
    questions = [
        ('Which library is used for data manipulation in Python?', 'Matplotlib', 'Pandas', 'Requests', 'Flask', 'b'),
        ('What is the term for a row in a Pandas DataFrame?', 'Series', 'Column', 'Observation/Index', 'List', 'c'),
        ('Which of these is a measure of dispersion?', 'Mean', 'Median', 'Standard Deviation', 'Mode', 'c'),
        ('What does ETL stand for in Data Engineering?', 'Extract, Transform, Load', 'Edit, Test, Log', 'Enable, Transfer, Load', 'Extract, Time, Loop', 'a'),
        ('Which type of plot is best for visualizing a distribution?', 'Line Chart', 'Pie Chart', 'Histogram', 'Scatter Plot', 'c')
    ]
    
    for q, a, b, c, d, correct in questions:
        cursor.execute("""
            INSERT INTO questions (exam_id, question, option_a, option_b, option_c, option_d, correct_answer) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (exam_id, q, a, b, c, d, correct))
    
    conn.commit()
    conn.close()
    print("Seed data added successfully.")

if __name__ == "__main__":
    seed()
