from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import sqlite3
from google import genai

# ==========================================
# GEMINI CLIENT
# ==========================================

client = genai.Client(
    api_key="AIzaSyD0DMHll6_puy8RrkULkbzlWjIlevYuMgo"
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
# WHATSAPP WEBHOOK
# ==========================================

@app.route("/whatsapp", methods=["POST"])
def whatsapp_bot():

    # ==========================================
    # RECEIVE MESSAGE
    # ==========================================

    incoming_msg = request.values.get(
        "Body",
        ""
    ).lower()

    # ==========================================
    # RECEIVE PHONE NUMBER
    # ==========================================

    phone = request.values.get(
        "From",
        ""
    )

    # Remove WhatsApp country code

    phone = phone.replace(
        "whatsapp:+91",
        ""
    )

    print("Phone:", phone)

    print("Message:", incoming_msg)

    # ==========================================
    # DATABASE CONNECTION
    # ==========================================

    conn = sqlite3.connect("students.db")

    cur = conn.cursor()

    # ==========================================
    # FIND STUDENT
    # ==========================================

    cur.execute(
        """
        SELECT * FROM students
        WHERE phone=?
        """,
        (phone,)
    )

    student = cur.fetchone()

    # ==========================================
    # TWILIO RESPONSE OBJECT
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

    student_phone = student[2]

    address = student[3]

    feestatus = student[4]

    # ==========================================
    # LOAD PREVIOUS CHAT HISTORY
    # ==========================================

    cur.execute(
        """
        SELECT user_message, bot_reply
        FROM chats
        WHERE phone=?
        ORDER BY id DESC
        LIMIT 5
        """,
        (phone,)
    )

    history = cur.fetchall()

    # ==========================================
    # BUILD CHAT CONTEXT
    # ==========================================

    chat_context = ""

    for chat in history:

        user_msg = chat[0]

        bot_msg = chat[1]

        chat_context += f"""
Student: {user_msg}
Bot: {bot_msg}
"""

    # ==========================================
    # STUDENT CONTEXT
    # ==========================================

    context = f"""
Student Information:

Student ID: {student_id}

Name: {name}

Phone: {student_phone}

Address: {address}

Fee Status: {feestatus}
"""

    # ==========================================
    # GEMINI PROMPT
    # ==========================================

    prompt = f"""
You are a helpful AI student assistant chatbot.

Student Information:
{context}

Previous Conversation:
{chat_context}

Current Student Question:
{incoming_msg}

Instructions:
- Reply naturally
- Reply briefly
- Use previous conversation if needed
- Use only provided student data
- Be professional
"""

    print("Prompt Created")

    # ==========================================
    # GEMINI RESPONSE
    # ==========================================

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        reply = response.text

        print("Gemini Response Generated")

    except Exception as e:

        reply = f"""
Gemini Error:
{str(e)}
"""

        print(reply)

    # ==========================================
    # SAVE CHAT HISTORY
    # ==========================================

    try:

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
                phone,
                incoming_msg,
                reply
            )
        )

        conn.commit()

        print("Chat Saved")

    except Exception as e:

        print(
            "Chat Save Error:",
            str(e)
        )

    # ==========================================
    # SEND WHATSAPP REPLY
    # ==========================================

    msg.body(reply)

    conn.close()

    return str(resp)

# ==========================================
# START FLASK SERVER
# ==========================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )