from threading import main_thread
import discord, io
from tempfile import TemporaryFile
from discord.ext import commands
from PIL import Image, ImageFilter, ImageFont, ImageDraw
from discord.file import File
import requests 
import pyimgur
import tempfile

class Welcome(commands.Cog):
    def __init__(self, client):
        self.client = client 

    @commands.Cog.listener()
    async def on_ready(self):
        print('>>> Welcome')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.get_channel(786297889135001643)
        mess_del = await channel.send("Bitte warte einen Moment!\nDies ist eine Beta und braucht dehalb mehr Zeit!")
        def add_corners(im, rad):
            circle = Image.new('L', (rad * 2, rad * 2), 0)
            draw = ImageDraw.Draw(circle)
            draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
            alpha = Image.new('L', im.size, 255)
            w, h = im.size
            alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
            alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
            alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
            alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
            im.putalpha(alpha)
            return im 

        def makeShadow(image, iterations, border, offset, backgroundColour, shadowColour):
            fullWidth  = image.size[0] + abs(offset[0]) + 2*border
            fullHeight = image.size[1] + abs(offset[1]) + 2*border
            
            #Create the shadow's image. Match the parent image's mode.
            shadow = Image.new(image.mode, (fullWidth, fullHeight), backgroundColour)
            
            # Place the shadow, with the required offset
            shadowLeft = border + max(offset[0], 0) #if <0, push the rest of the image right
            shadowTop  = border + max(offset[1], 0) #if <0, push the rest of the image down
            #Paste in the constant colour
            shadow = add_corners(shadow, 20)
            shadow.paste(shadowColour, 
                        [shadowLeft, shadowTop,
                        shadowLeft + image.size[0],
                        shadowTop  + image.size[1] ])
            
            # Apply the BLUR filter repeatedly
            for i in range(iterations):
                shadow = shadow.filter(ImageFilter.BLUR)

            # Paste the original image on top of the shadow 
            imgLeft = border - min(offset[0], 0) #if the shadow offset was <0, push right
            imgTop  = border - min(offset[1], 0) #if the shadow offset was <0, push down
            shadow.paste(image, (imgLeft, imgTop))

            return shadow



        my_image = Image.open("toga_banner_willkommen.png")

        pb = Image.open(requests.get(member.avatar_url, stream=True).raw)
        pb = add_corners(pb, 20)
        pb = pb.resize((250, 250))
        pb = makeShadow(pb, 10, 10, (10,10), (255,189,200), (68,68,68))

        title_font = ImageFont.truetype('Fonts\Lemon Tuesday.otf', 120)
        font2 = ImageFont.truetype('Fonts\Archive.otf', 120)

        title_text = "Willkommen"
        text = str(member).center(14)

        image_editable = ImageDraw.Draw(my_image)
        my_image.paste(pb, (50, 90), pb)

        image_editable.text((330, 70), title_text, (255, 255, 255), font=title_font)
        image_editable.text((325, 225), text, (256, 256, 256), font=font2)

        Gif = Image.open('rain.gif')
        foo= []

        for frame in range(0,Gif.n_frames):

            Gif.seek(frame)
            img = Gif.convert("RGBA")
        
            datas = img.getdata()
            
            newData = []
            
            for items in datas:
                if items[0] == 3 and items[1] in [0, 3, 36] and items[2] == 3:
                    newData.append((255, 255, 255, 0))
                else:
                    newData.append(items)

            img.putdata(newData)
            
            image = my_image.copy()
            
            
            image.paste(img, (0,0), img)
            foo.append(image)
            #img.save(f'GIFFING/{frame}.png') 
        
        foo[0].save('out.gif', save_all=True, append_images=foo[1:], optimize = True,  loop = 0)
        
        
        print('Debug2')
        im = pyimgur.Imgur("9b590a5e304bb1c")
        
        
        upload = im.upload_image('out.gif', title= 'Willkommen')
        
        print('Debug3')
        embed = discord.Embed(title = '**Willkommen**', description = f'Willkommen {member} auf Toga\'s Castle <33')
        embed.add_field(name = 'Hier kannst du die Regel lesen und akzeptieren', value='<#786325420483543071>', inline= False)
        embed.add_field(name = 'Hier kannst du deine Self Rolen abholen', value = '<#786546098633965568>', inline=False)
        embed.add_field(name = 'Viel Spaß auf dem Server <3', value = '** **')
        embed.set_thumbnail(url = 'https://cdn.discordapp.com/icons/786297889135001640/a_d54285cf3b6a35fded59fa13aeded7c4.gif?size=4096')
        toga = member.guild.get_member(746088479582322819)
        embed.set_footer(text = toga.name, icon_url=toga.avatar_url)
        embed.set_author(name = str(member), icon_url= member.avatar_url)
        embed.set_image(url = upload.link)
        
        await channel.send(embed = embed)
        #251 207 170
        await mess_del.delete()
        
    @commands.command()
    async def text(self, ctx):
        await self.on_member_join(ctx.author)
        
        #embed = discord.Embed()
        #embed.set_image(url = 'https://cdn.discordapp.com/avatars/811145882745438208/a_b6d3bcb0ef10b059b89317ad39b44070.gif?size=4096')
        #await ctx.send(embed = embed)


    
def setup(client):
    client.add_cog(Welcome(client))
