import discord as d
from discord.ext import commands
import functools
import typing
import asyncio
import time
"""
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
"""
#if __name__ == "__main__":
#   asyncio.run(main())


token=''

intents = d.Intents.all()
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix='?', intents=intents)

a=1
@bot.event
async def on_message(message):
    
    global a

    if message.author == bot.user:
        return
    if message.channel.id==1211148115550142464:
        try:
            n = int(message.content)
        except ValueError:
            return
        
        if n == a:
            a += 1
            await message.add_reaction("👍")

        else:
            await message.add_reaction("👎")
            a=1
    else:
        return

    await bot.process_commands(message)

bot.run(token)