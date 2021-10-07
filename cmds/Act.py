import json
import discord
from discord.ext import commands
from selenium import webdriver

# import ig_crawler.getindex as getindex
import ig_crawler.igcr as igcr1

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

    @commands.command()
    async def re(self, ctx):
        # browser = webdriver.Chrome()
        # index_result=getindex.main(False,browser,'https://www.instagram.com/solarkeem/')
        igcr=igcr1.Singleton()
        igcr.setusername("zamy_ding").geturl()
        await ctx.send("over")
    @commands.command()
    async def re2(self, ctx):
        # browser = webdriver.Chrome()
        # index_result=getindex.main(False,browser,'https://www.instagram.com/solarkeem/')
        igcr=igcr1.Singleton()
        igcr.setusername("solarkeem").geturl()
        await ctx.send("over")

    @commands.command()
    async def re3(self, ctx):
        # browser = webdriver.Chrome()
        # index_result=getindex.main(False,browser,'https://www.instagram.com/solarkeem/')
        igcr = igcr1.Singleton()
        igcr.setusername("mo_onbyul").refresh()
        await ctx.send("over")


def setup(bot):
    bot.add_cog(Act(bot))
