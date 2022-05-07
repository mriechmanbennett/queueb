import discord
from discord.ext import commands


# Pausing use of the cog for now, there is likely not a place for it in this bot.
# Leaving this up as a template
class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # pulse checkers
    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog is ready')

    @commands.command()
    async def pingy(self, ctx):
        await ctx.send('Pongy')


def setup(bot):
    bot.add_cog(Commands(bot))
