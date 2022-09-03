from flask import Flask, send_file
from threading import Thread

app = Flask("")


@app.route("/")
def home():
    return "Hello. I am Alfred!"


def run():
    app.run(host="0.0.0.0", port=8080)


def keep_alive():
    pass
