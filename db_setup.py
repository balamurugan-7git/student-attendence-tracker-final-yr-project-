import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    with open('database.sql', 'r') as f:
        conn.executescript(f.read())
    
    # Add a default admin if not exists
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE role = 'admin'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)", 
                       ('Admin', 'admin@example.com', 'admin123', 'admin'))
    
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    init_db()
