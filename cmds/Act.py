import json
import os.path

import discord
from discord.ext import commands
from selenium import webdriver

# import ig_crawler.getindex as getindex
import ig_crawler.igcr as igcr1
with open('setting.json', mode='r',encoding='utf8') as jFile:
    jdata = json.load(jFile)


class Act(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.jdata = jdata

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
        igcr = igcr1.Singleton()
        igcr.setusername("zamy_ding").geturl()
        await ctx.send("over")

    @commands.command()
    async def re2(self, ctx):
        # browser = webdriver.Chrome()
        # index_result=getindex.main(False,browser,'https://www.instagram.com/solarkeem/')
        igcr = igcr1.Singleton()
        igcr.setusername("solarkeem").geturl()
        await ctx.send("over")

    @commands.command()
    async def re3(self, ctx):
        # browser = webdriver.Chrome()
        # index_result=getindex.main(False,browser,'https://www.instagram.com/solarkeem/')
        igcr = igcr1.Singleton()
        igcr.setusername("mo_onbyul").refresh()
        await ctx.send("over")

    @commands.command()
    async def dd(self, ctx):
        igcr = igcr1.Singleton()
        igcr.setusername("mo_onbyul").downlaod()
        await ctx.send("over")

    @commands.command()
    async def ss(self, ctx):
        # pic = discord.File("E:\\Python\\pythonProject\\media\\pinzi__\\CNiEK0VjmEF_.mp4")
        pic = "https://instagram.ftpe7-1.fna.fbcdn.net/v/t51.2885-15/e35/s1080x1080/244449061_167572732207705_4716969686301795153_n.jpg?_nc_ht=instagram.ftpe7-1.fna.fbcdn.net&_nc_cat=1&_nc_ohc=OEqi6lnWXzIAX8ZNoAo&tn=L-RLhCleruoWyqFm&edm=ABfd0MgBAAAA&ccb=7-4&oh=59128e90b465423d5346b62953633f7f&oe=6168DB3F&_nc_sid=7bff83"
        await ctx.send(pic)


    @commands.command()
    async def s01(self, ctx):
        aa=self.jdata["Ig"]
        for username in aa:
            igcr = igcr1.Singleton()
            newpost = igcr.sendNewPost(username)
            for i in newpost:
                pic = discord.File(i)
                await ctx.send(file=pic)
        return


def setup(bot):
    bot.add_cog(Act(bot))



