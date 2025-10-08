import sqlite3

DB_NAME = "DataBase.SQLite"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
     CREATE TABLE IF NOT EXISTS incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT NOT NULL,
        type TEXT NOT NULL 
    )
    """) 

    cur.execute("""
     CREATE TABLE IF NOT EXISTS tickets(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer TEXT NOT NULL,
        service TEXT NOT NULL,
        incident_id INTEGER NOT NULL,
        status TEXT NOT NULL,
        creation_date TEXT NOT NULL,
        closing_date TEXT,
        FOREIGN KEY (incient_id) REFERENCES incidents (id)      
    )
    """)

    conn.commit()
    conn.close()
