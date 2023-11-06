# Logging.
import logging
import logging.config
logging.config.fileConfig("logging.conf")
botLog = logging.getLogger("bot")
botLog.debug("Logger initialized")
from pprint import pprint
import inspect



# Imports.
import os, discord, urllib.request, asyncio, bson
from dotenv import load_dotenv
from discord.ext import commands, tasks
from ops import *


# Token.
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")



# Dictionary.
checks = {}



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
    botLog.debug("enter")
    await interaction.response.defer()
    botLog.info(f'Ready check called by {interaction.user}, target {target}, mention {mention}, unique {unique}')

    #checkForConflicts = findUniqueReadyCheck(checks, interaction)
    #botLog.debug(checkForConflicts)

    await createReadyCheck(checks, interaction)

    botLog.debug("exit")
    return

@bot.tree.command(name="find", description="Query whether you have an open ready check")
async def find(interaction: discord.interactions.Interaction):
    botLog.debug("enter")
    await interaction.response.defer()

    result = findUniqueReadyCheck(checks, interaction)

    await interaction.followup.send(f'check found? {result}')
    botLog.debug("exit")
    return

@bot.tree.command(name="cancel", description="Cancel an open ready check")
async def cancel(interaction: discord.interactions.Interaction):
    botLog.debug("enter")
    await interaction.response.send_message('cancel received')
    botLog.debug("exit")
    return    

@bot.tree.command(name="clearall", description="Admin only: clear all ready checks")
async def clearall(interaction: discord.interactions.Interaction):
    botLog.debug("enter")
    await interaction.response.send_message('clearall received')
    botLog.debug("exit")
    return


# Bootstrap.
@bot.event
async def on_ready():
    botLog.debug("enter")
    await bot.change_presence(status=discord.Status.online)
    await bot.tree.sync()
    botLog.info(f'We have logged in as {bot.user}')
    botLog.debug("exit")
    return

bot.run(DISCORD_TOKEN)
print('Finished')