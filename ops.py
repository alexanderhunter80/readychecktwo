# Logging.
import logging
import logging.config
logging.config.fileConfig("logging.conf")
opsLog = logging.getLogger("ops")



# Imports.
import os
from dotenv import load_dotenv
from classes.readycheck import ReadyCheck, glimpse, findInOptions



# # ReadyCheck methods.
# def findUniqueReadyCheck(storage, message):
# 	opsLog.debug('enter findUniqueReadyCheck')
# 	opsLog.debug(collection)
# 	# ReadyCheck items should always be limited to one per user per channel
# 	test = collection.insert_one({name:"test",payload:"whatever"})
# 	opsLog.debug(test)
# 	result = collection.find_one({"author":message.author.id,"guild":message.guild.id,"channel":message.channel.id})
# 	opsLog.debug('exit %s', result)
# 	return result

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

	storage[rc.generateKey()] = rc
	opsLog.debug(f'Inserted {rc["id"]} into checks')	

	await interaction.followup.send(messageText)

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