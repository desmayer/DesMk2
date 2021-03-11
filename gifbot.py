#gifbot.py
import random

#sends a reaction gif of God of War
async def GetGoWGif(ctx):
    with open('resources/gow.txt') as f:
        sony_gif = f.read().splitlines()

    response = random.choice(sony_gif)
    await ctx.send(response)

#sends a reaction gif of The Last of Us 2
async def GetLou2Gif(ctx):
    with open('resources/lou2.txt') as f:
        sony_gif = f.read().splitlines()

    response = random.choice(sony_gif)
    await ctx.send(response)

#sends a reaction gif of B99
async def GetB99Gif(ctx):
    with open('resources/99.txt') as f:
        gif = f.read().splitlines()

    response = random.choice(gif)
    await ctx.send(response)
