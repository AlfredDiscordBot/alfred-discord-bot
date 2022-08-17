import os


def fix():
    print(os.getcwd())
    if not os.getcwd().endswith("alfred-discord-bot"):
        print("Yes")
