import discord
from discord.ext import commands
import  json

with open('setting.json', mode='r',encoding='utf8') as jFile:
    jdata = json.load(jFile)

class Event(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.jdata  = jdata


    @commands.Cog.listener()
    async def on_member_join(self,member):
        print(f'{member} join!')
        channel1 = self.bot.get_channel(int(jdata["channel_poster"]))
        await channel1.send(f'{member} join')

    @commands.Cog.listener()
    async def on_member_remove(self,member):
        print(f'{member} leave')
        channel1 = self.bot.get_channel(int(jdata["channel_poster"]))
        await channel1.send(f'{member} join')

    @commands.Cog.listener()
    async def on_message(self,msg):
        keywordlist = ['aa','bb','cc']
        # if xx in keywordlist:
        if msg.content == "apple" and msg.author != self.bot.user:
            await msg.channel.send("apple")
            rot=1
        elif msg.content.endswith("apple") :
            await msg.channel.send("HI")


def setup(bot):
    bot.add_cog(Event(bot))