import discord
import random
import os
from flask import Flask
from threading import Thread

# --- 【Render専用装備】サーバーを眠らせないための設定 ---
app = Flask(__name__)
@app.route('/')
def home(): return "Bot is alive!"

def run():
    # Renderが指定する窓口(ポート)を自動で使う
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- 【記事のコード】ボットのメイン機能 ---
intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("Ready! オンラインになったぜ！")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if client.user in message.mentions:
        answer_list = ["さすがですね！", "知らなかったです！"]
        answer = random.choice(answer_list)
        await message.channel.send(answer)

# --- 実行部分 ---
if __name__ == "__main__":
    # Renderで動かすためにWebサーバーを裏で起動
    Thread(target=run, daemon=True).start()
    
    # トークンはRenderの「Environment」から読み込む
    token = os.getenv("DISCORD_TOKEN")
    client.run(token)
