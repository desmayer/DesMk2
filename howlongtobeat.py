
import discord

def getGameDetails(game, currentEntry, gameCount):
    embedVar = discord.Embed(title=game.game_name, color=0x00ff00)
    #Set thumbnail
    picURL = "https://howlongtobeat.com"+game.game_image_url
    embedVar.set_thumbnail(url=picURL)

    #Some fields
    try:
        units = game.gameplay_main_unit
        if units == None:
            unitFormat = ""
        else:
            unitFormat = str(units)
    except:
        print("Error with main units")
    embedVar.add_field(name="Gameplay Main", value=str(game.gameplay_main) + " " + unitFormat, inline=False)

    try:
        units = game.gameplay_main_extra_unit
        if units == None:
            unitFormat = ""
        else:
            unitFormat = str(units)
        print(units)
    except:
        print("Error with extra units")
    embedVar.add_field(name="Gameplay Main + Extra", value=str(game.gameplay_main_extra) + " " + unitFormat, inline=False)

    try:
        units = game.gameplay_completionist_unit 
        if units == None:
            unitFormat = ""
        else:
            unitFormat = str(units)
        print(units)
    except:
        print("Error with extra units")
    embedVar.add_field(name="Completionist", value=str(game.gameplay_completionist) + " " + unitFormat, inline=False)
    embedVar.add_field(name="More Details", value="[HLTB](" + game.game_web_link + ")", inline=False)
    
    #Set footer
    embedVar.set_footer(text="Game " + str(currentEntry) + " of " + str(gameCount))
    return embedVar;
