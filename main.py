import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread

# 1. ボットの権限設定
intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix="!", intents=intents)

# 起動確認用
@bot.event
async def on_ready():
    print(f'ログイン成功！: {bot.user.name}')
    await bot.change_presence(activity=discord.Game(name="稼働中だぜ！"))

# 動作確認コマンド
@bot.command()
async def ping(ctx):
    await ctx.send('ポン！動いてるぜ、相棒！')

# 2. Render用のダミーサーバー（24時間稼働に必要）
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    # Renderは環境変数PORTを指定してくることがあるから、それに対応させてるぜ
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True # メインプログラムが終了した時に一緒に終了させる設定
    t.start()

# 3. 実行！
keep_alive()

# ⚠️ 注意：トークンの前後の " は消さないでくれよ！
import os

# 一番下の bot.run をこれに変える！
token = os.getenv("DISCORD_TOKEN")
bot.run(token)


