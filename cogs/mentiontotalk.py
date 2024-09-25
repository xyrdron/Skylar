import json
import time
import logging
import os

import discord
from discord import app_commands
from discord.ext import commands, tasks

import openai
from openai import OpenAI
from uwuipy import uwuipy
uwu = uwuipy.Uwuipy(None, 0.057, 0.01, 0.01, 0.1, False) # uwufier settings

class mentiontotalk(commands.Cog):

  def __init__(self, bot): # Setup Function
    self.bot = bot
    self._last_member = None
    openai.api_key = os.getenv("OPENAI_API_KEY")
    self.client = OpenAI()
    self.convo = {} # Conversation History
    self.convotime = {} # Time since last convo message
    self.convocount = {} # Amount of msgs in a convo
    with open('json/ai.json', 'r') as file:
      data = json.load(file)
    self.SysMsg = data['SysMsg']
    self.cleardeadchat.start()

  def appendMsg(self, msg, type, id): 
    if id not in self.convo:
      self.convo[id] = []
    if self.convo[id] == [] or self.convocount[id] > 6:
      self.convocount[id] = 0
      self.convo[id].append({"role": "system", "content": self.SysMsg})
    if id not in self.convotime:
      self.convotime[id] = time.time()
    self.convo[id].append({"role": type, "content": msg})
    self.convotime[id] = time.time()
    for key in self.convo:
      self.convo[key] = self.convo[key][-7:]
    self.convocount[id] += 1
    return self.convo[id]

  def mentiontotalk(self, msg, user, id):
    msg = msg.replace('<@1120326968609607690>', '')  # Main Bot
    msg = msg.replace('<@1208732989803204618>', '')  # DevTest Bot
    msg = 'user:' + str(user) + ' msg:' + msg

    convo = self.appendMsg(msg, 'user', id)

    # we will make a premium tier when we get monetized
    model = "gpt-4o"

    try:
        response = self.client.chat.completions.create(
        model=model,
        messages=convo,
        temperature=1.13,
        max_tokens=1096,
        top_p=0.56,
        frequency_penalty=0.2,
        presence_penalty=0.42)

        # we are not using uwuipy anymore but its here incase yes happens
        assistantmsg = uwu.uwuify(response.choices[0].message.content)
        #assistantmsg = response.choices[0].message.content
    except Exception as e:
        logging.error(f"AI Complication Failed: {e}")
        assistantmsg = 'It seems like im having some trouble compiling a response, please try again later and contact the devs if this persists.'

    self.appendMsg(assistantmsg, 'assistant', id)
    return assistantmsg

  # WHEN U PING THE BOT
  @commands.Cog.listener()
  async def on_message(self, message):
    # very important
    if message.author == self.bot.user:
      return
    if message.mention_everyone:
      return

    if isinstance(message.channel,discord.DMChannel) or self.bot.user.mentioned_in(message):
      async with message.channel.typing():
        await message.reply(
            self.mentiontotalk(message.content, message.author,str(message.author.id)))

  
  @tasks.loop(minutes=1)
  async def cleardeadchat(self):
    current_time = time.time()
    removekeys = []
    for id, stored_time in self.convotime.items():
      if current_time - stored_time > 180:
        removekeys.append(id)
    for id in removekeys:
      del self.convotime[id]
      del self.convocount[id]
      del self.convo[id]

  @commands.hybrid_command(name="talk", description="Talk to Trixie using slash commands")
  @app_commands.allowed_installs(guilds=True,users=True)
  @app_commands.allowed_contexts(guilds=True,dms=True,private_channels=True)
  @app_commands.describe(message="The message you want to send to Trixie")
  async def talk(self,ctx,message: str):
    await ctx.defer() 
    await ctx.send(self.mentiontotalk(message, ctx.author,str(ctx.author.id)))

def setup(client):
  return client.add_cog(mentiontotalk(client))
