import discord
import json
from discord.ext import commands
from discord.utils import get

class Counter(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(help='Conteggia tutti i messaggi nel server [270\'000]')
    async def conteggio(self, ctx):
        client = self.client
        server = client.get_guild(419080385989967872)
        channels = await server.fetch_channels()
        results = {}
        for i in channels:
            try:
                channel = client.get_channel(i.id)
                c = 0
                async for message in channel.history(limit=None):
                    c += 1
                print(str(i.name))
                print(str(c))
                results[str(i.name)] = c
            except:
                await ctx.send(f'{i.name} - Non conteggiato')

        with open('result.json', 'w') as fp:
            json.dump(results, fp)

        sum = 0
        for i in results:
            sum += int(results[i])

        await ctx.send(f'Totale messaggi: {str(sum)}')

def setup(client):
    client.add_cog(Counter(client))
