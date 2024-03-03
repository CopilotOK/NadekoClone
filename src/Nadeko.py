# imports
import discord
from discord.ext import commands
from random import choice, randint
import asyncio
from User import User
from Card import cards
from PIL import Image
from os import remove

# bot token
TOKEN = "nah bro"
# to change custom status like nadeko
presence = [".trivia --pokemon",".draw 5",".h for help",".h greet", ".h aar",
            ".crypto btc", ".ani steins;gate"]
# this variable stores the power of next card specified by cheater
cheaterNumber = 0
dealer = None
# bot initialization shit 
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=".", intents=intents)
# ping command 
@bot.command()
async def ping(ctx):
   embed = discord.Embed(description="**"+ctx.author.display_name+"#0000" +" :ping_pong:**"+str(randint(200,500))+"ms",
                         color=discord.Colour.from_rgb(113, 205, 64))
   await ctx.send(embed=embed)

# cheater command
@bot.command()
async def setnext(ctx):
   global cheaterNumber
   msg = ""
   # this thing stores the number specified in .setnext [] command if no 
   # exceptions have been made, if exception has been made then the command
   # aborts with the error message.
   for i in range(8,len(ctx.message.content)):
      if ctx.message.content[i]!=None:
         j = ctx.message.content[i]
         msg+=j
   try:
      msg = int(msg)
   except Exception: 
      await ctx.send("**invalid usage**\nsyntax:`.setnext integer`\nexample:`setnext 1`")
   else:
      pc = []
      for i in dealer.deck:
         if i.power==msg:
            pc.append(i)
      if len(pc)==0:
         await ctx.send(f"no more {msg}'s left")
      else:
         cheaterNumber = msg
         await ctx.send(cheaterNumber)

@bot.command()
async def flip(ctx):
   y = randint(1,2)
   if y==1:
      embyd = discord.Embed(description="Flipped **Head**",color=discord.Colour.from_rgb(113, 205, 64))
      embyd.set_author(name=ctx.author.name+"#0000", icon_url=ctx.author.avatar)
      embyd.set_image(url="https://cdn.discordapp.com/attachments/1213193280410488897/1213739243856199680/coins.png?ex=65f691c1&is=65e41cc1&hm=aa8fee838b736c3034c739ca8014130578a7e6995e1323ac2bff143ba48888c1&")
      await ctx.send(embed=embyd)
   if y==2:
      embyd = discord.Embed(description="Flipped **Tail**",color=discord.Colour.from_rgb(113, 205, 64))
      embyd.set_author(name=ctx.author.name+"#0000", icon_url=ctx.author.avatar)
      embyd.set_image(url="https://cdn.discordapp.com/attachments/1213193280410488897/1213739224986288190/coins.png?ex=65f691bd&is=65e41cbd&hm=6a3071d8bac05c296a6561626f6a325840ce4ca5ea9b35833aff11e7ce33347f&")
      await ctx.send(embed=embyd)

# deck reshuffle
@bot.command()
async def dsh(ctx):
   global dealer
   dealer = User(ctx.author.name)
   dealer.deck=cards.copy()
   embqd = discord.Embed(description="**"+ctx.author.display_name+"#0000**"+" Deck reshuffled.",
                         color=discord.Colour.from_rgb(113, 205, 64))
   await ctx.send(embed=embqd)

# draw command like nadeko
@bot.command()
async def draw(ctx):
   global cheaterNumber
   global dealer
   msg = ""
   for i in range(5,len(ctx.message.content)):
      if ctx.message.content[i]!=None:
         j = ctx.message.content[i]
         msg+=j
   msg.strip()
   try:
      msg = int(msg)
   except Exception:
      pass
   if (len(str(msg))==0) or (msg==1):
      if cheaterNumber==0:
         if (isinstance(dealer,User))==False:
            dealer = User(ctx.author.name)
         rolledcard = choice(cards)
         dealer.power_inhand += rolledcard.power
         dealer.deck.remove(rolledcard)
         deckleft = len(dealer.deck)
         embeddraw = discord.Embed(description=f"**{deckleft}** cards left in the deck",
                                 color=discord.Colour.from_rgb(113, 205, 64))
         embeddraw.set_image(url=rolledcard.image)
         embeddraw.set_author(name=ctx.author.name+"#0000", icon_url=ctx.author.avatar)
         await ctx.send(embed=embeddraw)
      else:
         if (isinstance(dealer,User))==False:
            dealer = User(ctx.author.name)
         possiblecards = []
         for i in dealer.deck:
            if i.power==cheaterNumber:
               possiblecards.append(i)
         rc = choice(possiblecards)
         dealer.power_inhand=rc.power
         dealer.deck.remove(rc)
         deckleft = len(dealer.deck)
         embeddraw = discord.Embed(description=f"**{deckleft}** cards left in the deck",
                                 color=discord.Colour.from_rgb(113, 205, 64))
         embeddraw.set_image(url=rc.image)
         embeddraw.set_author(name=ctx.author.name+"#0000", icon_url=ctx.author.avatar)
         cheaterNumber=0
         await ctx.send(embed=embeddraw)





   elif msg==2:
      if (isinstance(dealer,User))==False:
         dealer = User(ctx.author.name)
      rolledcard1 = choice(cards)
      dealer.deck.remove(rolledcard1)
      rolledcard2 = choice(cards)
      dealer.deck.remove(rolledcard2)
      deck_left = len(dealer.deck)
      img1 = Image.open(f"src/cardsimg/{rolledcard1.name}.jpg")
      img2 = Image.open(f"src/cardsimg/{rolledcard2.name}.jpg")
      WIDTH = img1.size[0] + img2.size[0]
      HEIGHT = img1.size[1]
      img3 = Image.new('RGB',(WIDTH,HEIGHT))
      img3.paste(img1,(0,0))
      img3.paste(img2,(img1.size[0],0))
      img3.save("temp.jpg")
      embed_2 = discord.Embed(description=f"**{deck_left}** cards left in the deck.",
                              color=discord.Colour.from_rgb(113, 205, 64))
      file = discord.File("temp.jpg",filename="temp.jpg")
      embed_2.add_field(name="Cards",value="2")
      embed_2.set_image(url="attachment://temp.jpg")
      print(len(cards))
      embed_2.set_author(name=ctx.author.name+"#0000", icon_url=ctx.author.avatar)
      await ctx.send(embed=embed_2, file=file)
      file.close()
      remove("temp.jpg")
      

   else:
      embed = discord.Embed(title="Command Error",
                            description='''Invalid number specified. Make sure you're specifying parameters in the correct\norder.
                            \n**`.draw`**
                            Draws a card from this server's deck. You can draw up to 10 cards by supplying a\nnumber of cards to draw.\n
                            **Usage**
                            `.draw`
                            `.draw 5`\n''',
                            color=discord.Colour.from_rgb(236, 44, 28))
      embed.set_footer(text="Admin may disable verbose errors via `.ve` command")
      

      await ctx.send(embed=embed)
   


# set the presence on ready 
@bot.event
async def on_ready(): 
   await bot.change_presence(activity=discord.Game(choice(presence)))

# :)
bot.run(TOKEN)