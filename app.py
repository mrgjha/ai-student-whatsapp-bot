from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():

    return "Railway Flask App Working"


@app.route("/whatsapp", methods=["GET", "POST"])
def whatsapp():

    return "WhatsApp Route Working"