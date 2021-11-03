import discord
from discord.ext import commands
import json
import re
from discord.abc import Messageable
from ig_crawler import igcr

with open('setting.json', mode='r', encoding='utf8') as jFile:
    jdata = json.load(jFile)


class Event(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.jdata = jdata

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f'{member} join!')
        channel1 = self.bot.get_channel(int(jdata["channel_poster"]))
        await channel1.send(f'{member} join')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f'{member} leave')
        channel1 = self.bot.get_channel(int(jdata["channel_poster"]))
        await channel1.send(f'{member} join')

    @commands.Cog.listener()
    async def on_message(self, msg):
        keywordlist = ['aa', 'bb', 'cc']
        # if xx in keywordlist:
        if msg.content == "apple" and msg.author != self.bot.user:
            await msg.channel.send("apple")
            rot = 1
        elif msg.content.endswith("apple"):
            await msg.channel.send("HI")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, data):
        channel1 = self.bot.get_channel(int(jdata["channel_poster"]))
        print(data.member.bot)
        emoji="⤵"
        msg_id = data.message_id
        aaa = await channel1.fetch_message(msg_id)
        # print(aaa.embeds[0].to_dict())
        if (aaa.embeds[0] != None and  (not data.member.bot)):
            current_embed = aaa.embeds[0].to_dict()
            if (current_embed['author']['name'] == 'Geting IG post'):
                username = current_embed['title']
                current_field = current_embed['fields'][0]['value']
                regex = re.compile(f'\[(.*?)]')
                current_shortcode = regex.match(current_field).group(0)[1:-1]
                imgs = igcr.Singleton().getPost(username=username, shortcode=current_shortcode)
                pics =[]
                for i in imgs:
                    pic = discord.File(i)
                    pics.append(pic)
                await channel1.send(files=pics)
            await aaa.remove_reaction(emoji, data.member)


def setup(bot):
    bot.add_cog(Event(bot))
