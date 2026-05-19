from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():

    return "AI WhatsApp Student Bot Running"


@app.route("/whatsapp", methods=["GET", "POST"])
def whatsapp():

    return "WhatsApp webhook working"


if __name__ == "__main__":

    import os

    port = int(
        os.environ.get("PORT", 8080)
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )