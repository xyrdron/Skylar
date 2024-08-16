# THIS IS AN EXAMPLE COG FILE
# Please dont edit this file but instead create a new file in the cogs folder and copy the code below into it
from discord.ext import commands

class example(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self._last_member = None

    # this is what a regular slash command would look like in a cog
  @commands.hybrid_command(name="test1", description="test command!")
  async def test(self,ctx):
    await ctx.defer() # this defers the command execution and will display "bot is thinking" to the user
    await ctx.send("pong")

def setup(client):
  return client.add_cog(example(client))