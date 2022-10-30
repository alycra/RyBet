import discord
import random
import os
from dotenv import load_dotenv
from discord.utils import get
from discord.ext import commands
intents = discord.Intents.default()
intents.message_content = True
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

client = commands.Bot(command_prefix="$", intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="RyBet's poker table"))

@client.event
async def on_message(message):
    username = str(message.author).split("#")[0]
    channel = str(message.channel.name)
    content = str(message.content).lower().split()

    if message.author == client.user:
        return

    if message.content.startswith('$coinflip') or message.content.startswith('$coin') or message.content.startswith('$flip'):
        try:
            bot_choice = random.getrandbits(1) #generate random bot number of 1 or 0
            if bot_choice: #apply a result to the number
                output = "Heads"
            else:
                output = "Tails"
            if len(content) == 3: #if there is the standard template: $cmd tag1 tag2
                if content[1] == "heads" or content[1] == "head": #taking the user input and converting it to binary
                    user_choice = 1
                elif content[1] == "tails" or content[1] == "tail":
                    user_choice = 0
                if user_choice == bot_choice: #if the users choice is the same as the bot
                    result = float(content[2]) * 2
                    await message.reply(":coin: "+ output +" | :white_check_mark: Player: " + username + "Wins | $" + result)
                else: #if the users choice is not the same as the bot
                    result = float(content[2]) * -1
                    await message.reply(":coin: "+ output +" | :x: House wins | $" + result)
            elif len(content) > 1:
                await message.reply("Incorrect usage, correct template: $coinflip heads 0.25")
            else:
                await message.reply(":coin: | " + output)
        except:
            await message.reply("Incorect usage of commant, use $help for correct usage")

    if message.content.startswith('$dicethrow') or message.content.startswith('$die'):
        try:
            bot_choice = random.randint(1,6)
            if len(content) == 3:
                user_choice = int(content[1])
                if 1 <= user_choice <=6:
                    if bot_choice == user_choice:
                        result = float(content[2]) * 3
                        await message.reply(":game_die: " + str(bot_choice) + " | :white_check_mark: Player: " + username + " wins | $" + result)
                    else:
                        result = float(content[2]) * -1
                        await message.reply(":x: " + str(bot_choice) + " | :x: House wins | $" + result)
                else:
                    await message.reply("Incorrect number range, for a dice: 1-6")
            elif len(content) > 1:
                await message.reply("Incorrect usage, correct template: $dicethrow 5 0.25")
            else:
                choice = random.randint(1,6)
                await message.reply(":game_die: | " + str(choice))
        except:
            await message.reply("Incorect usage of command, use $help for correct usage")

    if message.content.startswith('$dice'):
        choice = random.random()
        if choice <= 0.5:
            state = "Loss"
            emoji = ":x:"
        if choice > 0.5:
            state = "win"
            emoji = ":white_check_mark:"
        output = str(round(choice * 100, 2)) + "%"
        await message.reply(emoji + " | " + output)

@client.command()
async def ping(ctx):
    print("ping requested")
    await ctx.send(":ping_pong: | " + str(round(client.latency,2)) + "ms")

client.run(TOKEN)