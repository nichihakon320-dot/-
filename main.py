import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread
import sys

# Flask（Renderを寝かせないための設定）
app = Flask(__name__)

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
    await bot.change_presence(activity=discord.Game(name='!ping'))

@bot.command()
async def ping(ctx):
    await ctx.send('ポン！動いてるぜ、相棒！')

# Renderの「環境変数」からトークンを読み込む
def main():
    token = os.getenv("DISCORD_TOKEN")
    
    if not token:
        print("エラー: DISCORD_TOKENが見つかりません！")
        print("Render のEnvironment設定を確認してください。")
        sys.exit(1)
    
    # daemon=True で裏側のプログラムも綺麗に終了させる
    try:
        server_thread = Thread(target=run, daemon=True)
        server_thread.start()
        print("Flask サーバーを起動しました")
    except Exception as e:
        print(f"Flask サーバー起動エラー: {e}")
    
    try:
        bot.run(token)
    except Exception as e:
        print(f"ボット起動エラー: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
