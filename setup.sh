[ -d "lava/" ] && rm -rf lava/;
git clone "https://github.com/nextcord-ext/lava";
mv "lava/nextcord/ext/lava/" "/home/runner/alfred-discord-bot/venv/lib/python3.8/site-packages/nextcord/ext/lava/";
rm -rf lava/
nohup java -jar Lavalink.jar &