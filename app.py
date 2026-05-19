from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

from google import genai

import sqlite3
import os

# ==========================================
# GEMINI CLIENT
# ==========================================

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# ==========================================
# FLASK APP
# ==========================================

app = Flask(__name__)

# ==========================================
# DATABASE CONNECTION
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

db_path = os.path.join(
    BASE_DIR,
    "students.db"
)

conn = sqlite3.connect(
    db_path,
    check_same_thread=False
)

cur = conn.cursor()

# ==========================================
# HOME ROUTE
# ==========================================

@app.route("/")
def home():

    return "AI WhatsApp Student Bot Running"

# ==========================================
# WHATSAPP ROUTE
# ==========================================

@app.route("/whatsapp", methods=["POST"])
def whatsapp():

    try:

        incoming_msg = request.form.get(
            "Body",
            ""
        ).lower()

        sender = request.form.get(
            "From",
            ""
        )

        sender = sender.replace(
            "whatsapp:",
            ""
        )

        # ==========================================
        # FIND STUDENT
        # ==========================================

        cur.execute(
            """
            SELECT *
            FROM students
            WHERE phone=?
            """,
            (sender,)
        )

        student = cur.fetchone()

        # ==========================================
        # RESPONSE OBJECT
        # ==========================================

        resp = MessagingResponse()
        msg = resp.message()

        # ==========================================
        # STUDENT NOT FOUND
        # ==========================================

        if not student:

            msg.body(
                "Your number is not registered."
            )

            return str(resp)

        # ==========================================
        # STUDENT DATA
        # ==========================================

        student_id = student[0]
        name = student[1]
        phone = student[2]
        address = student[3]
        fee_status = student[4]

        # ==========================================
        # SIMPLE RULES
        # ==========================================

        if "id" in incoming_msg:

            reply = f"Your Student ID is {student_id}."

        elif "fee" in incoming_msg:

            reply = (
                f"Your fee status is "
                f"{fee_status}."
            )

        elif "address" in incoming_msg \
        or "live" in incoming_msg:

            reply = (
                f"You live in "
                f"{address}."
            )

        # ==========================================
        # GEMINI AI RESPONSE
        # ==========================================

        else:

            prompt = f"""
            Student Information:

            Name: {name}
            Student ID: {student_id}
            Phone: {phone}
            Address: {address}
            Fee Status: {fee_status}

            User Question:
            {incoming_msg}

            Answer politely.
            """

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            reply = response.text

        # ==========================================
        # SAVE CHAT
        # ==========================================

        cur.execute(
            """
            INSERT INTO chats
            (
                phone,
                user_message,
                bot_reply
            )
            VALUES (?, ?, ?)
            """,
            (
                sender,
                incoming_msg,
                reply
            )
        )

        conn.commit()

        # ==========================================
        # SEND RESPONSE
        # ==========================================

        msg.body(reply)

        return str(resp)

    except Exception as e:

        return str(e), 500