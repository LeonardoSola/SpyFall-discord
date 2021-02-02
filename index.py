import discord
from random import randint, shuffle
from scenes import scenes, images
from discord.ext import commands
import config

bot = commands.Bot(command_prefix=config.prefix)

players_list = []
gameinfo = {"started":False, "map":None, 'spy':None}


@bot.command()
async def ping(ctx):
    await ctx.send('Pong! {0}'.format(round(bot.latency, 1)))

@bot.command()
async def join(ctx):
    if ctx.channel.type is discord.ChannelType.private:
        return
    if gameinfo["started"]:
        await ctx.send('Game not started!')
        return
    if len(players_list) >= 8:
        await ctx.send('Maximum players reached!')
        return
    for x in players_list:
        if x.id == ctx.author.id:
            await ctx.send(f'You already joined the match!')
            return
    players_list.append(ctx.author)
    await ctx.send(f'Now have {len(players_list)} players')

@bot.command()
async def start(ctx):
    if ctx.channel.type is discord.ChannelType.private:
        return
    if gameinfo["started"]:
        await ctx.send('Game not started!')
        return
    if len(players_list) < 3:
        await ctx.send(f'Only have {len(players_list)} players, minimum of 3 players!')
        return

    message = "lista de jogadores:\n"
    for y, x in enumerate(players_list): 
        message+= f"{y+1} - <@{x.id}>\n"
    await ctx.send(message)

    random_map = randint(0, (len(scenes)-1))
    funcoes = []
    players_ingame = players_list.copy()
    for x,item in enumerate(scenes.items()):
        y, z = item
        if x == random_map:
            y,z
            gameinfo["map"] = y
            funcoes = z.copy()
    shuffle(players_ingame)
    shuffle(funcoes)
    funcoes = iter(funcoes)
    gameinfo["started"] = True
    for n,x in enumerate(players_ingame):
        if n == 0:
            if images["Spy"]:
                await x.send(f"Spy, find out where you are!", file=discord.File(images["Spy"])) 
            else:
                await x.send(f"Spy, find out where you are!")
            gameinfo["spy"] = x.id
            continue
        funcao = next(funcoes)
        if images[gameinfo["map"]]:
            await x.send(f'Place: {gameinfo["map"]}!\nFunction: {funcao}!',file=discord.File(images[gameinfo["map"]]))
        else:
            await x.send(f'Place: {gameinfo["map"]}!\nFunction: {funcao}!')
@bot.command()
async def players(ctx):
    if ctx.channel.type is discord.ChannelType.private:
        return
    message = "Players list:\n"
    for y, x in enumerate(players_list): 
        message+= f"{y+1} - <@{x.id}>\n"
    await ctx.send(message)      

@bot.command()
async def stop(ctx):
    global players_list
    global gameinfo
    if ctx.channel.type is discord.ChannelType.private:
        return
    if not gameinfo["started"]:
        await ctx.send('Game not started!')
        return
    await ctx.send(f'Place: {gameinfo["map"]}\n Spy: <@{gameinfo["spy"]}>')
    gameinfo["started"] = False
    gameinfo["map"] = None
    gameinfo["spy"] = None
    players_list = []

@bot.command()
async def places(ctx):
    message = "Places:\n"
    counter = 0
    for x,y in scenes.items():
        counter += 1
        message += f'{counter} - {x}\n'
    await ctx.send(message)

# Events
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Streaming(name="Github:", url="https://github.com/LeonardoSola"))
    print('Ready!')


bot.run(config.token)