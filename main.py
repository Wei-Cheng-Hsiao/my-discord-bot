import discord
import os

# 設定 Intents (權限設定)
intents = discord.Intents.default()
intents.message_content = True  # 務必開啟，否則讀不到訊息

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'目前登入身份：{client.user}')
    print('機器人已準備就緒！')

@client.event
async def on_message(message):
    # 排除機器人自己發送的訊息
    if message.author == client.user:
        return

    # 當收到 "!hello" 時回覆
    if message.content.startswith('!hello'):
        await message.channel.send('Hello! I am running on Zaebur!')

# 從環境變數讀取 Token (這是最安全的做法)
token = os.getenv('DISCORD_TOKEN')

if token:
    client.run(token)
else:
    print("錯誤：找不到 DISCORD_TOKEN 環境變數，請至 Zaebur 設定。")