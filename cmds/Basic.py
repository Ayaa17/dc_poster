import json
import discord
from discord.ext import commands


class basic(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"{round(self.bot.latency * 1000)}(ms)")

    @commands.command()
    async def resaid(self, ctx, *, msg):
        # async def resaid(self,ctx,msg):

        await ctx.message.delete()
        await ctx.send(msg)

    @commands.command()
    async def clean(self, ctx, num: int):
        await ctx.channel.purge(limit=num + 1)


def setup(bot):
    bot.add_cog(basic(bot))
