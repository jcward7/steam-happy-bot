import discord
import json

with open('config.json', 'r') as file:
    data = json.load(file)

BOT_TOKEN = data['token']
BOT_CLIENT = data['clientId']
BOT_GUILD = data['guildId']

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'------')
        print(f'Logged on as {self.user}!')
        print(f'------')
    
    async def on_message(self, message):
        if message.author.id == client.user.id:
            return
        
        if message.content.startswith('$hello'):
            await message.channel.send('Hello!')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = MyClient(intents=intents)


client.run(BOT_TOKEN)