# Logging.
import logging
import logging.config
logging.config.fileConfig("logging.conf")
opsLog = logging.getLogger("ops")



# Imports.
import os
from dotenv import load_dotenv
from classes.readycheck import ReadyCheck, glimpse, findInOptions



# ReadyCheck methods.
def findUniqueReadyCheck(storage, interaction):
	opsLog.debug('enter')

	result = False
	opsLog.debug(result)

	possibleKey = ReadyCheck.generateKeyFromInteraction(interaction)
	opsLog.debug(f'possible key {possibleKey}')

	if possibleKey in storage:
		result = True

	opsLog.debug(f'exit {result}')
	return result

#def findReadyCheckByMessageId(storage, id):
#	return collection.find_one({"message":id})

async def createReadyCheck(storage, interaction):
	opsLog.debug("enter")

	rc = ReadyCheck()
	rc.build(interaction)

	authorName = interaction.user.name
	messageText = f'{authorName} has called a ready check for {rc["target"]} players!  React to this message to signal that you are ready.'
	mentionInMessage = getRoleMentionFromInteraction(interaction)
	opsLog.debug(mentionInMessage)
	if mentionInMessage is not None:
		messageText = str(mentionInMessage)+" "+messageText
	opsLog.debug(messageText)

	sentMessage = await interaction.followup.send(messageText, wait=True)
	rc["sentMessage"] = sentMessage
	opsLog.debug(f"message id {rc['sentMessage'].id}")

	storage[rc.generateKey()] = rc
	opsLog.info(f'Inserted {rc.generateKey()} into checks')	

	opsLog.debug("exit")
	return

# async def removeReadyCheck(storage, bot, rc):
#     try:
#         channel = await bot.fetch_channel(rc["channel"])
#         message = await channel.fetch_message(rc["message"])
#         await message.delete()
#     except Exception as e:
#         logger.error(e)

#     collection.delete_one({"id":rc["id"]})

#     rcg = glimpse(rc)
#     logger.debug(f'Removed {rcg}')

#     return    

# async def clearAllReadyChecks(collection):
#     # TODO: loop through and try to delete all associated messages

#     result = collection.delete_many({})
#     logging.warning(f'Deleted {result.deleted_count} items from database')
    
#     return    






# Helper methods.

def getRoleMentionFromInteraction(interaction):
	opsLog.debug("enter")
	guild = interaction.guild
	opsLog.debug(guild)
	roleMentionId = findInOptions(interaction, "mention")
	opsLog.debug(f"roleMentionId {roleMentionId}")
	roleMention = None

	if roleMentionId is not None:
		roleMention = guild.get_role(int(roleMentionId)).mention
		opsLog.debug(f"roleMention {roleMention}")

	if roleMention is None:  
		roleMention = guild.default_role
		opsLog.debug(f"defaulting to role {roleMention}")

	opsLog.debug(f'Role: {roleMention}')

	opsLog.debug("exit")
	return roleMention