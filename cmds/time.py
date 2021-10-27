import datetime
import os

import discord
from discord.ext import commands
import json, asyncio, datetime
from ig_crawler import igcr
from ig_crawler import init


with open('setting.json', mode='r', encoding='utf8') as jFile:
    jdata = json.load(jFile)


class time(commands.Cog):
    def __init__(self, bot, *args, **kwargs):
        self.is_listening: bool = False;
        # self.igcr = igcr.Singleton()
        self.bot = bot
        # with open('setting.json', mode='r', encoding='utf8') as jFile:
        #     jdata = json.load(jFile)

        async def interval():
            count = 0
            await self.bot.wait_until_ready()
            # self.channel = self.bot.get_channel(int(jdata["Channel1"]))
            while not self.bot.is_closed():
                self.channel = self.bot.get_channel(int(jdata["channel_poster"]))
                time_now = datetime.datetime.now().strftime("%H%M")
                # await self.channel.send(f"Now is {time_now}")

                await asyncio.sleep(60)  # 單位:秒

        self.bg_task = self.bot.loop.create_task(interval())

    @commands.command()
    async def set_time(self, ctx, time):
        with open('setting.json', mode='r', encoding='utf8') as jFile:
            jdata = json.load(jFile)
            jdata["time"] = time
        with open("setting.json", mode="w", encoding="utf8") as jFile:
            json.dump(jdata, jFile, indent=4)
            await ctx.send(f"Set complete,Time is {jdata['time']} now")

    # 初始化 listening
    @commands.command()
    async def golisten(self, ctx):
        _igcr = igcr.Singleton()
        while not self.bot.is_closed() and self.is_listening:
            print(_igcr.islogin)
            if (_igcr.islogin == True):
                aa = jdata["Ig"]
                for username in aa:
                    print(username + " start...")
                    await ctx.send(username + " start...")
                    newpost = _igcr.sendNewPost(username)
                    pics=[]
                    for i in newpost:
                        pics.append(discord.File(i))
                        # pic = discord.File(i)
                    if(pics!=[]):
                        await ctx.send(files=pics)
            await asyncio.sleep(600)  # 單位:秒

    # embed
    @commands.command()
    async def golisten2(self, ctx):
        _igcr = igcr.Singleton()
        self.is_listening = True
        while not self.bot.is_closed() and self.is_listening:
            print(_igcr.islogin)
            if (_igcr.islogin == True):
                with open('setting.json', mode='r', encoding='utf8') as jFile:
                    jdata = json.load(jFile)
                aa = jdata["Ig"]
                for username in aa:
                    print(username + " start...")
                    await ctx.send(username + " start...")
                    _url=jdata[username]["url"]
                    _img =jdata[username]["icon"]
                    newPostShortcode=_igcr.setusername(username).getNew()
                    for i in newPostShortcode:
                        print(i[0])
                        _description = _igcr.setusername(username).getDescription(i[0])
                        embed=self.emm(username,_url,_description[0], _img ,i[0])
                        filedir = _igcr.getNewPost(username)[0]
                        pic = discord.File(filedir)
                        await ctx.send(file=pic, embed=embed)


    # 停止
    @commands.command()
    async def stoplisten(self, ctx):
        self.is_listening = False
        print("is_listening : "+str(self.is_listening))
        await ctx.send("is_listening : "+str(self.is_listening))

    # 開始
    @commands.command()
    async def startlisten(self, ctx):
        self.is_listening = True
        print("is_listening : " + str(self.is_listening))
        await ctx.send("is_listening : " + str(self.is_listening))

    def emm(self, _title="Basic settings", _url='https://www.instagram.com/', _description="description",icon = "",_shortcode='' ):

        embed = discord.Embed(title=_title,
                              url=_url,
                              description=_description, color=0xf00000)
        embed.set_author(name="Geting IG post ",
                         url="",
                         icon_url="https://lh3.googleusercontent.com/7JuFAFpLXd1u0mqAAE9frT3ydyKsAsm7Hjl0FE_Kz6TKg7d_3vBgNdesrjF7fwQ3aMXM6Q=s85")
        embed.set_thumbnail(
            url=icon)
        # embed.add_field(name="Time", value="undefined", inline=True)

        file_dir_pre = init.file_dir
        file_dir = file_dir_pre.format(username=_title)
        img=''
        for j in os.listdir(file_dir):
            if (j.find(_shortcode) != -1):
                # print(j)
                img = 'attachment://' + j
                break

        # img = 'attachment://'+str(_shortcode)+'_0.jpg'
        print(img)
        embed.set_image(url=img)

        return embed



def setup(bot):
    bot.add_cog(time(bot))
