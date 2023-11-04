# Logging.
import logging
import logging.config
logging.config.fileConfig("logging.conf")
log = logging.getLogger("bot")
log.debug("Logger initialized")



# Imports.
import os, discord, urllib.request, asyncio
from dotenv import load_dotenv
from discord.ext import commands, tasks



# Token.
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")



# Intents.
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
bot = commands.Bot(command_prefix='/', intents=intents)



# Message respondings.
@bot.event
async def on_message(message):
    print("message was: " + message.content)
    if message.author == bot.user:
        return
    if message.content == '!radar':
        urllib.request.urlretrieve('https://radar.weather.gov/ridge/standard/CONUS_loop.gif', "rdr.gif")
        await message.channel.send(file=discord.File('rdr.gif'))



# Commands.
@bot.tree.command(name="ready", description="Call a ready check")
async def readycheck(interaction: discord.interactions.Interaction, target: int, mention: discord.Role = None, unique: bool = None):
    await interaction.response.defer()
    log.debug(f'Received readycheck: %s, %s, %s', target, mention, unique)
    await interaction.followup.send('readycheck received!')



# Bootstrap.
@bot.event
async def on_ready():
    bot.change_presence(status=discord.Status.online)
    await bot.tree.sync()
    print(f'We have logged in as {bot.user}')

bot.run(DISCORD_TOKEN)
print('Finished')