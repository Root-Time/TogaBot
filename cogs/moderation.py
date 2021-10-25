import discord
from discord.embeds import EmptyEmbed
from discord.ext import commands
from discord_components import *
from Togamodule import *
from datetime import date, datetime, timedelta


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client 

    def save(self):
        with open('Data/Mute.yaml', 'w') as f:
            yaml.dump(self.mute, f)
        with open('Data/Warn1.yaml', 'w') as f:
            yaml.dump(self.warn, f)

    async def Warn_Logs(self):
        logs = self.client.guilds[0].get_channel(892037267122716702)
        mess_id = config.get('Warn_Message_ID')
        Liste = []
        for player,warn_stufe in warn.items():
            Liste.append(f'<@{player}> (Stufe {warn_stufe})')
            
        message = '\n'.join(Liste)

        try: 
            mess = await logs.fetch_message(mess_id)
            await mess.edit(embed = embed('Verwahnte:', message))
        except: 
            mess = await logs.send(embed = embed('Verwahnte:', message))
            config['Warn_Message_ID'] = mess.id
            with open('Data/config.yaml', 'w') as f:
                yaml.dump(config, f)
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.Warn_Logs()
        with open('Data/Mute.yaml', 'r') as f:
            self.mute = yaml.load(f)
        with open('Data/Warn.yaml', 'r') as f:
            self.warn = yaml.load(f)
        
        self.roles = [786318061798948924, 863329187455696947, 825832643102244865, 786551975961559060, 849958208574980137, 786489810670845993, 882224186435698738]
        print('>>> Moderation')
    
    @commands.command()
    async def kick(self, ctx, player : discord.Member = None, grund = 'Keine Grund angegeben'):
        owner : discord.Member = ctx.author
        logs = ctx.guild.get_channel(logs_id)
        j = 'jemanden'
        await ctx.message.delete()
        if not ctx.author.guild_permissions.kick_members:
            await send(ctx.channel, embed = mod(ctx.author, f'Du hast keine Rechte um {player or j} vom Server zu kicken!'))
            await send(logs, embed = log(f'{ctx.author} hat versucht {player or j} zu kicken!', 1, owner))
            return 
        if not player:
            return await send(ctx.channel, embed = mod(ctx.author, 'Du kannst nicht niemanden kicken!'))
        if ctx.author == player:
            return await send(ctx.channel, embed = mod(ctx.author, 'Warum? Du kannst dich nicht selber kicken!?'))
        try:
            await player.kick(reason = grund + f' (von {owner})')
        except:
            await send(ctx.channel, embed = mod(ctx.author, f'Nicht geschafft {player} zu kicken!'))


    @commands.command()
    async def ban(self, ctx, player : discord.Member = None, grund = 'Kein Grund angegeben'):
        owner : discord.Member = ctx.author
        logs = ctx.guild.get_channel(logs_id)
        j = 'jemanden'
        await ctx.message.delete()
        if not ctx.author.guild_permissions.kick_members:
            await send(ctx.channel, embed = mod(ctx.author, f'Du hast keine Rechte um {player or j} vom Server zu bannen!'))
            await send(logs, embed = log(f'{ctx.author} hat versucht {player or j} zu bannen!', 1, owner))
            return 
        if not player:
            return await send(ctx.channel, embed = mod(ctx.author, 'Du kannst nicht niemanden bannen!'))
        if ctx.author == player:
            return await send(ctx.channel, embed = mod(ctx.author, 'Warum? Du kannst dich nicht selber bannen!?'))
        try:
            if not await ask(ctx.channel, f'Bist du dir Sicher das du {player.mention} bannen willst?', owner, client):
                return
            await player.ban(reason = grund + f' (von {owner})')
            await send(logs, embed = log(f'{player} wurde von {ctx.author} gebannt!', player = ctx.author))
        except:
            await send(ctx.channel, embed = mod(ctx.author, f'Nicht geschafft {player} zu bannen!'))
        
    @commands.command()
    async def mute(self, ctx, player : discord.Member = None, time = 24, grund = 'Kein Grund angegeben'):
        guild = ctx.guild
        owner = ctx.author
        channel = ctx.channel
        mute = ctx.guild.get_role(874814934440083486)
        j = 'jemanden'
        logs = ctx.guild.get_channel(logs_id)
        
        await ctx.message.delete()
        
        for role in self.roles:
            role = guild.get_role(role)
            if role not in ctx.author.roles:
                await send(ctx.channel, embed = mod(ctx.author, f'Du hast keine Rechte um {player or j} im Server zu muten!'))
                await send(logs, embed = log(f'{ctx.author} hat versucht {player or j} zu muten!', 1, owner))
                return 
        if not player:
            return await send(ctx.channel, embed = mod(ctx.author, 'Du kannst nicht niemanden muten!'))

        new_time = datetime.now() + timedelta(hours = time)
        if player.id in self.mute.keys():
            old_time = self.mute.get(player.id)
            
            if not await ask(channel, f'{player} ist schon bis {old_time} gemutet\nWillst ihn denoch um weiter {(new_time - old_time).total_seconds() / 3600} Stunden muten?', owner, client):
                return
            
            self.mute[player.id] = new_time
            # TODO add Mute ROll
            await player.add_roles(mute)
            self.save()
            
            await send(channel, embed = mod(owner, f'Du hast erfolreich {player} um weitere {(new_time - old_time).total_seconds() / 3600} gemutet!'))
            await send(logs, embed = log(f'{owner} hat {player} bis um {new_time} gemutet!', player = owner))
            return    
        
        if not await ask(channel, f'Bist du dir Sicher das du {player.name} bis {new_time} muten?', owner, client):
            return
        
        mute[player.id] = new_time
        await player.add_roles(mute)
        self.save()

        await send(channel, embed = mod(owner, f'Du hast erfolreich {player} bis {new_time} gemutet!'))
        await send(logs, embed = log(f'{owner} hat {player} bis um {new_time} gemutet!', player = owner))
        return  

    @commands.command()
    async def warn(self, ctx, player : discord.Member = None):
        guild = ctx.guild
        owner = ctx.author
        channel = ctx.channel
        mute = guild.get_role(874814934440083486)
        
        j = 'jemanden'
        logs = ctx.guild.get_channel(logs_id)
        
        await ctx.message.delete()
        
        
        for role in self.roles:
            role = guild.get_role(role)
            if role in ctx.author.roles:
                break
        else:
            await send(ctx.channel, embed = mod(ctx.author, f'Du hast keine Rechte um {player or j} im Server zu verwahnen!'))
            await send(logs, embed = log(f'{ctx.author} hat versucht {player or j} zu verwahnen!', 1, owner))
            return
        
        if not player:
            return await send(ctx.channel, embed = mod(ctx.author, 'Du kannst nicht niemanden verwahnen!'))
        
        warn_level = warn.get(player.id, 0) + 1
        with open('Data/Warn.yaml', 'w') as f:
            warn[player.id] = warn_level
            yaml.dump(warn, f)
        
        await send(channel, embed = mod(owner, f'{player} wurde erfolgreich verwahnt!\nDies ist nun seine {warn_level}.Verwahnung!'))
        
        if warn_level == 5:
            await send(channel, embed = mod(owner, f'{player} wird nun gebannt da es sein 5 Wahnung ist!!!'))
            await player.ban(reason = '5 Verwahnung!!!')
            await self.Warn_Logs()
            return
        if warn_level == 3:
            new_time = datetime.now() + timedelta(hours = 24)
            mute[player.id] = new_time
            await player.add_roles(mute)


            await send(logs, embed = log(f'{player} wurde bis {new_time} gemutet!\nWegen 3.Verwahnung!', player = owner))
            await self.Warn_Logs()
            return
        if warn_level == 3:
            new_time = datetime.now() + timedelta(hours = 48)
            mute[player.id] = new_time
            await player.add_roles(mute)

            await self.Warn_Logs()
            await send(logs, embed = log(f'{player} wurde bis {new_time} gemutet!\nWegen 4.Verwahnung!', player = owner))
            return
        
def setup(client):
    client.add_cog(Moderation(client))
