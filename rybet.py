#rybet.py

#importing all the libaries used
import discord
import discord.utils
from discord.ext import commands
import os
from dotenv import load_dotenv
import random

#setting up the core information from the bot
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
bot = commands.Bot(command_prefix='$', description="RyBet's bot")

#Automatic rules for when the bot is active
@bot.event
async def on_ready():
    print("Rybet is online as" + bot.user.name + " | " + bot.user.id)

#automatically grant new members a standard role
@bot.event(pass_context=True)
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name="Player")
    await  bot.add_roles(member, role)

#standard coinflip
@bot.command()
async def coinflip(ctx):
    choice = random.getrandbits(1)
    if choice:
        output = "Heads"
    else:
        output = "Tails"
    await ctx.reply(":coin: | " + output)


#activating the bot
bot.run(TOKEN)