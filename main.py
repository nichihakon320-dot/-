import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread

# Flask（Renderを寝かせないための設定）
app = Flask('')
@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

# Discordボットの設定
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'ログイン成功！: {bot.user.name}')

@bot.command()
async def ping(ctx):
    await ctx.send('ポン！動いてるぜ、相棒！')

# Renderの「環境変数」からトークンを読み込む
def main():
    server_thread = Thread(target=run)
    server_thread.start()
    
    token = os.getenv("DISCORD_TOKEN")
    if token:
        bot.run(token)
    else:
        print("エラー: DISCORD_TOKENが見つからないぜ！Renderの設定を確認してくれ。")

if __name__ == "__main__":
    main()
