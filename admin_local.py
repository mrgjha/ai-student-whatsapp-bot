import streamlit as st
import sqlite3
import pandas as pd

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="AI Student Admin Dashboard",
    page_icon="🎓",
    layout="wide"
)

# ==========================================
# DATABASE CONNECTION
# ==========================================

conn = sqlite3.connect(
    "students.db",
    check_same_thread=False
)

cur = conn.cursor()

# ==========================================
# TITLE
# ==========================================

st.title("🎓 AI Student Admin Dashboard")

st.markdown("---")

# ==========================================
# ANALYTICS SECTION
# ==========================================

total_students = cur.execute(
    """
    SELECT COUNT(*)
    FROM students
    """
).fetchone()[0]

paid_students = cur.execute(
    """
    SELECT COUNT(*)
    FROM students
    WHERE feestatus='Paid'
    """
).fetchone()[0]

pending_students = cur.execute(
    """
    SELECT COUNT(*)
    FROM students
    WHERE feestatus='Pending'
    """
).fetchone()[0]

total_chats = cur.execute(
    """
    SELECT COUNT(*)
    FROM chats
    """
).fetchone()[0]

# ==========================================
# METRICS CARDS
# ==========================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "👨‍🎓 Total Students",
    total_students
)

col2.metric(
    "✅ Paid",
    paid_students
)

col3.metric(
    "❌ Pending",
    pending_students
)

col4.metric(
    "💬 Total Chats",
    total_chats
)

st.markdown("---")

# ==========================================
# SIDEBAR MENU
# ==========================================

menu = st.sidebar.selectbox(
    "📌 Select Option",
    [
        "View Students",
        "Add Student",
        "Update Fee Status",
        "Delete Student",
        "View Chats"
    ]
)

# ==========================================
# VIEW STUDENTS
# ==========================================

if menu == "View Students":

    st.header("📋 Student Records")

    df = pd.read_sql_query(
        """
        SELECT *
        FROM students
        """,
        conn
    )

    st.dataframe(
        df,
        use_container_width=True
    )

# ==========================================
# ADD STUDENT
# ==========================================

elif menu == "Add Student":

    st.header("➕ Add New Student")

    student_id = st.number_input(
        "Student ID",
        step=1
    )

    name = st.text_input(
        "Student Name"
    )

    phone = st.text_input(
        "Phone Number"
    )

    address = st.text_input(
        "Address"
    )

    feestatus = st.selectbox(
        "Fee Status",
        [
            "Paid",
            "Pending"
        ]
    )

    if st.button("Add Student"):

        try:

            cur.execute(
                """
                INSERT INTO students
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    student_id,
                    name,
                    phone,
                    address,
                    feestatus
                )
            )

            conn.commit()

            st.success(
                "✅ Student Added Successfully"
            )

        except Exception as e:

            st.error(str(e))

# ==========================================
# UPDATE FEE STATUS
# ==========================================

elif menu == "Update Fee Status":

    st.header("💰 Update Fee Status")

    phone = st.text_input(
        "Enter Phone Number"
    )

    new_status = st.selectbox(
        "Select New Status",
        [
            "Paid",
            "Pending"
        ]
    )

    if st.button("Update"):

        cur.execute(
            """
            UPDATE students
            SET feestatus=?
            WHERE phone=?
            """,
            (
                new_status,
                phone
            )
        )

        conn.commit()

        st.success(
            "✅ Fee Status Updated"
        )

# ==========================================
# DELETE STUDENT
# ==========================================

elif menu == "Delete Student":

    st.header("🗑 Delete Student")

    phone = st.text_input(
        "Enter Phone Number"
    )

    if st.button("Delete"):

        cur.execute(
            """
            DELETE FROM students
            WHERE phone=?
            """,
            (phone,)
        )

        conn.commit()

        st.success(
            "✅ Student Deleted"
        )

# ==========================================
# VIEW CHAT HISTORY
# ==========================================

elif menu == "View Chats":

    st.header("💬 Chat History")

    df = pd.read_sql_query(
        """
        SELECT *
        FROM chats
        ORDER BY id DESC
        """,
        conn
    )

    st.dataframe(
        df,
        use_container_width=True
    )

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.caption(
    "🚀 AI WhatsApp Student Assistant Dashboard"
)