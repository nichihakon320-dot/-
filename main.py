import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread
import sys

# --- Renderでボットを永続化するための設定 ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    # Renderのポートを自動取得
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- Discordボットの本体設定 ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ ログイン成功！: {bot.user.name}', flush=True)

@bot.command()
async def ping(ctx):
    await ctx.send('ポン！生きてるぜ、相棒！')

# --- 実行部分 ---
def main():
    # 裏側でWebサーバーを動かす
    Thread(target=run, daemon=True).start()
    
    # RenderのEnvironment設定からトークンを読み込む
    token = os.getenv("DISCORD_TOKEN")
    
    if not token:
        print("❌ エラー: DISCORD_TOKENが設定されてないぜ！", flush=True)
        sys.exit(1)
        
    try:
        print("🤖 ボットを起動中...", flush=True)
        bot.run(token)
    except Exception as e:
        print(f"❌ 起動失敗: {e}", flush=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
