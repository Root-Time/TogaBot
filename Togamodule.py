from datetime import datetime
import discord
import asyncio
import yaml
from discord_components import *
from PIL import Image, ImageFont, ImageDraw


client = None

with open('Data/Settings.yaml', 'r') as f:
    setting = yaml.load(f, Loader=yaml.FullLoader) or {}   
    logs_id = setting.get('Logs')
with open('Data/Warn.yaml', 'r') as f:
    warn = yaml.load(f, Loader=yaml.FullLoader) or {} 
with open('Data/Mute.yaml', 'r') as f:
    mute = yaml.load(f, Loader=yaml.FullLoader) or {} 
with open('Data/config.yaml', 'r') as f:
    config = yaml.load(f, Loader=yaml.FullLoader) or {}



def start(_client):
    global client, logs
    client = _client

    

async def send(channel, *args, **kwargs):
    """
    channel -> Discord Channel, 
    Button -> ButtonTyp
    Message -> str, 
    embed (Title, Text, Color or (Format), (Format)) -> tuple, 
    time (Delete After) -> Int, float, 
    check(for wait) -> function, 
    """
    embed = kwargs.get('embed')
    time = kwargs.get('time')
    check = kwargs.get('check')
    Message = kwargs.get('mess') or kwargs.get('Message') or kwargs.get('message')
    #load
       
    mess = await channel.send(Message, embed = embed, delete_after = time, components = [[i for i in args]] if args else None)

    if not check:
        return mess

    while True:
        try :event = await client.wait_for('button_click', check = lambda event: event.message == mess, timeout = time)
        except asyncio.TimeoutError:
            event = None
        if await check(event): break
        
def embed(title, description, c=0):
    if c in ['blue', 'b']: 
        c = 3447003  # blue
    elif c in ['red', 'r']: 
        c = 15158332 # red
    elif c in ['green', 'g']: 
        c = 3066993  # green
    elif c in ['orange', 'o']: 
        c = 15105570 # orange
    return discord.Embed(title=title, description=description, colour=c)

def error(text):
    return embed('Error', text, 'r')

def mod(author, text):
    embed1 = discord.Embed(description=f"```yaml\n{text}```", color=10038562)
    embed1.set_footer(text = f'angefragt von {author}', icon_url = author.avatar_url)
    embed1.set_author(name = 'Moderation', icon_url = 'https://cdn.discordapp.com/attachments/888481775347728435/889969546293805056/image0.jpg')
    embed1.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/888481775347728435/889969546293805056/image0.jpg')
    return embed1

def log(text, mode = 0, player = "Unbekannt"):
    """
    0 -> Normal
    1 -> Warning
    2 -> Critical
    """
    if mode == 0:
        name = "Logger"
    elif mode == 1:
        name = 'Warning'
    else:
        name = 'Critical Error'
        
    embed1 = discord.Embed(description=f"```yaml\n{text}```", color=0, timestep = datetime.now())
    embed1.set_author(name = name, icon_url = 'https://cdn.discordapp.com/attachments/888481775347728435/889969546293805056/image0.jpg')
    embed1.set_footer(text = f'verursacht von {player}', icon_url = player.avatar_url if player != 'Unbekannt' else 'https://cdn.discordapp.com/attachments/881237542836510780/890266853937668126/Fragezeichen_-_Vector-Icon-300x300.png')
    return embed1

def error(text):
    embed1 = discord.Embed(description=f"```yaml\n{text}```", color= 15158332)
    embed1.set_author(name = 'Error', icon_url = 'https://cdn.discordapp.com/attachments/888481775347728435/889969546293805056/image0.jpg')
    #embed1.set_footer(text = f'verursacht von {player}', icon_url = player.avatar_url if player != 'Unbekannt' else 'https://cdn.discordapp.com/attachments/881237542836510780/890266853937668126/Fragezeichen_-_Vector-Icon-300x300.png')
    return embed1

def lev(text, player):
    embed1 = discord.Embed(description=f"```yaml\n{text}```", color=0, timestep = datetime.now())
    embed1.set_footer(text = f'Level von {player}', icon_url = player.avatar_url if player != 'Unbekannt' else 'https://cdn.discordapp.com/attachments/881237542836510780/890266853937668126/Fragezeichen_-_Vector-Icon-300x300.png')
    return embed1

def info(text):
    return embed('Info', text, 'o')

async def respond(event):
    await event.respond(content = 'Du bist nicht berechtigt diesen Knopf zu drücken!')

def button(label, style = ButtonStyle.blue, id = 1, disabled = False, url = None):
    return Button(label= label, style=style, id = id, disabled = disabled, url = url)

async def ask(channel, text, author, client):
    mess = await channel.send(embed = embed('Bestätigung', text, 'b'), delete_after = 30, components = [[button('ja'), button('Nein', ButtonStyle.red, id = 2)]])
    #mess = await send(channel, button('ja'), button('Nein', ButtonStyle.red, id = 2), embed = embed, time = 30)
    
    while True:
        try :event = await client.wait_for('button_click', check = lambda event: event.message == mess, timeout = 30)
        except asyncio.TimeoutError:
            return
        if event.author == author:
            await mess.delete() 
            if event.component.id == "1":
                await event.respond(type = 6)
                return True
            await event.respond(type = 6)
            return
        await respond(event)

def do_toplist(start_number, pictures, names):
    
    toplist_img = Image.open('toplist1.jpg')
    trans = Image.open('Toga_Trans.png')
    trans = trans.convert("RGBA")
    line = 136
    for pb in pictures:
        pb = pb.resize((40, 40))
        toplist_img.paste(pb, (85, line))
        line += 69

    ###Text
    Font = ImageFont.truetype('Fonts\Archive.otf', 30)
    top_text = ImageDraw.Draw(toplist_img)

    #Name
    #Number
    line = 143
    number = start_number
    for name in names:   
        top_text.text((130, line), name , (251, 207, 170), font=Font)
        top_text.text((35, line), str(number).center(3) , (251, 207, 170), font=Font)
        line += 69
        number += 1
        
    toplist_img.paste(trans,(0,0), trans)
    
    return toplist_img