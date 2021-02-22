#critic.py
import os
import random
import json
from discord.ext import commands
from dotenv import load_dotenv
from urllib.request import Request, urlopen
import discord
import asyncio


def getGameDetails(gameId, currentEntry, gameCount):
    #let's get some game data!!
    gameRequestString = 'https://api.opencritic.com/api/game/{}'.format(gameId)
    gameReq = Request(gameRequestString, headers={'User-Agent': 'Mozilla/5.0'})    
    gamewebpage = urlopen(gameReq).read()
    gamedata = json.loads(gamewebpage.decode())
    gameDescription = gamedata["description"]
    gameURL = "https://opencritic.com/game/" + str(gameId) + "/" + gamedata["name"].replace(" ","%20")

    print(gameURL)
    
    #set a tier & colour
    try:
        tier = gamedata["tier"]
        print(tier)
        if tier == "Mighty":
            tierUrl="https://opencritic.com/assets/tiers/mighty-man.png"
            embedColour = 0xfd440a
        elif tier == "Strong":
            tierUrl="https://opencritic.com/assets/tiers/strong-man.png"
            embedColour = 0xaa36ba
        elif tier == "Fair":
            tierUrl="https://opencritic.com/assets/tiers/fair-man.png"
            embedColour = 0x4aa1ce
        elif tier == "Weak":
            tierUrl="https://opencritic.com/assets/tiers/weak-man.png"
            embedColour = 0x81b16b
        else:
            tierUrl=""
            embedColour = 0x00ff00
    except:
        print("Error finding a tier")
    
    embedVar = discord.Embed(title=gamedata["name"], description=gameDescription[:150] + "..." + "[more](" + gameURL + ")", color=embedColour)        
    #try set a thumbnail
    try:
        gameThumbnail = gamedata["mastheadScreenshot"]["thumbnail"]
        embedVar.set_thumbnail(url="https://"+gameThumbnail[2:])
    except:
        print("No image found")
        
    #Set Dev/Pub
    try:
        for element in gamedata["Companies"]:
            if element["type"] == "DEVELOPER":
                embedVar.add_field(name="Developer",value=element["name"])
            elif element["type"] == "PUBLISHER":
                embedVar.add_field(name="Publisher",value=element["name"])
    except:
        print("Error finding pub/dev")

    #set top critic average
    try:
        embedVar.add_field(name="Top Critic Average",value=round(gamedata["topCriticScore"]))
    except:
        print("Error finding critic details")
    
    #set critic recommend %
    try:
        recommend = str(round(gamedata["percentRecommended"])) + "%"
        embedVar.add_field(name="Critics Recommend",value=recommend)
    except:
        print("Error finding critic % recommend")
    
    #set tier image
    if len(tierUrl) > 0:
        embedVar.set_image(url=tierUrl)
            
    embedVar.set_footer(text="Game " + str(currentEntry) + " of " + str(gameCount))
    return embedVar

