from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():

    return "AI WhatsApp Student Bot Running"


@app.route("/health")
def health():

    return "healthy"


@app.route("/whatsapp", methods=["GET", "POST"])
def whatsapp():

    return "WhatsApp webhook working"