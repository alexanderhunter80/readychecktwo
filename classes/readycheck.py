import logging
import logging.config
logging.config.fileConfig("logging.conf")
readyLog = logging.getLogger("readycheck")

from discord import Message
from collections.abc import MutableMapping
import uuid
from datetime import datetime

class ReadyCheck(MutableMapping):
    def __init__(self, data=()):
        self.mapping = {}
        self.mapping["id"] = uuid.uuid4()
        self.mapping["input"] = None
        self.mapping["target"] = None        
        self.mapping["mention"] = None
        self.mapping["uniqueReactors"] = None
        self.mapping["author"] = None
        self.mapping["guild"] = None
        self.mapping["channel"] = None
        self.mapping["authorLastKnownName"] = None
        self.mapping["guildLastKnownName"] = None
        self.mapping["channelLastKnownName"] = None
        self.mapping["createdAt"] = datetime.utcnow()
        self.mapping["updatedAt"] = datetime.utcnow()
        self.update(data)

    def __getitem__(self, key):
        return self.mapping[key]

    def __delitem__(self, key):
        del self.mapping[key]

    def __setitem__(self, key, value):
        self.mapping[key] = value
        
    def __iter__(self):
        return iter(self.mapping)

    def __len__(self):
        return len(self.mapping)

    def __repr__(self):
        return f'{type(self).__name__}({self.mapping})'



    def build(self, interaction):
        readyLog.debug("enter")
        readyLog.debug(interaction.data)
        self.mapping["input"] = interaction.data
        self.mapping["target"] = findInOptions(interaction, "target")
        self.mapping["mention"] = findInOptions(interaction, "mention")
        self.mapping["uniqueReactors"] = findInOptions(interaction, "uniqueReactors")
        self.mapping["author"] = interaction.user.id
        self.mapping["guild"] = interaction.guild_id
        self.mapping["channel"] = interaction.channel_id
        self.mapping["authorLastKnownName"] = interaction.user.name
        self.mapping["guildLastKnownName"] = interaction.guild.name
        self.mapping["channelLastKnownName"] = interaction.channel.name
        self.mapping["updatedAt"] = datetime.utcnow()
        readyLog.debug("Built "+glimpse(self))
        readyLog.debug("exit")
        return self

    def generateKey(self):
        readyLog.debug("enter")
        generatedKey = self["author"] + self["guild"] + self["channel"]
        readyLog.debug(f"exit {generatedKey}")
        return generatedKey

    def generateKeyFromInteraction(interaction):
        readyLog.debug("enter")
        generatedKey = interaction.user.id + interaction.guild_id + interaction.channel_id
        readyLog.debug(f"exit {generatedKey}")
        return generatedKey

def glimpse(rc):
    return f'ReadyCheck: {rc["authorLastKnownName"]} in {rc["guildLastKnownName"]} / {rc["channelLastKnownName"]} : target {rc["target"]}, {rc["mention"]}, {rc["uniqueReactors"]}'

def findInOptions(interaction, name):
    readyLog.debug(f"enter {name}")
    result = None
    for o in interaction.data['options']:
        if o['name'] == name:
            result = o['value']
            break
    readyLog.debug(f"exit {name} {result}")
    return result    