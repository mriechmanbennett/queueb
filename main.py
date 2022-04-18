# Main
import discord
from discord.ext import commands
import os


# retrieves the secret key from another directory outside the repo.
# temporary fix until I spend time to learn a better way
def getSecret():
    os.chdir('..')
    secretFile = open('secret.txt', 'r')
    fileString = secretFile.read()
    secretFile.close()
    os.chdir('queueb')
    return fileString


# function to initialize queue

# function to join the queue

# function to leave the queue

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


# function to clear the queue (admin only)


##########################################
# Begins Main:
##########################################
# Retrieves secret key from the outside file
secret = getSecret()

# Initializes the game queue and the lobby queue
gameQueue = []
lobbyQueue = []

# Initializes the bot with the command prefix ;
bot = commands.Bot(command_prefix=';')


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
        await ctx.send(str(ctx.author) + ' is already in queue')
    else:
        lobbyQueue.append(ctx.author)
        await ctx.send(str(ctx.author) + ' has joined the queue')


@bot.command()
async def q(ctx):
    lobbyPrint = lobbyToString(lobbyQueue)
    await ctx.send(lobbyPrint)


@bot.command()
async def leave(ctx):
    if ctx.author in lobbyQueue:
        lobbyQueue.remove(ctx.author)
        await ctx.send(str(ctx.author) + ' has left the queue')
    else:
        await ctx.send('You were not in queue')


bot.run(secret)
