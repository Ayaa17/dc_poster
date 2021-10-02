import json
import discord
from discord.ext import commands


class Act(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sendpic(self, ctx):
        pic = discord.File("E:\\Python\\pythonProject\\media\\xxazuki_ikuzaxx\\B8bDtybBxNZ_.jpg")
        await ctx.send(file=pic)

    @commands.command()
    async def sendvideo(self, ctx):
        pic = discord.File("E:\\Python\\pythonProject\\media\\pinzi__\\CNiEK0VjmEF_.mp4")
        await ctx.send(file=pic)


def setup(bot):
    bot.add_cog(Act(bot))
