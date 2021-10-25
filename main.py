from Togamodule import *
import discord
from discord.ext import commands


intents=intents=discord.Intents.all()
bot = commands.Bot(command_prefix="t.", intents = intents, description='Bot von Toga\'s Anstalt')

@bot.event
async def on_ready():
    DiscordComponents(bot)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Toga Chan"))
    print('Toga is ready!!')
    

#bot.load_extension("cogs.moderation")
bot.load_extension("cogs.LevelSystem")
#bot.load_extension("cogs.Selfrole")
#bot.load_extension("cogs.Welcome")

    
#bot.run('NzM2NjMxNDgwMjc2NjE1MTc0.Xxxnhg.MaPa-QCK0hmS4nIJtqjfZpvDMAg')
bot.run("ODkxNzcwNTg2MjMyMTMxNjA0.YVDMFA.J7Xg8Nu0XjA2AZX3ScWgTt4PlYg")
