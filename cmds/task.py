import discord
from discord.ext import commands
import json, asyncio ,datetime

with open('setting.json', mode='r', encoding='utf8') as jFile:
    jdata = json.load(jFile)

class task(commands.Cog):
    def __init__(self,bot,*args,**kwargs):
        self.bot =bot
        async def interval():
            count = 0
            await self.bot.wait_until_ready()
            self.channel = self.bot.get_channel(int(jdata["channel_poster"]))
            while not self.bot.is_closed() and count<1:
                await self.channel.send("HI ,Im running")
                await asyncio.sleep(5)  #單位:秒
                count+=1

        self.bg_task=self.bot.loop.create_task(interval())

    @commands.command()
    async def set_channel(self,ctx,ch:int):
        # await self.channel.send(f"Change to channel{ch}")
        prechannel=self.channel
        self.channel = self.bot.get_channel(ch)
        await prechannel.send(f"Change to {self.channel} : {prechannel.mention}->{self.channel.mention}")
        await self.channel.send(f"Change to {self.channel} : {prechannel.mention}->{self.channel.mention}")


def setup(bot):
    bot.add_cog(task(bot))