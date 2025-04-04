import discord
import json
import subprocess
from discord import app_commands
import asyncio
from typing import Literal

with open('config.json', 'r') as file:
    data = json.load(file)

BOT_TOKEN = data['token']
BOT_CLIENT = discord.Object(id=data['clientId'])
BOT_GUILD = discord.Object(id=data['guildId'])

MC_PATH_START = data['mcPathStart']
MC_PATH_STOP = data['mcPathStop']
MC_SERVER_STATUS = False

VALHEIM_PATH_START = data['valheimPathStart']
VALHEIM_PATH_STOP = data['valheimPathStop']
VALHEIM_SERVER_STATUS = False

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=BOT_GUILD)
        await self.tree.sync(guild=BOT_GUILD)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
client = MyClient(intents=intents)

@client.event
async def on_ready():
    print(f'------')
    print(f'Logged on as {client.user}!')
    print(f'------')
    await client.change_presence(activity=discord.Game("steamhappy"))


@client.tree.command(name = "hello", description = "Says hello to the user!")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f'Hi!')

@client.tree.command(name = "server", description = "Start or stop the minecraft server")
@app_commands.describe(action='If you want to start or stop the server', game='the game server you want to start/stop')
async def server(interaction: discord.Interaction, action: Literal['start', 'stop'], game: Literal['minecraft', 'valheim']):
    global MC_SERVER_STATUS
    global VALHEIM_SERVER_STATUS
    if action == "start":
        if game == "minecraft":
            if MC_SERVER_STATUS == True:
                await interaction.response.defer()
                await asyncio.sleep(delay=0)
                await interaction.followup.send(f'MC Geyser has already been started.')
            elif MC_SERVER_STATUS == False:
                mc_proc_start = subprocess.Popen([MC_PATH_START], shell=False)
                await interaction.response.defer()
                await asyncio.sleep(delay=0)
                await interaction.followup.send(f'MC Geyser is starting up.')
                await client.change_presence(activity=discord.Game("MC Geyser 1.21.4"))
                MC_SERVER_STATUS = True
            else:
                await interaction.response.send_message(f'If this message appears: what the fuck did you do')
        if game == "valheim":
            if VALHEIM_SERVER_STATUS == True:
                await interaction.response.defer()
                await asyncio.sleep(delay=0)
                await interaction.followup.send(f'Valheim Vanilla has already been started.')
            elif VALHEIM_SERVER_STATUS == False:
                valheim_proc_start = subprocess.Popen([VALHEIM_PATH_START], shell=False)
                await interaction.response.defer()
                await asyncio.sleep(delay=0)
                await interaction.followup.send(f'Valheim Vanilla is starting up.')
                await client.change_presence(activity=discord.Game("Valheim Vanilla: Patch 0.220.5"))
                VALHEIM_SERVER_STATUS = True
            else:
                await interaction.response.send_message(f'If this message appears: what the fuck did you do')
    elif action == "stop":
        if game == "minecraft":
            if MC_SERVER_STATUS == False:
                await interaction.response.defer()
                await asyncio.sleep(delay=0)
                await interaction.followup.send(f'Minecraft Geyser needs to be started first.')
            elif MC_SERVER_STATUS == True:
                mc_proc_stop = subprocess.run([MC_PATH_STOP])
                await interaction.response.defer()
                await asyncio.sleep(delay=0)
                await interaction.followup.send(f'Minecraft Geyser is being stopped.')
                await client.change_presence(activity=discord.Game("steamhappy"))
                MC_SERVER_STATUS = False
            else:
               await interaction.response.send_message(f'If this message appears: what the fuck did you do') 
        if game == "valheim":
            if VALHEIM_SERVER_STATUS == False:
                await interaction.response.defer()
                await asyncio.sleep(delay=0)
                await interaction.followup.send(f'Valheim Vanilla needs to be started first.')
            elif VALHEIM_SERVER_STATUS == True:
                valheim_proc_stop = subprocess.run([VALHEIM_PATH_STOP])
                await interaction.response.defer()
                await asyncio.sleep(delay=0)
                await interaction.followup.send(f'Valheim Vanilla is being stopped.')
                await client.change_presence(activity=discord.Game("steamhappy"))
                VALHEIM_SERVER_STATUS = False
            else:
               await interaction.response.send_message(f'If this message appears: what the fuck did you do') 
    else:
        await interaction.response.send_message(f'If this message appears: what the fuck did you do')


client.run(BOT_TOKEN)