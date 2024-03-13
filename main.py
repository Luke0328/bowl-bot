import asyncio
from dotenv import load_dotenv
import discord
from discord.ext import commands
import os

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!bb ', intents=intents, help_command=None)

async def load():
    await bot.load_extension('bowlbot')

async def main():
    await load()
    await bot.start(TOKEN)

asyncio.run(main())