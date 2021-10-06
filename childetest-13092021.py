import discord
import random
import logging
from discord.ext import commands

intents = discord.Intents(messages=True, guilds=True, members=True)
bot = commands.Bot(command_prefix='!')

logging.basicConfig(level=logging.WARNING)

TOKEN = 'ODgzMzI1ODY1NDc0MjY5MTky.YTITUQ.7Wh0Vp6DG_V7ecGRDDPPkPVbYYM'

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Streaming(name='alpha v0.0.6', url='https://www.twitch.tv/Bluecat201'))    
    print('Connected to bot: {}'.format(bot.user.name))
    print('Bot ID: {}'.format(bot.user.id))


@bot.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    server = str(message.guild.name)
    mention = str(message.author.mention)
    print(f'{username}: {user_message} ({channel}) [{server}]')

    if message.author == bot.user:
        return

    if user_message.lower() == 'hello':
        await message.channel.send(f'hello {mention} <:ciciahuj:849285790479286283> ! How are you?')
    elif user_message.lower() == 'ahoj':
        await message.channel.send(f'Ahoj {mention} <:ciciahuj:849285790479286283> ! Jak se vede?')
    elif user_message.lower() == 'bye':
        await message.channel.send(f'See you later {mention} <:ciciahuj:849285790479286283>  !')
        return
    elif user_message.lower() == '!random':
        response = f'This is your random number: {random.randrange(1000000)}'
        await message.channel.send(response)
    elif user_message.lower() == '!invite':
        await message.channel.send('Tohle je invite https://discord.com/api/oauth2/authorize?client_id=883325865474269192&permissions=8&scope=bot')
        return
    elif user_message.lower() == '!support':
        await message.channel.send('Zde najdete podporu serveru: https://dsc.gg/bluecat | https://discord.gg/43H2HxB3Ax')
        return
    elif user_message.lower() == '!twitch':
        await message.channel.send('můj twitch: https://www.twitch.tv/bluecat201')
        return
    
    elif user_message.lower() == '!help':
        await message.channel.send('hello, ahoj, bye, dobré ráno, dobrou noc, gm, gn, !random, !invite, !support, !twitch')
        return
    
    if user_message.lower() == 'dobré ráno':
        await message.channel.send(f'Krásné dobré ráno ti přeji {mention} <:ciciahuj:849285790479286283>  !')
    elif user_message.lower() == 'dobrou noc':
        await message.channel.send(f'Dobrou noc a krásné sny ti přeji {mention} <:ciciahuj:849285790479286283> !')
    elif user_message.lower() == 'gm':
        await message.channel.send(f'Krásné dobré ráno ti přeji {mention} <:ciciahuj:849285790479286283> !')
    elif user_message.lower() == 'gn':
        await message.channel.send(f'Dobrou noc a krásné sny ti přeji {mention} <:ciciahuj:849285790479286283>  !')
    elif user_message.lower() == 'bluecat':
        nah = random.randrange(8)
        if nah == 0:
            await message.channel.send('https://tenor.com/view/blue-cat-wo-gif-21442488')
        elif nah == 1:
            await message.channel.send('https://tenor.com/view/bluecat-cute-cute-cartoon-playing-gif-13607070')
        elif nah == 2:
            await message.channel.send('https://tenor.com/view/blue-bugcat-capoo-cat-cant-reach-gif-14132398')
        elif nah == 3:
            await message.channel.send('https://tenor.com/view/bonnejournee-hello-ok-gif-20245217')
        elif nah == 4:
            await message.channel.send('https://tenor.com/view/blue-cat-bug-cat-capoo-no-i-dont-like-gif-14132390')
        elif nah == 5:
            await message.channel.send('https://tenor.com/view/crazy-blue-cat-cat-toilet-paper-nuts-tissue-gif-16005330')
        elif nah == 6:
            await message.channel.send('https://tenor.com/view/crazy-blue-cat-cat-high-five-good-job-gif-16005331')
        elif nah == 7:
            await message.channel.send('https://tenor.com/view/cat-crazy-blue-cat-rest-chill-gif-15931350')
        elif nah == 8:
            await message.channel.send('https://tenor.com/view/wiggle-random-blue-cat-dance-body-rolls-gif-16721254')
        elif nah == 9:
            await message.channel.send('https://tenor.com/view/cat-crazy-blue-cat-money-mine-dont-touch-gif-15942487')
        elif nah == 10:
            await message.channel.send('https://tenor.com/view/cat-crazt-blue-cat-work-computer-notebook-gif-16038891')
        elif nah == 11:
            await message.channel.send('https://tenor.com/view/blue-cat-bugcat-capoo-sleep-time-gif-14132347')
        elif nah == 12:
            await message.channel.send('https://tenor.com/view/blue-cat-bugcat-capoo-writing-gif-14132351')
        elif nah == 13:
            await message.channel.send('https://tenor.com/view/bugcat-bugcatsticker-excited-gif-12962907')
        elif nah == 14:
            await message.channel.send('https://tenor.com/view/blue-bugcat-capoo-cat-cellphone-gif-14132395')
        
@bot.event
async def on_member_join(member):
    server = str(member.guild.name)
    print(f'{member} se připojil na server {server}')

@bot.event
async def on_guild_join(guild):
    print(f'Bot byl přidán na server: {guild}')

@bot.event
async def on_guild_remove(guild):
    print(f'Bot byl odebrán ze serveru: {guild}')

@bot.event
async def on_member_remove(member):
    server = str(member.guild.name)
    print(f'{member} se odpojil  ze serveru {server}')

@bot.event
async def on_guild_role_create(role):
    server = str(role.guild.name)
    print(f'Role {role} byla vytvořena [{server}]')

@bot.event
async def on_guild_role_delete(role):
    server = str(role.guild.name)
    print(f'Role {role} byla smazána [{server}]')

@bot.event
async def on_guild_role_update(before,after):
    server = str(before.guild.name)
    print(f'Role {before} byla změněna na {after} na serveru {server}')

@bot.event
async def on_message_edit(before,after):
    server = str(before.guild.name)
    username = str(before.author)
    prvni = str(before.content)
    potom = str(after.content)
    print(f'Zpráva "{prvni}" byla změněna na "{potom}" od {username} ({server})')

@bot.event
async def on_message_delete(message):
    zprava = str(message.content)
    username = str(message.author)
    server = str(message.guild.name)
    channel = str(message.channel.name)
    print(f'Zpráva "{zprava}" od {username} v roomce {channel} na serveru {server} byla smazána')


    
bot.run(TOKEN)
