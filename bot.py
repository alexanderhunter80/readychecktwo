# Import various libraries.
import os, discord, urllib.request, asyncio
from dotenv import load_dotenv
from discord.ext import commands, tasks

# Set the token.
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
print(DISCORD_TOKEN)

# Define whatever this is.
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
print(intents)
client = commands.Bot(command_prefix='/', intents=intents)

# Message respondings.
@client.event
async def on_message(message):
    print("message was: " + message.content)
    if message.author == client.user:
        return
    if message.content == '!radar':
        urllib.request.urlretrieve('https://radar.weather.gov/ridge/standard/CONUS_loop.gif', "rdr.gif")
        await message.channel.send(file=discord.File('rdr.gif'))

#Commands
@client.tree.command(name="radar", description="Retrieves the live doppler radar for a station, if none given, gets CONUS.")
async def _space(ctx: discord.interactions.Interaction):
	await ctx.response.send_message(file=discord.File('rdr.gif'))

@client.event
async def on_ready():
    client.change_presence(status=discord.Status.online)
    await client.tree.sync()
    print(f'We have logged in as {client.user}')

client.run(DISCORD_TOKEN)
print('Finished')