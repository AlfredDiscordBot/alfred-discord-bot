#!/bin/bash
install-pkg tmux
tmux new-session -s Lavalink -d 'java -jar Lavalink.jar'
sleep 10
tmux new-session -s Bot -d 'python3 ./main.py'