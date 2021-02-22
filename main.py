#desmk2.py
import os
import random
import json
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
from urllib.request import Request, urlopen
import discord

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.command(name='99', help='Responds with a random quote from Brooklyn 99')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)

@bot.command(name='amazing', help='Shows how amazing something is')
async def amazing(ctx):
    response = 'https://cdn.discordapp.com/attachments/742349549292617839/795230531528818698/Schermata_2021-01-03_alle_11.00.48.png'
    await ctx.send(response)

@bot.command(name='critic', help='Shows critic score for a searched game')
async def critic(ctx, game):
    def getGameDetails(gameId):
        #let's get some game data!!
        gameRequestString = 'https://api.opencritic.com/api/game/{}'.format(gameId)
        gameReq = Request(gameRequestString, headers={'User-Agent': 'Mozilla/5.0'})    
        gamewebpage = urlopen(gameReq).read()
        gamedata = json.loads(gamewebpage.decode())
        gameDescription = gamedata["description"]  
        embedVar = discord.Embed(title=gamedata["name"], description=gameDescription[:150] + "... " + "[more](https://www.google.com)", color=0x00ff00)        
        #try set a thumbnail
        try:
            gameThumbnail = gamedata["mastheadScreenshot"]["thumbnail"]
            embedVar.set_thumbnail(url="https://"+gameThumbnail[2:])
        except:
            print("No image found")

        try:
            for element in gamedata["Companies"]:
                if element["type"] == "DEVELOPER":
                    embedVar.add_field(name="Developer",value=element["name"])
                elif element["type"] == "PUBLISHER":
                    embedVar.add_field(name="Publisher",value=element["name"])
        except:
            print("Error finding pub/dev")

        embedVar.add_field(name="Tier",value=gamedata["tier"])
        embedVar.set_footer(text=str(currentEntry) + "/" + str(gameCount))
        return embedVar
    
    #fetch the game id
    idRequestString = 'https://api.opencritic.com/api/game/search?criteria={}'.format(game)
    idReq = Request(idRequestString, headers={'User-Agent': 'Mozilla/5.0'})    
    webpage = urlopen(idReq).read()
    data = json.loads(webpage.decode())

    #total number of games found
    gameCount = len(data)

    #current entry
    currentEntry = 1

    #check if there are any results
    if len(data) == 0:
        response = 'No Games found for search criteria {}'.format(game)
        await ctx.send(response)

    print(data[currentEntry - 1]["id"])
    embedVar = getGameDetails(data[currentEntry - 1]["id"])
    message = await ctx.send(embed=embedVar)
    await message.add_reaction("◀️")
    await message.add_reaction("▶️")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]
        # This makes sure nobody except the command sender can interact with the "menu"
    
        
    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", timeout=60, check=check)
            # waiting for a reaction to be added - times out after x seconds, 60 in this
            # example

            if str(reaction.emoji) == "▶️" and currentEntry != gameCount:
                currentEntry += 1

                #reset the id
                gameId = data[currentEntry - 1]["id"]
                print(gameId)
                #fetch the game details
                embedVar = getGameDetails(gameId)
                
                await message.edit(embed=embedVar)
                await message.remove_reaction(reaction, user)
            elif str(reaction.emoji) == "◀️" and currentEntry > 1:
                currentEntry -= 1

                gameId = data[currentEntry - 1]["id"]
                
                #fetch the game details
                embedVar = getGameDetails(gameId)
                await message.edit(embed=embedVar)
                await message.remove_reaction(reaction, user)
            else:
                await message.remove_reaction(reaction, user)
        except asyncio.TimeoutError:
            await message.delete()
            break
        
bot.run(TOKEN)
