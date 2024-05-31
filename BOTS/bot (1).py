import discord as d
from discord.ext import commands
import functools
import typing
import random
import asyncio
import datetime
import time

def to_thread(func: typing.Callable) -> typing.Coroutine:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        wrapped = functools.partial(func, *args, **kwargs)
        return await loop.run_in_executor(None, wrapped)
    return wrapper

@to_thread
def blocking_func(a, b, c=1):
    time.sleep(a + b + c)
    return " "

async def main():
    a = await blocking_func(1, 2, 3)
    print(a)

if __name__ == "__main__":
    asyncio.run(main())


token=''

intents = d.Intents.all()
intents.guilds = True
intents.message_content = True

client = d.Client(intents=intents)
bot = commands.Bot(command_prefix='?', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user} Ready!')

@bot.command(name='hola')
async def hola(cxt):
    await cxt.send("Hola!!111!1!")

@bot.command(name='usuarios')
async def usuario(cxt):
    print(bot.users)
    await cxt.send([i.global_name for i in bot.users if i.bot==False])

@bot.command(name='mensaje')
async def proff(cxt):
    if len(cxt.message.content.split(' ',1))==1:
        await cxt.send('No hay mensaje')
    else:
        await cxt.send(cxt.message.content.split(' ',1)[1])

@bot.command(name='pic')
async def pic(cxt):
    print([i.name for i in bot.users]+[i.global_name for i in bot.users],len(cxt.message.content.split(' ')))
    if (len(cxt.message.content.split(' '))>1) and (cxt.message.content.split(' ',1)[1] in [i.name for i in bot.users]+[i.global_name for i in bot.users]):
        name=cxt.message.content.split(' ',1)[1]
        a=0
        for i in bot.users:
            if name == i.name or name == i.global_name:
                break
            else:
                a+=1
        user=bot.users[a]
    elif len(cxt.message.content.split(' '))==1:
        user=cxt.author
    else:
        await cxt.send('nombre invalido')
        return
    url=user.display_avatar.url
    embed= d.Embed(title=f"Pic de {user}",color=d.Color.dark_gold())
    embed.set_image(url=url)
    embed.set_footer(text='Hecho por mi bot',icon_url=bot.user.display_avatar.url)
    await cxt.send(embed=embed)
    
@bot.command()
async def info(ctx):
    embed = d.Embed(title=f"{ctx.guild.name}", description="Hola soy jarvis tu bot", timestamp=datetime.datetime.now(datetime.UTC), color=d.Color.pink())
    embed.add_field(name="Server created at", value = f"{ctx.guild.created_at}")
    embed.add_field(name = "Server OWner", value = f"{ctx.guild.owner}")
    embed.add_field(name = "Server ID", value = f"{ctx.guild.id}")
    embed.set_thumbnail(url = f"{ctx.guild.icon}")
    await ctx.send(embed=embed)

@bot.command(name='bye')
async def dc(cxt):
    await cxt.send("ADIOS!")
    await bot.close()
    
@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()
    await ctx.send(f'Conectado al canal de voz: {channel}')

@bot.command()
async def leave(ctx):
    voice_client = ctx.guild.voice_client
    if voice_client:
        await voice_client.disconnect()
        await ctx.send('Desconectado del canal de voz')
    else:
        await ctx.send('No estoy conectado a un canal de voz')

bot.run(token)