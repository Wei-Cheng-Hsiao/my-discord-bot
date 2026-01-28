import discord
import os
import google.generativeai as genai

# --- 設定區 ---
# 讀取環境變數
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# --- 初始化 Discord ---
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# --- 初始化 Google Gemini ---
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    # 使用 Flash 模型 (速度快、免費額度高)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    print("警告：未偵測到 GOOGLE_API_KEY，AI 功能將無法使用。")

@client.event
async def on_ready():
    print(f'已登入為：{client.user}')
    print('--- 您的 AI 助理已上線 (Gemini Mode) ---')

@client.event
async def on_message(message):
    # 1. 忽略機器人自己的訊息
    if message.author == client.user:
        return

    # 2. 顯示使用者輸入了什麼 (方便除錯)
    print(f"收到訊息: {message.content} from {message.author}")

    # 3. 只要不是指令 (如 !hello)，就當作是在跟 AI 聊天
    # 這裡我們設定：所有訊息都回覆 (你可以之後改成只回應特定開頭)
    if message.content.startswith('!hello'):
         await message.channel.send('Hello! I am upgraded with Gemini Brain!')
         return

    try:
        # 顯示「正在輸入...」的狀態
        async with message.channel.typing():
            if GOOGLE_API_KEY:
                # 呼叫 Gemini
                response = model.generate_content(message.content)
                reply_text = response.text
                
                # Discord 單次訊息上限 2000 字，做簡單切割
                if len(reply_text) > 2000:
                    await message.channel.send(reply_text[:2000] + "\n(訊息太長，已截斷...)")
                else:
                    await message.channel.send(reply_text)
            else:
                await message.channel.send("錯誤：我的大腦 (API Key) 還沒接好，請檢查 Zaebur 設定。")

    except Exception as e:
        await message.channel.send(f"發生錯誤：{str(e)}")
        print(f"Error: {e}")

# 啟動機器人
if DISCORD_TOKEN:
    client.run(DISCORD_TOKEN)