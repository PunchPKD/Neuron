import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
from AI_Handler import response
from datetime import datetime

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
async def summary(ctx):
    total = 0
    convoMatrix = []
    async for messages in ctx.channel.history(limit=30, oldest_first=True, around=datetime.now()):
        if messages.content != "-count" and messages.author != bot.user:
            convoMatrix.append([])
            convoMatrix[total].append(messages.author.display_name)
            convoMatrix[total].append(messages.content)
            total += 1

    def matrix_to_string(matrix):
        rows = [' : '.join(row) for row in matrix]
        result = '\n'.join(rows)
        return result

    convo = matrix_to_string(convoMatrix)
    await ctx.message.channel.send(response(convo=convo).text)

bot.run(token=token, log_handler=handler, log_level=logging.DEBUG)
