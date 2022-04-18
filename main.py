# Main
import discord
from discord.ext import commands
import os


# This is a very hacky custom help menu. This will need improvement when the bot matures
class CustomHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping):
        for cog in mapping:
            await self.get_destination().send('```;register\t-\tRegister with the bot\n;join\t-\tJoin the '
                                              'queue\n;leave\t-\tLeave the queue\n;queue\t-\tSee who is currently in '
                                              'queue\n;clear\t-\tClear all players from the queue```')
        return await super().send_bot_help(mapping)


# retrieves the secret key from another directory outside the repo.
# temporary fix until I spend time to learn a better way
def getSecret():
    os.chdir('..')
    secretFile = open('secret.txt', 'r')
    fileString = secretFile.read()
    secretFile.close()
    os.chdir('queueb')
    return fileString


# function to turn the lobby list into a string for printing
def playerListStr(pQueue):
    playerListString = ''
    for item in pQueue:
        playerListString += str(item) + '\n'
    return playerListString


# function to print the lobby queue
def lobbyToString(pQueue):
    lobbyMarkdownString = ('```Lobby Queue [' + str(len(pQueue)) + '/10]\n' + str(playerListStr(pQueue)) + '```')
    return lobbyMarkdownString


##########################################
# Begins Main:
##########################################
# Retrieves secret key from the outside file
secret = getSecret()

# Initializes the game queue and the lobby queue
gameQueue = []
lobbyQueue = []

# Initializes the bot with the command prefix ; and the custom help command
bot = commands.Bot(command_prefix=';', help_command=CustomHelpCommand())


@bot.event
async def on_ready():
    print('Bot is ready')


@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')


# commands related to registration

# commands related to user access to the queue
@bot.command()
async def join(ctx):
    if ctx.author in lobbyQueue:
        await ctx.send('```' + str(ctx.author) + ' is already in queue```')
    else:
        lobbyQueue.append(ctx.author)
        await ctx.send('```[' + str(len(lobbyQueue)) + '/10] ' + str(ctx.author) + ' has joined the queue```')


@bot.command()
async def queue(ctx):
    lobbyPrint = lobbyToString(lobbyQueue)
    await ctx.send(lobbyPrint)


@bot.command()
async def leave(ctx):
    if ctx.author in lobbyQueue:
        lobbyQueue.remove(ctx.author)
        await ctx.send('```[' + str(len(lobbyQueue)) + '/10] ' + str(ctx.author) + ' has left the queue```')
    else:
        await ctx.send('```' + str(ctx.author) + ' was not in queue```')


@bot.command()
async def clear(ctx):
    lobbyQueue.clear()
    await ctx.send('```[0/10] The queue has been cleared```')


# Commands to enable aliases to the above bot commands
@bot.command()
async def j(ctx):
    await join(ctx)


@bot.command()
async def q(ctx):
    await queue(ctx)


@bot.command()
async def l(ctx):
    await leave(ctx)


@bot.command()
async def c(ctx):
    await clear(ctx)


bot.run(secret)
