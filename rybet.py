import discord
import random
import os
from dotenv import load_dotenv
from discord.utils import get
from discord.ext import commands
intents = discord.Intents.default()
intents.message_content = True
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

ADMIN = '762737260617269268'

client = commands.Bot(command_prefix='$', intents=intents)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="RyBet's poker table"))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$scam'):
        await message.reply("https://cdn.discordapp.com/attachments/1034515302446268446/1036332161827078144/videoplayback.mp4")
    await client.process_commands(message)


@client.command()  # ping command
async def ping(ctx):
    await ctx.send(':ping_pong: | ' + str(round(client.latency, 2)) + 'ms')


@client.command()  # coinflip
async def coinflip(ctx, choice: str = None, amount: float = None):
    bot_choice = random.getrandbits(1)  # generate random bot number of 1 or 0
    if bot_choice:  # apply a result to the number
        output = 'Heads'
    else:
        output = 'Tails'
    if choice != None:
        if amount != None:
            try:
                if choice == 'heads' or choice == 'head':  # taking the user input and converting it to binary
                    user_choice = 1
                elif choice == 'tails' or choice == 'tail':
                    user_choice = 0
                if user_choice == bot_choice:  # if the users choice is the same as the bot
                    result = amount * 2.0
                    emoji = ':white_check_mark:'
                else:  # if the users choice is not the same as the bot
                    result = amount * -1.0
                    emoji = ':x:'
                await ctx.reply(':coin: | ' + emoji + ' | $' + str(result))
            except:
                await ctx.reply('Incorect usage of command, use $help for correct usage')
        else:
            await ctx.reply('Please specifiy a bet wager')
    else:
        await ctx.reply(':coin: | ' + output)


@client.command()  # Dice
async def dice(ctx, user_choice: float = None, amount: float = None):
    bot_choice = random.random()
    output = str(round(bot_choice * 100, 2)) + '%'
    if user_choice != None:
        if amount != None:
            try:
                user_choice = user_choice/100.0
                if user_choice <= bot_choice:
                    state = 'Loss'
                    emoji = ':x:'
                    result = amount * -1.0
                elif user_choice > bot_choice:
                    state = 'win'
                    emoji = ':white_check_mark:'
                    result = amount / user_choice
                await ctx.reply(':signal_strength: | ' + emoji + ' | $' + str(result))
            except:
                await ctx.reply('Incorect usage of command, use $help for correct usage')
        else:
            await ctx.reply('Please specifiy a bet wager')
    else:
        if bot_choice <= 0.5:
            emoji = ':x:'
        elif bot_choice > 0.5:
            emoji = ':white_check_mark:'
        await ctx.reply(':signal_strength: | ' + emoji + ' | ' + output)


@client.command()  # dicethrow
async def dicethrow(ctx, user_choice: float = None, amount: float = None):
    bot_choice = random.randint(1, 6)
    if user_choice != None:
        if amount != None:
            try:
                if user_choice == bot_choice:
                    emoji = ':white_check_mark:'
                    result = amount * 6.0
                else:
                    emoji = ':x:'
                    result = amount * -1.0
                await ctx.reply(':game_die: | ' + emoji + ' | $' + str(result))
            except:
                await ctx.reply('Incorect usage of command, use $help for correct usage')
        else:
            await ctx.reply('Please specifiy a bet wager')
    else:
        await ctx.reply(':game_die: | ' + str(bot_choice))

client.run(TOKEN)
