import sqlite3

# ==========================================
# CONNECT DATABASE
# ==========================================

conn = sqlite3.connect("students.db")

cur = conn.cursor()

# ==========================================
# CREATE STUDENTS TABLE
# ==========================================

cur.execute("""
CREATE TABLE IF NOT EXISTS students (

    id INTEGER PRIMARY KEY,

    name TEXT,

    phone TEXT,

    address TEXT,

    feestatus TEXT
)
""")

# ==========================================
# CREATE CHATS TABLE
# ==========================================

cur.execute("""
CREATE TABLE IF NOT EXISTS chats (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    phone TEXT,

    user_message TEXT,

    bot_reply TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# ==========================================
# INSERT SAMPLE STUDENT
# ==========================================

students = [

    (
        1,
        "Gyanendra Jha",
        "8951539438",
        "Mithapur",
        "Paid"
    )

]

# ==========================================
# INSERT DATA
# ==========================================

cur.executemany(
    """
    INSERT OR REPLACE INTO students
    VALUES (?, ?, ?, ?, ?)
    """,
    students
)

# ==========================================
# SAVE CHANGES
# ==========================================

conn.commit()

print("Database and tables created successfully")

conn.close()