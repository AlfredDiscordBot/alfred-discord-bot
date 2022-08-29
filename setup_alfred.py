import os

if "nextcord/" in os.listdir():
    os.system("rm -rf nextcord/")

for i in open("setup.sh").read().split("\n"):
    os.system(i)