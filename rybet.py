import discord
import random
import os
from dotenv import load_dotenv
intents = discord.Intents.default()
intents.message_content = True
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="RyBet's poker table"))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
        
    if message.content.startswith('$ping'):
        await message.channel.send(":ping_pong: | " + str(round(client.latency,2)) + "ms")

    if message.content.startswith('$coinflip'):
        choice = random.getrandbits(1)
        if choice:
            output = "Heads"
        else:
            output = "Tails"
        await message.reply(":coin: | " + output)

    if message.content.startswith('$diethrow'):
        choice = random.randint(1,6)
        await message.reply(":game_die: | " + str(choice))

    if message.content.startswith('$dice'):
        choice = random.random()
        if choice <= 0.5:
            state = "Loss"
            emoji = ":x:"
        if choice > 0.5:
            state = "win"
            emoji = ":white_check_mark:"
        output = str(choice * 100) + "%"
        await message.reply(emoji + " | " + output)
    

client.run(TOKEN)