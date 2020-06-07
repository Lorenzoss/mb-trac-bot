import discord
import cv2
import os
import requests
import tensorflow as tf
from datetime import datetime
from discord.utils import get
from discord.ext import commands

modelScreen = tf.keras.models.load_model('machineLearning/screen.model')
modelFoto = tf.keras.models.load_model('machineLearning/foto.model')

categoriesScreen = ['hud', 'nohud']
categoriesFoto = ['foto', 'screen']

filepath = 'temp/tempScreen.png'

texts = {
'hudIt':f'''Ciao <@%s>, è stato rilevato che la tua screen potrebbe avere degli hud.
Ti chiedo gentilmente di rimuovere la screen e se possibile ricaricarla senza hud secondo il regolamento <#681795560721743894>.\n
Se invece ritieni che si tratti di un errore ignora questo messaggio.\n*Per aiutarmi a migliorare il mio algoritmo visita <#715861909471232030> e <#715861927439499361>*''',
'hudEn':f'''Hey <@%s>, the bot has detected that your last screen could have the huds.
Please remove it and if you can resend it without huds, check the rules at <#681795560721743894>.\n
If you think that is an error no problem, ignore it.\n*To help me improve my algorithms check <#715861909471232030> and <#715861927439499361>*'''
}

def prepareScreen(filepath):
    img_size_x = 512
    img_size_y = 256
    img_array = cv2.imread(filepath, cv2.IMREAD_COLOR)
    new_array = cv2.resize(img_array, (img_size_x, img_size_y))
    return new_array.reshape(-1, img_size_x, img_size_y, 3)

def prepareFoto(filepath):
    img_size_x = 450
    img_size_y = 350
    img_array = cv2.imread(filepath, cv2.IMREAD_COLOR)
    new_array = cv2.resize(img_array, (img_size_x, img_size_y))
    return new_array.reshape(-1, img_size_x, img_size_y, 3)

def getScreen(linkScreen, fileName):
    r = requests.get(linkScreen, stream=True)
    with open(fileName, 'wb') as f:
        f.write(r.content)

class MachineLearning(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, ctx):
        client = self.client
        initDate = datetime.now()
        if ctx.author.bot == True:
            pass
        elif ctx.channel.id == 650627936826687507:
            getScreen(ctx.attachments[0].url, filepath)
            prediction = modelScreen.predict([prepareScreen(filepath)])
            if categoriesScreen[int(prediction[0][0])] == 'hud':
                channel_msg = client.get_channel(659856847854895114)
                server = client.get_guild(419080385989967872)
                role = get(server.roles, name='Guest')
                member = server.get_member(ctx.author.id)
                if role in member.roles:
                    await channel_msg.send(texts['hudEn']%str(ctx.author.id))
                else:
                    await channel_msg.send(texts['hudIt']%str(ctx.author.id))
            os.remove(filepath)
        elif ctx.channel.id == 715904557204635648:
            if ctx.attachments:
                getScreen(ctx.attachments[0].url, filepath)
                prediction = modelScreen.predict([prepareScreen(filepath)])
                channel = client.get_channel(715904557204635648)
                if categoriesScreen[int(prediction[0][0])] == 'hud':
                    await channel.send('La screen probabilmente ha gli hud')
                elif categoriesScreen[int(prediction[0][0])] == 'nohud':
                    await channel.send('La screen probabilmente non ha gli hud')
                os.remove(filepath)
        elif ctx.channel.id == 716758711506567188:
            if ctx.attachments:
                getScreen(ctx.attachments[0].url, filepath)
                prediction = modelFoto.predict([prepareFoto(filepath)])
                channel = client.get_channel(716758711506567188)
                if categoriesFoto[int(prediction[0][0])] == 'screen':
                    await channel.send(f'Secondo i miei complessi calcoli è probabilmente una screen - {datetime.now() - initDate}')
                elif categoriesFoto[int(prediction[0][0])] == 'foto':
                    await channel.send(f'Secondo i miei complessi calcoli è probabilmente una foto - {datetime.now() - initDate}')
                os.remove(filepath)

def setup(client):
    client.add_cog(MachineLearning(client))
