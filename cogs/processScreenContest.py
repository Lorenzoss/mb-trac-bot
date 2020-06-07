import discord
import os
import json
import asyncio
import requests
import pandas as pd
import pyshorteners
from datetime import datetime
from wetransfer import TransferApi
from PIL import Image, ImageDraw, ImageOps, ImageFont
from discord.utils import get
from discord.ext import commands
from concurrent.futures import ThreadPoolExecutor

minStars = 20
with open('tokens.json', mode='r') as f:
    token = json.load(f)['wetransfer']
weTransferApi = TransferApi(token)

def getScreen(linkScreen, fileName):
    r = requests.get(linkScreen, stream=True)
    with open(fileName, 'wb') as f:
        f.write(r.content)

def checkDir(nameDir):
    if not os.path.exists(nameDir):
        os.mkdir(nameDir)
        print(f'Cartella {nameDir} inesistente - Cartella creata')


class ProcessScreenContest(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def screenContest(self, ctx, month):
        client = self.client
        dateStart = datetime.now()
        if os.path.exists('Screen'):
            shutil.rmtree('Screen')
        file = f'screenContest/logs/screen_contest_{str(month)}_{str(datetime.today().year)}.csv'
        df = pd.read_csv(file)
        df.sort_values(['Count Star', 'Message ID', 'Author ID', 'Links'], axis=0, ascending=False, inplace=True,)
        await ctx.send('Creazione screen in corso ...')
        upFiles = []
        # Check if the dir exist - if not it create them
        checkDir('temp/tempScreen')
        checkDir('temp/tempAvatar')
        checkDir('temp/finalScreen')
        directory = 'temp/finalScreen/'
        def generateScreens():
            c = 0  # Counter for df indices
            for i in df['Message ID']:
                if int(df.loc[df['Message ID'] == i, 'Count Star']) >= minStars:
                    server = client.get_guild(419080385989967872)
                    member = server.get_member(int(df.loc[df['Message ID'] == i, 'Author ID']))
                    if member != None:
                        if server == member.guild:
                            user = client.get_user(int(df.loc[df['Message ID'] == i, 'Author ID']))
                            color = member.colour
                            index = df.index[df['Message ID'] == i].tolist()[0]
                            screenLinkDownload = df.loc[index,'Links']
                            avatarLinkDownload = user.avatar_url
                            firstName = str(user.display_name)
                            secondName = f'{str(user.name)}#{str(user.discriminator)}'
                            if firstName == 'Crownzilla ✪':
                                firstName = 'Crownzilla'
                            if secondName == '@Crownzilla ✪#2937':
                                secondName = '@Crownzilla#2937'
                            else:
                                pass

                            if '|' in firstName:
                                nameFile = firstName.replace('|','')
                            else:
                                nameFile = firstName
                            if '|' in user.display_name:
                                editImageName = directory + f'{str(c + 1)}_' + str(user.display_name).replace('|','') + '.png'
                            else:
                                editImageName = directory + f'{str(c + 1)}_{str(user.display_name)}.png'

                            filenameScreen = f'temp/tempScreen/temp_{nameFile}.png'
                            filenameAvatar = f'temp/tempAvatar/temp_{nameFile}.png'

                            getScreen(screenLinkDownload, filenameScreen)

                            if os.path.exists(filenameScreen):
                                getScreen(avatarLinkDownload, filenameAvatar)
                                # Resize images - Not complete, it requires some if cond for images which are not in 16:9
                                with Image.open(filenameScreen) as image:
                                    width, height = image.size
                                    # Scale
                                    if width != 1920 and height != 1080:
                                        image = ImageOps.fit(image, (1920, 1080), method=3, centering=(0.5, 0.5))
                                    image.save(filenameScreen)  # Overwrite temp screen
                                with Image.open(filenameScreen).convert('RGBA') as image:
                                    width, height = image.size
                                    # Crop
                                    #image = image.crop((0, 81, 1920, 1080))  # Crop the top
                                    image = image.crop((0, 0, 1920, 1080))  # Restore the default size (16:9)
                                    tempImage = Image.new('RGBA', [1920,1080], (255,255,255,0))
                                    # Author box
                                    draw = ImageDraw.Draw(tempImage)
                                    draw.rectangle([(0, 1080), (1920, 1000)], fill=(51, 53, 63, 230))  # Main box
                                    draw.rectangle([(0, 1000), (1920, 999)], fill=(66, 68, 78, 230))  # 'Line'

                                    image = Image.alpha_composite(image, tempImage)

                                    # Avatar
                                    with Image.open(filenameAvatar) as avatar:  # Open and modify the Avatar
                                        avatar = avatar.resize((60, 60))
                                        # Mask
                                        size = (1500, 1500)
                                        mask = Image.new('L', size, 0)
                                        draw = ImageDraw.Draw(mask)
                                        draw.ellipse((0, 0) + size, fill=255)
                                        mask = mask.resize((60, 60), resample=3)
                                        avatar = avatar.resize((60, 60))
                                        image.paste(avatar, (850, 1010), mask=mask)
                                    # Author name
                                    fontMain = ImageFont.truetype('resources/fonts/Whitney-Semibold.ttf', 28)  # First name
                                    fontSub = ImageFont.truetype('resources/fonts/Whitney-Medium.ttf', 25)  # Second name
                                    t = ImageDraw.Draw(image)
                                    t.text((width / 2 - 30, 1010), firstName, fill=(color.r, color.g, color.b), font=fontMain, align='left')
                                    t.text((width / 2 - 30, 1042), secondName, fill=(110, 115, 125), font=fontSub, align='left')
                                    image.save(editImageName)
                                    # Delete temp files
                                    os.remove(filenameAvatar)
                                    os.remove(filenameScreen)
                                    upFiles.append(editImageName)
                            c += 1
                else:
                    break
        # Fix for bot freeze
        loop = asyncio.get_event_loop()
        block = await loop.run_in_executor(ThreadPoolExecutor(), generateScreens)
        await ctx.send(f'Upload screen ... {str(datetime.now() - dateStart)}')
        def uploadScreen():
            link = (weTransferApi.upload_files('Screen contest', upFiles))
        block2 = await loop.run_in_executor(ThreadPoolExecutor(), uploadScreen)
        await ctx.send(f'Download screen: {str(link)}')
        for i in os.listdir('./temp/finalScreen'):
            os.remove(f'./temp/finalScreen/{i}')

def setup(client):
    client.add_cog(ProcessScreenContest(client))
