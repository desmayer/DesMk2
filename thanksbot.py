from replit import db
import discord

async def ThankUser(ctx, user: discord.Member = None, channel: discord.TextChannel = None):
  print(user.id)
  value = None
  userThanking = "<@"+str(ctx.author.id)+">"
  userToThank = "<@"+str(user.id)+">"
  try:
    value = db[user.id]
  except:
    print("no value found atm")
    
  if value is None:
    db[user.id] = 1
  else:
    db[user.id] = int(value) + 1

  description = userThanking + " has thanked you " + userToThank + "!\n\n You have been thanked " + str(db[user.id]) + " times!"
  embedVar = discord.Embed(title="Thank You!", description=description, color=0x00ff00)
  embedVar.set_image(url="https://media.giphy.com/media/KBDzqHidthiHbeus6B/giphy.gif")

  await channel.send(content=description, embed=embedVar)

async def ThankCount(ctx, user: discord.Member = None):
  userToShow = "<@"+str(user.id)+">"
  value = None
  try:
    value = db[user.id]
  except:
    print("no value found atm")
  print(value)
  valueString = "0"
  if value:
    valueString = str(value)

  await ctx.send(userToShow + " has been thanked " + valueString + " times!")

async def ThankChart(ctx):
  keys = db.keys()