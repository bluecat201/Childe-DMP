import discord
import random
import logging
import os
from discord_buttons_plugin import *
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
bot = commands.Bot(command_prefix = determine_prefix, help_command=None) #prefix bota
buttons = ButtonsClient(bot)
slash = SlashCommand(bot, sync_commands=True)


logging.basicConfig(level=logging.INFO)
TOKEN = ''

#Přihlášení do bota
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Streaming(name='Beta v0.1.2', url='https://www.twitch.tv/Bluecat201')) #status bota   
    print('Connected to bot: {}'.format(bot.user.name))
    print('Bot ID: {}'.format(bot.user.id))

#test button
@bot.command()
async def cbutton(ctx):
    await buttons.send(
        content = "this is the message",
        channel = ctx.channel.id,
        components = [
            ActionRow([
                Button(
                    label = "A button",
                    style = ButtonType().Primary,
                    custom_id = "button_one"
                )
            ])
        ]
    )

@buttons.click
async def button_one(ctx):
    await ctx.reply("Hello")

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

#help
@bot.command()
async def help(ctx):
    embed=discord.Embed(title="Help",description="ban - Zabanování uživatele\n bluecat - random bluecat gif\n help - tohle\n hug - Random hug gif pro někoho\n info - Info o botovi\n invite - Invite na bota\n kick - kick uživatele\n kiss - Random hug gif pro někoho\n ping - latence bota\n setprefix - Nastavení prefixu bota, jen pro **Administratory**\n sudo - mluvení za bota, jen pro **Administrátory**\n support - Invite na server majitele bota, kde najedete podporu bota\n twitch - Odkaz na twitch majitele\n unban - Unban uživatele\n\n\n **Slash commands**\n RPS - hra kámen, nůžky, papír s pc\n Linky - Odkazy na soc sítě majitele bota", color=0x000000)
    await ctx.send(embed=embed)

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
    nah = random.randint(1,20)
    await ctx.message.delete()
    embed=discord.Embed(color=0x0B0B45)
    file = discord.File(f"C:/Users/User/Desktop/škola/DMP/Childe-DMP/Bluecat/{nah}.gif", filename=f"image.gif")
    embed.set_image(url=f"attachment://image.gif")
    await ctx.send(file=file, embed=embed)


#info
@bot.command(aliases=['Info','INFO'], brief="Info o botu", help="Vypíše informace o botovi")
async def info(ctx):
    await ctx.send(f"Bot vzniká jako moje dlouhodobá maturitní práce :)\nDatum vydání první alpha verze: 5.9.2021 \nDatum vydání první beta verze: 30.9.2021\nPlánované vydaní plné verze bota: ||1.3 - 29.4.2022|| \nNaprogrogramováno v pythonu \nPokud máte jakékoliv poznámky, rady či nápady pro bota, můžete je napsat na !support server. ;)\nPočet serverů, na kterých jsem: {len(bot.guilds)}\nVerze bota: Beta 0.1.2 \nOwner: 𝕭𝖑𝖚𝖊𝖈𝖆𝖙#0406")

#latence
@bot.command(aliases=['Ping','PING'],brief="Pong", help="Vypíše latency bota")
async def ping(ctx):
    await ctx.send('Pong! {0}ms'.format(round(bot.latency, 1)))

#kiss
@bot.command(aliases=['Kiss','KISS'],help="Náhodný gif kiss s pingem dané osoby",brief="Kiss gif, pro někoho")
async def kiss(ctx,member : discord.User = None):
    if member is None:
        await ctx.send('Musíš někoho označit/zadat ID')
    else:
        nah = random.randint(1,100)
        await ctx.message.delete()
        embed=discord.Embed(description=f"{ctx.author.mention} líbá {member.mention}", color=0xFFFF00)
        file = discord.File(f"C:/Users/User/Desktop/škola/DMP/Childe-DMP/kiss/{nah}.gif", filename=f"image.gif")
        embed.set_image(url=f"attachment://image.gif")
        await ctx.send(file=file, embed=embed)

#hug
@bot.command(aliases=['Hug','HUG'],help="Náhodný gif hug s pingem dané osoby",brief="Hug gif, pro někoho")
async def hug(ctx,member : discord.User = None):
    if member is None:
        await ctx.send('Musíš někoho označit/zadat ID')
    else:
        nah = random.randint(1,100)
        await ctx.message.delete()
        embed=discord.Embed(description=f"{ctx.author.mention} objímá {member.mention}", color=0xFFFF00)
        file = discord.File(f"C:/Users/User/Desktop/škola/DMP/Childe-DMP/hug/{nah}.gif", filename=f"image.gif")
        embed.set_image(url=f"attachment://image.gif")
        await ctx.send(file=file, embed=embed)
        
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
        await ctx.send("Omlouvám se, ale pokud chcete použít tenhle command musíte mít oprávnění **vyhodit uživatele**.")

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