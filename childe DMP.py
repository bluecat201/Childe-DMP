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
# Example shop
mainshop = [{"name": "Hodinky", "price": 100, "description": "Prostě hodinky"},
            {"name": "Laptop", "price": 1000, "description": "Laptop, co víc chceš vědět"},
            {"name": "PC", "price": 10000, "description": "Počítač na hraní her"}]

# Balance command
@bot.command(aliases=['bal'])
async def balance(ctx, member: discord.Member = None):
    if member is None:
        await open_account(ctx.author)
        user = ctx.author
        users = await get_bank_data()
        wallet_amt = users[str(user.id)]["wallet"]
        bank_amt = users[str(user.id)]["bank"]
        em = discord.Embed(title=f"{ctx.author.name}'s balance", color=discord.Color.red())
        em.add_field(name="Peněženka", value=wallet_amt)
        em.add_field(name="Banka", value=bank_amt)
        await ctx.send(embed=em)
    else:
        await open_account(member)
        user = member
        users = await get_bank_data()
        wallet_amt = users[str(user.id)]["wallet"]
        bank_amt = users[str(user.id)]["bank"]
        em = discord.Embed(title=f"{member.name}'s balance", color=discord.Color.red())
        em.add_field(name="Peněženka", value=wallet_amt)
        em.add_field(name="Banka", value=bank_amt)
        await ctx.send(embed=em)

# Beg command
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        cd = round(error.retry_after)
        minutes = str(cd // 60)
        seconds = str(cd % 60)
        msg = f'**Stále máš cooldown**, prosím zkus to znovu za {minutes}min a {seconds}s'
        await ctx.send(msg)

@bot.command(aliases=['BEG', 'Beg'])
@commands.cooldown(1, 3600, commands.BucketType.user)
async def beg(ctx):
    await open_account(ctx.author)
    users = await get_bank_data()
    user = ctx.author
    earnings = random.randrange(101)
    await ctx.send(f"Někdo ti dal {earnings} korun!!")
    users[str(user.id)]["wallet"] += earnings
    with open("mainbank.json", "w") as f:
        json.dump(users, f)

# Withdraw command
@bot.command(aliases=['with'])
async def withdraw(ctx, amount: int = None):
    await open_account(ctx.author)
    if amount is None:
        await ctx.send("Prosím zadejte množství")
        return
    bal = await update_bank(ctx.author)
    if amount > bal[1]:
        await ctx.send("Nemáte tolik peněz v bance")
        return
    if amount < 0:
        await ctx.send("Hodnota nemůže být záporná")
        return
    await update_bank(ctx.author, amount)
    await update_bank(ctx.author, -amount, "bank")
    await ctx.send(f"Vybral jsi {amount} peněz")

# Give command
@bot.command(aliases=['Give', 'GIVE'])
async def give(ctx, member: discord.Member, amount: int = None):
    await open_account(ctx.author)
    await open_account(member)
    if amount is None:
        await ctx.send("Prosím zadejte množství")
        return
    bal = await update_bank(ctx.author)
    if amount > bal[1]:
        await ctx.send("Nemáte tolik peněz")
        return
    if amount < 0:
        await ctx.send("Hodnota nemůže být záporná")
        return
    await update_bank(ctx.author, -amount, "bank")
    await update_bank(member, amount, "bank")
    await ctx.send(f"Dal jsi {amount} peněz")  

# Rob command
@bot.command(aliases=['ROB', 'Rob'])
@commands.cooldown(1, 60, commands.BucketType.user)
async def rob(ctx, member: discord.Member):
    await open_account(ctx.author)
    await open_account(member)
    bal = await update_bank(member)
    if bal[0] < 100:
        await ctx.send("Nevyplatí se to")
        return
    earnings = random.randrange(0, bal[0])
    await update_bank(ctx.author, earnings)
    await update_bank(member, -earnings)
    await ctx.send(f"Kradl jsi a získal jsi {earnings} peněz")

# Deposit command
@bot.command(aliases=['dep'])
async def deposit(ctx, amount: int = None):
    await open_account(ctx.author)
    if amount is None:
        await ctx.send("Prosím zadejte množství")
        return
    bal = await update_bank(ctx.author)
    if amount > bal[0]:
        await ctx.send("Nemáte tolik peněz")
        return
    if amount < 0:
        await ctx.send("Hodnota nemůže být záporná")
        return
    await update_bank(ctx.author, -amount)
    await update_bank(ctx.author, amount, "bank")
    await ctx.send(f"Uložil jsi {amount} peněz")

# Slots command
@bot.command()
async def slots(ctx, amount: int = None):
    await open_account(ctx.author)
    if amount is None:
        await ctx.send("Prosím zadejte množství")
        return
    bal = await update_bank(ctx.author)
    if amount > bal[0]:
        await ctx.send("Nemáte tolik peněz")
        return
    if amount < 0:
        await ctx.send("Hodnota nemůže být záporná")
        return
    final = [random.choice(["X", "O", "Q"]) for _ in range(3)]
    await ctx.send(str(final))
    if final[0] == final[1] and final[1] == final[2]:
        await update_bank(ctx.author, 2 * amount)
        await ctx.send("Vyhrál jsi")
    else:
        await update_bank(ctx.author, -amount)
        await ctx.send("Prohrál jsi")

# Shop command
@bot.command()
async def shop(ctx):
    em = discord.Embed(title="Shop")
    for item in mainshop:
        name = item["name"]
        price = item["price"]
        desc = item["description"]
        em.add_field(name=name, value=f"{price} | {desc}")
    await ctx.send(embed=em)

# Buy command
@bot.command()
async def buy(ctx, item: str, amount: int = 1):
    await open_account(ctx.author)
    res = await buy_this(ctx.author, item, amount)
    if not res[0]:
        if res[1] == 1:
            await ctx.send("Tento předmět nemáme")
        elif res[1] == 2:
            await ctx.send(f"Nemáš dostatek peněz v peněžence aby si koupil {amount} {item}")

# Bag command
@bot.command()
async def bag(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()
    bag = users.get(str(user.id), {}).get("bag", [])
    em = discord.Embed(title="Bag")
    for item in bag:
        name = item["item"]
        amount = item["amount"]
        em.add_field(name=name, value=amount)
    await ctx.send(embed=em)

# Helper function for buying items
async def buy_this(user, item_name, amount):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break
    if name_ is None:
        return [False, 1]
    cost = price * amount
    users = await get_bank_data()
    bal = await update_bank(user)
    if bal[0] < cost:
        return [False, 2]
    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index += 1
        if t is None:
            obj = {"item": item_name, "amount": amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item": item_name, "amount": amount}
        users[str(user.id)]["bag"] = [obj]
    with open("mainbank.json", "w") as f:
        json.dump(users, f)
    await update_bank(user, -cost, "wallet")
    return [True, "Worked"]

# Helper function for creating accounts
async def open_account(user):
    users = await get_bank_data()
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {"wallet": 0, "bank": 0, "bag": []}
    with open("mainbank.json", "w") as f:
        json.dump(users, f)
    return True

# Helper function for getting bank data
async def get_bank_data():
    with open("mainbank.json", "r") as f:
        return json.load(f)

# Helper function for updating bank balances
async def update_bank(user, change=0, mode="wallet"):
    users = await get_bank_data()
    users[str(user.id)][mode] += change
    with open("mainbank.json", "w") as f:
        json.dump(users, f)
    return [users[str(user.id)]["wallet"], users[str(user.id)]["bank"]]


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

#|Roleplay|

# Obecná funkce pro příkazy
async def fetch_neko_action(ctx, description, endpoint, member=None):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://nekos.best/api/v2/{endpoint}") as resp:
            if resp.status == 200:
                data = await resp.json()
                image_url = data["results"][0]["url"]
                embed = discord.Embed(description=description, color=0xadd8e6)
                embed.set_image(url=image_url)
                await ctx.message.delete()
                await ctx.send(embed=embed)
            else:
                await ctx.send("Nepodařilo se získat data z API. Zkuste to prosím znovu.")

#bite
@bot.command(aliases=['Bite', 'BITE'])
async def bite(ctx, member: discord.User = None):
    if member is None:
        await ctx.send("Musíš někoho označit/zadat ID")
    else:
        description = f"{ctx.author.mention} kouše {member.mention}"
        await fetch_neko_action(ctx, description, "bite")

#blush
@bot.command(aliases=['Blush', 'BLUSH'])
async def blush(ctx):
    description = f"{ctx.author.mention} se červená"
    await fetch_neko_action(ctx, description, "blush")

#bored
@bot.command(aliases=['Bored','BORED'])
async def bored(ctx):
    description = f"{ctx.author.mention} se nudí"
    await fetch_neko_action(ctx, description, "bored")

#cry
@bot.command(aliases=['Cry','CRY'])
async def cry(ctx):
    description = f"{ctx.author.mention} brečí"
    await fetch_neko_action(ctx, description, "cry")

#cuddle
@bot.command(aliases=['Cuddle', 'CUDDLE'])
async def cuddle(ctx, member: discord.User = None):
    if member is None:
        await ctx.send("Musíš někoho označit/zadat ID")
    else:
        description = f"{ctx.author.mention} se mazlí s {member.mention}"
        await fetch_neko_action(ctx, description, "cuddle")

#dance
async def dance(ctx):
    description = f"{ctx.author.mention} tancuje"
    await fetch_neko_action(ctx, description, "dance")

#facepalm
@bot.command(aliases=['Facepalm','FACEPALM'])
async def facepalm(ctx):
    description = f"{ctx.author.mention} si dává facepalm"
    await fetch_neko_action(ctx, description, "facepalm")

#feed
@bot.command(aliases=['Feed','FEED'])
async def feed(ctx,member : discord.User = None):
    if member is None:
        await ctx.send("Musíš někoho označit/zadat ID")
    else:
        description = f"{ctx.author.mention} krmí {member.mention}"
        await fetch_neko_action(ctx, description, "feed")

#happy
@bot.command(aliases=['Happy','HAPPY'])
async def happy(ctx):
    description = f"{ctx.author.mention} je šťastný"
    await fetch_neko_action(ctx, description, "happy")

#highfive
@bot.command(aliases=['Highfive','HIGHFIVE'])
async def highfive(ctx,member : discord.User = None):
    if member is None:
        await ctx.send("Musíš někoho označit/zadat ID")
    else:
        description = f"{ctx.author.mention} si dává highfive s {member.mention}"
        await fetch_neko_action(ctx, description, "highfive")

#hug
@bot.command(aliases=['Hug','HUG'])
async def hug(ctx,member : discord.User = None):
    if member is None:
        await ctx.send("Musíš někoho označit/zadat ID")
    else:
        description = f"{ctx.author.mention} objímá {member.mention}"
        await fetch_neko_action(ctx, description, "hug")

#kiss
@bot.command(aliases=['Kiss','KISS'])
async def kiss(ctx,member : discord.User = None):
    if member is None:
        await ctx.send("Musíš někoho označit/zadat ID")
    else:
        description = f"{ctx.author.mention} líbá {member.mention}"
        await fetch_neko_action(ctx, description, "kiss")

#laugh
@bot.command(aliases=['Laugh','LAUGH'])
async def laugh(ctx):
    description = f"{ctx.author.mention} se směje"
    await fetch_neko_action(ctx, description, "laugh")

#pat
@bot.command(aliases=['Pat','PAT'])
async def pat(ctx,member : discord.User = None):
    if member is None:
        await ctx.send("Musíš někoho označit/zadat ID")
    else:
        description = f"{ctx.author.mention} hladí {member.mention}"
        await fetch_neko_action(ctx, description, "pat")

#poke
@bot.command(aliases=['Poke','POKE'])
async def poke(ctx,member : discord.User = None):
    if member is None:
        await ctx.send("Musíš někoho označit/zadat ID")
    else:
        description = f"{ctx.author.mention} strká {member.mention}"
        await fetch_neko_action(ctx, description, "poke")

#pout
@bot.command(aliases=['Pout','POUT'])
async def pout(ctx):
    description = f"{ctx.author.mention} se mračí"
    await fetch_neko_action(ctx, description, "pout")

#shrug
@bot.command(aliases=['Shrug','SHRUG'])
async def shrug(ctx):
    description = f"{ctx.author.mention} krčí rameny"
    await fetch_neko_action(ctx, description, "shrug")

#slap
@bot.command(aliases=['Slap', 'SLAP'])
async def slap(ctx, member: discord.User = None):
    if member is None:
        await ctx.send("Musíš někoho označit/zadat ID")
    else:
        description = f"{ctx.author.mention} dává facku {member.mention}"
        await fetch_neko_action(ctx, description, "slap")

#sleep
@bot.command(aliases=['Sleep','SLEEP'])
async def sleep(ctx):
    description = f"{ctx.author.mention} spí"
    await fetch_neko_action(ctx, description, "sleep")

#smile
@bot.command(aliases=['Smile','SMILE'])
async def smile(ctx):
    description = f"{ctx.author.mention} usmívá se"
    await fetch_neko_action(ctx, description, "smile")

#smug
@bot.command(aliases=['Smug','SMUG'])
async def smug(ctx):
    description = f"{ctx.author.mention} je samolibý"
    await fetch_neko_action(ctx, description, "smug")

#stare
@bot.command(aliases=['Stare','STARE'])
async def stare(ctx,member : discord.User = None):
    if member is None:
        await ctx.send("Musíš někoho označit/zadat ID")
    else:
        description = f"{ctx.author.mention} civí na {member.mention}"
        await fetch_neko_action(ctx, description, "stare")

#think
@bot.command(aliases=['Think','THINK'])
async def think(ctx):
    description = f"{ctx.author.mention} přemýšlí"
    await fetch_neko_action(ctx, description, "think")

#thumbsup
@bot.command(aliases=['Thumbsup','THUMBSUP'])
async def thumbsup(ctx):
    description = f"{ctx.author.mention} dává palec nahoru"
    await fetch_neko_action(ctx, description, "thumbsup")

#tickle
@bot.command(aliases=['Tickle','TICKLE'])
async def tickle(ctx,member : discord.User = None):
    if member is None:
        await ctx.send("Musíš někoho označit/zadat ID")
    else:
        description = f"{ctx.author.mention} lechtá {member.mention}"
        await fetch_neko_action(ctx, description, "tickle")

#wave
@bot.command(aliases=['Wave','WAVE'])
async def wave(ctx):
    description = f"{ctx.author.mention} mává"
    await fetch_neko_action(ctx, description, "wave")

#wink
@bot.command(aliases=['Wink','WINK'])
async def wink(ctx):
    description = f"{ctx.author.mention} mrká"
    await fetch_neko_action(ctx, description, "wink")
  
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