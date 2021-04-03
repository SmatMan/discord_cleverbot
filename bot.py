import discord
from discord.ext import commands
import asyncio

import cleverbotfree.cbfree
import time
import sys

import config as cfg # config.py file

bot = commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
    print("Bot is ready.")

@bot.command(aliases=['talk', 'start_conversation'])
async def start(ctx):
    await ctx.send("Starting up...")
    cb = cleverbotfree.cbfree.Cleverbot()
    print(f"{str(ctx.message.author)} has started a session.")
    try:
        cb.browser.get(cb.url)
        welcomeEmbed = discord.Embed(title="Welcome to the Chatbot!", description="Once you're done, you may say **quit** to end the session. Note, the bot can only respond to one message at a time, any message sent while the bot is typing in chat will not be answered.", color=0x00D700)
        await ctx.send(embed=welcomeEmbed)
        while True:
            cb.get_form()
            userInput = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
            if userInput.content == 'quit':
                break
            with ctx.typing():
                cb.send_input(str(userInput.content))
                botResponse = cb.get_response()
            await ctx.send(botResponse)
        cb.browser.close()
        stopEmbed = discord.Embed(title="Session Ended.", description="Bye!", color=0xFF0000)
        await ctx.send(embed=stopEmbed)
    except KeyboardInterrupt:
        cb.browser.close()


bot.run(cfg.token)
