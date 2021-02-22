import os
import discord
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from pyyoutube import Api
from random import randrange
from dotenv import load_dotenv

load_dotenv()
API = os.getenv('GOOGLE_API')
def GetFridayFeature(ctx):
    api = Api(api_key=API)
    playlist_item_by_playlist = api.get_playlist_items(playlist_id="PLLUkxbIkknLuK6BLdOs-QDAJiDQTM7Xei", count=None)

    totalVideos = len(playlist_item_by_playlist.items)
    number = randrange(totalVideos)
    print(number)
    print(playlist_item_by_playlist.items[number].snippet.title)
    video = playlist_item_by_playlist.items[number]
    embedVar = discord.Embed(title=video.snippet.title, url="https://www.youtube.com/watch?v="+video.contentDetails.videoId, color=0x0ed0f1)
    embedVar.add_field(name="Published", value=video.contentDetails.videoPublishedAt)
    embedVar.set_image(url=video.snippet.thumbnails.standard.url)

    return embedVar
    
