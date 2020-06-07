import discord
import os
import json
from discord.ext import commands

with open('tokens.json', mode='r') as f:
    token = json.load(f)['discord']

test = False

if not test:
    client = commands.Bot(command_prefix='.')
    #Import all extisting cogs from cog dir
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')
            print('Loaded cog: ' + str(filename))
else:
    client = commands.Bot(command_prefix='!')

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    print(f'{extension} loaded')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    print(f'{extension} unloaded')

@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    print(f'{extension} reloaded')

@client.command()
async def reloadAll(ctx):
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.unload_extension(f'cogs.{filename[:-3]}')
            print('Unloaded cog: ' + str(filename))
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')
            print('Loaded cog: ' + str(filename))

client.run(token)
