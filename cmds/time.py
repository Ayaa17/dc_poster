import datetime
import discord
from discord.ext import commands
import json, asyncio, datetime
from ig_crawler import igcr

with open('setting.json', mode='r', encoding='utf8') as jFile:
    jdata = json.load(jFile)


class time(commands.Cog):
    def __init__(self, bot, *args, **kwargs):
        self.is_listening: bool = False;
        self.bot = bot
        with open('setting.json', mode='r', encoding='utf8') as jFile:
            jdata = json.load(jFile)

        async def interval():
            count = 0
            await self.bot.wait_until_ready()
            # self.channel = self.bot.get_channel(int(jdata["Channel1"]))
            while not self.bot.is_closed():
                self.channel = self.bot.get_channel(int(jdata["channel_poster"]))
                time_now = datetime.datetime.now().strftime("%H%M")
                await self.channel.send(f"Now is {time_now}")

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

    @commands.command()
    async def golisten(self, ctx):
        _igcr = igcr.Singleton()
        self.is_listening = True
        while not self.bot.is_closed() and self.is_listening:
            print(_igcr.islogin)
            if (_igcr.islogin == True):
                aa = jdata["Ig"]
                for username in aa:
                    print(username + " start...")
                    await ctx.send(username + " start...")
                    newpost = _igcr.sendNewPost(username)
                    for i in newpost:
                        pic = discord.File(i)
                        await ctx.send(file=pic)
            await asyncio.sleep(600)  # 單位:秒

    @commands.command()
    async def stoplisten(self, ctx):
        self.is_listening = False
        print("is_listening : "+str(self.is_listening))
        await ctx.send("is_listening : "+str(self.is_listening))


def setup(bot):
    bot.add_cog(time(bot))
