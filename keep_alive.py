from flask import Flask, send_file
from threading import Thread

app = Flask("")


@app.route("/")
def home():
    return "Hello. I am Alfred!"


@app.route("/info")
def info():
    return send_file("BotInfo.jpg", attachment_filename="BotInfo.jpg")


def run():
    app.run(host="0.0.0.0", port=8080)


def keep_alive():
    t = Thread(target=run)
    t.setDaemon(True)
    t.start()
