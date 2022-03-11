#!/bin/bash
install-pkg tmux
tmux new-session -s Lavalink -d 'java -jar Lavalink.jar'
python3 main.py