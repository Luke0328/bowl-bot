import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

@bot.command()
async def help(ctx, arg):
    help_msg = """
    !stats - display current lifetime stats
    !addscore - add scores from a game

    """
    await ctx.send(help_msg)

@bot.command()
async def addscore(ctx, arg):
    

    await ctx.send('Scores added!')

bot.run(TOKEN)
