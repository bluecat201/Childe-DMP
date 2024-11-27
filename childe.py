import discord
import aiohttp
from discord.ext import commands, tasks
import random
import json
import os
import asyncio
from discord.ui import Button, View
from discord import app_commands
from discord.ext.commands import MissingPermissions
from roleplay import Roleplay
from economy import Economy
import aiofiles


# Nastavení prefixu
async def determine_prefix(bot, message):
    guild = message.guild
    if guild:
        return custom_prefix.get(guild.id, default_prefixes)
    else:
        return default_prefixes

# Nastavení základních proměnných
os.chdir("C:\\Users\\Elitebook\\Desktop\\Childe\\Childe-DMP")
custom_prefix = {}
default_prefixes = ['!']

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix=determine_prefix, intents=intents)
bot.warnings = {}  # guild_id : {member_id: [count, [(admin_id, reason)]]}


# Event: Bot je připraven
@bot.event
async def on_ready():
    print(f'Connected to bot: {bot.user.name}')
    print(f'Bot ID: {bot.user.id}')
    await bot.change_presence(activity=discord.Streaming(name='Beta v0.2.6', url='https://www.twitch.tv/Bluecat201'))
    await bot.add_cog(Roleplay(bot))
    await bot.add_cog(Economy(bot))
    # Inicializace varování
    for guild in bot.guilds:
        bot.warnings[guild.id] = {}

        if not os.path.exists(f"{guild.id}.txt"):
            with open(f"{guild.id}.txt", "w") as f:
                pass

        async with aiofiles.open(f"{guild.id}.txt", mode="r") as file:
            lines = await file.readlines()
            for line in lines:
                data = line.split(" ")
                member_id = int(data[0])
                admin_id = int(data[1])
                reason = " ".join(data[2:]).strip("\n")
                bot.warnings[guild.id].setdefault(member_id, [0, []])
                bot.warnings[guild.id][member_id][0] += 1
                bot.warnings[guild.id][member_id][1].append((admin_id, reason))

# Event: Připojení na nový server
@bot.event
async def on_guild_join(guild):
    bot.warnings[guild.id] = {}

# Slash příkaz: Kámen, nůžky, papír
@bot.tree.command(name="rps", description="Zahraj si kámen, nůžky, papír")
@app_commands.choices(option=[
    app_commands.Choice(name="Kámen", value="1"),
    app_commands.Choice(name="Nůžky", value="2"),
    app_commands.Choice(name="Papír", value="3"),
])
async def rps(interaction: discord.Interaction, option: app_commands.Choice[str]):
    pc = random.randint(1, 3)
    outcomes = {
        ("1", 1): "Kámen vs Kámen\n REMÍZA",
        ("1", 2): "Kámen vs Nůžky\n VYHRÁL JSI",
        ("1", 3): "Kámen vs Papír\n PROHRÁL JSI",
        ("2", 1): "Nůžky vs Kámen\n PROHRÁL JSI",
        ("2", 2): "Nůžky vs Nůžky\n REMÍZA",
        ("2", 3): "Nůžky vs Papír\n VYHRÁL JSI",
        ("3", 1): "Papír vs Kámen\n VYHRÁL JSI",
        ("3", 2): "Papír vs Nůžky\n PROHRÁL JSI",
        ("3", 3): "Papír vs Papír\n REMÍZA",
    }
    await interaction.response.send_message(outcomes[(option.value, pc)])


# Slash příkaz: Odkazy
@bot.tree.command(name="link", description="Moje odkazy")
@app_commands.choices(option=[
    app_commands.Choice(name="Twitch", value="Můj twitch: https://www.twitch.tv/bluecat201"),
    app_commands.Choice(name="Support", value="Zde najdete moji podporu: https://dsc.gg/bluecat | https://discord.gg/43H2HxB3Ax"),
    app_commands.Choice(name="Youtube", value="hl. kanál: https://www.youtube.com/channel/UCwY2CDHkQGmCIwgVgEJKt8w"),
    app_commands.Choice(name="Instagram", value="Můj IG: https://www.instagram.com/bluecat221/"),
    app_commands.Choice(name="Web", value="Můj web: https://bluecat201.weebly.com/"),
])
async def link(interaction: discord.Interaction, option: app_commands.Choice[str]):
    await interaction.response.send_message(option.value)


# Spuštění bota
TOKEN = ''

#|non-slash|  
#NORMAL COMMANDS
#ban
@bot.command(aliases=['Ban', 'BAN'])
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.User = None, *, reason=None):
    if member is None:
        await ctx.send("Prosím zadejte ID#discriminator k banu")
    if member == ctx.author:
        await ctx.send("Nemůžeš zabanovat sám sebe")
    else:
        await member.ban(reason=reason)
        await ctx.send(f'{member.mention} byl zabanován z důvodu: {reason}.')

#ban error
@ban.error
async def ban_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("Omlouvám se ale pro použití tohoto commandu potřebuješ mít oprávnění **Zabanovat uživatele**.")


#bluecat
@bot.command(aliases=['Bluecat','BLUECAT'])
async def bluecat(ctx):
    nah = random.randint(1,20)
    await ctx.message.delete()
    embed=discord.Embed(color=0x0B0B45)
    file = discord.File(f"C:/Users/Elitebook/Desktop/Childe/Childe-DMP/bluecat/{nah}.gif", filename=f"image.gif")
    embed.set_image(url=f"attachment://image.gif")
    await ctx.send(file=file, embed=embed)

#d
@bot.command()
async def d(ctx):
    await ctx.send("<:cicisrdicko:849285560832360531>")


#info
@bot.command(aliases=['Info','INFO'])
async def info(ctx):
    await ctx.send(f"Bot vznikal jako moje dlouhodobá maturitní práce :)\nDatum vydání první alpha verze: 5.9.2021 \nDatum vydání první beta verze: 30.9.2021\nNaprogramováno v pythonu \nPokud máte jakékoliv poznámky, rady či nápady pro bota, můžete je napsat na !support server. ;)\nPočet serverů, na kterých jsem: {len(bot.guilds)}\nVerze bota: Beta 0.2.6 \nDeveloper: Bluecat201")

#invite bota
@bot.command(aliases=['Invite','INVITE'])
async def invite(ctx):
    await ctx.send("Zde je můj invite: https://discord.com/api/oauth2/authorize?client_id=883325865474269192&permissions=8&scope=bot%20applications.commands")

#Kick
@bot.command(aliases=['Kick','KICK'])
@commands.has_permissions(kick_members=True) #oprávnění na kick?
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member.mention} byl vyhozen z důvodu: {reason}.")

#Nemá oprávnění na kick
@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Omlouvám se, ale pokud chcete použít tenhle command musíte mít oprávnění **vyhodit uživatele**.")


#unmute
@bot.command()
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    embed = discord.Embed(title="unmuted", description=f"{member.mention} was unmuted ", colour=discord.Colour.light_gray())
    await ctx.send(embed=embed)
    await member.send(f" Byl jsi unmutnut v: {guild.name}")
    await member.remove_roles(mutedRole)

#mute
@bot.command()
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member=None, time=None,*,reason=None):
    if not member:
        await ctx.send("Musíte označit uživatele kterého chcete mutnout")
    elif not time:
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name="Muted")

        if not mutedRole:
            mutedRole = await guild.create_role(name="Muted")

            for channel in guild.channels:
                await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
        if not reason:
            reason="No reason given"
        embed = discord.Embed(title="muted", description=f"{member.mention} was muted ", colour=discord.Colour.light_gray())
        embed.add_field(name="reason:", value=reason, inline=False)
        await ctx.send(embed=embed)
        await member.send(f" Byl jsi mutnut v: {guild.name} Důvod: {reason}")
        await member.add_roles(mutedRole, reason=reason)
    else:
        if not reason:
            reason="No reason given"
        #teď manipulace s časem mutu

        try:
            seconds = int(time[:-1]) #získá číslo z časového argumentu
            duration = time[-1] #získá jednotku času, s, m, h, d
            if duration == "s":
                seconds = seconds*1
            elif duration == "m":
                seconds = seconds * 60
            elif duration == "h":
                seconds = seconds * 60 * 60
            elif duration == "d":
                seconds = seconds * 86400
            else:
                await ctx.send("Nesprávně zadaný čas")
                return
        except Exception as e:
            print(e)
            await ctx.send("Nesprávně zadaný čas")
            return
        guild = ctx.guild
        Muted = discord.utils.get(guild.roles,name="Muted")
        if not Muted:
            Muted = await guild.create_role(name="Muted")
            for channel in guild.channels:
                await channel.set_permissions(Muted, speak=False, send_message=False, read_message_history=True, read_messages=False)
        await member.add_roles(Muted, reason=reason)
        muted_embed = discord.Embed(title="Muted a user", description=f"{member.mention} Byl mutnut {ctx.author.mention} z důvodu *{reason}* na {time}")
        await ctx.send(embed=muted_embed)
        await member.send(f" Byl jsi mutnut v: {guild.name} z důvodu *{reason}* na dobu {seconds}")
        await asyncio.sleep(seconds)
        await member.remove_roles(Muted)
        unmute_embed = discord.Embed(title="Konec mutu",description=f"{member.mention} byl unmutnut")
        await ctx.send(embed=unmute_embed)
        await member.send(f" Byl jsi unmutnut v: {guild.name}")


#ping
@bot.command(aliases=['Ping','PING'])
async def ping(ctx):
    await ctx.send('Pong! {0}ms'.format(round(bot.latency, 1)))

#Nastavení prefixu
@commands.has_guild_permissions(manage_messages=True)
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

#purge
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def purge(ctx, limit: int):
        await ctx.message.delete()
        await ctx.channel.purge(limit=limit)
        await ctx.send('Vymazáno {}'.format(ctx.author.mention))

@purge.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Nemůžeš tohle udělat")


#sudo
@commands.has_guild_permissions(administrator=True)
@bot.command(aliases=['Sudo','SUDO'])
async def sudo(ctx, *, arg):
    await ctx.send(arg)
    await ctx.message.delete()

#nemá oprávnění
@sudo.error
async def sudo_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Omlouvám se ale pro použití tohoto commandu potřebuješ mít opravnění **Administrator**.")

#support
@bot.command(aliases=['Support','SUPPORT'])
async def support(ctx):
    await ctx.send("Zde najdete moji podporu: https://dsc.gg/bluecat | https://discord.gg/43H2HxB3Ax")

#twitch
@bot.command(aliases=['Twitch','TWITCH'])
async def twitch(ctx):
    await ctx.send("Zde je twitch mého stvořitele: https://www.twitch.tv/bluecat201")

#unban
@bot.command(aliases=['ub','UNBAN','Unban'])
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


#warn
@bot.command()
@commands.has_permissions(administrator=True)
async def warn(ctx, member: discord.Member=None, *, reason=None):
    if member is None:
        return await ctx.send("Uživatel nebyl nalezen, nebo jste ho zapomněli zadat")
    
    if reason is None:
        return await ctx.send("Prosím, zadejte důvod warnu pro tohoto uživatele")

    try:
        first_warning = False
        bot.warnings[ctx.guild.id][member.id][0] += 1
        bot.warnings[ctx.guild.id][member.id][1].append((ctx.author.id, reason))
    
    except KeyError:
        first_warning = True
        bot.warnings[ctx.guild.id][member.id] = [1, [(ctx.author.id, reason)]]
    
    count = bot.warnings[ctx.guild.id][member.id][0]

    async with aiofiles.open(f"{ctx.guild.id}.txt", mode="a") as file:
        await file.write(f"{member.id} {ctx.author.id} {reason}\n")

    await ctx.send(f"{member.mention} has {count} {'warning' if first_warning else 'warnings'}.")
    
#warnings
@bot.command()
@commands.has_permissions(administrator=True)
async def warnings(ctx, member: discord.Member=None):
    if member is None:
        return await ctx.send("Uživatel nebyl nalezen, nebo jste ho zapomněli zadat")

    embed = discord.Embed(title=f"Warnings {member.name}",description="", colour=discord.Colour.red())
    try:
        i = 1
        for admin_id, reason in bot.warnings[ctx.guild.id][member.id][1]:
            admin = ctx.guild.get_member(admin_id)
            print(admin)
            embed.description += f"**Warning {i}** od: {admin.mention} z důvodu: *'{reason}'*.\n"
            i += 1

        await ctx.send(embed=embed)
    
    except KeyError: #no warnings
        await ctx.send("Tento uživatel nemá žádné warny") 

#|výstup do konzole|

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


#bot.ipc.start()
bot.run(TOKEN)
