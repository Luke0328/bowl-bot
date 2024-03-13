from db import Database
from discord.ext import commands

class BowlBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'We have logged in as {self.bot.user}')

    @commands.command()
    async def help(self, ctx):
        help_msg = "\n".join([
        '!stats - display current lifetime stats',
        '!addscore - add scores from a game'
        ])
        await ctx.send(help_msg)

    @commands.command()
    async def addscore(self, ctx):
        author = ctx.author


        await ctx.send('Scores added!')

async def setup(client):
    await client.add_cog(BowlBot(client))
