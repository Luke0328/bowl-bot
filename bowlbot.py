import datetime
from db import Database
from discord.ext import commands

class BowlBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = None

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'We have logged in as {self.bot.user}')
        self.db = Database()

    @commands.command()
    async def help(self, ctx):
        help_msg = "\n".join([
        '!bb stats - display current lifetime stats',
        '!bb addscore - add scores from a game'
        ])
        await ctx.send(help_msg)

    # addscore pts strikes spares extra_open_frame
    @commands.command()
    async def addscore(self, ctx):
        author = ctx.author

        await ctx.send('Please enter your score in the following format: \'points strikes spares\'')
        
        def check(m):
            return m.author == author and m.channel == ctx.channel
        
        score_msg = await self.bot.wait_for('message', check=check)

        await ctx.send('Did you receive an extra frame? (y/n)')
        extra_frame_msg = await self.bot.wait_for('message', check=check)

        score_data = score_msg.content.split()
        extra_frame_msg_text = extra_frame_msg.content

        # check score and extra frame messages for errors
        res_msg = 'd'
        if len(score_data) != 3:
            res_msg = 'Please only input three values following the provided format.'
        elif int(score_data[0]) < 0 or int(score_data[1]) < 0 or int(score_data[2]) < 0:
            res_msg = 'Points, strikes, or spares can not be negative. Please try again.'
        elif int(score_data[0]) > 300:
            res_msg = 'Can not score over 300 points. Please try again.'
        elif int(score_data[1]) > 12:
            res_msg = 'Can not score more than 12 strikes in a game. Please try again.'
        elif int(score_data[2]) > 10:
            res_msg = 'Can not score more than 10 spares in a game. Please try again.'
        elif extra_frame_msg_text != 'y' and extra_frame_msg_text != 'n':
            res_msg = 'Please enter only y or n.'
        elif int(score_data[1]) == 0 and int(score_data[2]) == 0 and extra_frame_msg_text == 'y':
            res_msg = 'Can not receive an extra frame with no strikes or spares. Please try again.'
        else:
            extra = False
            if (extra_frame_msg_text == 'y'):
                extra = True
            score = {
                "pts": int(score_data[0]),
                "strk": int(score_data[1]),
                "spr": int(score_data[2]),
                "extra": extra,
                "date": datetime.datetime.now(tz=datetime.timezone.utc),
            }

            add_score_succeeded = self.db.add_score(author, score)
            if add_score_succeeded:
                res_msg = 'Score successfully added!'
            else:
                res_msg = 'Failed to add score.'

        await ctx.send(res_msg)

    @commands.command()
    async def stats(self, ctx):
        author = ctx.author
        stats_msg = self.db.get_stats(author)
        await ctx.send(stats_msg)

async def setup(client):
    await client.add_cog(BowlBot(client))
