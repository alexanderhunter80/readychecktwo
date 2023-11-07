# Logging.
import logging
import logging.config
logging.config.fileConfig("logging.conf")
opsLog = logging.getLogger("ops")



# Imports.
import os
from dotenv import load_dotenv
from classes.readycheck import ReadyCheck, glimpse, findInOptions, generateFingerprintFromInteraction



# ReadyCheck methods.
def findUniqueReadyCheck(storage, interaction):
	opsLog.debug('enter')

	result = False

	possibleFingerprint = generateFingerprintFromInteraction(interaction)
	opsLog.debug(f'possible fingerprint {possibleFingerprint}')

	allChecks = storage.values()
	for rc in allChecks:
		if rc["fingerprint"] == possibleFingerprint:
			result = True
			break

	opsLog.debug(f'exit {result}')
	return result

def getReadyCheckByMessageId(storage, id):
	opsLog.debug('enter')
	result = None
	if id in storage:
		result = storage[id]
	opsLog.debug(f'exit {glimpse(result) if result is not None else result}')
	return result

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
	rc["sentMessageID"] = sentMessage.id
	opsLog.debug(f"message id {rc['sentMessageID']}")

	storage[rc["sentMessageID"]] = rc
	opsLog.info(f'Inserted {glimpse(rc)} into checks')	

	opsLog.debug("exit")
	return

async def isReadyCheckComplete(bot, payload, rc):
	opsLog.debug("enter")
	result = False

	channel = await bot.fetch_channel(payload.channel_id)
	message = await channel.fetch_message(payload.message_id)
	opsLog.debug(f'Message retrieved: {message}')

	if message is None:
		return result

	reactors = await countReactorsToMessage(message, rc["uniqueReactors"])
	log.debug(f'Reactors: {reactors}')

	# check against target

	opsLog.debug("exit")
	return	

async def countReactorsToMessage(message, uniqueReactors):	
	opsLog.debug(f"enter {uniqueReactors}")
	result = 0

	if uniqueReactors is True:
		opsLog.debug("uniqueReactors is true, counting reactions per person")
		reactors = set()
		for r in message.reactions:
			opsLog.debug(f'Reaction: {r.emoji}')
			rlist = [user async for user in r.users()]
			for user in rlist:
				opsLog.debug(f'User: {user.name}')
				reactors.add(user.id)
			result = len(reactors)
	elif uniqueReactors is False:
		opsLog.debug("uniqueReactors is false, counting total reactions")
		for r in message.reactions:
			result += r.count
	else:
		raise TypeError("uniqueReactors was not a boolean")

	opsLog.debug(f"exit {result}")
	return result

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