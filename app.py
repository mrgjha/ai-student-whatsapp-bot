from flask import Flask
from twilio.twiml.messaging_response import MessagingResponse
from flask import request

app = Flask(__name__)

@app.route("/")
def home():

    return "AI WhatsApp Student Bot Running"


@app.route("/health")
def health():

    return "healthy"


@app.route("/whatsapp", methods=["GET", "POST"])
def whatsapp():

    incoming_msg = request.form.get(
        "Body",
        ""
    )

    resp = MessagingResponse()

    msg = resp.message()

    msg.body(
        f"You said: {incoming_msg}"
    )

    return str(resp)