import datetime
import discord
from discord.ext import commands
import json, asyncio ,datetime

# with open('setting.json', mode='r', encoding='utf8') as jFile:
#     jdata = json.load(jFile)

class time(commands.Cog):
    def __init__(self,bot,*args,**kwargs):
        self.bot = bot
        with open('setting.json', mode='r', encoding='utf8') as jFile:
            jdata = json.load(jFile)
        async def interval():
            count = 0
            await self.bot.wait_until_ready()
            # self.channel = self.bot.get_channel(int(jdata["Channel1"]))
            while not self.bot.is_closed():
                self.channel = self.bot.get_channel(int(jdata["Channel1"]))
                time_now= datetime.datetime.now().strftime("%H%M")
                await self.channel.send(f"Now is {time_now}")
                if time_now == jdata["time"]:

                    await self.channel.send("HIHI,TIME")
                await asyncio.sleep(5)  #單位:秒


        self.bg_task=self.bot.loop.create_task(interval())

    @commands.command()
    async def set_time(self,ctx,time):
        with open('setting.json', mode='r', encoding='utf8') as jFile:
            jdata = json.load(jFile)
            jdata["time"]=time
        with open("setting.json",mode = "w",encoding="utf8") as jFile:
            json.dump(jdata,jFile,indent= 4)
            await ctx.send(f"Set complete,Time is {jdata['time']} now")

def setup(bot):
    bot.add_cog(time(bot))