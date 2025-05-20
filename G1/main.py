import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log',encoding='utf-8',mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='-', intents=intents)
@bot.event
async def on_ready():
    print(f"done")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "test" in message.content.lower():
        await message.channel.send(f"success1")
        lastMessage = await message.channel.fetch_message(message.id)
        await message.channel.send(lastMessage.content)
    
    await bot.process_commands(message)

@bot.command()
async def count(ctx):
    total = 0
    newArray = []
    async for messages in ctx.channel.history(limit=30):
        if messages.content != "-count" and messages.author != bot.user:
            newArray.append(messages.content)
            total += 1
    #await ctx.message.channel.send("you have sended total "+ str(total) +" messages out of last 100 messages")
    await ctx.message.channel.send(newArray)

bot.run(token=token, log_handler=handler, log_level=logging.DEBUG)
