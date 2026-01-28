import discord
import os

# 設定 Intents
intents = discord.Intents.default()
intents.message_content = True 

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'目前登入身份：{client.user}')
    print('機器人已準備就緒！')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        await message.channel.send('Hello! I am running on Zaebur!')

token = os.getenv('DISCORD_TOKEN')

if token:
    client.run(token)
else:
    print("錯誤：找不到 DISCORD_TOKEN 環境變數")