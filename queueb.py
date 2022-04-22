# Main
import discord
from discord.ext import commands
import os
from CustomHelp import CustomHelpCommand
import datetime
from game import Game


# retrieves the secret key from another directory outside the repo.
# temporary fix until I spend time to learn a better way
def getSecret():
    os.chdir('..')
    secretFile = open('secret.txt', 'r')
    fileString = secretFile.read()
    secretFile.close()
    os.chdir('queueb')
    return fileString


def makeGame(lobbyQueue):
    # make a new game, will eventually gen numbers
    newGame = Game(lobbyQueue, 0)
    return newGame


# pops the queue to make a game lobby. Should be agnostic of how many players are in the lobby, to allow a manual pop
# returns the new game as a game object
def popQueue(lobbyQueue):
    newGame = makeGame(lobbyQueue)
    return newGame


# function to turn a list or dictionary of players into a string for printing
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


def main():
    # Initializes the bot with the command prefix ; and the custom help command
    bot = commands.Bot(command_prefix=';', help_command=CustomHelpCommand())

    # Loads all cogs available in the ./cogs directory
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')

    ############################################
    # Bot Initialization:
    ############################################

    # Initializes the game queue and the lobby queue variables
    activeGames = {}  # dictionary with gameID as key and game object as value
    lobbyQueue = {}  # Dictionary with player id as key and time they joined queue as value

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
            lobbyQueue.update({ctx.author: datetime.datetime.now()})
            await ctx.send('```[' + str(len(lobbyQueue)) + '/10] ' + str(ctx.author) + ' has joined the queue```')

            if len(lobbyQueue) > 9:
                newGame = popQueue(lobbyQueue)  # Code to pop queue if there are 10 players in queue
                activeGames.update({newGame.getID(): newGame})  # adds this game to the active games list
                # notify players that the queue has popped
                await ctx.channel.send('```The game is ready!\nCaptains will now pick teams```')
                # A spam notification could be annoying, leaving it off for now unless there's a problem of people not
                # showing.
                # for player in newGame.getPlayerList():
                    # await ctx.channel.send(f"{player.mention}")
                captainList = newGame.returnCaptains()
                await ctx.channel.send('```Captain 1 - ' + str(captainList[0]) + '\nCaptain 2 - ' + str(captainList[1])
                                       + '```')

    @bot.command()
    async def queue(ctx):
        lobbyPrint = lobbyToString(lobbyQueue)
        await ctx.send(lobbyPrint)

    @bot.command()
    async def leave(ctx):
        if ctx.author in lobbyQueue:
            lobbyQueue.pop(ctx.author)
            await ctx.send('```[' + str(len(lobbyQueue)) + '/10] ' + str(ctx.author) + ' has left the queue```')
        else:
            await ctx.send('```' + str(ctx.author) + ' was not in queue```')

    ##########################
    # Mod commands - in the future will be accessible only to mods
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

    # Mod Aliases
    @bot.command()
    async def c(ctx):
        await clear(ctx)

    # User accessible commands for cog management. Unneeded, but left here for future reference
    # @bot.command()
    # async def load(ctx, extension):
    #     bot.load_extension(f'cogs.{extension}')

    # @bot.command()
    # async def unload(ctx, extension):
    #     bot.unload_extension(f'cogs.{extension})')

    # @bot.command()
    # async def reload(ctx, extension):
    #     bot.unload_extension(f'cogs.{extension})')
    #     bot.load_extension(f'cogs.{extension}')

    # Retrieves secret key from the outside file
    secret = getSecret()

    # Runs the bot with the secret key that was obtained previously, then clears the secret variable
    bot.run(secret)
    secret = 'no secret'


if __name__ == '__main__':
    main()
