# Logging.
import logging
import logging.config
logging.config.fileConfig("logging.conf")
log = logging.getLogger("ops")



# Imports.
import os
from dotenv import load_dotenv
from classes.readycheck import ReadyCheck, glimpse



# Database methods.
def findUniqueReadyCheck(collection, message):
	log.debug('enter findUniqueReadyCheck')
	log.debug(collection)
	# ReadyCheck items should always be limited to one per user per channel
	test = collection.insert_one({name:"test",payload:"whatever"})
	log.debug(test)
	result = collection.find_one({"author":message.author.id,"guild":message.guild.id,"channel":message.channel.id})
	log.debug('exit %s', result)
	return result

def findReadyCheckByMessageId(collection, id):
	return collection.find_one({"message":id})

async def createReadyCheck(ctx, target, mention, uniqueReactors, collection):
	rc = ReadyCheck()
	rc.build(ctx.message, target, mention, uniqueReactors)            

	authorName = ctx.message.author.name

	messageText = f'{authorName} has called a ready check for {rc["target"]} players!  React to this message to signal that you are ready.'

	mentionInMessage = getRoleMentionByName(ctx.message.guild, rc["mention"])

	if mentionInMessage is not None:
		messageText = mentionInMessage+" "+messageText

	sentMessage = await ctx.send(messageText)
	rc["message"] = sentMessage.id

	collection.insert_one(rc)
	log.debug(f'Inserted {rc["id"]} into checks')  

	return

# async def removeReadyCheck(bot, collection, rc):
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