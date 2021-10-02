import json
import os
import discord
from discord.ext import commands

with open('setting.json', 'r',encoding='utf8') as jfile:
    settingfile = json.load(jfile)

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print(">>Bot is online<<")
    channel = bot.get_channel(settingfile['channel_poster'])
    await channel.send(f">>Bot is online<<")



for filename in os.listdir('./cmds'):
    if(filename.endswith('.py')):
        try:
            bot.load_extension(f"cmds.{filename[:-3]}")
            print("import: "+filename)
        except:
            print("import: " + filename+" fail")

# 啟動bot()token
if __name__ =='__main__':
    bot.run(settingfile['TOKEN'])


