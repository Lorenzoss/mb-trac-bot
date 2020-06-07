import discord
import pandas
import csv
import os
from discord.utils import get
from discord.ext import commands
from pandas.plotting import table
import pandas as pd
import matplotlib.pyplot as plt

class Utility(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(status=discord.Status.online, activity=discord.Game('ls'))
        print(f'{self.client.user} has connected to Discord!')

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.client.latency * 1000)} ms')
        
    @commands.command(hidden=True)
    async def cleanConsole(self, ctx):
        print('\n'*25)

    @commands.command(aliases=['moniSenzaSpunta', 'noSpunta'], help='Restituisce una lista con tutti gli utenti senza spunta')
    async def senzaSpunta(self, ctx):
        client = self.client
        server = client.get_guild(419080385989967872)
        role = get(server.roles, name='Senza spunta')
        a, i = '', 0
        for member in server.members:
            if role in member.roles:
                a = a + f'\n{str(member.display_name)}'
                i = i + 1
        await ctx.send(a)
        await ctx.send(f'**Totale membri senza spunta: {str(i)}**')

    @commands.command(aliases=['cdc'], hidden=True)
    async def consiglioDiClasse(self, ctx, arg1, arg2):
        client = self.client
        user = client.get_user(int(arg1[3:-1]))
        if user == None:
            await ctx.send('Utente non trovato')
        attribute = arg2.lower()
        categories = [
            'ciacerello',
            'rompicojoni',
            'sbruffone',
            'zizzagnatore',
            'mona-innocuo',
        ]
        pagelle = []
        index = None
        userPresent = False

        if not attribute in categories:
            text = 'Categoria non valida\nLe categorie sono:'
            for i in categories:
                text += '\n' + '- ' + i
            await ctx.send(text)
        else:
            try:
                with open('utility/pagelle.csv', mode='r') as f:
                    csv_reader = csv.reader(f, delimiter=',')
                    for line in csv_reader:
                        pagelle.append(line)
            except:
                with open('utility/pagelle.csv', mode='w') as f:
                    print('utility/pagelle.csv creato')
            finally:
                for line in pagelle:
                    if line[0] == str(user.id):
                        userPresent = True
                        index = pagelle.index(line)

                if userPresent == False:
                    pagelle.append([str(user.id), 0, 0, 0, 0, 0])
                    index = pagelle.index([str(user.id), 0, 0, 0, 0, 0])
                if attribute == categories[0]:
                    pagelle[index][1] = 1
                elif attribute == categories[1]:
                    pagelle[index][2] = 1
                elif attribute == categories[2]:
                    pagelle[index][3] = 1
                elif attribute == categories[3]:
                    pagelle[index][4] = 1
                elif attribute == categories[4]:
                    pagelle[index][5] = 1

                with open('utility/pagelle.csv', mode='w', newline='') as f:
                    csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    for line in pagelle:
                        csv_writer.writerow(line)
                await ctx.send(f'Aggiunto **{arg2}** a <@{str(user.id)}>!')

    @commands.command(hidden=True)
    async def pagelle(self, ctx):
        client = self.client
        try:
            with open('utility/pagelle.csv', mode='r') as f:
                utenti,ciacerelli,rompicojoni,sbruffoni,zizzagnatori,mona = [],[],[],[],[],[]
                def tableValue(arg):
                    if arg == '0':
                        return ' '
                    elif arg == '1':
                        return 'X'

                server = client.get_guild(419080385989967872)
                csv_reader = csv.reader(f, delimiter=',')
                for line in csv_reader:
                    utenti.append(server.get_member(int(line[0])).display_name)
                    ciacerelli.append(tableValue(str(line[1])))
                    rompicojoni.append(tableValue(str(line[2])))
                    sbruffoni.append(tableValue(str(line[3])))
                    zizzagnatori.append(tableValue(str(line[4])))
                    mona.append(tableValue(str(line[5])))

                df = pd.DataFrame()

                df['Utente'] = utenti
                df['Ciacerello'] = ciacerelli
                df['Rompicojoni'] = rompicojoni
                df['Sbruffone'] = sbruffoni
                df['Zizzagnatore'] = zizzagnatori
                df['Mona-innocuo'] = mona

            colors = [[0.9,0.5,0.13],[0.9,0.5,0.13],[0.9,0.5,0.13],[0.9,0.5,0.13],[0.9,0.5,0.13],[0.9,0.5,0.13]]
            fig, ax = plt.subplots(figsize=(10, 0.75)) # set size frame
            ax.xaxis.set_visible(False)  # hide the x axis
            ax.yaxis.set_visible(False)  # hide the y axis
            ax.set_frame_on(False)  # no visible frame, uncomment if size is ok
            tab = table(ax, df,
                        loc='upper right',
                        colWidths=[0.15]*len(df.columns),
                        cellLoc='center',
                        colColours=colors)  # where df is your data frame
            tab.auto_set_font_size(False) # Activate set fontsize manually
            tab.set_fontsize(11) # if ++fontsize is necessary ++colWidths
            tab.scale(1.2, 1.3) # change size table
            plt.savefig('temp/table.png', transparent=True)
            file = discord.File('temp/table.png', filename='temp/table.png')
            await ctx.send('', file=file)
            os.remove('temp/table.png')
        except:
            await ctx.send('File pagelle.csv inesistente')

def setup(client):
    client.add_cog(Utility(client))
