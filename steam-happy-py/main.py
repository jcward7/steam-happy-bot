import discord
import json
import subprocess
from discord import app_commands

with open('config.json', 'r') as file:
    data = json.load(file)

BOT_TOKEN = data['token']
MC_PATH = data['mcPath']
BOT_CLIENT = discord.Object(id=data['clientId'])
BOT_GUILD = discord.Object(id=data['guildId'])

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
client = MyClient(intents=intents)

@client.event
async def on_ready():
    print(f'------')
    print(f'Logged on as {client.user}!')
    print(f'------')


@client.tree.command(name = "hello", description = "Says hello to the user!")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f'{interaction.user.mention} Hi!')


@client.tree.command(name = "server", description = "Starts the minecraft server.")
async def server(interaction: discord.Interaction):
    server = subprocess.Popen([MC_PATH])
    await interaction.response.send_message(f'{interaction.user.mention} Server has now started!')

client.run(BOT_TOKEN)