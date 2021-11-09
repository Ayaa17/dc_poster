import datetime
import os
import random

import discord
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash import cog_ext

import json, asyncio, datetime
from ig_crawler import igcr
from ig_crawler import init, unit, database

with open('setting.json', mode='r', encoding='utf8') as jFile:
    jdata = json.load(jFile)


class time(commands.Cog):
    def __init__(self, bot, *args, **kwargs):
        self.is_listening: bool = False;
        # self.igcr = igcr.Singleton()
        self.bot = bot

        with open('setting.json', mode='r', encoding='utf8') as jFile:
            self.jdata = json.load(jFile)

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
                    pics = []
                    for i in newpost:
                        pics.append(discord.File(i))
                        # pic = discord.File(i)
                    if (pics != []):
                        await ctx.send(files=pics)
            await asyncio.sleep(600)  # 單位:秒

    # embed
    @commands.command()
    async def golisten2(self, ctx):
        _igcr = igcr.Singleton()
        self.is_listening = True
        while not self.bot.is_closed() and self.is_listening and _igcr.islogin:
            #     with open('setting.json', mode='r', encoding='utf8') as jFile:
            #         jdata = json.load(jFile)
            jdata = self.jdata
            aa = jdata["Ig"]
            for username in aa:
                try:
                    print(username + " start...")
                    # await ctx.send(username + " start...")
                    _url = jdata[username]["url"]
                    _img = jdata[username]["icon"]
                    is_new = _igcr.setusername(username).refresh()
                    if (is_new):
                        _igcr.setusername(username).downlaod()
                        newPostShortcode = _igcr.setusername(username).getNew()
                        for i in newPostShortcode:
                            with open('setting.json', mode='r', encoding='utf8') as jFile:
                                jdata = json.load(jFile)
                            # print(i[0])
                            _description = _igcr.setusername(username).getDescription(i[0])[0]
                            _time = _igcr.setusername(username).gettime(i[0])[0][0]
                            _time = unit.trans2time(_time)
                            embed = self.emm(username, _url, _description[0], _img, i[0], _time)
                            filedir = _igcr.getPost(username, i[0])[0]
                            pic = discord.File(filedir)
                            sent_msg = await ctx.send(file=pic, embed=embed)
                            await sent_msg.add_reaction("⤵")
                            await asyncio.sleep(15)
                        await asyncio.sleep(15)
                    await asyncio.sleep(15)
                except:
                    print(username + " error...")
                    return
                await asyncio.sleep(60)
            await asyncio.sleep(600)

    @cog_ext.cog_slash(name="getNew", description="IG New post", guild_ids=jdata['guild_ids'])
    async def getNew(self, ctx):
        await ctx.send("Start ...")
        _igcr = igcr.Singleton()
        self.is_listening = True
        if not self.bot.is_closed() and self.is_listening and _igcr.islogin:
            #     with open('setting.json', mode='r', encoding='utf8') as jFile:
            #         jdata = json.load(jFile)
            jdata = self.jdata
            aa = jdata["Ig"]
            for username in aa:
                try:
                    print(username + " start...")
                    # await ctx.send(username + " start...")
                    _url = jdata[username]["url"]
                    _img = jdata[username]["icon"]
                    is_new = _igcr.setusername(username).refresh()
                    if (is_new):
                        _igcr.setusername(username).downlaod()
                        newPostShortcode = _igcr.setusername(username).getNew()
                        for i in newPostShortcode:
                            with open('setting.json', mode='r', encoding='utf8') as jFile:
                                jdata = json.load(jFile)
                            # print(i[0])
                            _description = _igcr.setusername(username).getDescription(i[0])[0]
                            _time = _igcr.setusername(username).gettime(i[0])[0][0]
                            _time = unit.trans2time(_time)
                            embed = self.emm(username, _url, _description[0], _img, i[0], _time)
                            filedir = _igcr.getPost(username, i[0])[0]
                            pic = discord.File(filedir)
                            sent_msg = await ctx.send(file=pic, embed=embed)
                            await sent_msg.add_reaction("⤵")
                            _database_name = 'Instagram_forbot.db'
                            database.updateSendDB(i[0], _database_name, username)
                    await asyncio.sleep(10)
                except:
                    print(username + "/WRONG")
                    break;
        await ctx.send("OVER!")

    @cog_ext.cog_slash(name="getRandom", description="IG Random post", guild_ids=jdata['guild_ids'])
    async def getrandom(self, ctx):
        _igcr = igcr.Singleton()
        jdata = self.jdata
        username = jdata['Ig'][random.randint(0, 3)]
        _url = jdata[username]["url"]
        _img = jdata[username]["icon"]
        randomShortcode = _igcr.getrandom(username)
        # for i in randomShortcode:
        # print(randomShortcode)
        i = randomShortcode
        _description = _igcr.setusername(username).getDescription(i[0])[0]
        _time = _igcr.setusername(username).gettime(i[0])[0][0]
        _time = unit.trans2time(_time)
        embed = self.emm(username, _url, _description[0], _img, i[0], _time,True)
        try:
            filedir = _igcr.getPost(username, i[0])[0]
        except:
            print(username + "," + i[0])
            ur=init.url_prefix_post+i[0]
            await ctx.send("ERROR: " + username + "," + i[0]+"\n"+str(ur))
            return
        # print(filedir)
        pic = discord.File(filedir)
        sent_msg = await ctx.send(file=pic, embed=embed)
        await sent_msg.add_reaction("⤵")


    @cog_ext.cog_slash(name="getpost", description="IG the post", guild_ids=jdata['guild_ids'])
    async def getpost00(self, ctx, username, shortcode):
        _igcr = igcr.Singleton()
        jdata = self.jdata
        username = username
        _url = jdata[username]["url"]
        _img = jdata[username]["icon"]
        # for i in randomShortcode:
        # print(randomShortcode)
        i = (shortcode,)
        print(i[0])
        _description = _igcr.setusername(username).getDescription(i[0])[0]
        _time = _igcr.setusername(username).gettime(i[0])[0][0]
        _time = unit.trans2time(_time)
        embed = self.emm(username, _url, _description[0], _img, i[0], _time, True)
        try:
            filedir = _igcr.getPost(username, i[0])[0]
        except:
            print(username + "," + i[0])
            ur = init.url_prefix_post + i[0]
            await ctx.send("ERROR: " + username + "," + i[0] + "\n" + str(ur))
            return
        # print(filedir)
        pic = discord.File(filedir)
        sent_msg = await ctx.send(file=pic, embed=embed)
        await sent_msg.add_reaction("⤵")

    # 停止
    @commands.command()
    async def stoplisten(self, ctx):
        self.is_listening = False
        print("is_listening : " + str(self.is_listening))
        await ctx.send("is_listening : " + str(self.is_listening))

    # 開始
    @commands.command()
    async def startlisten(self, ctx):
        self.is_listening = True
        print("is_listening : " + str(self.is_listening))
        await ctx.send("is_listening : " + str(self.is_listening))

    def emm(self, _title="Basic settings", _url='https://www.instagram.com/', _description="description", icon="",
            _shortcode='', time='', random_: bool = False):
        embed = discord.Embed(title=_title,
                              url=_url,
                              description=_description + '\n\n.______.______.______.______.______.______.______.______.______.______.______.______.______.______.______.______.______.______.______',
                              color=0xf00000)
        embed.set_author(name="Geting IG post ",
                         url="",
                         icon_url="https://lh3.googleusercontent.com/7JuFAFpLXd1u0mqAAE9frT3ydyKsAsm7Hjl0FE_Kz6TKg7d_3vBgNdesrjF7fwQ3aMXM6Q=s85")
        embed.set_thumbnail(
            url=icon)
        post_url = f'[{_shortcode}]({init.url_prefix_post + _shortcode})'
        if (random_):
            embed.add_field(name="The Random Post URL", value=post_url, inline=True)
        else:
            embed.add_field(name="The New Post URL", value=post_url, inline=True)

        foot = f"Time: {time} UTC+8 "
        icon_url = "https://cdn.icon-icons.com/icons2/2037/PNG/512/ig_instagram_media_social_icon_124260.png"
        embed.set_footer(text=foot, icon_url=icon_url)

        file_dir_pre = init.file_dir
        file_dir = file_dir_pre.format(username=_title)
        img = ''
        for j in os.listdir(file_dir):
            if (j.find(_shortcode) != -1):
                # print(j)
                img = 'attachment://' + j
                break
        # img = 'attachment://'+str(_shortcode)+'_0.jpg'
        # print(img)
        embed.set_image(url=img)

        return embed

    @cog_ext.cog_slash(name="golistening", description="IG", guild_ids=jdata['guild_ids'])
    async def golisten2(self, ctx):
        await ctx.send("Start listening")
        _igcr = igcr.Singleton()
        self.is_listening = True
        while not self.bot.is_closed() and self.is_listening and _igcr.islogin:
            #     with open('setting.json', mode='r', encoding='utf8') as jFile:
            #         jdata = json.load(jFile)
            jdata = self.jdata
            aa = jdata["Ig"]
            for username in aa:
                try:
                    print(username + " start...")
                    # await ctx.send(username + " start...")
                    _url = jdata[username]["url"]
                    _img = jdata[username]["icon"]
                    is_new = _igcr.setusername(username).refresh()
                    if (is_new):
                        _igcr.setusername(username).downlaod()
                        newPostShortcode = _igcr.setusername(username).getNew()
                        for i in newPostShortcode:
                            with open('setting.json', mode='r', encoding='utf8') as jFile:
                                jdata = json.load(jFile)
                            # print(i[0])
                            _description = _igcr.setusername(username).getDescription(i[0])[0]
                            _time = _igcr.setusername(username).gettime(i[0])[0][0]
                            _time = unit.trans2time(_time)
                            embed = self.emm(username, _url, _description[0], _img, i[0], _time)
                            filedir = _igcr.getPost(username, i[0])[0]
                            pic = discord.File(filedir)
                            sent_msg = await ctx.send(file=pic, embed=embed)
                            await sent_msg.add_reaction("⤵")
                            await asyncio.sleep(15)
                        await asyncio.sleep(15)
                    await asyncio.sleep(15)
                except:
                    break;
                await asyncio.sleep(60)
            await asyncio.sleep(600)
        await ctx.send("Close listeing")


def setup(bot):
    bot.add_cog(time(bot))
