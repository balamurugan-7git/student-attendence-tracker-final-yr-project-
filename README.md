# Online Examination System

A secure, web-based examination platform built with Python (Flask), SQLite, HTML, and modern CSS.

## 🚀 Features
- **Secure Authentication**: Session-based login for Students and Admins.
- **Student Dashboard**: Take exams, view scores, and track progress.
- **Admin Dashboard**: Create exams, add questions, and view student performance.
- **Automated Evaluation**: Real-time MCQ assessment.
- **Timed Exams**: Built-in countdown timer with auto-submission.
- **Modern UI**: Dark-themed glassmorphism design.

## 🛠️ Technology Stack
- **Frontend**: HTML5, Vanilla CSS3 (Glassmorphism), JavaScript
- **Backend**: Python (Flask)
- **Database**: SQLite (SQL)

## 📂 Project Structure
```
online_exam/
├── static/
│   └── css/style.css
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── exam.html
│   ├── result.html
│   └── admin.html
├── app.py
├── db_setup.py
├── database.sql
└── README.md
```

## ⚙️ How to Run the Project

### Option 1: One-Click Setup (Recommended)
Simply double-click the **`verify_system.bat`** file. This will:
1.  Install required libraries (`flask`, `requests`).
2.  Initialize the database and add sample data.
3.  Start the server and run an automated test to verify everything works.

### Option 2: Manual Run
1.  **Install Flask**: `pip install flask`
2.  **Initialize Database**: `python db_setup.py`
3.  **Run Server**: `python app.py`
4.  **Access**: Open `http://127.0.0.1:5000` in your browser.

## 🧑‍💻 Login Credentials
- **Admin**: `admin@example.com` / `admin123`
- **Student**: Register a new account on the landing page!

---
*Developed for Final Year Project - 2026*
