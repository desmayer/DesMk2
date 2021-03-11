import requests
import discord
import asyncio
from bs4 import BeautifulSoup

async def FetchPSNProfile(ctx, profile):
    URL = 'https://psnprofiles.com/' + profile
    page = requests.get(URL)
    print(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='user-bar')
    #avatar
    try:
        avatar = results.find('div', class_='avatar').find('img')['src']
    except:
        await ctx.send("Profile " + profile + " not found on PSNProfiles \nPlease goto https://psnprofiles.com/ to update your profile")

    #level
    level = results.find('li', class_='icon-sprite level').text 
    
    #trophies
    total = results.find('li', class_='total').text.strip()
    plats = results.find('li', class_='platinum').text.strip()    
    gold = results.find('li', class_='gold').text.strip()
    silver = results.find('li', class_='silver').text.strip()
    bronze = results.find('li', class_='bronze').text.strip()

    #last trophy?
    lastTrophies = soup.find(id='recent-trophies')
    
    lastTrophyName = lastTrophies.find(attrs={"data-id": True}).find('a',class_='title').text.strip()
    lastTrophyGame = lastTrophies.find(attrs={"data-id": True}).find('span',class_='small_info_green').text.strip()
    lastTrophyLevel = lastTrophies.find(attrs={"data-id": True}).find('span',class_='separator left').find('img')['title']
    print(lastTrophyLevel)
    
    embedVar = discord.Embed(title=profile + "'s Trophy Details",url=URL, color=0x00ff00)
    embedVar.set_thumbnail(url=avatar)
    embedVar.set_image(url="https://card.psnprofiles.com/1/"+ profile +".png")
    embedVar.add_field(name="Level", value=level, inline=False)
    embedVar.add_field(name="Total", value=total, inline=True)
    embedVar.add_field(name="Platinum", value=plats, inline=False)
    embedVar.add_field(name="Gold", value=gold, inline=True)
    embedVar.add_field(name="Silver", value=silver, inline=True)
    embedVar.add_field(name="Bronze", value=bronze, inline=True)
    embedVar.add_field(name="Last Trophy", value=lastTrophyName +' (' + lastTrophyLevel + ')' + ' ' + lastTrophyGame, inline=True)    
    print('https://card.psnprofiles.com/2/' + profile + '.png')
    #footer
    embedVar.set_footer(text="Information requested by: {}".format(ctx.author.display_name))
    await ctx.send(embed=embedVar)

async def FetchNextTrophy(ctx, bot, profile, trophy_type, platform):
    trophy_type_format = "all"
    if trophy_type.lower() == "b":
        trophy_type_format = "bronze"
    elif trophy_type.lower() == "s":
        trophy_type_format = "silver"
    elif trophy_type.lower() == "g":
        trophy_type_format = "gold"
    elif trophy_type.lower() == "p":
        trophy_type_format = "platinum"
    
    URL = 'https://psnprofiles.com/' + profile + '/log?earned=unearned&platform=' + platform.lower() + '&type=' + trophy_type_format.lower()
    page = requests.get(URL)
    print(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='user-bar')
    
    #avatar
    try:
        avatar = results.find('div', class_='avatar').find('img')['src']
    except:
        await ctx.send("Profile " + profile + " not found on PSNProfiles \nPlease goto https://psnprofiles.com/ to update your profile")

    trophyTable = soup.find('table', class_='zebra')
    data = trophyTable.find_all('tr')

    #total number of games found
    trophiesFound = len(data)
    gameCount = trophiesFound if trophiesFound < 11 else 10
    print(gameCount)
    #current entry
    currentEntry = 1
    
    embedVar = await BuildTrophyDetails(ctx, data[0], profile,currentEntry, gameCount)
    message = await ctx.send(embed=embedVar)
    await message.add_reaction("◀️")
    await message.add_reaction("▶️")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]
        # This makes sure nobody except the command sender can interact with the "menu"

    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", timeout=180, check=check)
            # waiting for a reaction to be added - times out after x seconds, 60 in this
            # example

            if str(reaction.emoji) == "▶️" and currentEntry != gameCount:
                currentEntry += 1

                #fetch the game details
                embedVar = await BuildTrophyDetails(ctx, data[currentEntry - 1], profile,currentEntry, gameCount)
                await message.edit(embed=embedVar)
                await message.remove_reaction(reaction, user)
            elif str(reaction.emoji) == "◀️" and currentEntry > 1:
                currentEntry -= 1
                #fetch the game details
                embedVar = await BuildTrophyDetails(ctx, data[currentEntry - 1], profile,currentEntry, gameCount)
                await message.edit(embed=embedVar)
                await message.remove_reaction(reaction, user)
            else:
                await message.remove_reaction(reaction, user)
        except asyncio.TimeoutError:
            break

async def BuildTrophyDetails(ctx, trophyDetails, profile, currentEntry, gameCount):
    trophyImage = trophyDetails.find('img', class_='trophy')['src']
    gameImage = trophyDetails.find('img', class_='game')['src']
    trophyURL = trophyDetails.find('a', class_='title')['href']

    #basic details
    gameName = trophyDetails.find('img', class_='game')['title']
    trophyName = trophyDetails.find('a', class_='title').text.strip()
    trophyType = trophyDetails.find_all('span', class_='separator left')[2].find('img')['title']
    trophyTypeImg = trophyDetails.find_all('span', class_='separator left')[2].find('img')['src']

    #ratity details
    trophyRarity= trophyDetails.find_all('span', class_='separator left')[1].find('nobr').text.strip()
    trophyRarityPercentage = trophyDetails.find_all('span', class_='separator left')[1].find('span', class_='typo-top').text.strip()

    color = 0xc06437
    if trophyType.lower() == "silver":
        color = 0xc5c5c5
    elif trophyType.lower() == "gold":
        color = 0xe2aa52
    elif trophyType.lower() == "platinum":
        color = 0xb5c5e4
    
    #print(trophyDetails.prettify())
    embedVar = discord.Embed(title=profile + "'s Next Trophy",url='https://psnprofiles.com'+trophyURL, color=color)
    embedVar.set_thumbnail(url='https://psnprofiles.com'+trophyTypeImg)
    embedVar.set_image(url=trophyImage)
    embedVar.add_field(name="Game", value=gameName, inline=False)
    embedVar.add_field(name="Trophy", value=trophyName, inline=False)
    embedVar.add_field(name="Type", value=trophyType, inline=True)
    embedVar.add_field(name="Rarity", value=trophyRarity + ' ('+trophyRarityPercentage+')', inline=True)

    #footer
    embedVar.set_footer(text="Trophy " + str(currentEntry) + " of " + str(gameCount) +"\nInformation requested by: {}".format(ctx.author.display_name))

    return embedVar;

async def TrophyList(ctx, bot, game):
    URL = 'https://psnprofiles.com/search/games?q=' + game
    page = requests.get(URL)
    print(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    trophyTable = soup.find('table', class_='box zebra')
    data = trophyTable.find_all('tr')

    #total number of games found
    trophiesFound = len(data)
    gameCount = trophiesFound if trophiesFound < 21 else 20
    print(gameCount)
    #current entry
    currentEntry = 1

    embedVar = await BuildTrophyListDetails(ctx, data[0],currentEntry, gameCount)
    message = await ctx.send(embed=embedVar)
    await message.add_reaction("◀️")
    await message.add_reaction("▶️")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]
        # This makes sure nobody except the command sender can interact with the "menu"

    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", timeout=180, check=check)
            # waiting for a reaction to be added - times out after x seconds, 60 in this
            # example

            if str(reaction.emoji) == "▶️" and currentEntry != gameCount:
                currentEntry += 1

                #fetch the game details
                embedVar = await BuildTrophyListDetails(ctx, data[currentEntry - 1],currentEntry, gameCount)
                await message.edit(embed=embedVar)
                await message.remove_reaction(reaction, user)
            elif str(reaction.emoji) == "◀️" and currentEntry > 1:
                currentEntry -= 1
                #fetch the game details
                embedVar = await BuildTrophyListDetails(ctx, data[currentEntry - 1],currentEntry, gameCount)
                await message.edit(embed=embedVar)
                await message.remove_reaction(reaction, user)
            else:
                await message.remove_reaction(reaction, user)
        except asyncio.TimeoutError:
            break

async def BuildTrophyListDetails(ctx, trophyDetails, currentEntry, gameCount):
    gameImage = trophyDetails.find('img', class_='game')['src']

    #basic details
    gameName = trophyDetails.find('a', class_='title').text.strip()
    gameURL = trophyDetails.find('a', class_='title')['href']
    trophyCount = trophyDetails.find('div', class_='trophy-count').find('span').text.strip()
    platform = trophyDetails.find('div', class_='platforms').find('span').text.strip()
    
    try:
        plats = trophyDetails.find('li', class_='icon-sprite platinum').text.strip()
    except:
        plats = "0"
        
    gold = trophyDetails.find('li', class_='icon-sprite gold').text.strip()
    silver = trophyDetails.find('li', class_='icon-sprite silver').text.strip()
    bronze = trophyDetails.find('li', class_='icon-sprite bronze').text.strip()
    
    color = 0xc06437
    
    #print(trophyDetails.prettify())
    embedVar = discord.Embed(title=gameName + " Trophy List",url='https://psnprofiles.com'+gameURL, color=color)
    embedVar.set_thumbnail(url=gameImage)
    embedVar.add_field(name="Trophies", value=trophyCount, inline=False)
    embedVar.add_field(name="Platform", value=platform, inline=True)
    embedVar.add_field(name="Platinum", value=plats, inline=False)
    embedVar.add_field(name="Gold", value=gold, inline=True)
    embedVar.add_field(name="Silver", value=silver, inline=True)
    embedVar.add_field(name="Bronze", value=bronze, inline=True)
    embedVar.add_field(name="Guide(s)", value='https://psnprofiles.com'+gameURL.replace('trophies','guides'), inline=True)
    #embedVar.add_field(name="Type", value=trophyType, inline=True)
    #embedVar.add_field(name="Rarity", value=trophyRarity + ' ('+trophyRarityPercentage+')', inline=True)

    #footer
    embedVar.set_footer(text="Trophy " + str(currentEntry) + " of " + str(gameCount) +"\nInformation requested by: {}".format(ctx.author.display_name))

    return embedVar;
