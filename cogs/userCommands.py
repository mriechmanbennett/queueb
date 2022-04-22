import discord
from discord.ext import commands


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog is ready')

    @commands.command()
    async def pingy(self, ctx):
        await ctx.send('Pongy')


def setup(bot):
    bot.add_cog(Commands(bot))
    