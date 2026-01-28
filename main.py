import google.generativeai as genai
import os
import discord

# --- 設定區 ---
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# --- 診斷模式：只列出模型 ---
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    print("====== 正在檢查可用模型清單 ======")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"發現模型: {m.name}")
    except Exception as e:
        print(f"檢查失敗: {e}")
    print("==================================")
else:
    print("錯誤：沒有 API Key")

# 為了不讓 Zaebur 以為程式跑完就掛了，我們還是讓 Discord 上線一下
intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('診斷機器人待命中...')

if DISCORD_TOKEN:
    client.run(DISCORD_TOKEN)