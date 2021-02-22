#desmk2.py
import os
import random
import json
from discord.ext import commands
from dotenv import load_dotenv
from urllib.request import Request, urlopen
import discord
import asyncio
import opencritic
import howlongtobeat
from howlongtobeatpy import HowLongToBeat
from keep_alive import keep_alive

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')
discord.Client.setUserName = "Astro"

@bot.event
async def on_message(message):
  #bot command channel
    if message.content != "!hltb" or message.content != "!critic":
      await bot.process_commands(message)
    else:
      if message.channel.id == 813426964886847538:
        #this is astro
          if message.author.id == 813312198151503924:
              return
          
          validMessage = message.content.startswith("!")
          if validMessage == False:
              await message.delete()
          else:
              await bot.process_commands(message)
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

@bot.command(name='dance')
async def dance(ctx):
    dance_gifs = [
        'https://media1.giphy.com/media/QzdJer4CUPGheUFa1n/giphy.gif',
        'https://media2.giphy.com/media/D34Wn98AYstonHXdU0/giphy.gif',
        'https://media3.giphy.com/media/JomvkWHpkhZ1XHLuOT/giphy.gif'
    ]
    response = random.choice(dance_gifs)
    await ctx.send(response)

@bot.command(name='pet')
async def pet(ctx):
  response = 'https://cdn.discordapp.com/attachments/724233887659720805/812110115947282472/saoirse-pat.gif'
  await ctx.send(response)

@bot.command(name='amazing', help='Shows how amazing something is')
async def amazing(ctx):
    response = 'https://cdn.discordapp.com/attachments/742349549292617839/795230531528818698/Schermata_2021-01-03_alle_11.00.48.png'
    await ctx.send(response)
@bot.command(name="hltb", help='Shows how long a game will take for you to beat!')
async def hltb(ctx ,*,game):
    print(ctx.channel)
    if ctx.channel.id != 813426964886847538:
        print("ERROR")
        await ctx.send("Sorry " + ctx.author.name + ", that is not allowed here!")
        return
    #fetch the game
    print(game)
    data = await HowLongToBeat().async_search(game)

    #total number of games found
    gameCount = len(data)

    #current entry
    currentEntry = 1

    #check if there are any results
    if len(data) == 0:
        response = 'No Games found for search criteria {}'.format(game)
        await ctx.send(response)

    
    embedVar = howlongtobeat.getGameDetails(data[currentEntry-1], currentEntry, gameCount)    
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
                gameId = data[currentEntry - 1]
                #fetch the game details
                embedVar = howlongtobeat.getGameDetails(gameId, currentEntry, gameCount)
                
                await message.edit(embed=embedVar)
                await message.remove_reaction(reaction, user)
            elif str(reaction.emoji) == "◀️" and currentEntry > 1:
                currentEntry -= 1
                gameId = data[currentEntry - 1]
                #fetch the game details
                embedVar = howlongtobeat.getGameDetails(gameId, currentEntry, gameCount)
                await message.edit(embed=embedVar)
                await message.remove_reaction(reaction, user)
            else:
                await message.remove_reaction(reaction, user)
        except asyncio.TimeoutError:
            break
    
@bot.command(name='critic', help='Shows critic score for a searched game')
async def critic(ctx,*, game):
    print(ctx.channel)
    if ctx.channel.id != 813426964886847538:
        print("ERROR")
        await ctx.send("Sorry " + ctx.author.name + ", that is not allowed here!")
        return
    print(game)
    #fetch the game id
    print(game.replace(" ","%20"))
    idRequestString = 'https://api.opencritic.com/api/game/search?criteria={}'.format(game.replace(" ","%20"))
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
    embedVar = opencritic.getGameDetails(data[currentEntry - 1]["id"], currentEntry, gameCount)
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
                gameName = data[currentEntry - 1]["name"]
                print(gameId)
                #fetch the game details
                embedVar = opencritic.getGameDetails(gameId, currentEntry, gameCount)
                
                await message.edit(embed=embedVar)
                await message.remove_reaction(reaction, user)
            elif str(reaction.emoji) == "◀️" and currentEntry > 1:
                currentEntry -= 1

                gameId = data[currentEntry - 1]["id"]
                gameName = data[currentEntry - 1]["name"]
                
                #fetch the game details
                embedVar = opencritic.getGameDetails(gameId, currentEntry, gameCount)
                await message.edit(embed=embedVar)
                await message.remove_reaction(reaction, user)
            else:
                await message.remove_reaction(reaction, user)
        except asyncio.TimeoutError:
            break
keep_alive()   
bot.run(TOKEN)
