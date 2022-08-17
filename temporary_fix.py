import os


def fix():
    print(os.getcwd())
    if not os.getcwd().endswith("alfred-discord-bot"):
        print(os.system("cd alfred-discord-bot"))
