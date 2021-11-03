import json
import os
import discord
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_choice,create_option

from cmds import time

with open('setting.json', 'r',encoding='utf8') as jfile:
    settingfile = json.load(jfile)

bot = commands.Bot(command_prefix='!')
slash = SlashCommand(bot,sync_commands=True)

@slash.slash(
    name="hello",
    description="send hello",
    guild_ids=settingfile['guild_ids']
)
async def _hello(ctx):
    await ctx.send("!sendpic")

@bot.event
async def on_ready():
    print(">>Bot is online<<")
    channel = bot.get_channel(settingfile['channel_poster'])
    await channel.send(f">>Bot is online<<")


@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cmds.{extension}')
    await ctx.send(f"Loaded {extension} ")

@bot.command()
async def reload(ctx, extension):
    bot.reload_extension(f'cmds.{extension}')
    await ctx.send(f"ReLoaded {extension} ")

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f"cmds.{extension}")
    await ctx.send(f"UnLoaded {extension} ")



for filename in os.listdir('./cmds'):
    if(filename.endswith('.py')):
        # bot.load_extension(f"cmds.{filename[:-3]}")
        try:
            bot.load_extension(f"cmds.{filename[:-3]}")
            print("import: "+filename)
        except:
            print("import: " + filename+" fail")

# 啟動bot()token
if __name__ =='__main__':
    bot.run(settingfile['TOKEN'])


