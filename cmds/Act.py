import json
import os.path

import discord
from discord.ext import commands
from selenium import webdriver
from ig_crawler import init
import ig_crawler.getindex as getindex
import ig_crawler.igcr as igcr1

with open('setting.json', mode='r', encoding='utf8') as jFile:
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
    async def re2(self, ctx):
        # browser = webdriver.Chrome()
        # index_result=getindex.main(False,browser,'https://www.instagram.com/solarkeem/')
        igcr = igcr1.Singleton()
        igcr.setusername("solarkeem").geturl()
        await ctx.send("over")

    @commands.command()
    async def s01(self, ctx):
        aa = self.jdata["Ig"]
        for username in aa:
            igcr = igcr1.Singleton()
            newpost = igcr.sendNewPost(username)
            for i in newpost:
                pic = discord.File(i)
                await ctx.send(file=pic)
        return

    @commands.command()
    async def em(self, ctx):
        emm = self.emm()
        # print(emm)
        pic = discord.File("E:\\Python\\pythonProject\\media\\xxazuki_ikuzaxx\\CVZ7kceBMDF_.jpg")
        pic2 = discord.File("E:\\Python\\pythonProject\\media\\xxazuki_ikuzaxx\\B8bDtybBxNZ_.jpg")

        await ctx.send(files=[pic, pic2], embed=emm)
        return

    def emm(self, _title="Basic settings", _url=init.url_whee, _description="description", ):

        _title = "solarkeem"
        _url = jdata[_title]
        _description = igcr1.Singleton().setusername("solarkeem").getDescription("CUXSz5aPzIh")
        embed = discord.Embed(title=_title,
                              url=_url,
                              description=_description, color=0xf00000)
        embed.set_author(name="Geting IG post ",
                         url="",
                         icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ-84QJaofvWOR-Y_pUqut53hJ_-tkYiRBbWA&usqp=CAU")
        embed.set_thumbnail(
            url="attachment://CVZ7kceBMDF_.jpg")
        # embed.add_field(name="Time", value="undefined", inline=True)
        embed.set_image(url="attachment://B8bDtybBxNZ_.jpg")

        return embed

    @commands.command()
    async def aa(self, ctx):
        aa=igcr1.Singleton().setusername("solarkeem").getNew()
        for i in aa:
            print(i[0])
        return

    @commands.command()
    async def az(self, ctx):
        aa = igcr1.Singleton().setusername("whee_inthemood").refresh()
        print(str(aa))
        return

    @commands.command()
    async def aza(self, ctx):
        with open('setting.json', mode='r', encoding='utf8') as jFile:
            jdata = json.load(jFile)
            username="whee_inthemood"

            print(jdata[username]['icon'])
        return

def setup(bot):
    bot.add_cog(Act(bot))
