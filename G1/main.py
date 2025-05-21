import discord
from discord.ext import commands
from discord import app_commands

import logging
import os

from typing import Literal
from datetime import datetime, timedelta
from enum import Enum

from dotenv import load_dotenv
from AI_Handler import response

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

    try:
        await bot.tree.sync()
        print("synced")
        
    except Exception as e:
        print(f"error : {e}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "test" in message.content.lower():
        await message.channel.send(f"success1")

class duration(Enum):
    last_one_hour = 1
    last_two_hour = 2
    last_three_hour = 3

@bot.tree.command(name="summary", description="summarise the recent chat")
@app_commands.describe(
    duration= 'select how much to summarise',
)
async def summary(ctx: discord.integrations, duration: duration = 1):
    total = 0
    convoMatrix = []
    async for messages in ctx.channel.history(oldest_first=True, after=datetime.now()-timedelta(hours=duration.value)):
        if messages.content != "-summary" and messages.author != bot.user:
            convoMatrix.append([])
            convoMatrix[total].append(messages.author.display_name)
            convoMatrix[total].append(messages.content)
            total += 1

    def matrix_to_string(matrix):
        rows = [' : '.join(row) for row in matrix]
        result = '\n'.join(rows)
        return result

    convo = matrix_to_string(convoMatrix)
    await ctx.response.send_message(response(convo=convo).text)

bot.run(token=token, log_handler=handler, log_level=logging.DEBUG)
