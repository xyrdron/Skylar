import io
import os
import random
import uuid
import logging

import aiohttp
import discord
from discord import File, app_commands
from discord.ext import commands
from PIL import Image

import utilities.embeds as embeds

class bottest(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self._last_member = None

  @commands.hybrid_command(name="ship", description="Ship 2 people")
  @app_commands.allowed_installs(guilds=True,users=True)
  @app_commands.allowed_contexts(guilds=True,dms=True,private_channels=True)
  @app_commands.describe(user1="The first person you want to ship")
  @app_commands.describe(user2="The second person you want to ship")
  async def ship(self, ctx, user1: discord.User, user2: discord.User):
    await ctx.defer() 
    try:
      async with aiohttp.ClientSession() as session:
          async with session.get(str(user1.avatar.url)) as response1: # type: ignore
              user1_avatar = Image.open(io.BytesIO(await response1.read()))
          async with session.get(str(user2.avatar.url)) as response2: # type: ignore
              user2_avatar = Image.open(io.BytesIO(await response2.read()))

      # we make a image
      user1_avatar = user1_avatar.resize((128, 128))
      user2_avatar = user2_avatar.resize((128, 128))

      combined_image = Image.new('RGB', (256, 128), (255, 255, 255))
      combined_image.paste(user1_avatar, (0, 0))
      combined_image.paste(user2_avatar, (128, 0))

      unique_filename = f"temp/{uuid.uuid4()}.png"
      combined_image.save(unique_filename)

      file = File(fp=unique_filename, filename='ship.png')

      # the bit where we ship them
      percent = round(random.uniform(0, 100), 2)

      # the epic caption (we do this later)
      msg = 'hehe~'

      # embed ahh bit
      embed = embeds.embedCreate(f'{percent}%', msg, discord.Color.pink())
      embed.set_image(url='attachment://ship.png') # type: ignore

      await ctx.send(content=f'miku ships you! :0\n{user1.mention}{user2.mention}', embed=embed, file=file)
      os.remove(unique_filename)
    except Exception as e:
      logging.error(f"An error occurred: {e}")
      await ctx.send(f"An error occurred, If the problem persists report the bug on our [server](https://discord.gg/VU5GkWQmGp) or [github](https://github.com/xyrdron/MikuBOT/issues)")

def setup(client):
  return client.add_cog(bottest(client))