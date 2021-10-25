from datetime import datetime
import discord
from discord import user
from discord import colour
from discord.errors import DiscordException
from discord.ext import commands
from Togamodule import *
import yaml, json, io
from PIL import Image, ImageFilter, ImageFont, ImageDraw
import requests
import pyimgur


class LevelSystem(commands.Cog):
    def __init__(self, client):
        self.client = client 
        with open('level.yaml') as f:
            #self.level = yaml.load(f, Loader=yaml.FullLoader) or {}
            self.level = yaml.load(f, Loader=yaml.FullLoader)
        with open('users.json') as f:
            self.users = json.load(f)
        with open('nitro.yaml') as f:
            self.nitro = yaml.load(f, Loader=yaml.FullLoader) or {'Nitro': False} 
        print(self.nitro)

    
    async def reset(self):
        while True:
            await asyncio.sleep(20)
            self.users['cooldown'] = []
    
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('>>> Level System')
        self.client.loop.create_task(self.reset())
        
        
        
        
        
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.update_data(self.users, member)
        with open('users.json', 'w') as f:
            json.dump(self.users, f)

    
    @commands.Cog.listener()
    async def on_message(self, ctx):

        if ctx.author.bot: return
        author = ctx.author

        if author.id in self.users.get('cooldown', []):
            return

        
        await self.update_data(self.users, author)
        await self.add_experience(self.users, author, 5)
        await self.level_up(self.users, author, ctx)
        
        self.users['cooldown'].append(author.id)
        

        await asyncio.sleep(3)
        
        
        if author.id in self.users.get('cooldown', []):
            self.users["cooldown"].remove(author.id)
            with open('users.json', 'w') as f:
                json.dump(self.users, f)
        
        
        

    async def update_data(self, users, user):
        if not f'{user.id}' in self.users:
            self.users[f'{user.id}'] = {}
            self.users[f'{user.id}']['experience'] = 0
            self.users[f'{user.id}']['level'] = 1
        with open('users.json', 'w') as f:
            json.dump(self.users, f)

    async def add_experience(self, users, user, exp):
        self.users[f'{user.id}']['experience'] += exp
        with open('users.json', 'w') as f:
            json.dump(self.users, f)
    

    async def level_up(self, users, user, message):
        experience = self.users[f'{user.id}']['experience']
        lvl_start = self.users[f'{user.id}']['level']
        lvl_end = int(experience ** (1 / 4))
        if lvl_start < lvl_end:
            channel = message.guild.get_channel(895013303858913340)
            await send(channel, message = user.mention, embed = embed('LevelSystem', f'Du bist ein Level aufgestiegen!\nDu bist nun Level {lvl_end}'))
            self.users[f'{user.id}']['level'] = lvl_end
            if lvl_end == 2 and not self.nitro.get('Nitro'):
                self.nitro['Nitro'] = True
                with open('nitro.yaml', 'w') as f:
                    yaml.dump(self.nitro, f)
                id = 795306274467348510
                toga = message.guild.get_member(id)
                await toga.send(f'{user} hat die Level 20 erreicht!\nAm {datetime.now()}')
            role_id = self.level.get(lvl_end) or 0
            role = message.guild.get_role(role_id)
            if not role: return
            await user.add_roles(role)
            
            
        with open('users.json', 'w') as f:
            json.dump(self.users, f)
        
    @commands.command()
    async def level(self, ctx, member: discord.Member = None):
        
        if ctx.channel.id not in [805120734401790022, 895012195937689641]:
            return await send(ctx.channel, embed = error(f'{ctx.author.display_name}\nDu kannst nur im Bot Channel diesen Befehl ausführen'))
        
        if not member: 
            member = ctx.author 
        
        
        lvl = self.users[str(member.id)]['level']
        exp = self.users[str(member.id)]['experience']
        next_xp = (lvl +1)**4
        users = {}
        for k, v in self.users.items():
            if k == 'cooldown':
                continue
            users[k] = v
        rank_list_tuple = sorted(users.items(), reverse = True, key = lambda d: d[1]["experience"])
        rank_list = [i[0] for i in rank_list_tuple]
        rank = rank_list.index(str(member.id))
        
        embed = discord.Embed(title = f'__{str(member)} Level Stats__', colour = 15105570)
        #embed.set_author(name = str(member), icon_url = member.avatar_url)
        embed.set_footer(text = 'angefragt von {}'.format(str(ctx.author)), icon_url = ctx.author.avatar_url)
        embed.set_thumbnail(url = member.avatar_url)
        embed.add_field(name = 'Level', value = lvl, inline = True)
        embed.add_field(name = 'Rank', value = rank, inline = True)
        embed.add_field(name = 'XP', value = f'{exp}/{next_xp} ({"%.2f" % (100/ next_xp * exp)}%)', inline= False)
        embed.add_field(name = 'Event', value = 'Erste Level 20 bekommt Nitro(10€)')
        
        await ctx.send(embed = embed)
        
        
    @commands.command(aliases=["leaderboard"])
    async def top(self, ctx):
        if ctx.channel.id not in [805120734401790022, 895012195937689641]:
            return await send(ctx.channel, embed = error(f'{ctx.author.display_name}\nDu kannst nur im Bot Channel diesen Befehl ausführen'))
        
        mess_del = await ctx.channel.send("Bitte warte einen Moment!\nDies ist eine Beta und braucht dehalb mehr Zeit!")

        users = {}
        for k, v in self.users.items():
            if k == 'cooldown':
                continue
            users[k] = v
        new_dict1 = dict(sorted(users.items(), reverse = True, key = lambda d: d[1]["experience"]))
        names = [] 
        pictures = []
        i = 0
        for k in new_dict1.keys():
            if i == 40:
                break
            try:
                user = ctx.guild.get_member(int(k))
                name = user.display_name
                print('Test1')
                pic = Image.open(requests.get(user.avatar_url, stream=True).raw)
                print('Test2')
                try: pic.seek(1)
                except: pass
                names.append(name)
                pictures.append(pic)
            except: pass
            
            i += 1
        
        #Message = 'Top-Liste\n' + '\n'.join(names)
        #await ctx.send('Top-Liste\n' + '\n'.join(names))  
        #print(pictures)
        
        top_list_pic = do_toplist(1, pictures[:8], names[:8])
        
        top_list_pic.save('image.png')
        
        im = pyimgur.Imgur("9b590a5e304bb1c")
        upload = im.upload_image('image.png', title= 'Toplist')
        
        
        """ with io.BytesIO() as image_binary:
            top_list_pic.save(image_binary, 'PNG')
            image_binary.seek(0)
            
            file = discord.File('image.png', filename='image.png') """
            
        
        
        
        embed1 = discord.Embed(colour = 15105570)
        embed1.set_author(name = 'Toga\'s Castle (BETA!)', icon_url = 'https://cdn.discordapp.com/attachments/888481775347728435/889969546293805056/image0.jpg')
        embed1.set_image(url=upload.link)
        
        mess = await ctx.channel.send(embed = embed1, 
            components = [[button('Vorher', style=ButtonStyle.red, disabled = False), button('Nächste', id = 2)]])
        
        #mess = await ctx.send(file = file , embed = embed1)
        
        await mess_del.delete()
        
        site_start = 0
        site_end = 8
        while True:
            event = await self.client.wait_for('button_click', check = lambda event: event.message == mess)
            await mess.edit(components = [[button('Vorher', style=ButtonStyle.red, disabled = True), button('Nächste', id = 2, disabled= True)]], timeout = 30)
            await event.respond(type = 6)
            if event.component.id == '2':
                site_start += 8
                site_end += 8
            else:
                site_start -= 8
                site_end -= 8
            
            print(f'Start: {site_start}\nEnd: {site_end}')
            
            top_list_pic1 = do_toplist(site_start, pictures[site_start:site_end], names[site_start:site_end])
            top_list_pic1.save('image.png')
            """ with io.BytesIO() as image_binary1:
                top_list_pic1.save(image_binary1, 'PNG')
                image_binary1.seek(0)
                file1 = discord.File('image.png', filename='image.png') """
            upload = im.upload_image('image.png', title= 'Toplist')
            embed1 = discord.Embed(colour = 15105570)
            embed1.set_author(name = 'Toga\'s Castle (BETA!)', icon_url = 'https://cdn.discordapp.com/attachments/888481775347728435/889969546293805056/image0.jpg')
            embed1.set_image(url = upload.link)
            await mess.edit(embed = embed1, 
                            components = [[button('Vorher', style=ButtonStyle.red, disabled = False), button('Nächste', id = 2)]])
            print('Progress Finish')
            
        
        
            
    @commands.command()
    async def setlevel(self, ctx, number, level : discord.Role):
        return
        self.level[int(number)] = level.id
        with open('level.yaml', 'w') as f:
            yaml.dump(self.level, f)
    
    
def setup(client):
    client.add_cog(LevelSystem(client))
