import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!',
                   description='Warframe market price checker')


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)


@bot.command()
async def hello():
    await bot.say('Hello!')

token = open('token.txt','r').read()
bot.run(token)
