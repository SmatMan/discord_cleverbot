import discord.py
from discord.ext import commands
import asyncio

import cleverbot_free
import time
import sys

import config as cfg # config.py file

bot = commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
    print("Bot is ready.")
bot.run(cfg.token)