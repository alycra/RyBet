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

@client.event #depo/withdraw
async def args(message, usr, amount):
    if message.author == client.user:
        return
    
    if message.author.id == 762737260617269268:
        if message.content.startswith('$deposit') or message.content.startswith('$depo'):
            await message.reply('Added: ' + amount + " to <@" + usr.id + "> balance")

client.run(TOKEN)