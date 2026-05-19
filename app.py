from flask import Flask
from flask import request

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
# HOME ROUTE
# ==========================================

@app.route("/")
def home():

    return "AI WhatsApp Student Bot Running"

# ==========================================
# HEALTH ROUTE
# ==========================================

@app.route("/health")
def health():

    return "healthy"

# ==========================================
# WHATSAPP ROUTE
# ==========================================

@app.route("/whatsapp", methods=["GET", "POST"])
def whatsapp():

    try:

        # ==========================================
        # RECEIVE MESSAGE
        # ==========================================

        incoming_msg = request.form.get(
            "Body",
            ""
        ).lower()

        # ==========================================
        # RECEIVE PHONE NUMBER
        # ==========================================

        sender = request.form.get(
            "From",
            ""
        )

        sender = sender.replace(
            "whatsapp:+91",
            ""
        )

        print("Sender:", sender)

        print("Message:", incoming_msg)

        # ==========================================
        # DATABASE CONNECTION
        # ==========================================

        conn = sqlite3.connect(
            "students.db"
        )

        cur = conn.cursor()

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
        # TWILIO RESPONSE
        # ==========================================

        resp = MessagingResponse()

        msg = resp.message()

        # ==========================================
        # STUDENT NOT FOUND
        # ==========================================

        if not student:

            msg.body(
                "Student not found in database."
            )

            conn.close()

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
        # SIMPLE RULE-BASED RESPONSES
        # ==========================================

        if "fee" in incoming_msg:

            reply = (
                f"Your fee status is "
                f"{fee_status}."
            )

        elif "id" in incoming_msg:

            reply = (
                f"Your Student ID is "
                f"{student_id}."
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
            You are a helpful AI student assistant.

            Student Information:

            Name: {name}

            Student ID: {student_id}

            Phone: {phone}

            Address: {address}

            Fee Status: {fee_status}

            Student Question:
            {incoming_msg}

            Reply politely and briefly.
            """

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            reply = response.text

        # ==========================================
        # SEND WHATSAPP RESPONSE
        # ==========================================

        msg.body(reply)

        conn.close()

        return str(resp)

    except Exception as e:

        return str(e), 500