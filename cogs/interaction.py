import discord
from discord.ext import commands


class Interaction(commands.Cog):
    def __init__(self, client):
        self.client = client 

    @commands.command()
    async def hug(self, ctx, player : discord.Member = None):
        #with open()
        #await ctx.send(embed = )
        pass

def setup(client):
    client.add_cog(Interaction(client))
