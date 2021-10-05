import discord
import random
import logging
import os
from dislash import slash_commands
from dislash.interactions import *
from discord.ext import commands,tasks
from discord.ext.commands import has_permissions, CheckFailure

custom_prefixes = {}
default_prefixes = ['!']

async def determine_prefix(bot, message):
    guild = message.guild
    if guild:
        return custom_prefixes.get(guild.id, default_prefixes)
    else:
        return default_prefixes

intents = discord.Intents(messages=True, guilds=True, members=True)
bot = commands.Bot(command_prefix = determine_prefix) #prefix bota


logging.basicConfig(level=logging.WARNING)

TOKEN = 'ODgzMzI1ODY1NDc0MjY5MTky.YTITUQ.7Wh0Vp6DG_V7ecGRDDPPkPVbYYM'

#Přihlášení do bota
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Streaming(name='Beta v0.1.0', url='https://www.twitch.tv/Bluecat201')) #status bota   
    print('Connected to bot: {}'.format(bot.user.name))
    print('Bot ID: {}'.format(bot.user.id))

#Nastavení prefixu
@bot.command(aliases=['Setprefix','SETPREFIX'],brief = "Nastaví prefix bota", help="Nastaví prefix bota, co víc k tomu chceš vědět?")
@commands.guild_only()
async def setprefix(ctx, *, prefixes=""):
    custom_prefix[ctx.guild.id] = prefixes.split() or default_prefixes
    await ctx.send("Prefix nastaven!")

        
#invite bota
@bot.command(aliases=['Invite','INVITE'], brief="Invite na bota.", help="Pošle invite, díky kterému si bota můžete přidat k sobě na server")
async def invite(ctx):
    await ctx.send("Zde je můj invite: https://discord.com/api/oauth2/authorize?client_id=883325865474269192&permissions=8&scope=bot")

#support
@bot.command(aliases=['Support','SUPPORT'], brief="Invite na server majitele bota", help="Pošle invite na server majitele bota, co chceš víc vědět?")
async def support(ctx):
    await ctx.send("Zde najdete moji podporu: https://dsc.gg/bluecat | https://discord.gg/43H2HxB3Ax")

#twitch
@bot.command(aliases=['Twitch','TWITCH'], brief="Odkaz na twitch majitele bota", help="Odkaz na twitch majitele bota, co chceš víc vědět?")
async def twitch(ctx):
    await ctx.send("Zde je twitch mého stvořitele: https://www.twitch.tv/bluecat201")

#mluevení za bota
@commands.has_guild_permissions(manage_messages=True)
@bot.command(aliases=['Sudo','SUDO'],brief="Mluvení za bota", help="Za command napíšeš co chceš aby napsal bot a on to napíše")
async def sudo(ctx, *, arg):
    await ctx.send(arg)
    await ctx.message.delete()

#nemá oprávnění
@sudo.error
async def sudo_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Omlouvám se ale pro použití tohoto commandu potřebuješ mít opravnění **Spravovat zprávy**.")

#d
@bot.command()
async def d(ctx):
    await ctx.send("<:cicisrdicko:849285560832360531>")


#bluecat
@bot.command(aliases=['Bluecat','BLUECAT'],help='Pošle náhodný gif modré kočky', brief='Bluecat gif')
async def bluecat(ctx):
    nah = random.randrange(15)
    if nah == 0:
        await ctx.channel.send('https://tenor.com/view/blue-cat-wo-gif-21442488')
    elif nah == 1:
        await ctx.channel.send('https://tenor.com/view/bluecat-cute-cute-cartoon-playing-gif-13607070')
    elif nah == 2:
        await ctx.channel.send('https://tenor.com/view/blue-bugcat-capoo-cat-cant-reach-gif-14132398')
    elif nah == 3:
        await ctx.channel.send('https://tenor.com/view/bonnejournee-hello-ok-gif-20245217')
    elif nah == 4:
        await ctx.channel.send('https://tenor.com/view/blue-cat-bug-cat-capoo-no-i-dont-like-gif-14132390')
    elif nah == 5:
        await ctx.channel.send('https://tenor.com/view/crazy-blue-cat-cat-toilet-paper-nuts-tissue-gif-16005330')
    elif nah == 6:
        await ctx.channel.send('https://tenor.com/view/crazy-blue-cat-cat-high-five-good-job-gif-16005331')
    elif nah == 7:
        await ctx.channel.send('https://tenor.com/view/cat-crazy-blue-cat-rest-chill-gif-15931350')
    elif nah == 8:
        await ctx.channel.send('https://tenor.com/view/wiggle-random-blue-cat-dance-body-rolls-gif-16721254')
    elif nah == 9:
        await ctx.channel.send('https://tenor.com/view/cat-crazy-blue-cat-money-mine-dont-touch-gif-15942487')
    elif nah == 10:
        await ctx.channel.send('https://tenor.com/view/cat-crazt-blue-cat-work-computer-notebook-gif-16038891')
    elif nah == 11:
        await ctx.channel.send('https://tenor.com/view/blue-cat-bugcat-capoo-sleep-time-gif-14132347')
    elif nah == 12:
        await ctx.channel.send('https://tenor.com/view/blue-cat-bugcat-capoo-writing-gif-14132351')
    elif nah == 13:
        await ctx.channel.send('https://tenor.com/view/bugcat-bugcatsticker-excited-gif-12962907')
    elif nah == 14:
        await ctx.channel.send('https://tenor.com/view/blue-bugcat-capoo-cat-cellphone-gif-14132395')


#info
@bot.command(aliases=['Info','INFO'], brief="Info o botu", help="Vypíše informace o botovi")
async def info(ctx):
    await ctx.send(f"Bot vzniká jako moje dlouhodobá maturitní práce :)\nDatum vydání první alpha verze: 5.9.2021 \nDatum vydání první beta verze: 30.9.2021\nPlánované vydaní plné verze bota: ||1.3 - 29.4.2022|| \nNaprogrogramováno v pythonu \nPokud máte jakékoliv poznámky, rady či nápady pro bota, můžete je napsat na !support server. ;)\nPočet serverů, na kterých jsem: {len(bot.guilds)}\nVerze bota: Alpha 0.0.9 \nOwner: 𝕭𝖑𝖚𝖊𝖈𝖆𝖙#0406")

#latence
@bot.command(aliases=['Ping','PING'],brief="Pong", help="Vypíše latency bota")
async def ping(ctx):
    await ctx.send('Pong! {0}ms'.format(round(bot.latency, 1)))
    
#hug
@bot.command(aliases=['Hug','HUG'],help="Náhodný gif hug s pingem dané osoby",brief="Hug gif, pro někoho")
async def hug(ctx,member : discord.User = None):
    if member is None:
        await ctx.send('Musíš někoho označit/zadat ID')
    else:
        nah = random.randrange(100)
        await ctx.message.delete()
        if nah == 0:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/anime-hug-sweet-love-gif-14246498")
        elif nah == 1:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/teria-wang-kishuku-gakkou-no-juliet-hug-anime-gif-16509980")
        elif nah == 2:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/hug-anime-care-comfort-understanding-gif-15793129")
        elif nah == 3:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/hug-anime-gif-11074788")
        elif nah == 4:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/anime-hug-love-smile-gif-15942846")
        elif nah == 5:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/hug-anime-gif-15793126")
        elif nah == 6:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/sakura-quest-anime-animes-hug-hugging-gif-14721541")
        elif nah == 7:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/anime-hug-sweet-anime-gif-13857539")
        elif nah == 8:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/hugs-and-love-gif-19327081")
        elif nah == 9:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/toilet-bound-hanakokun-anime-anime-hug-gif-16831471")
        elif nah == 10:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/cuddle-hug-anime-bunny-costumes-happy-gif-17956092")
        elif nah == 11:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/anime-hug-gif-13221036")
        elif nah == 12:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/a-whisker-away-hug-love-anime-embrace-gif-17694740")
        elif nah == 13:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/horimiya-izumi-miyamura-hori-kyoko-couple-hug-gif-14539121")
        elif nah == 14:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/anime-couple-hug-cute-cuddle-gif-14898682")
        elif nah == 15:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/chiya-urara-meirochou-anime-saku-gif-8995974")
        elif nah == 16:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/anime-anime-hug-sweet-happy-in-love-gif-16103131")
        elif nah == 17:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/hug-anime-clingy-gif-7552075")
        elif nah == 18:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/anime-acchi-kocchi-anime-couple-neko-anime-rain-gif-16085531")
        elif nah == 19:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/anime-bed-bedtime-sleep-night-gif-12375072")
        elif nah == 20:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/hug-anime-gif-4898650")
        elif nah == 21:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/hug-anime-love-sweet-tight-hug-gif-7324587")
        elif nah == 22:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/anime-cheeks-hugs-gif-14106856")
        elif nah == 23:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/hug-anime-cartoon-japanese-fall-gif-7552093")
        elif nah == 24:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/anime-hug-hearts-hug-bff-gif-13857541")
        elif nah == 25:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/anime-anime-love-hug-love-sweet-gif-16131468")
        elif nah == 26:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/anime-hug-manga-cuddle-japan-gif-10522729")
        elif nah == 27:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/hug-cat-cute-aww-anime-gif-9200935")
        elif nah == 28:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/hug-anime-hug-cry-happy-anime-happy-gif-19679116")
        elif nah == 29:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/hug-couple-love-gif-14584871")
        elif nah == 30:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/anime-hug-love-hug-gif-13925386")
        elif nah == 31:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/my-little-monster-anime-hug-love-gif-13221416")
        elif nah == 32:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/hug-anime-sweet-gif-10195705")
        elif nah == 33:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/anime-hug-love-gif-15900664")
        elif nah == 34:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/blushing-anime-girl-couple-hug-gif-19423749")
        elif nah == 35:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/loli-dragon-anime-cute-hug-gif-9920978")
        elif nah == 36:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/anime-hug-cuddle-love-care-gif-17265727")
        elif nah == 37:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/%E0%B8%81%E0%B8%AD%E0%B8%94-gif-18374323")
        elif nah == 38:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/crying-anime-kyoukai-no-kanata-hug-hugging-anime-hug-tight-tight-hug-gif-17880570")
        elif nah == 39:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/anime-cute-girl-kotori-itsuka-date-a-live-gif-17438857")
        elif nah == 40:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/abra%C3%A7o-hug-miss-you-gif-14903944")
        elif nah == 41:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/hug-anime-gif-19674705")
        elif nah == 42:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/kakegurui-yumeko-jabami-hug-anime-anime-hug-gif-17991101")
        elif nah == 43:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/kiss-anime-cute-couples-gif-17252595")
        elif nah == 44:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/hug-anime-sweet-couple-gif-12668480")
        elif nah == 45:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/tackle-hug-couple-anime-cute-couple-love-gif-17023255")
        elif nah == 46:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/hug-anime-hug-anime-cute-uwu-gif-17264448")
        elif nah == 47:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/anime-hug-cuddle-gif-19768597")
        elif nah == 48:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/anime-choke-hug-too-tight-gif-14108949")
        elif nah == 49:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/cute-anime-hug-love-come-here-gif-7864716")
        elif nah == 50:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/sound-euphonium-hug-miss-you-hugs-hugging-gif-9882931")
        elif nah == 51:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/cuddle-nuzzle-cute-hug-hugging-gif-9375012")
        elif nah == 52:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/anime-cute-sweet-hug-gif-12668681")
        elif nah == 53:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/abrazo-hug-anime-gif-10307432")
        elif nah == 54:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/hug-sad-gif-14924015")
        elif nah == 55:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/chuunibyou-anime-couple-anime-couple-cute-gif-13576064")
        elif nah == 56:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/anime-cute-sweet-hug-gif-12668673")
        elif nah == 57:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/hug-darker-than-black-anime-gif-13976210")
        elif nah == 58:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/anime-hug-catgirl-neko-gif-9383138")
        elif nah == 59:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/hug-love-anime-kevyox-gif-14407779")
        elif nah == 60:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/love-hug-safe-couple-sweet-gif-15944593")
        elif nah == 61:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/hug-anime-crying-comfort-gif-15793130")
        elif nah == 62:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/elfenlied-kouta-nyu-lucy-hugging-gif-6238016")
        elif nah == 63:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/anime-couple-anime-winter-anime-cold-anime-snow-anime-snuggle-gif-15764601")
        elif nah == 64:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/manga-anime-sweet-gif-14844150")
        elif nah == 65:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/noragami-hug-anime-hug-smile-cute-gif-16980741")
        elif nah == 66:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/anime-anime-hug-anime-girls-anime-girls-hug-anime-yuri-hug-gif-16724635")
        elif nah == 67:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/love-hug-anime-affection-rain-gif-5634630")
        elif nah == 68:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/love-holding-hands-anime-cute-gif-17040364")
        elif nah == 69:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/hug-cuddle-comfort-love-friends-gif-5166500")
        elif nah == 70:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/anime-couples-bed-sleeping-sweet-gif-15069983")
        elif nah == 71:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/anime-hug-friends-cute-kawaii-gif-17363491")
        elif nah == 72:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/anime-hug-sweet-couple-gif-14389983")
        elif nah == 73:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/anime-hug-anime-cuddle-anime-love-gif-17789653")
        elif nah == 74:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/abra%C3%A7o-hug-love-bff-gif-14903952")
        elif nah == 75:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/hug-love-anime-gif-14566838")
        elif nah == 76:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/anime-cute-sweet-hug-gif-12668677")
        elif nah == 77:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/hug-cuddle-anime-cute-anime-hug-gif-18960633")
        elif nah == 78: 
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/anime-hug-sweet-couple-gif-12668472")
        elif nah == 79:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/anime-hug-its-ok-gif-13041472")
        elif nah == 80:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/darling-in-the-franxx-zhiro-zero-two-hiro-hiro-hugs-zero-two-gif-17406911")
        elif nah == 81:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/anime-pink-hair-zero-two-darling-in-the-franxx-002-gif-17316358")
        elif nah == 82:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/hug-zerotwo-gif-18106019")
        elif nah == 83:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/%D0%B0%D0%BD%D0%B8%D0%BC%D0%B5-darling-in-the-franxx-zero-two-hiro-hug-gif-14688041")
        elif nah == 84:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/hug-angelbeats-gif-12970895")
        elif nah == 85:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/sunset-sad-angel-beats-yuzuru-gif-20989612")
        elif nah == 86:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/hug-happy-cheer-yay-gamer-gif-12387846")
        elif nah == 87:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/ed-and-winry-hug-fma-love-gif-11492699")
        elif nah == 88:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/full-metal-alchemist-elric-hug-hugging-alphonse-gif-5770556")
        elif nah == 89:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/hug-gif-19389699")
        elif nah == 90:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/high-school-dxd-hug-sairaorg-issei-anime-gif-17403860")
        elif nah == 91:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/ohshc-ouran-high-school-host-club-anime-manga-japanese-anime-gif-5513135")
        elif nah == 92:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/cuddle-anime-hug-anime-hug-anime-gif-22458388")
        elif nah == 93:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/citrus-harumi-yuzu-hug-anime-gif-18171387")
        elif nah == 94:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/mei-aihara-citrus-hug-gif-18273620")
        elif nah == 95:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/yuri-on-ice-hug-love-shocked-gif-15095543")
        elif nah == 96:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/vikturi-yurionice-hug-hold-anime-gif-7171614")
        elif nah == 97:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/anime-hug-sweet-in-love-love-gif-17770766")
        elif nah == 98:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/evangelion-ritsuko-hug-gif-18089415")
        elif nah == 99:
            await ctx.channel.send(f"{ctx.author.mention} objímá {member.mention} https://tenor.com/view/nge-neon-genesis-evangelion-mari-asuka-eva-gif-22999430")
        
        
#Kick
@bot.command(aliases=['Kick','KICK'], brief="Kick uživatele", help="Vyhodí zmíněného uživatele ze serveru. Pouze pro lidi s právem vyhodit uživatele")
@commands.has_permissions(kick_members=True) #oprávnění na kick?
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member.mention} byl vyhozen z důvodu: {reason}.")

#Nemá oprávnění na kick
@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Omlouvám se, ale pokud chcete použít temhle command musíte mít oprávnění **vyhodit uživatele**.")

#ban
@bot.command(aliases=['Ban','BAN'], brief="Ban uživatele", help="Zakáže přístup zmíněnému uživately na server. Pouze pro lidi s právem zabanovat uživatele")
@commands.has_permissions(ban_members=True) #oprávnění na ban?
async def ban(ctx, member : discord.User = None, *, reason=None):

    if member is None: 
        await ctx.send("Prosím zadejte ID#discriminator k banu")
    if member == ctx.message.author:
        await ctx.channel.send("Nemůžeš zabanovat sám sebe")
    else:
        await member.ban(reason=reason)
        await ctx.send(f'{member.mention} byl zabanován z důvodu: {reason}.')

#Nemá oprávnění na ban
@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Omlouvám se ale pro použití tohoto commandu potřebuješ mít opravnění **Zabanovat uživatele**.")

#unban
@bot.command(aliases=['ub','UNBAN','Unban'], brief="Unban uživatele", help="Odstraní zákaz zmíněnému uživately na server. Pouze pro lidi s právem zabanovat uživatele")
@commands.has_guild_permissions(ban_members=True) #má oprávnění na ban?
@commands.bot_has_permissions(ban_members=True) #má bot oprávnění na ban?
async def unban(ctx, member: discord.User = None, *, reason=None): 

    if reason is None:  #uživatel neuvedl důvod
          reason = f"{ctx.author.name}#{ctx.author.discriminator} Neuvedl žádný důvod"
    if member is None: #uživatel nezadal uživatele k unbanu
          await ctx.send("Prosím zadejte ID#discriminator k unbanu")
    x = len(reason)   
    if x > 460: # 460 = limit znaků na reason
          return await ctx.send('Důvod musí mít maximálně 460 znaků')
    else:
          await ctx.guild.unban(member, reason=reason)
          await ctx.send(f'{member} byl odbannut z důvodu: {reason}')
    
#Nemá oprávnění/nebyl nalezen uživatel
@unban.error
async def unban_error(self,ctx, error): 
    if isinstance(error, commands.MemberNotFound): #nebyl nalezen uživatel k unbanu
                    await ctx.send("Žádný uživatel nebyl nalezen")
    elif isinstance(error, commands.BotMissingPermissions): #bot nemá oprávnění
                    await ctx.send("Bot nemá oprávnění zabanovat uživatele aby mohl použít tenhle command.")
    elif isinstance(error,commands.MissingPermissions): #uživatel nemá oprávnění
                    await ctx.send("Nemáš oprávnění zabanovat uživatele aby mohl použít tenhle command")


#logace připojení uživatele
@bot.event
async def on_member_join(member):
    server = str(member.guild.name)
    print(f'{member} se připojil na server {server}')

#logace přidání bota na server
@bot.event
async def on_guild_join(guild):
    print(f'Bot byl přidán na server: {guild}')

#logace odebrání bota ze serveru
@bot.event
async def on_guild_remove(guild):
    print(f'Bot byl odebrán ze serveru: {guild}')

#Logace odpojení uživatele
@bot.event
async def on_member_remove(member):
    server = str(member.guild.name)
    print(f'{member} se odpojil  ze serveru {server}')

#logace vytvoření role
@bot.event
async def on_guild_role_create(role):
    server = str(role.guild.name)
    print(f'Role {role} byla vytvořena [{server}]')

#logace smazání role
@bot.event
async def on_guild_role_delete(role):
    server = str(role.guild.name)
    print(f'Role {role} byla smazána [{server}]')

#logace přidání role uživately
@bot.event
async def on_guild_role_update(before,after):
    server = str(before.guild.name)
    print(f'Role {before} byla změněna na {after} na serveru {server}')

#logace změny zprávy
@bot.event
async def on_message_edit(before,after):
    server = str(before.guild.name)
    username = str(before.author)
    prvni = str(before.content)
    potom = str(after.content)
    print(f'Zpráva "{prvni}" byla změněna na "{potom}" od {username} ({server})')

#logace smazání zprávy
@bot.event
async def on_message_delete(message):
    zprava = str(message.content)
    username = str(message.author)
    server = str(message.guild.name)
    channel = str(message.channel.name)
    print(f'Zpráva "{zprava}" od {username} v roomce {channel} na serveru {server} byla smazána')

bot.run(TOKEN)
