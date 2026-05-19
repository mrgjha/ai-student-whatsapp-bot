import sqlite3

conn = sqlite3.connect("students.db")

cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS students (

    id INTEGER PRIMARY KEY,

    name TEXT,

    phone TEXT,

    address TEXT,

    feestatus TEXT
)
""")

students = [

    (
        1,
        "Gyanendra Jha",
        "YOUR_PHONE_NUMBER",
        "Mithapur",
        "Paid"
    )

]

cur.executemany(
    """
    INSERT OR REPLACE INTO students
    VALUES (?, ?, ?, ?, ?)
    """,
    students
)

conn.commit()

print("Database created")

conn.close()