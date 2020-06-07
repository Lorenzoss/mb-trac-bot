import discord
from discord.ext import commands

moderators = [
    110373155301793792, # Lorenzo
    305788036736614400, # Nicko
    369489846743465985  # Fab
]

class EmojiAnimated(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def doge(self, ctx):
        if ctx.author.id in moderators:
            await ctx.message.delete(delay=0)
            await ctx.send("<a:doge:714909671559004160>")
        else:
            await ctx.send("Se vuoi usare le emoji animate comprati nitro, cancaro!")

    @commands.command()
    async def thinking(self, ctx):
        if ctx.author.id in moderators:
            await ctx.message.delete(delay=0)
            await ctx.send("<a:thinking:714909658128711792>")
        else:
            await ctx.send("Se vuoi usare le emoji animate comprati nitro, cancaro!")

    @commands.command()
    async def hype(self, ctx):
        if ctx.author.id in moderators:
            await ctx.message.delete(delay=0)
            await ctx.send("<a:hype:714911249669947505>")
        else:
            await ctx.send("Se vuoi usare le emoji animate comprati nitro, cancaro!")

    @commands.command()
    async def popcorn(self, ctx):
        if ctx.author.id in moderators:
            await ctx.message.delete(delay=0)
            await ctx.send("<a:popcorn:714911260503834695>")
        else:
            await ctx.send("Se vuoi usare le emoji animate comprati nitro, cancaro!")

    @commands.command()
    async def smart(self, ctx):
        if ctx.author.id in moderators:
            await ctx.message.delete(delay=0)
            await ctx.send("<a:smart:714911287045521488>")
        else:
            await ctx.send("Se vuoi usare le emoji animate comprati nitro, cancaro!")

def setup(client):
    client.add_cog(EmojiAnimated(client))
