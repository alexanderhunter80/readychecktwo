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
    botLog.debug("enter")
    botLog.debug(payload)

    rc = getReadyCheckByMessageId(checks, payload.message_id)
    checkExists = rc is not None
    botLog.debug(f'RC found? {checkExists}')

    if checkExists:
        isReady = await isReadyCheckComplete(bot, payload, rc)

    #if isReady:
    #   completeReadyCheck()

    botLog.debug("exit")
    return



# Commands.
@bot.tree.command(name="ready", description="Call a ready check")
async def ready(interaction: discord.interactions.Interaction, target: int, mention: discord.Role = None, unique: bool = True):
    botLog.debug("enter")
    await interaction.response.defer()
    botLog.info(f'Ready check called by {interaction.user}, target {target}, mention {mention}, unique {unique}')

    checkForConflicts = findUniqueReadyCheck(checks, interaction)
    if checkForConflicts:
        botLog.info("Conflicting ReadyCheck found, DMing user")
        msg = await interaction.followup.send("Can't create ready check!", wait=True)
        await msg.delete()
        await interaction.user.send("Only one ReadyCheck can be active per user per channel.  Use /cancel to remove the existing ReadyCheck if desired.")
        return
    else:
        botLog.debug("No conflicting ReadyCheck found")

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