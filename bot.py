# Logging.
import logging
import logging.config
logging.config.fileConfig("logging.conf")
botLog = logging.getLogger("bot")
botLog.debug("Logger initialized")
from pprint import pprint
import inspect



# Imports.
import os, discord, urllib.request, asyncio, pymongo, bson
from dotenv import load_dotenv
from discord.ext import commands, tasks
from ops import *


# Token.
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")



# Database.
# Create admin user with db.createUser({user:'username',pwd:'password',roles:[{role:'userAdmin',db:'admin'}]})
# Then edit /etc/mongod.conf "security:authorization:true"
MONGO_U=os.getenv("MONGODB_USERNAME")
MONGO_P=os.getenv("MONGODB_PW")
MONGO_AS=os.getenv("MONGODB_AUTHSOURCE")
mongoClient = pymongo.MongoClient(username=MONGO_U, password=MONGO_P, authSource=MONGO_AS, uuidRepresentation='standard')
botLog.debug(mongoClient)
db = mongoClient.readycheck
botLog.debug(db.list_collection_names())
checks = db.checks



# Intents.
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
bot = commands.Bot(command_prefix='/', intents=intents)



# Event listeners.
@bot.event
async def on_raw_reaction_add(payload):
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    user = await bot.fetch_user(payload.user_id)
    botLog.debug(f'Heard raw reaction add: %s, %s, %s', channel, message, user)
    return



# Commands.
@bot.tree.command(name="ready", description="Call a ready check")
async def ready(interaction: discord.interactions.Interaction, target: int, mention: discord.Role = None, unique: bool = None):
    await interaction.response.defer()
    botLog.info(f'Ready check called by {interaction.user}, target {target}, mention {mention}, unique {unique}')

    botLog.debug(pprint(inspect.getmembers(interaction)))


    #checkForConflicts = findUniqueReadyCheck(checks, interaction.message)
    #botLog.debug(checkForConflicts)


    await interaction.followup.send('readycheck received')
    return

@bot.tree.command(name="cancel", description="Cancel an open ready check")
async def cancel(interaction: discord.interactions.Interaction):
    await interaction.response.send_message('cancel received')
    return

@bot.tree.command(name="clearall", description="Admin only: clear all ready checks")
async def clearall(interaction: discord.interactions.Interaction):
    await interaction.response.send_message('clearall received')
    return


# Bootstrap.
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online)
    await bot.tree.sync()
    print(f'We have logged in as {bot.user}')

bot.run(DISCORD_TOKEN)
print('Finished')