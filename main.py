# Main
import discord
from discord.ext import commands
import os

# retrieves the secret key from another directory outside the repo.
# temporary fix until I spend time to learn a better way
def getSecret():
    os.chdir('../secrets')
    secretFile = open('secret.txt', 'r')
    fileString = secretFile.read()
    secretFile.close()
    os.chdir('../queueb')
    return fileString

secret = getSecret()



@client.event
async def on_ready():
    print('Bot is ready')

@client.command()
async def ping(ctx):
    await ctx.send