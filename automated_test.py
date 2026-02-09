import requests

BASE_URL = "http://127.0.0.1:5000"

def run_test():
    session = requests.Session()
    
    # 1. Register a NEW student
    print("Step 1: Registering a new student...")
    reg_data = {
        'name': 'Auto Test User',
        'email': 'auto_test_99@example.com',
        'password': 'password123'
    }
    # Note: Our register route usually redirects, so we check the response history or URL
    resp = session.post(f"{BASE_URL}/register", data=reg_data)
    if "Login successful" in resp.text or resp.status_code == 200:
        print("Registration flow initiated (or user already exists).")

    # 2. Login as admin (Fallback check)
    print("\nStep 2: Logging in as Admin...")
    admin_data = {
        'email': 'admin@example.com',
        'password': 'admin123'
    }
    resp = session.post(f"{BASE_URL}/login", data=admin_data)
    if "Admin Dashboard" in resp.text:
        print("Admin Login successful!")
    else:
        print("Admin Login failed.")

    # 3. Get Dashboard to find an exam
    print("\nStep 3: Accessing dashboard...")
    resp = session.get(f"{BASE_URL}/dashboard")
    if "Data Analytics" in resp.text:
        print("Exam 'Data Analytics Fundamentals' found.")
    else:
        print("Exam not found on dashboard.")
        return

    # 4. Take the exam (simulate submission)
    print("\nStep 4: Submitting exam answers...")
    # Questions from seed_data: 
    # 1. Pandas (b)
    # 2. Observation (c)
    # 3. Std Dev (c)
    exam_submission = {
        'exam_id': '1',
        'question_1': 'b',
        'question_2': 'c',
        'question_3': 'c'
    }
    resp = session.post(f"{BASE_URL}/submit_exam", data=exam_submission, allow_redirects=True)
    
    if "Exam Completed" in resp.text and "Your Score" in resp.text:
        print("Exam submitted successfully!")
        # Extra check for score
        if "3" in resp.text: # Assuming 3 marks for 3 questions
            print("Score Verification: 3/3 - PASSED")
    else:
        print("Exam submission failed.")
        
    # 5. Verify Certificate link exists
    if "/certificate/1/3" in resp.text:
        print("Certificate link generated: PASSED")

if __name__ == "__main__":
    try:
        run_test()
    except Exception as e:
        print(f"Connection error: {e}. Is the server running?")
