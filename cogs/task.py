import discord
import csv
import shutil
from bs4 import BeautifulSoup
from datetime import datetime
from discord.ext import commands, tasks

class Tasks(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.modhubScrapper.start()
        self.modListScrapper.start()
        self.loopTaskUtentiSqualificati.start()

    @tasks.loop(seconds=60)
    async def loopTaskUtentiSqualificati(self):
        client = self.client
        with open('screenContest/utentiSqualificati.csv', mode='r', encoding='cp1252') as f:
            utentiSqualificati = csv.reader(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in utentiSqualificati:
                if int(row[1]) <= 60:
                    server = client.get_guild(419080385989967872)
                    member = server.get_member(int(row[0]))
                    role = get(server.roles, name='Squalificato')
                    await member.remove_roles(role, reason='Sono passati 7 giorni')
        with open('screenContest/utentiSqualificati.csv', mode='r', encoding='cp1252') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            with open('temp/tempUtentiSqualificati.csv', mode='w', newline='', encoding='cp1252') as temp:
                writer = csv.writer(temp, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for row in reader:
                    if int(row[1]) <= 60:
                        pass
                    else:
                        writer.writerow([row[0],str(int(row[1])-60)])
        shutil.move('temp/tempUtentiSqualificati.csv', 'screenContest/utentiSqualificati.csv')

    newModsMsg = None
    @tasks.loop(seconds=60)
    async def modhubScrapper(self):
        if not datetime.today().weekday() > 4:
            newModsMsg = newModsMsg
            if 14 <= datetime.today().now().hour <= 17:
                client = self.client
                url = 'https://www.farming-simulator.com/mods.php?lang=en&country=it'
                res = requests.get(url)
                htmlPage = res.content
                soup = BeautifulSoup(htmlPage, 'html.parser')
                mods = soup.select('div.mod-item__content')
                categories = soup.select('div.mod-item__img')
                lastModName, newMods = '', False
                with open('scrapper/modhub/lastMod.txt', 'r') as file:
                    for line in file:
                        lastModName = line

                if mods[0].h4.text != lastModName:
                    with open('scrapper/modhub/lastMod.txt', 'w') as file:
                        file.write(mods[0].h4.text)
                    newMods = True
                    if newModsMsg == None:
                        date = f'{str(datetime.today().day)}/{str(datetime.today().month)}/{str(datetime.today().year)}'
                        embed = discord.Embed(
                            colour=discord.Colour.green(),
                            title=f'Nuove mod - {date}',
                        )
                        embed.add_field(name='Top', value='Nessuna', inline=False)
                        embed.add_field(name='New', value='Nessuna', inline=True)
                        embed.add_field(name='Update', value='Nessuna', inline=True)
                        embed.set_footer(text=f'{str(datetime.today().day)}/{str(datetime.today().month)}/{str(datetime.today().year)}')
                        embed.set_thumbnail(url='https://i.imgur.com/Ls2FTTc.png')
                        channel = client.get_channel(560860216384684033)
                        newModsMsg = await channel.send(embed=embed)

                if newModsMsg != None:
                    embed = newModsMsg.embeds[0]
                    oldEmbed = embed.to_dict()

                    textTop = oldEmbed['fields'][0]['value']
                    textNew = oldEmbed['fields'][1]['value']
                    try:
                        textNew2 = oldEmbed['fields'][3]['value']
                        textNew2Exist = True
                    except:
                        textNew2 = 'Nessuna'
                        textNew2Exist = False
                    textUpdate = oldEmbed['fields'][2]['value']
                    try:
                        textUpdate2 = oldEmbed['fields'][4]['value']
                        textUpdate2Exist = True
                    except:
                        textUpdate2 = 'Nessuna'
                        textUpdate2Exist = False

                    c = 0
                    for i in mods:
                        mod = i.h4.text
                        author = i.span.text
                        category = categories[c].div.text
                        link = pyshorteners.Shortener().tinyurl.short('https://www.farming-simulator.com/' + categories[c].find('a', href=True)['href'])

                        if mod != lastModName:
                            textToAdd = f'[→ ]({link})**{mod}**  *{author}*'
                            if category == 'NEW!':
                                if textNew == 'Nessuna':
                                    textNew = textToAdd
                                elif len(textNew + '\n' + textToAdd) >= 1024:
                                    if textNew2 == 'Nessuna':
                                        textNew2 = textToAdd
                                    else:
                                        textNew2 = textNew2 + '\n' + textToAdd
                                else:
                                    textNew = textNew + '\n' + textToAdd
                            elif category == 'UPDATE!':
                                if textUpdate == 'Nessuna':
                                    textUpdate = textToAdd
                                elif len(textUpdate + '\n' + textToAdd) >= 1024:
                                    if textUpdate2 == 'Nessuna':
                                        textUpdate2 = textToAdd
                                    else:
                                        textUpdate2 = textUpdate2 + '\n' + textToAdd
                                else:
                                    textUpdate = textUpdate + '\n' + textToAdd
                            elif category == 'TOP!':
                                if textTop == 'Nessuna':
                                    textTop = textToAdd
                                else:
                                    textTop = textTop + '\n' + textToAdd
                        else:
                            break
                        c += 1

                    if newMods == True:
                        embed.set_field_at(index=0, name='Top', value=textTop, inline=False)
                        embed.set_field_at(index=1, name='New', value=textNew, inline=True)
                        embed.set_field_at(index=2, name='Update', value=textUpdate, inline=True)
                        if textNew2Exist:
                            embed.set_field_at(index=3, name='New2', value=textNew2, inline=False)
                        if textUpdate2Exist:
                            embed.set_field_at(index=4, name='Update2', value=textUpdate2, inline=True)
                        if textNew2 != 'Nessuna' or textUpdate2 != 'Nessuna':
                            embed.add_field(name='New [2]', value=textNew2, inline=True)
                        if textUpdate2 != 'Nessuna':
                            embed.add_field(name='Update [2]', value=textUpdate2, inline=True)

                        await newModsMsg.edit(embed=embed)
                else:
                    print('Messaggio modhub non trovato')
            elif newModsMsg != None:
                newModsMsg = None

    @tasks.loop(seconds=350)
    async def modListScrapper(self):
        if not datetime.today().weekday() > 4:
            if 13 <= datetime.today().now().hour <= 15:
                client = self.client
                url = 'https://forum.giants-software.com/viewtopic.php?f=963&t=140422'
                res = requests.get(url)
                htmlPage = res.content
                soup = BeautifulSoup(htmlPage, 'html.parser')

                contents = soup.select('div.content')
                text = contents[0].text
                text = text[1492:-15]
                oldText, newText = '', ''

                with open('scrapper/listNewMods/list.txt', 'w', encoding='cp1252') as f:
                    f.write(text)
                with open('scrapper/listNewMods/list.txt', 'r', encoding='cp1252') as f:
                    newText = f.readlines()
                with open('scrapper/listNewMods/oldList.txt', 'r', encoding='cp1252') as f:
                    oldText = f.readlines()

                if not newText == oldText:
                    channel = client.get_channel(560860216384684033)
                    await channel.send(text)
                    with open('scrapper/listNewMods/oldList.txt', 'w', encoding='cp1252') as f:
                        f.write(text)

def setup(client):
    client.add_cog(Tasks(client))
