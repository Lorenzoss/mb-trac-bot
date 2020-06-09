import discord
import asyncio
from datetime import datetime
from discord.ext import commands
from discord.utils import get

class Aziende(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ultimiMess(self, ctx):
        client = self.client
        server = client.get_guild(419080385989967872)
        channels = await server.fetch_channels()
        text = ''
        for channel in channels:
            channel = client.get_channel(channel.id)
            if str(channel.category) == 'Le vostre aziende':
                try:
                    lastMessage = await channel.history(limit=1).flatten()
                    text += f'\n*{channel.name}:* ultimo messaggio **{(datetime.now() - lastMessage[0].created_at).days} giorni fa**'
                except:
                    pass
        await ctx.send(text)

    @commands.command()
    async def ultimiMess60g(self, ctx):
        client = self.client
        server = client.get_guild(419080385989967872)
        channels = await server.fetch_channels()
        text = ''
        for channel in channels:
            channel = client.get_channel(channel.id)
            if str(channel.category) == 'Le vostre aziende':
                try:
                    lastMessage = await channel.history(limit=1).flatten()
                    if (datetime.now() - lastMessage[0].created_at).days >= 60:
                        text += f'\n*{channel.name}:* ultimo messaggio **{(datetime.now() - lastMessage[0].created_at).days} giorni fa**'
                except:
                    pass
        await ctx.send(text)

    @commands.command(help='Riordina le farm in ordine alfabetico')
    async def reorder(self, ctx):
        client = self.client
        server = client.get_guild(419080385989967872)
        channels = await server.fetch_channels()
        farms = []
        initPos = None
        for channel in channels:
            channel = client.get_channel(channel.id)
            if str(channel.category) == 'Le vostre aziende':
                if not str(channel.name) == 'informazioni':
                    farms.append(channel.name)
                    if initPos == None:
                        initPos = int(channel.position)
        farms.sort()
        c = 0
        for i in farms:
            channel = discord.utils.get(channels, name=i)
            pos = initPos + c
            await channel.edit(position=pos)
            c += 1
        await ctx.send('Canali riordinati in ordine alfabetico!')

    @commands.command()
    async def test(self, ctx):
        client = self.client
        delete = False
        member = client.get_guild(419080385989967872).get_member(ctx.author.id)
        channel = await member.create_dm()
        try:
            msg = await channel.send(content=f'''Ciao {member.name}, la tua sezione personale sul server di Nicko87 non è aggiornata da più di 90 giorni.
Per mantenere il server ordinato vorremmo sapere se hai intenzione nei prossimi giorni di utilizzarla.
Se sì aggiungi la reazione ✅, in alternativa se non ti interessa più aggiungi la reazione ❌ e il tuo canale verrà eliminato.
\n*Se non verrà aggiunta nessuna reazione entro una settimana il canale sarà eliminato*''')
        except:
            msg = await channel.send()

        await msg.add_reaction('✅')
        await msg.add_reaction('❌')

        def check(react, user):
            if not user.bot:
                return str(react.emoji)
        try:
            react, user = await client.wait_for('reaction_add', timeout=25.0, check=check)
            if react.emoji == '✅':
                delete = False
            elif react.emoji == '❌':
                delete = True
        except asyncio.TimeoutError:
            delete = True
            await channel.send('Tempo finito')
        finally:
            if delete == True:
                await channel.send('Il canale sarà cancellato')
            else:
                await channel.send('Il canale non sarà cancellato')

def setup(client):
    client.add_cog(Aziende(client))
