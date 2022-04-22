import discord
from discord.ext import commands


# This is a very hacky custom help menu. This will need improvement as the bot matures
class CustomHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping):
        # Removed this for loop temporarily. I got it from a guide, and it iterates once for each cog loaded.
        # If I used a less hacky help function, it would be fine. I can revisit this later, leaving the for in for
        # future reference.
        # for cog in mapping:
        await self.get_destination().send('```queueb commands:\n;register    -        Register with the '
                                          'bot\n;join        -        Join the queue\n;leave       -        Leave '
                                          'the queue\n;queue       -        See who is currently in queue\n;clear '
                                          '      -        Clear all players from the queue```')
        return await super().send_bot_help(mapping)