# This example requires the 'message_content' intent.
import os
import discord
import random
import logging
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

token = ''

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$ping'):
        await message.channel.send('pong')
    if message.content.startswith('$coinflip'):
        result = random.randint(1,2)
        output = "error"
        if (result == 1):
            output = "heads"
        if (result == 2):
            output = "tails"
        await message.channel.send(output)

client.run(token, log_handler=handler)