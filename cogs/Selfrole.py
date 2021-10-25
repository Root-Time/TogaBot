import discord
from discord import file
from discord import reaction
from discord import message
from Togamodule import *
from discord.ext import commands
from discord_components import *
import yaml

class Selfrole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.Cog.listener()
    async def on_ready(self):
        with open('Data/selfroles.yaml', 'r') as f:
            self.selfroles = yaml.load(f, Loader = yaml.FullLoader) or {}
        self.reaction = self.selfroles.get('reactions', {})
        self.selfroles['reactions'] = self.reaction
        print('>>> Self Role')
    
   
    @commands.Cog.listener()
    async def on_button_click(self, event):
        id = event.component.label
        mess = event.message
        guild = event.guild
        author = event.author
        
        Only = mess.id in self.selfroles.keys()
        
        if id not in self.reaction.keys(): return
        
        role_id = self.reaction[id]
        role = guild.get_role(int(role_id))
        
        if not role: 
            return await event.respond(content = 'Diese Rolle funktioniert nicht! Bitte melde das!')
        
        await event.respond(type = 6)
        
        if role in author.roles:
            await author.remove_roles(role)
            return 
        
        if Only:
            for role_name in self.selfroles[mess.id]:
                del_role_id = self.reaction[role_name]
                del_role = guild.get_role(int(del_role_id))
                if del_role in author.roles:
                    await author.remove_roles(del_role)
        await author.add_roles(role)
            
        
        

def setup(bot):
    bot.add_cog(Selfrole(bot))
