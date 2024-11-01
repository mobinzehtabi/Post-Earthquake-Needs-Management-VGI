import sqlite3

def init_db():
    conn = sqlite3.connect('requests.db')
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            location TEXT NOT NULL
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS need (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            water BOOLEAN NOT NULL,
            food BOOLEAN NOT NULL,
            medical_supplies BOOLEAN NOT NULL,
            shelter BOOLEAN NOT NULL,
            other TEXT,
            FOREIGN KEY (user_id) REFERENCES user (id)
        )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
