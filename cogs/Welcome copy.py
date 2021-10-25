from threading import main_thread
import discord, io
from tempfile import TemporaryFile
from discord.ext import commands
from PIL import Image, ImageFilter, ImageFont, ImageDraw
from discord.file import File
import requests 


class Welcome(commands.Cog):
    def __init__(self, client):
        self.client = client 

    @commands.Cog.listener()
    async def on_ready(self):
        print('>>> Welcome')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        



        my_image = Image.open("Testing/toga_banner_willkommen.png")
        pb = Image.open(requests.get(member.avatar_url, stream=True).raw)
        #pb = Image.open('PLSS.png')
        #pb.save('NEWPB.png')
        #time.sleep(5)
        pb = pb.resize((250, 250))



        #pb.save('PLSS.png')


        title_font = ImageFont.truetype('Testing\Lemon Tuesday.otf', 120)
        font2 = ImageFont.truetype('Testing\Archive.otf', 30)

        title_text = "Willkommen"
        text = member.display_name.center(14)

        image_editable = ImageDraw.Draw(my_image)
        #my_image.paste(pb, (50, 85), pb)
        my_image.paste(pb, (50, 85), pb)

        image_editable.text((330, 70), title_text, (255, 255, 255), font=title_font)
        image_editable.text((325, 225), text, (256, 256, 256), font=font2)

        channel = member.guild.get_channel(786297889135001643)

        my_image.save(member.display_name + '.png')
        
        await channel.send(file = discord.File(member.display_name + '.png'))
        

    

def setup(client):
    client.add_cog(Welcome(client))
