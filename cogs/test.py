from discord.ext import commands

class bottest(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self._last_member = None

  @commands.hybrid_command(name="test1", description="test command")
  async def test1(self,ctx):
    await ctx.send("pong")

def setup(client):
  return client.add_cog(bottest(client))