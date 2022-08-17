import os


def fix():
    print(os.getcwd())
    if os.getcwd().endswith("alfred-discord-bot"):
        print("Yes")
