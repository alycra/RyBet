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
    username = str(message.author).split('#')[0]
    channel = str(message.channel.name)
    content = str(message.content).lower().split()

    if message.author == client.user:
        return
    if message.content.startswith('$scam'):
        await message.reply("https://cdn.discordapp.com/attachments/1034515302446268446/1036332161827078144/videoplayback.mp4")

    if message.content.startswith('$dicethrow') or message.content.startswith('$die'):
        try:
            bot_choice = random.randint(1,6)
            if len(content) == 3:
                user_choice = int(content[1])
                if 1 <= user_choice <=6:
                    if bot_choice == user_choice:
                        result = float(content[2]) * 3
                        await message.reply(':game_die: ' + str(bot_choice) + ' | :white_check_mark: Player: ' + username + ' wins | $' + result)
                    else:
                        result = float(content[2]) * -1
                        await message.reply(':x: ' + str(bot_choice) + ' | :x: House wins | $' + result)
                else:
                    await message.reply('Incorrect number range, for a dice: 1-6')
            elif len(content) > 1:
                await message.reply('Incorrect usage, correct template: $dicethrow 5 0.25')
            else:
                choice = random.randint(1,6)
                await message.reply(':game_die: | ' + str(choice))
        except:
            await message.reply('Incorect usage of command, use $help for correct usage')
    await client.process_commands(message)

@client.command() #ping command
async def ping(ctx):
    await ctx.send(':ping_pong: | ' + str(round(client.latency,2)) + 'ms')

@client.command() #coinflip
async def coinflip(ctx, choice : str = None, amount : float = None):
    bot_choice = random.getrandbits(1) #generate random bot number of 1 or 0
    if bot_choice: #apply a result to the number
        output = 'Heads'
    else:
        output = 'Tails'
    if choice != None:
        if amount != None:
            try:
                if choice == 'heads' or choice == 'head': #taking the user input and converting it to binary
                    user_choice = 1
                elif choice == 'tails' or choice == 'tail':
                    user_choice = 0
                if user_choice == bot_choice: #if the users choice is the same as the bot
                    result = amount * 2.0
                    await ctx.reply(':coin: '+ output +' | :white_check_mark: Player Wins | $' + str(result))
                else: #if the users choice is not the same as the bot
                    result = amount * -1.0
                    await ctx.reply(':coin: '+ output +' | :x: House wins | $' + str(result))
            except:
                await ctx.reply('Incorect usage of command, use $help for correct usage')
        else:
            await ctx.reply('Please specifiy a bet wager')
    else:
        await ctx.reply(':coin: | ' + output)

@client.command()
async def dice(ctx, user_choice : float = None, amount : float = None):
    bot_choice = random.random()
    output = str(round(bot_choice * 100, 2)) + '%'
    if user_choice != None:
        if amount != None:
            try:
                user_choice = 1.0 - (user_choice/100.0)
                if user_choice <= bot_choice:
                    state = 'Loss'
                    message = 'House wins'
                    emoji = ':x:'
                    result = amount * -1.0
                elif user_choice > bot_choice:
                    state = 'win'
                    message = 'Player wins'
                    emoji = ':white_check_mark:'
                    result = amount / user_choice
                await ctx.reply(emoji + ' | ' + message + ' | $' + result)
            except Exception as e:
                await ctx.reply('Incorect usage of command, use $help for correct usage')
                print (e)
        else:
            await ctx.reply('Please specifiy a bet wager')
    else:
        if bot_choice <= 0.5:
            state = 'Loss'
            emoji = ':x:'
        elif bot_choice > 0.5:
            state = 'win'
            emoji = ':white_check_mark:'
        await ctx.reply(emoji + ' | ' + state + ' | ' + output)



client.run(TOKEN)