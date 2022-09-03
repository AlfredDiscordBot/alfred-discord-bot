import os
import time

from threading import Thread

if "nextcord/" in os.listdir():
    os.system("rm -rf nextcord/")

os.system("pip install git+https://github.com/nextcord-ext/lava")
lava = Thread(target=lambda: os.system("java -jar Lavalink.jar"))
lava.start()
time.sleep(10)
print("Starting Bot")
