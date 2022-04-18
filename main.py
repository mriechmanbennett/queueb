# Main
import discord
from discord.ext import commands
import os


# This is a very hacky custom help menu. This will need improvement as the bot matures
class CustomHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping):
        for cog in mapping:
            await self.get_destination().send('```queueb commands:\n;register    -        Register with the '
                                              'bot\n;join        -        Join the queue\n;leave       -        Leave '
                                              'the queue\n;queue       -        See who is currently in queue\n;clear '
                                              '      -        Clear all players from the queue```')
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


# function to turn a list of players into a string for printing
def playerListStr(pQueue):
    playerListString = ''
    for item in pQueue:
        playerListString += str(item) + '\n'
    return playerListString


# function to print the lobby queue
def lobbyToString(pQueue):
    lobbyMarkdownString = ('```Lobby Queue [' + str(len(pQueue)) + '/10]\n' + str(playerListStr(pQueue)) + '```')
    return lobbyMarkdownString


# function to print the game and players
def gameToString(pQueue, gameID):
    gameMarkdownString = ('```Game #' + str(gameID) + '\n' + str(playerListStr(pQueue) + '```'))


############################################
# Secret Management and Bot Initialization:
############################################
# Retrieves secret key from the outside file
secret = getSecret()

# Initializes the game queue and the lobby queue global variables
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


#################################################
# commands related to registration and standings
#################################################
# Command to register for the ten mans
@bot.command()
async def register(ctx):
    await ctx.send('```User registration under development. Use ;join to join the queue```')


# Command to view current top of the leaderboard
@bot.command()
async def leaderboard(ctx):
    await ctx.send('```leaderboard formatted here```')


# Command to view current elo and standings
@bot.command()
async def elo(ctx):
    await ctx.send('```your elo and leaderboard standings here```')


###############################################
# commands related to user access to the queue
###############################################
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


##########################
# Mod commands
##########################
@bot.command()
async def clear(ctx):
    lobbyQueue.clear()
    await ctx.send('```[0/10] The queue has been cleared```')


#######################################################
# Commands to enable aliases to the above bot commands
#######################################################
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


# Runs the bot with the secret key that was obtained previously
bot.run(secret)
secret = 'no secret'
