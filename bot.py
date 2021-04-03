import discord
from discord.ext import commands
from discord.ext.commands import cooldown
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
@cooldown(1, 100000)
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
        start.reset_cooldown(ctx)
        stopEmbed = discord.Embed(title="Session Ended.", description="Bye!", color=0xFF0000)
        await ctx.send(embed=stopEmbed)
    except KeyboardInterrupt:
        cb.browser.close()
        start.reset_cooldown(ctx)
@start.error
async def start_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandOnCooldown):
        await ctx.send(f"Hey, <@{ctx.message.author.id}>! Someone is already using the bot.")

bot.run(cfg.token)
