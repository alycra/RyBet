import discord
import random
import os
from dotenv import load_dotenv
from discord.utils import get
from discord.ext import commands
import mysql.connector as database
intents = discord.Intents.default()
intents.message_content = True
load_dotenv()


TOKEN = os.getenv('DISCORD_TOKEN')
try:
    conn = database.connect(
        user=os.getenv('DBUSER'),
        password=os.getenv('DBPASS'),
        host='localhost',
        database='rybet'
    )
except database.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)
cur = conn.cursor()
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
    bot_choice = random.getrandbits(1)
    if bot_choice:
        output = 'Heads'
    else:
        output = 'Tails'
    if choice != None:
        if amount != None:
            try:
                if choice == 'heads' or choice == 'head':
                    user_choice = 1
                elif choice == 'tails' or choice == 'tail':
                    user_choice = 0
                if user_choice == bot_choice:
                    result = amount
                    emoji = ':white_check_mark:'
                else:
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
                # if user input 70, becomes 0.7
                user_choice = (user_choice/100.0)
                if user_choice <= bot_choice:  # if bot has less, user wins
                    state = 'Win'
                    emoji = ':white_check_mark:'
                    result = (amount / (1.0 - user_choice)) - amount
                elif user_choice > bot_choice:  # if bot has more, bot wins
                    state = 'loss'
                    emoji = ':x:'
                    result = amount * -1.0
                await ctx.reply(':signal_strength: | ' + emoji + " " + output + ' | $' + str(result))
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
                    result = amount * 5.0
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


@client.command()  # depo
async def deposit(ctx, user_id: int = None, amount: float = None):
    if ctx.message.author.id == 762737260617269268:
        if user_id != None:
            if amount != None:
                try:
                    amount = get_bal(id) + amount
                    statement = "INSERT INTO rybet (id,balance) VALUES (%s, %s)"
                    data = (user_id, amount)
                    conn.commit()
                    await ctx.reply('Successfully added, current balance: ')
                except:
                    await ctx.reply('Error adding to database')
            else:
                await ctx.reply('Please specifiy an amount')
        else:
            await ctx.reply('Incorect usage of command, use $help for correct usage')
    else:
        await ctx.reply('Incorrect permissions')


def get_bal(id):
    try:
        statement = "SELECT balance FROM rybet WHERE id=%s"
        data = (id)
        cursor.execute(statement, data)
        for (balance) in cursor:
            return balance
    except:
        print('error getting bal for user' + id)


client.run(TOKEN)
