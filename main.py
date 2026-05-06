import discord
import os
from flask import Flask
from threading import Thread

# --- 1. ポート待機問題の対策 (Flask) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is online!"

def run_flask():
    # Renderから指定されたポート、なければ5000（または8080）で待機
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- 2. Discordボットの設定 ---
intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Ready! {client.user} がオンラインになったぜ！", flush=True)

# --- 3. 実行部分（ここが心臓部だ！） ---
def main():
    # Flaskを別スレッドで起動して、ポート待機問題をクリアする
    t = Thread(target=run_flask)
    t.daemon = True # メインが死んだら一緒に死ぬ設定
    t.start()
    
    # Discordボットを起動
    token = os.getenv("DISCORD_TOKEN")
    if token:
        client.run(token)
    else:
        print("❌ エラー: トークンが見つからないぜ！")

if __name__ == "__main__":
    main()
