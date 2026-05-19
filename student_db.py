import sqlite3

# ==========================================
# CONNECT DATABASE
# ==========================================

conn = sqlite3.connect(
    "students.db"
)

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

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# ==========================================
# SAMPLE STUDENT
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
# INSERT SAMPLE DATA
# ==========================================

cur.executemany(
    """
    INSERT OR REPLACE INTO students
    VALUES (?, ?, ?, ?, ?)
    """,
    students
)

conn.commit()

print("Database created successfully")

conn.close()