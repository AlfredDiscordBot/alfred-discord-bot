import os

def fix():
    if not os.getcwd().endswith("alfred-discord-bot"):
        os.system("cd alfred-discord-bot")