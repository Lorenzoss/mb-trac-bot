import discord
from discord.ext import commands
from discord.utils import get

class NewMembers(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, ctx):
        client = self.client
        channel_react = client.get_channel(ctx.channel_id)
        channel_flag = client.get_channel(612381669910904874)
        if channel_react == channel_flag:
            if str(ctx.emoji) == "✅":
                if ctx.message_id == 612624238058274816:
                    user = client.get_user(ctx.user_id)
                    server = client.get_guild(419080385989967872)
                    member = server.get_member(ctx.user_id)
                    role = get(server.roles, name="Senza spunta")
                    if role in member.roles:
                        await member.remove_roles(role, reason="Il mona ha messo la spunta")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, ctx):
        client = self.client
        channel_react = client.get_channel(ctx.channel_id)
        channel_flag = client.get_channel(612381669910904874)
        if channel_react == channel_flag:
            if str(ctx.emoji) == "✅":
                if ctx.message_id == 612624238058274816:
                    user = client.get_user(ctx.user_id)
                    server = client.get_guild(419080385989967872)
                    member = server.get_member(ctx.user_id)
                    role = get(server.roles, name="Senza spunta")
                    if not role in member.roles:
                        await member.add_roles(role, reason="Il mona ha tolto la spunta")

def setup(client):
    client.add_cog(NewMembers(client))
