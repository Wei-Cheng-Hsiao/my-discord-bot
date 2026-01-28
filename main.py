import discord
import os
import google.generativeai as genai

# --- 環境變數 ---
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# --- 設定 AI ---
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    # 這裡換回最標準的 flash 名稱
    model = genai.GenerativeModel('gemini-1.5-flash')

# --- 設定 Discord ---
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    # flush=True 讓 Log 強制顯示，不會再一片空白
    print(f'成功登入：{client.user}', flush=True)
    print('--- Gemini 1.5 Flash 機器人準備就緒 ---', flush=True)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # 收到任何訊息都印出來確認
    print(f"收到訊息: {message.content}", flush=True)

    if message.content.startswith('!hello'):
        await message.channel.send('Hello! I am Gemini Flash Bot!')
        return

    # AI 對話功能
    try:
        async with message.channel.typing():
            response = model.generate_content(message.content)
            await message.channel.send(response.text)
            print("已回覆訊息", flush=True)
    except Exception as e:
        error_msg = f"發生錯誤: {e}"
        print(error_msg, flush=True)
        await message.channel.send(error_msg)

if DISCORD_TOKEN:
    client.run(DISCORD_TOKEN)