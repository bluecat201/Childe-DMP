import discord
import random
import logging
import os
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
from discord.ext import commands,tasks
from discord.ext.commands import has_permissions, CheckFailure

custom_prefix = {}
default_prefixes = ['!']

async def determine_prefix(bot, message):
    guild = message.guild
    if guild:
        return custom_prefix.get(guild.id, default_prefixes)
    else:
        return default_prefixes

intents = discord.Intents(messages=True, guilds=True, members=True)
bot = commands.Bot(command_prefix = determine_prefix) #prefix bota
slash = SlashCommand(bot, sync_commands=True)


logging.basicConfig(level=logging.INFO)
TOKEN = ''

#kámen, nůžky, papír
@slash.slash(
    name="RPS",
    description="Kámen, nůžky, papír",
    options=[
        create_option(
            name="option",
            description="Vyber si",
            required=True,
            option_type=3,
            choices=[
                create_choice(
                    name="Kámen",
                    value="1"
                ),
                create_choice(
                    name="Nůžky",
                    value="2"
                ),
                create_choice(
                    name="Papír",
                    value="3"
                )
            ]
        )
    ]
)
async def _RPS(ctx:SlashContext, option:str):   #1=kámen 2=nůžky 3=papír
    pc= random.randint(1,3)
    if option=="1" and pc==1:
        await ctx.send("Kámen vs Kámen\n REMÍZA")
    elif option=="1" and pc==2:
        await ctx.send("Kámen vs Nůžky\n VYHRÁL JSI")
    elif option=="1" and pc==3:
        await ctx.send("Kámen vs Papír\n PROHRÁL JSI")
    elif option=="2" and pc==1:
        await ctx.send("Nůžky vs Kámen\n PROHRÁL JSI")
    elif option=="2" and pc==2:
        await ctx.send("Nůžky vs Nůžky\n REMÍZA")
    elif option=="2" and pc==3:
        await ctx.send("Nůžky vs Papír\n VYHRÁL JSI")
    elif option=="3" and pc==1:
        await ctx.send("Papír vs Kámen\n VYHRÁL JSI")
    elif option=="3" and pc==2:
        await ctx.send("Papír vs Nůžky\n PROHRÁL JSI")
    elif option=="3" and pc==3:
        await ctx.send("Papír vs Papír\n REMÍZA")

#Odkazy
@slash.slash(
    name="link",
    description="Moje odkazy",
    options=[
        create_option(
            name="option",
            description="Vyber si jaký odkaz chceš",
            required=True,
            option_type=3,
            choices=[
                create_choice(
                    name="Twitch",
                    value="Můj twitch: https://www.twitch.tv/bluecat201"
                ),
                create_choice(
                    name="Support",
                    value="Zde najdete moji podporu: https://dsc.gg/bluecat | https://discord.gg/43H2HxB3Ax"
                ),
                create_choice(
                    name="Youtube",
                    value="hl. kanál: https://www.youtube.com/channel/UCwY2CDHkQGmCIwgVgEJKt8w"
                ),
                create_choice(
                    name="Instagram",
                    value="Můj IG: https://www.instagram.com/bluecat221/"
                ),
                create_choice(
                    name="Web",
                    value="Můj web: https://bluecat201.weebly.com/"
                )
            ]
        )
    ]
)
async def _link(ctx:SlashContext, option:str):
    await ctx.send(option)

#Přihlášení do bota
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Streaming(name='Beta v0.1.1', url='https://www.twitch.tv/Bluecat201')) #status bota   
    print('Connected to bot: {}'.format(bot.user.name))
    print('Bot ID: {}'.format(bot.user.id))

#Nastavení prefixu
@commands.has_guild_permissions(administrator=True)
@bot.command(aliases=['Setprefix','SETPREFIX'],brief = "Nastaví prefix bota", help="Nastaví prefix bota, co víc k tomu chceš vědět?")
@commands.guild_only()
async def setprefix(ctx, *, prefixes=""):
    custom_prefix[ctx.guild.id] = prefixes.split() or default_prefixes
    await ctx.send("Prefix nastaven!")

#nemá oprávnění na setprefix
@setprefix.error
async def sudo_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Omlouvám se ale pro použití tohoto commandu potřebuješ mít opravnění **Administrator**.")
        
#invite bota
@bot.command(aliases=['Invite','INVITE'], brief="Invite na bota.", help="Pošle invite, díky kterému si bota můžete přidat k sobě na server")
async def invite(ctx):
    await ctx.send("Zde je můj invite: https://discord.com/api/oauth2/authorize?client_id=883325865474269192&permissions=8&scope=bot%20applications.commands")

#support
@bot.command(aliases=['Support','SUPPORT'], brief="Invite na server majitele bota", help="Pošle invite na server majitele bota, co chceš víc vědět?")
async def support(ctx):
    await ctx.send("Zde najdete moji podporu: https://dsc.gg/bluecat | https://discord.gg/43H2HxB3Ax")

#twitch
@bot.command(aliases=['Twitch','TWITCH'], brief="Odkaz na twitch majitele bota", help="Odkaz na twitch majitele bota, co chceš víc vědět?")
async def twitch(ctx):
    await ctx.send("Zde je twitch mého stvořitele: https://www.twitch.tv/bluecat201")

#mluevení za bota
@commands.has_guild_permissions(administrator=True)
@bot.command(aliases=['Sudo','SUDO'],brief="Mluvení za bota", help="Za command napíšeš co chceš aby napsal bot a on to napíše")
async def sudo(ctx, *, arg):
    await ctx.send(arg)
    await ctx.message.delete()

#nemá oprávnění
@sudo.error
async def sudo_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Omlouvám se ale pro použití tohoto commandu potřebuješ mít opravnění **Administrator**.")

#d
@bot.command()
async def d(ctx):
    await ctx.send("<:cicisrdicko:849285560832360531>")


#bluecat
@bot.command(aliases=['Bluecat','BLUECAT'],help='Pošle náhodný gif modré kočky', brief='Bluecat gif')
async def bluecat(ctx):
    nah = random.randint(0,19)
    embed=discord.Embed(color=0x0B0B45)
    if nah == 0:
        embed.set_image(url="https://c.tenor.com/fORGSJaP4GwAAAAC/blue-cat-wo.gif")
        await ctx.send(embed=embed)
    elif nah == 1:
        embed.set_image(url="https://c.tenor.com/bSleCKyyveEAAAAC/bluecat-cute.gif")
        await ctx.send(embed=embed)
    elif nah == 2:
        embed.set_image(url="https://c.tenor.com/D0aN1jITREUAAAAC/blue-bugcat.gif")
        await ctx.send(embed=embed)
    elif nah == 3:
        embed.set_image(url="https://c.tenor.com/J8Sz2t6XwzUAAAAC/bonnejournee-hello.gif")
        await ctx.send(embed=embed)
    elif nah == 4:
        embed.set_image(url="https://c.tenor.com/vadBPwveI50AAAAC/blue-cat-bug-cat-capoo.gif")
        await ctx.send(embed=embed)
    elif nah == 5:
        embed.set_image(url="https://c.tenor.com/3l8Zk8liuWMAAAAC/crazy-blue-cat-cat.gif")
        await ctx.send(embed=embed)
    elif nah == 6:
        embed.set_image(url="https://c.tenor.com/l73iIUVPxo8AAAAC/crazy-blue-cat-cat.gif")
        await ctx.send(embed=embed)
    elif nah == 7:
        embed.set_image(url="https://c.tenor.com/Zu1bfl2DtZEAAAAC/cat-crazy-blue-cat.gif")
        await ctx.send(embed=embed)
    elif nah == 8:
        embed.set_image(url="https://c.tenor.com/2NzI0HjUdVoAAAAC/wiggle-random.gif")
        await ctx.send(embed=embed)
    elif nah == 9:
        embed.set_image(url="https://c.tenor.com/XNGhq50aZ4cAAAAC/cat-crazy-blue-cat.gif")
        await ctx.send(embed=embed)
    elif nah == 10:
        embed.set_image(url="https://c.tenor.com/XiS-MmoQvCMAAAAC/cat-crazt-blue-cat.gif")
        await ctx.send(embed=embed)
    elif nah == 11:
        embed.set_image(url="https://c.tenor.com/cpteQxT2mIAAAAAC/blue-cat.gif")
        await ctx.send(embed=embed)
    elif nah == 12:
        embed.set_image(url="https://c.tenor.com/94ZDYicBkrEAAAAC/blue-cat.gif")
        await ctx.send(embed=embed)
    elif nah == 13:
        embed.set_image(url="https://c.tenor.com/mRSz5lJbtW0AAAAC/bugcat-bugcatsticker.gif")
        await ctx.send(embed=embed)
    elif nah == 14:
        embed.set_image(url="https://c.tenor.com/JGFWu0GIcDsAAAAC/blue-bugcat.gif")
        await ctx.send(embed=embed)
    elif nah == 15:
        embed.set_image(url="https://c.tenor.com/6bpYwINwasQAAAAC/capoo-bugcat-capoo.gif")
        await ctx.send(embed=embed)
    elif nah == 16:
        embed.set_image(url="https://c.tenor.com/feJE-gpuuyMAAAAC/cat-crazy-blue-cat.gif")
        await ctx.send(embed=embed)
    elif nah == 17:
        embed.set_image(url="https://c.tenor.com/uMxAPszmTQoAAAAC/cat-crazy-blue-cat.gif")
        await ctx.send(embed=embed)
    elif nah == 18:
        embed.set_image(url="https://c.tenor.com/APnr0hEBj2EAAAAC/cat-crazy-blue-cat.gif")
        await ctx.send(embed=embed)
    elif nah == 19:
        embed.set_image(url="https://c.tenor.com/pyqCUy7VNCkAAAAC/bugcat-capoo.gif")
        await ctx.send(embed=embed)


#info
@bot.command(aliases=['Info','INFO'], brief="Info o botu", help="Vypíše informace o botovi")
async def info(ctx):
    await ctx.send(f"Bot vzniká jako moje dlouhodobá maturitní práce :)\nDatum vydání první alpha verze: 5.9.2021 \nDatum vydání první beta verze: 30.9.2021\nPlánované vydaní plné verze bota: ||1.3 - 29.4.2022|| \nNaprogrogramováno v pythonu \nPokud máte jakékoliv poznámky, rady či nápady pro bota, můžete je napsat na !support server. ;)\nPočet serverů, na kterých jsem: {len(bot.guilds)}\nVerze bota: Beta 0.1.0 \nOwner: 𝕭𝖑𝖚𝖊𝖈𝖆𝖙#9203")

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
        nah = random.randint(0,99)
        await ctx.message.delete()
        embed=discord.Embed(description=f"{ctx.author.mention} objímá {member.mention}", color=0xFFFF00)
        if nah == 0:
            embed.set_image(url="https://c.tenor.com/9e1aE_xBLCsAAAAC/anime-hug.gif")
            await ctx.send(embed=embed)
        elif nah == 1:
            embed.set_image(url="https://c.tenor.com/Ct4bdr2ZGeAAAAAC/teria-wang-kishuku-gakkou-no-juliet.gif")
            await ctx.send(embed=embed)
        elif nah == 2:
            embed.set_image(url="https://c.tenor.com/c8M8yU1q6c4AAAAC/hug-anime.gif")
            await ctx.send(embed=embed)
        elif nah == 3:
            embed.set_image(url="https://c.tenor.com/z2QaiBZCLCQAAAAC/hug-anime.gif")
            await ctx.send(embed=embed)
        elif nah == 4:
            embed.set_image(url="https://c.tenor.com/DVOTqLcB2jUAAAAC/anime-hug-love.gif")
            await ctx.send(embed=embed)
        elif nah == 5:
            embed.set_image(url="https://c.tenor.com/0vl21YIsGvgAAAAC/hug-anime.gif")
            await ctx.send(embed=embed)
        elif nah == 6:
            embed.set_image(url="https://c.tenor.com/xgVPw2QK5n8AAAAC/sakura-quest-anime.gif")
            await ctx.send(embed=embed)
        elif nah == 7:
            embed.set_image(url="https://c.tenor.com/dIvoDyyk5LIAAAAC/anime-hug-sweet.gif")
            await ctx.send(embed=embed)
        elif nah == 8:
            embed.set_image(url="https://c.tenor.com/2bWwi8DhDsAAAAAC/hugs-and-love.gif")
            await ctx.send(embed=embed)
        elif nah == 9:
            embed.set_image(url="https://c.tenor.com/xIuXbMtA38sAAAAd/toilet-bound-hanakokun.gif")
            await ctx.send(embed=embed)
        elif nah == 10:
            embed.set_image(url="https://c.tenor.com/ItpTQW2UKPYAAAAC/cuddle-hug.gif")
            await ctx.send(embed=embed)
        elif nah == 11:
            embed.set_image(url="https://c.tenor.com/kPgR6UH6AXcAAAAC/anime-hug.gif")
            await ctx.send(embed=embed)
        elif nah == 12:
            embed.set_image(url="https://c.tenor.com/0PIj7XctFr4AAAAC/a-whisker-away-hug.gif")
            await ctx.send(embed=embed)
        elif nah == 13:
            embed.set_image(url="https://c.tenor.com/KD__SewDxK0AAAAC/horimiya-izumi-miyamura.gif")
            await ctx.send(embed=embed)
        elif nah == 14:
            embed.set_image(url="https://c.tenor.com/G9yuomdknAsAAAAd/anime-couple.gif")
            await ctx.send(embed=embed)
        elif nah == 15:
            embed.set_image(url="https://c.tenor.com/SPs0Rpt7HAcAAAAC/chiya-urara.gif")
            await ctx.send(embed=embed)
        elif nah == 16:
            embed.set_image(url="https://c.tenor.com/EKS8EWkhZJUAAAAC/anime-anime-hug.gif")
            await ctx.send(embed=embed)
        elif nah == 17:
            embed.set_image(url="https://c.tenor.com/UhcyGsGpLNIAAAAC/hug-anime.gif")
            await ctx.send(embed=embed)
        elif nah == 18:
            embed.set_image(url="https://c.tenor.com/stLEkL3l0NAAAAAC/anime-acchi-kocchi.gif")
            await ctx.send(embed=embed)
        elif nah == 19:
            embed.set_image(url="https://c.tenor.com/JTqXUbfSSkYAAAAC/anime-bed.gif")
            await ctx.send(embed=embed)
        elif nah == 20:
            embed.set_image(url="https://c.tenor.com/F1VUry86n7kAAAAC/hug-anime.gif")
            await ctx.send(embed=embed)
        elif nah == 21:
            embed.set_image(url="https://c.tenor.com/jQ0FcfbsXqIAAAAC/hug-anime.gif")
            await ctx.send(embed=embed)
        elif nah == 22:
            embed.set_image(url="https://c.tenor.com/X5nBTYuoKpoAAAAC/anime-cheeks.gif")
            await ctx.send(embed=embed)
        elif nah == 23:
            embed.set_image(url="https://c.tenor.com/pcULC09CfkgAAAAC/hug-anime.gif")
            await ctx.send(embed=embed)
        elif nah == 24:
            embed.set_image(url="https://c.tenor.com/nHkiUCkS04gAAAAC/anime-hug-hearts.gif")
            await ctx.send(embed=embed)
        elif nah == 25:
            embed.set_image(url="https://c.tenor.com/qQXjMmdgYioAAAAC/anime-anime-love.gif")
            await ctx.send(embed=embed)
        elif nah == 26:
            embed.set_image(url="https://c.tenor.com/VqazOH8fQ8gAAAAC/anime-hug.gif")
            await ctx.send(embed=embed)
        elif nah == 27:
            embed.set_image(url="https://c.tenor.com/vkiqyZJWJ4wAAAAC/hug-cat.gif")
            await ctx.send(embed=embed)
        elif nah == 28:
            embed.set_image(url="https://c.tenor.com/Pd2sMiVr09YAAAAC/hug-anime-hug.gif")
            await ctx.send(embed=embed)
        elif nah == 29:
            embed.set_image(url="https://c.tenor.com/EnfEuWDXthkAAAAC/hug-couple.gif")
            await ctx.send(embed=embed)
        elif nah == 30:
            embed.set_image(url="https://c.tenor.com/S3KQ1sDod7gAAAAC/anime-hug-love.gif")
            await ctx.send(embed=embed)
        elif nah == 31:
            embed.set_image(url="https://c.tenor.com/yGIZgfY778MAAAAC/my-little-monster-anime.gif")
            await ctx.send(embed=embed)
        elif nah == 32:
            embed.set_image(url="https://c.tenor.com/ztEJgrjFe54AAAAC/hug-anime.gif")
            await ctx.send(embed=embed)
        elif nah == 33:
            embed.set_image(url="https://c.tenor.com/83QLplerW8sAAAAC/anime-hug.gif")
            await ctx.send(embed=embed)
        elif nah == 34:
            embed.set_image(url="https://c.tenor.com/SDQNVUH6sCMAAAAC/blushing-anime.gif")
            await ctx.send(embed=embed)
        elif nah == 35:
            embed.set_image(url="https://c.tenor.com/fLxZt7jo1YEAAAAC/loli-dragon.gif")
            await ctx.send(embed=embed)
        elif nah == 36:
            embed.set_image(url="https://c.tenor.com/5UwhB5xQSTEAAAAC/anime-hug.gif")
            await ctx.send(embed=embed)
        elif nah == 37:
            embed.set_image(url="https://c.tenor.com/epQeAT-abYgAAAAC/%E0%B8%81%E0%B8%AD%E0%B8%94.gif")
            await ctx.send(embed=embed)
        elif nah == 38:
            embed.set_image(url="https://c.tenor.com/Qw4m3inaSZYAAAAC/crying-anime-kyoukai-no-kanata-hug.gif")
            await ctx.send(embed=embed)
        elif nah == 39:
            embed.set_image(url="https://c.tenor.com/mmQyXP3JvKwAAAAC/anime-cute.gif")
            await ctx.send(embed=embed)
        elif nah == 40:
            embed.set_image(url="https://c.tenor.com/z6wApX13fSEAAAAC/abra%C3%A7o-hug.gif")
            await ctx.send(embed=embed)
        elif nah == 41:
            embed.set_image(url="https://c.tenor.com/nmzZIEFv8nkAAAAC/hug-anime.gif")
            await ctx.send(embed=embed)
        elif nah == 42:
            embed.set_image(url="https://c.tenor.com/3JhgCdprym8AAAAC/kakegurui-yumeko-jabami.gif")
            await ctx.send(embed=embed)
        elif nah == 43:
            embed.set_image(url="https://c.tenor.com/uZbyY_n5VZoAAAAC/kiss-anime.gif")
            await ctx.send(embed=embed)
        elif nah == 44:
            embed.set_image(url="https://c.tenor.com/zirc8LTWVUkAAAAC/hug-anime.gif")
            await ctx.send(embed=embed)
        elif nah == 45:
            embed.set_image(url="https://c.tenor.com/sBFE3GeNpJ4AAAAC/tackle-hug-couple.gif")
            await ctx.send(embed=embed)
        elif nah == 46:
            embed.set_image(url="https://c.tenor.com/2lr9uM5JmPQAAAAC/hug-anime-hug.gif")
            await ctx.send(embed=embed)
        elif nah == 47:
            embed.set_image(url="https://c.tenor.com/zvlN9ZJEaj4AAAAC/anime-hug.gif")
            await ctx.send(embed=embed)
        elif nah == 48:
            embed.set_image(url="https://c.tenor.com/ixaDEFhZJSsAAAAC/anime-choke.gif")
            await ctx.send(embed=embed)
        elif nah == 49:
            embed.set_image(url="https://c.tenor.com/ljXMDMzMaxcAAAAC/cute-anime.gif")
            await ctx.send(embed=embed)
        elif nah == 50:
            embed.set_image(url="https://c.tenor.com/o1jezAk92FUAAAAC/sound-euphonium-hug.gif")
            await ctx.send(embed=embed)
        elif nah == 51:
            embed.set_image(url="https://c.tenor.com/5u1n4SYgd3AAAAAC/cuddle-nuzzle.gif")
            await ctx.send(embed=embed)
        elif nah == 52:
            embed.set_image(url="https://c.tenor.com/rQ2QQQ9Wu_MAAAAC/anime-cute.gif")
            await ctx.send(embed=embed)
        elif nah == 53:
            embed.set_image(url="https://c.tenor.com/ncblDAj_2FwAAAAC/abrazo-hug.gif")
            await ctx.send(embed=embed)
        elif nah == 54:
            embed.set_image(url="https://c.tenor.com/22VxM2JL_r0AAAAd/hug-sad.gif")
            await ctx.send(embed=embed)
        elif nah == 55:
            embed.set_image(url="https://c.tenor.com/GJ6oX6r0mZsAAAAC/chuunibyou-anime.gif")
            await ctx.send(embed=embed)
        elif nah == 56:
            embed.set_image(url="https://c.tenor.com/CfwNyKCP-L4AAAAC/anime-cute.gif")
            await ctx.send(embed=embed)
        elif nah == 57:
            embed.set_image(url="https://c.tenor.com/uIBg3BLATf0AAAAC/hug-darker.gif")
            await ctx.send(embed=embed)
        elif nah == 58:
            embed.set_image(url="https://c.tenor.com/l0AcbwYY50sAAAAC/anime-hug.gif")
            await ctx.send(embed=embed)
        elif nah == 59:
            embed.set_image(url="https://c.tenor.com/Q83w83J1VzUAAAAC/hug-love.gif")
            await ctx.send(embed=embed)
        elif nah == 60:
            embed.set_image(url="https://c.tenor.com/IRG8Ji4th6kAAAAC/love-hug.gif")
            await ctx.send(embed=embed)
        elif nah == 61:
            embed.set_image(url="https://c.tenor.com/ek1fEuNncMAAAAAC/hug-anime.gif")
            await ctx.send(embed=embed)
        elif nah == 62:
            embed.set_image(url="https://c.tenor.com/IC8bGfUwtL4AAAAC/elfenlied-kouta.gif")
            await ctx.send(embed=embed)
        elif nah == 63:
            embed.set_image(url="https://c.tenor.com/84vXUVCdL4AAAAAC/anime-couple-anime-winter.gif")
            await ctx.send(embed=embed)
        elif nah == 64:
            embed.set_image(url="https://c.tenor.com/6o00RFQhxzsAAAAC/manga-anime.gif")
            await ctx.send(embed=embed)
        elif nah == 65:
            embed.set_image(url="https://c.tenor.com/DtJ3jwoZ-jUAAAAC/noragami-hug.gif")
            await ctx.send(embed=embed)
        elif nah == 66:
            embed.set_image(url="https://c.tenor.com/qr-CxJEClOAAAAAd/anime-anime-hug.gif")
            await ctx.send(embed=embed)
        elif nah == 67:
            embed.set_image(url="https://c.tenor.com/kP7ssdam30oAAAAC/love-hug.gif")
            await ctx.send(embed=embed)
        elif nah == 68:
            embed.set_image(url="https://c.tenor.com/WUZAwo5KFdMAAAAd/love-holding-hands.gif")
            await ctx.send(embed=embed)
        elif nah == 69:
            embed.set_image(url="https://c.tenor.com/3ergzHiRIBwAAAAC/hug-cuddle.gif")
            await ctx.send(embed=embed)
        elif nah == 70:
            embed.set_image(url="https://c.tenor.com/GuHHnDT6quYAAAAd/anime-couples.gif")
            await ctx.send(embed=embed)
        elif nah == 71:
            embed.set_image(url="https://c.tenor.com/cFhjNVecNGcAAAAC/anime-hug.gif")
            await ctx.send(embed=embed)
        elif nah == 72:
            embed.set_image(url="https://c.tenor.com/i9MDVwZtSOcAAAAd/anime-hug.gif")
            await ctx.send(embed=embed)
        elif nah == 73:
            embed.set_image(url="https://c.tenor.com/71Cux-aY4G4AAAAC/anime-hug.gif")
            await ctx.send(embed=embed)
        elif nah == 74:
            embed.set_image(url="https://c.tenor.com/qF7mO4nnL0sAAAAC/abra%C3%A7o-hug.gif")
            await ctx.send(embed=embed)
        elif nah == 75:
            embed.set_image(url="https://c.tenor.com/I3lwUAtmLI8AAAAC/hug-love.gif")
            await ctx.send(embed=embed)
        elif nah == 76:
            embed.set_image(url="https://c.tenor.com/jDJlRRFUge4AAAAC/anime-cute.gif")
            await ctx.send(embed=embed)
        elif nah == 77:
            embed.set_image(url="https://c.tenor.com/keasv-Cnh4kAAAAd/hug-cuddle.gif")
            await ctx.send(embed=embed)
        elif nah == 78: 
            embed.set_image(url="https://c.tenor.com/wTcSp6je00YAAAAC/anime-hug.gif")
            await ctx.send(embed=embed)
        elif nah == 79:
            embed.set_image(url="https://c.tenor.com/RRmtObXpOegAAAAC/anime-hug.gif")
            await ctx.send(embed=embed)
        elif nah == 80:
            embed.set_image(url="https://c.tenor.com/c0qkKNy2H6IAAAAd/darling-in-the-franxx-zhiro.gif")
            await ctx.send(embed=embed)
        elif nah == 81:
            embed.set_image(url="https://c.tenor.com/8-PnV57w01sAAAAd/anime-pink-hair.gif")
            await ctx.send(embed=embed)
        elif nah == 82:
            embed.set_image(url="https://c.tenor.com/oWYEaH8x-sMAAAAC/hug-zerotwo.gif")
            await ctx.send(embed=embed)
        elif nah == 83:
            embed.set_image(url="https://c.tenor.com/MASjtj5fg7EAAAAC/%D0%B0%D0%BD%D0%B8%D0%BC%D0%B5-darling-in-the-franxx.gif")
            await ctx.send(embed=embed)
        elif nah == 84:
            embed.set_image(url="https://c.tenor.com/Ml4PdOdQGTMAAAAd/hug-angelbeats.gif")
            await ctx.send(embed=embed)
        elif nah == 85:
            embed.set_image(url="https://c.tenor.com/b1z__hMUKloAAAAd/sunset-sad.gif")
            await ctx.send(embed=embed)
        elif nah == 86:
            embed.set_image(url="https://c.tenor.com/iLsPfRvx-IoAAAAC/hug-happy.gif")
            await ctx.send(embed=embed)
        elif nah == 87:
            embed.set_image(url="https://c.tenor.com/LhuSoLDP_Q0AAAAC/ed-and-winry-hug.gif")
            await ctx.send(embed=embed)
        elif nah == 88:
            embed.set_image(url="https://c.tenor.com/cOJHQQDw2ykAAAAC/full-metal-alchemist-elric.gif")
            await ctx.send(embed=embed)
        elif nah == 89:
            embed.set_image(url="https://c.tenor.com/_Q9aixiFpGoAAAAC/hug.gif")
            await ctx.send(embed=embed)
        elif nah == 90:
            embed.set_image(url="https://c.tenor.com/DPygDikJDWkAAAAd/high-school-dxd-hug.gif")
            await ctx.send(embed=embed)
        elif nah == 91:
            embed.set_image(url="https://c.tenor.com/Ln_wIGuTVQUAAAAC/ohshc-ouran-high-school-host-club.gif")
            await ctx.send(embed=embed)
        elif nah == 92:
            embed.set_image(url="https://c.tenor.com/08vDStcjoGAAAAAd/cuddle-anime-hug-anime.gif")
            await ctx.send(embed=embed)
        elif nah == 93:
            embed.set_image(url="https://c.tenor.com/vBzOvBQ5MugAAAAC/citrus-harumi.gif")
            await ctx.send(embed=embed)
        elif nah == 94:
            embed.set_image(url="https://c.tenor.com/jwtpRuzWsQIAAAAC/mei-aihara.gif")
            await ctx.send(embed=embed)
        elif nah == 95:
            embed.set_image(url="https://c.tenor.com/wrFFpt0QQq0AAAAC/yuri-on-ice.gif")
            await ctx.send(embed=embed)
        elif nah == 96:
            embed.set_image(url="https://c.tenor.com/dVduziBWMGwAAAAd/vikturi-yurionice.gif")
            await ctx.send(embed=embed)
        elif nah == 97:
            embed.set_image(url="https://c.tenor.com/rCixLedVnsMAAAAC/anime-hug.gif")
            await ctx.send(embed=embed)
        elif nah == 98:
            embed.set_image(url="https://c.tenor.com/6JWa6o9OPUYAAAAC/evangelion-ritsuko.gif")
            await ctx.send(embed=embed)
        elif nah == 99:
            embed.set_image(url="https://c.tenor.com/ZI905qOL1OYAAAAd/nge-neon-genesis-evangelion.gif")
            await ctx.send(embed=embed)
        
        
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