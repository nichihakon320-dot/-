import discord
from discord.ext import commands
import os
import sys
import traceback
from flask import Flask
from threading import Thread

# Renderのポート設定を自動に合わせるように修正！
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    # Renderが指定するポート（または8080）で待機するぜ
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# Discordボットの設定
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ ログイン成功！: {bot.user.name}')

@bot.command()
async def ping(ctx):
    await ctx.send('ポン！動いてるぜ、相棒！')

def main():
    # サーバーを裏で動かす
    server_thread = Thread(target=run, daemon=True)
    server_thread.start()
    
    token = os.getenv("DISCORD_TOKEN")
    
    # トークンが設定されていない場合
    if not token:
        print("❌【エラー】DISCORD_TOKENが見つからないぜ！RenderのEnvironment設定を見直してくれ。")
        sys.exit(1)
        
    # ここからが最強のエラーキャッチだ！
    try:
        bot.run(token)
    except discord.errors.LoginFailure:
        print("❌【エラー】トークンが間違っているか、Discord側に無効化されてるぜ！もう一度ポータルでReset Tokenだ！")
    except discord.errors.PrivilegedIntentsRequired:
        print("❌【エラー】Discordポータルの『MESSAGE CONTENT INTENT』がOFFになってるぜ！ONにして保存してくれ！")
    except Exception as e:
        print("❌【予期せぬエラーが発生したぜ！】")
        traceback.print_exc()

if __name__ == "__main__":
    main()
