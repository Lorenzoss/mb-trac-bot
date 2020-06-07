import discord
import time
from discord.ext import commands

class Useless(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def mosconi(self, ctx):
        msg = await ctx.send("<:Mosconi_basta:635900996526014514>")
        for i in range(10):
            time.sleep(1)
            await msg.edit(content=str("<:Mosconi_senzaParole:635897171618693130>"))
            time.sleep(1)
            await msg.edit(content=str("<:Mosconi_wtf:635898640002711591>"))
            time.sleep(1)
            await msg.edit(content=str("<:Mosconi_basta:635900996526014514>"))
            time.sleep(1)

    @commands.command()
    async def mosc1(self, ctx):
        await ctx.send("https://tenor.com/J6W7.gif")

    @commands.command()
    async def mosc2(self, ctx):
        await ctx.send("https://tenor.com/FGG4.gif")

    @commands.command()
    async def mosc3(self, ctx):
        await ctx.send("https://tenor.com/0UMA.gif")

    @commands.command()
    async def canc(self, ctx):
        await ctx.send("https://tenor.com/bcwA5.gif")

    @commands.command()
    async def please(self, ctx):
        await ctx.send("https://imgur.com/a/AZn1j5D")

    @commands.command(aliases=['rc', 'miSonoRottoIl'])
    async def misonorottoil(self, ctx):
        await ctx.send("**Cazzo**\nhttps://www.youtube.com/watch?v=FTMB5H1AOl8")

def setup(client):
    client.add_cog(Useless(client))
