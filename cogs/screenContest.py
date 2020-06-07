import discord
import os
import csv
import shutil
import pandas as pd
from discord.ext import commands
from discord.utils import get
from datetime import datetime

texts = {
'maxScreenIt':'<@%s> per questo mese hai già mandato 5 screen! L\'ultima screen inviata sarà cancellata in automatico.',
'maxScreenEn':'<@%s> for this month you already sent 5 screens! The last screen will be automatically deleted.',
'autovoteIt':'Altolà birbante <@%s>!\nAvete infranto il regolamento votando la vostra stessa screen.\nGrazie al potere conferitomi da messere <@110373155301793792> in vece del sovrano <@305788036736614400> vi squalifico da codesto contest per 7 giornate.',
'autovoteEn':'Halt rascal <@%s>!\nYou can not vote your screen, you are disqualified for 7 days.',
}

linkbase = "https://discordapp.com/channels/419080385989967872/650627936826687507/"

def checkDir(nameDir):
    if not os.path.exists(nameDir):
        os.mkdir(nameDir)
        print(f'Cartella {nameDir} inesistente - Cartella creata')

def countScreens():
    screenTot = {}
    pathCSV = pathBase + f'/screen_contest_{str(datetime.today().month)}_{str(datetime.today().year)}.csv'
    df = pd.read_csv(pathCSV, header = 0)
    for i in df['Author ID']:
        if not i in screenTot:
            screenTot[i] = 1
        else:
            screenTot[i] += 1
    return screenTot

pathBase = 'screenContest/logs'
contestChannelID = 650627936826687507

class ScreenContest(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, ctx):
        client = self.client
        if not ctx.author.bot:
            if ctx.channel.id == contestChannelID and ctx.attachments:
                checkDir(pathBase)
                pathCSV = pathBase + f'/screen_contest_{str(datetime.today().month)}_{str(datetime.today().year)}.csv'
                if not os.path.exists(pathCSV):
                    with open(pathCSV, mode='w') as f:
                        writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        writer.writerow(['Author ID', 'Message ID', 'Count Star', 'Links'])
                        print(pathCSV + 'inesistente - File creato')
                #Check if the user has send more than 5 screen for that month
                #If yes the last one is deleted and the user is notified
                df = pd.read_csv(pathCSV, header = 0)
                screenTot = countScreens()
                with open(pathCSV, mode='a', newline='') as f:
                    writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow([ctx.author.id, ctx.id, 0, ctx.attachments[0].url])
                try:
                    if screenTot[ctx.author.id] > 5:
                        channel_msg = client.get_channel(659856847854895114)
                        server = client.get_guild(419080385989967872)
                        role = get(server.roles, name='Guest')
                        member = server.get_member(ctx.author.id)
                        if role in member.roles:
                            await channel_msg.send(texts['maxScreenEn']%str(ctx.author.id))
                        else:
                            await channel_msg.send(texts['maxScreenIt']%str(ctx.author.id))
                        await ctx.delete(delay=5)
                except:
                    pass

    @commands.Cog.listener()
    async def on_message_delete(self, ctx):
        client = self.client
        #Remove the screen from the csv database
        if ctx.channel.id == contestChannelID:
            pathCSV = pathBase + f'/screen_contest_{str(datetime.today().month)}_{str(datetime.today().year)}.csv'
            tempfile = 'temp/tempContest.csv'
            fields = ['Author ID', 'Message ID', 'Count Star', 'Links']
            #Basically it creates a new csv file without the row of the deleted screen
            with open(pathCSV, mode='r') as csvfile:
                reader = csv.DictReader(csvfile, fieldnames=fields)
                with open(tempfile, mode='w', newline='') as temp:
                    writer = csv.DictWriter(temp, fieldnames=fields)
                    for row in reader:
                        if row:
                            if row['Message ID'] == str(ctx.id):
                                pass
                            else:
                                row = {'Author ID': row['Author ID'], 'Message ID': row['Message ID'], 'Count Star': row['Count Star'], 'Links': row['Links']}
                                writer.writerow(row)
            shutil.move(tempfile, pathCSV)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, ctx):
        client = self.client
        if ctx.channel_id == contestChannelID:
            channel = client.get_channel(ctx.channel_id)
            channel_msg = client.get_channel(659856847854895114)
            user = client.get_user(ctx.user_id)
            message = await channel.fetch_message(ctx.message_id)
            react = get(message.reactions, emoji='\U00002B50')
            #Check if the user voted his own screen -> If yes it will be disqualified and msg deleted
            if ctx.user_id == message.author.id and str(ctx.emoji) == '⭐':
                server = client.get_guild(message.guild.id)
                member = server.get_member(ctx.user_id)
                role = get(message.guild.roles, name='Squalificato')
                roleGuest = get(message.guild.roles, name='Guest')
                if roleGuest in member.roles:
                    await channel_msg.send(texts['autovoteEn']%str(message.author.id))
                else:
                    await channel_msg.send(texts['autovoteIt']%str(message.author.id))
                await member.add_roles(role, reason='Autovotazione')
                try:
                    with open('screenContest/utentiSqualificati.csv', mode='a', newline='') as f:
                        utentiSqualificati= csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        utentiSqualificati.writerow([str(ctx.user_id), '604800'])
                except:
                    with open('screenContest/utentiSqualificati.csv', mode='w') as f:
                        utentiSqualificati = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        utentiSqualificati.writerow(['Author ID', 'Time left'])
                finally:
                    await message.delete(delay=0)

                print(f'{str(datetime.now())} -- {str(user.name)} --- id: {str(ctx.user_id)} ha aggiunto la stella al messaggio: {str(ctx.message_id)}')

            #Update the number of votes in the csv database
            if str(ctx.emoji) == '⭐' and ctx.channel_id == contestChannelID:
                pathCSV = pathBase + f'/screen_contest_{str(datetime.today().month)}_{str(datetime.today().year)}.csv'
                tempfile = 'tempContest.csv'
                fields = ['Author ID', 'Message ID', 'Count Star', 'Links']
                #Basically it creates a new csv file with the updated counted votes
                with open(pathCSV, mode='r') as csvfile:
                    reader = csv.DictReader(csvfile, fieldnames=fields)
                    with open(tempfile, mode='w', newline='') as temp:
                        writer = csv.DictWriter(temp, fieldnames=fields)
                        for row in reader:
                            if row:
                                if row['Message ID'] == str(ctx.message_id):
                                    if react == None:
                                        reactCount = 0
                                    else:
                                        reactCount = react.count
                                    row['Count Star'] = str(reactCount)
                                row = {'Author ID': row['Author ID'], 'Message ID': row['Message ID'], 'Count Star': row['Count Star'], 'Links': row['Links']}
                                writer.writerow(row)
                shutil.move(tempfile, pathCSV)

    @commands.command(help='Restituisce il numero di screen inviate')
    async def screen(self, ctx):
        count = 0
        pathContestCSV = f'screenContest/logs/screen_contest_{str(datetime.today().month)}_{str(datetime.today().year)}.csv'
        df = pd.read_csv(pathContestCSV, header = 0)
        for i in df['Author ID']:
            if i == ctx.author.id:
                count += 1
        await ctx.send(f'<@{str(ctx.author.id)}> hai mandato {str(count)} screen')

    @commands.command(help='Restituisce il numero totale di screen inviate')
    async def totScreen(self, ctx):
        client = self.client
        embed = discord.Embed(
            colour=discord.Colour.blue(),
            title='Screen partecipanti',
        )
        text, count = '', 0
        screenTot = countScreens()
        for i in screenTot:
            user = client.get_user(int(i))
            if user != None:
                text = text + str(user.name) + ': ' + str(screenTot[i]) + '/5' + '\n'
                count += screenTot[i]
        embed.add_field(name='Numero screen', value=str(text), inline=False)
        embed.add_field(name='Totale screen', value=str(count), inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def countStar(self, ctx):
        client = self.client
        channel = client.get_channel(contestChannelID)
        currentMonth = datetime.today().month
        checkDir(pathBase)
        pathCSV = pathBase + '/screen_contest_' + str(datetime.today().month) + '_' + str(datetime.today().year) + '.csv'
        #Reset csv database
        with open(pathCSV, mode='w') as f:
            writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['Author ID', 'Message ID', 'Count Star', 'Links'])
            print(pathCSV + '- File creato o resettato')
        #Search all the messages at the current month
        async for message in channel.history(limit=500):
            if message.created_at.month == currentMonth:
                react = get(message.reactions, emoji='\U00002B50')
                if message.attachments:
                    if react == None:
                        reactCount = 0
                    else:
                        reactCount = react.count
                    with open(pathCSV, mode='a', newline='') as f:
                        contestLog = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        contestLog.writerow([message.author.id, message.id, reactCount, message.attachments[0].url])
            else:
                break
        await ctx.send('Conteggio effettuato!')

    @commands.command(help='Invia la classifica del contest dal 1° al 15° posto')
    async def classificaContest(self, ctx):
        client = self.client
        embed = discord.Embed(
            colour=discord.Colour.blue(),
            title='Classifica screen contest',
            description='Primi 15 posti',
        )
        count = 0
        pathContestCSV = f'screenContest/logs/screen_contest_{str(datetime.today().month)}_{str(datetime.today().year)}.csv'
        df = pd.read_csv(pathContestCSV, header = 0)
        df.sort_values(['Count Star', 'Message ID', 'Author ID', 'Links'], axis=0, ascending=False, inplace=True,)
        for i in df['Message ID']:
            countStar = int(df.loc[df['Message ID'] == i, 'Count Star'])
            user = client.get_user(int(df.loc[df['Message ID'] == i, 'Author ID']))
            link = linkbase + str(i)
            testo = f'[Stelle: {str(countStar)}]({str(link)})'
            if count < 15:
                if count == 0:
                    embed.add_field(name='🥇' + str(user.name), value=testo, inline=True)
                elif count == 1:
                    embed.add_field(name='🥈' + str(user.name), value=testo, inline=True)
                elif count == 2:
                    embed.add_field(name='🥉' + str(user.name), value=testo, inline=True)
                else:
                    embed.add_field(name=str(user.name), value=testo, inline=True)
            else:
                break
            count += 1
        await ctx.send(embed=embed)

    @commands.command(help='Invia la classifica del contest dal 16° al 50° posto')
    async def classificaCompleta(self, ctx):
        client = self.client
        embed = discord.Embed(
            colour=discord.Colour.blue(),
            title='Classifica screen contest',
            description='Dal 16° posto al 50°',
        )
        text3, text4, text5, text6, text7, text8, text9 = '','','','','','',''
        count = 0
        pathContestCSV = f'screenContest/logs/screen_contest_{str(datetime.today().month)}_{str(datetime.today().year)}.csv'
        df = pd.read_csv(pathContestCSV, header = 0)
        df.sort_values(['Count Star', 'Message ID', 'Author ID', 'Links'], axis=0, ascending=False, inplace=True,)
        for i in df['Message ID']:
            countStar = int(df.loc[df['Message ID'] == i, 'Count Star'])
            user = client.get_user(int(df.loc[df['Message ID'] == i, 'Author ID']))
            link = linkbase + str(i)
            testo = f'[Stelle: {str(countStar)}]({str(link)})'
            if count < 15:
                pass
            elif count < 20:
                text3 = text3 + f'**{str(user.name)}:**{testo}\n'
            elif count < 25:
                text4 = text4 + f'**{str(user.name)}:**{testo}\n'
            elif count < 30:
                text5 = text5 + f'**{str(user.name)}:**{testo}\n'
            elif count < 35:
                text6 = text6 + f'**{str(user.name)}:**{testo}\n'
            elif count < 40:
                text7 = text7 + f'**{str(user.name)}:**{testo}\n'
            elif count < 45:
                text8 = text8 + f'**{str(user.name)}:**{testo}\n'
            elif count < 50:
                text9 = text9 + f'**{str(user.name)}:**{testo}\n'
            else:
                break
            count += 1
        if text3 != '':
            embed.add_field(name='Posti dal 16° al 20°:', value=str(text3), inline=False)
        else:
            pass
        if text4 != '':
            embed.add_field(name='Posti dal 21° al 25°:', value=str(text4), inline=False)
        else:
            pass
        if text5 != '':
            embed.add_field(name='Posti dal 26° al 30°:', value=str(text5), inline=False)
        else:
            pass
        if text6 != '':
            embed.add_field(name='Posti dal 31° al 35°:', value=str(text6), inline=False)
        else:
            pass
        if text7 != '':
            embed.add_field(name='Posti dal 36° al 40°:', value=str(text7), inline=False)
        else:
            pass
        if text8 != '':
            embed.add_field(name='Posti dal 41° al 45°:', value=str(text8), inline=False)
        else:
            pass
        if text9 != '':
            embed.add_field(name='Posti dal 46° al 50°:', value=str(text9), inline=False)
        else:
            pass
        await ctx.send(embed=embed)

    @commands.command(help='Restituisce se si è squalificati')
    async def squalificato(self, ctx):
        id = ctx.author.id
        client = self.client
        with open('screenContest/utentiSqualificati.csv', mode='r') as f:
            squalificatoValue = None
            utentiSqualificati = csv.reader(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            if os.stat('screenContest/utentiSqualificati.csv').st_size == 0:
                squalificatoValue = False
            else:
                for row in utentiSqualificati:
                    if row[0] == str(id):
                        seconds = int(row[1])
                        m, s = divmod(seconds, 60)
                        h, m = divmod(m, 60)
                        d, h = divmod(h, 24)
                        if d == 1:
                            time = f'{d:d} giorno, {h:d}:{m:02d} ore'
                        elif d > 1:
                            time = f'{d:d} giorni, {h:d}:{m:02d} ore'
                        elif d < 1:
                            time = f'{h:d}:{m:02d} ore'
                        await ctx.send(f'<@{str(id)}> sei squalificato ancora per: {time}')
                        squalificatoValue = True
                        break
                    else:
                        squalificatoValue = False
            if squalificatoValue == False:
                await ctx.send(f'<@{str(id)}> non sei squalificato!')

def setup(client):
    client.add_cog(ScreenContest(client))
