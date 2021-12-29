import discord
import random
import logging
import json
import os
import asyncio
import aiofiles
from discord_buttons_plugin import *
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
from discord.ext import commands,tasks
from discord.ext.commands import has_permissions, CheckFailure


os.chdir("C:\\Users\\User\\Desktop\\škola\\DMP\\Childe-DMP")
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
bot.warnings = {} #guild_id : {member_id: [count, [(admin_id, reason)]]}
buttons = ButtonsClient(bot)
slash = SlashCommand(bot, sync_commands=True)


logging.basicConfig(level=logging.INFO)
TOKEN = ''

#Přihlášení do bota
@bot.event
async def on_ready():
    for guild in bot.guilds:
        bot.warnings[guild.id] = {}

        async with aiofiles.open(f"{guild.id}.txt", mode="a") as temp:
            pass


        async with aiofiles.open(f"{guild.id}.txt", mode="r") as file:
            lines = await file.readlines()

            for line in lines:
                data = line.split(" ")
                member_id = int(data[0])
                admin_id = int(data[1])
                reason = " ".join(data[2:]).strip("\n")

                try:
                    bot.warnings[guild.id][member_id][0] += 1
                    bot.warnings[guild.id][member_id][1].append((admin_id, reason))

                except KeyError:
                    bot.warnings[guild.id][member_id] = [1, [(admin_id, reason)]]

    await bot.change_presence(activity=discord.Streaming(name='Beta v0.2.3', url='https://www.twitch.tv/Bluecat201')) #status bota   
    print('Connected to bot: {}'.format(bot.user.name))
    print('Bot ID: {}'.format(bot.user.id))

@bot.event
async def on_guild_join(guild):
    bot.warnings[guild.id] = {}

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

#Economy

mainshop = [{"name":"Hodinky","price":100,"description":"Prostě hodinky"},
            {"name":"Laptop","price":1000,"description":"Laptop, co víc chceš vědět"},
            {"name":"PC","price":10000,"description":"Počítač na hraní her"}]

#balance
@bot.command(aliases=['bal'])
async def balance(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]

    em = discord.Embed(title = f"{ctx.author.name}'s balance",color = discord.Color.red())
    em.add_field(name = "Peněženka",value = wallet_amt)
    em.add_field(name = "Banka",value = bank_amt)
    await ctx.send(embed = em)

#beg
@bot.event
async def on_command_error(ctx,error):
    if isinstance(error, commands.CommandOnCooldown): #kontroluje jestli je na cooldownu
        msg = '**Stále máš cooldown**, prosím zkus to znovu za {:.2f}s'.format(error.retry_after)
        await ctx.send(msg)

@bot.command(aliases=['BEG','Beg'])
@commands.cooldown(1,60,commands.BucketType.user)

async def beg(ctx):
    await open_account(ctx.author)

    users = await get_bank_data()

    user = ctx.author

    earnings = random.randrange(101)

    await ctx.send(f"Někdo ti dal {earnings} korun!!")


    users[str(user.id)]["wallet"] += earnings

    with open("mainbank.json","w") as f:
        json.dump(users,f)

#withdraw
@bot.command(aliases=['with'])
async def withdraw(ctx,amount = None):
    await open_account(ctx.author)

    if amount == None:
        await ctx.send("Prosím zadejte množství")
        return
    
    bal = await update_bank(ctx.author)

    amount = int(amount)
    if amount>bal[1]:
        await ctx.send("Nemáte tolik peněz v bance")
        return
    if amount<0:
        await ctx.send("Hodnota nemůže být záporná")
        return
    
    await update_bank(ctx.author,amount)
    await update_bank(ctx.author,-1*amount,"bank")

    await ctx.send(f"Vybral jsi {amount} peněz")

#give
@bot.command(aliases=['Give','GIVE'])
async def give(ctx,member:discord.Member,amount = None):
    await open_account(ctx.author)
    await open_account(member)

    if amount == None:
        await ctx.send("Prosím zadejte množství")
        return
    
    bal = await update_bank(ctx.author)

    amount = int(amount)
    if amount>bal[1]:
        await ctx.send("Nemáte tolik peněz")
        return
    if amount<0:
        await ctx.send("Hodnota nemůže být záporná")
        return
    
    await update_bank(ctx.author,-1*amount,"bank")
    await update_bank(member,amount,"bank")

    await ctx.send(f"Dal jsi {amount} peněz")  

#rob
@bot.command(aliases=['Rob','ROB'])
async def rob(ctx,member:discord.Member):
    await open_account(ctx.author)
    await open_account(member)

    bal = await update_bank(member)

    if bal[0]<100:
        await ctx.send("Nevyplatí se to")
        return
    
    earnings = random.randrange(0, bal[0])

    await update_bank(ctx.author,earnings)
    await update_bank(member,-1*earnings)

    await ctx.send(f"Kradl jsi a získal jsi {earnings} peněz")  

#deposite
@bot.command(aliases=['dep'])
async def deposit(ctx,amount = None):
    await open_account(ctx.author)

    if amount == None:
        await ctx.send("Prosím zadejte množství")
        return
    
    bal = await update_bank(ctx.author)

    amount = int(amount)
    if amount>bal[0]:
        await ctx.send("Nemáte tolik peněz")
        return
    if amount<0:
        await ctx.send("Hodnota nemůže být záporná")
        return
    
    await update_bank(ctx.author,-1*amount)
    await update_bank(ctx.author,amount,"bank")

    await ctx.send(f"Uložil jsi {amount} peněz")  

#slots
@bot.command()
async def slots(ctx,amount = None):
    await open_account(ctx.author)

    if amount == None:
        await ctx.send("Prosím zadejte množství")
        return
    
    bal = await update_bank(ctx.author)

    amount = int(amount)
    if amount>bal[0]:
        await ctx.send("Nemáte tolik peněz")
        return
    if amount<0:
        await ctx.send("Hodnota nemůže být záporná")
        return
    
    final = []
    for i in range(3):
        a = random.choice(["X","O","Q"])

        final.append(a)
    await ctx.send(str(final))
    
    if final[0] == final[1] or final[0] == final[2] or final[2] == final[1]:
        await update_bank(ctx.author,2*amount)
        await ctx.send("Vyhrál jsi")
    else:
        await update_bank(ctx.author,-1*amount)
        await ctx.send("Prohrál jsi")

#shop
@bot.command()
async def shop(ctx):
    em = discord.Embed(title = "Shop")

    for item in mainshop:
        name = item["name"]
        price = item["price"]
        desc = item["description"]
        em.add_field(name = name, value = f"{price} | {desc}")
    
    await ctx.send(embed=em)

#buy
@bot.command()
async def buy(ctx,item,amount = 1):
    await open_account(ctx.author)

    res = await buy_this(ctx.author,item,amount)

    if not res[0]:
        if res[1]==1:
            await ctx.send("Tento předmět nemáme")
            return
        if res[1]==2:
            await ctx.send(f"Nemáš dostatek peněz v peněžence aby si koupil {amount} {item}")

#bag
@bot.command()
async def bag(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    try:
        bag = users[str(user.id)]["bag"]
    except:
        bag = []

    em = discord.Embed(title = "Bag")
    for item in bag:
        name = item["item"]
        amount = item["amount"]

        em.add_field(name = name, value = amount)

    await ctx.send(embed = em)

async def buy_this(user,item_name,amount):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break
    
    if name_ == None:
        return [False,1]

    cost = price*amount
    
    users = await get_bank_data()

    bal = await update_bank(user)

    if bal[0]<cost:
        return [False,2]
    
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
            index+=1
        if t == None:
            obj = {"item":item_name, "amount":amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item":item_name, "amount":amount}
        users[str(user.id)]["bag"] = [obj]

    with open("mainbank.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost*-1,"wallet")
    return [True,"Worked"]

async def open_account(user):
    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open("mainbank.json","w") as f:
        json.dump(users,f)
    return True

async def get_bank_data():
    with open("mainbank.json","r") as f:
        users = json.load(f)

    return users

async def update_bank(user,change = 0,mode = "wallet"):
    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open("mainbank.json","w") as f:
        json.dump(users,f)
    
    bal = [users[str(user.id)]["wallet"],users[str(user.id)]["bank"]]
    return bal

#NORMAL COMMANDS
#ban
@bot.command(aliases=['Ban','BAN'])
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

#bluecat
@bot.command(aliases=['Bluecat','BLUECAT'])
async def bluecat(ctx):
    nah = random.randint(1,20)
    await ctx.message.delete()
    embed=discord.Embed(color=0x0B0B45)
    file = discord.File(f"C:/Users/User/Desktop/škola/DMP/Childe-DMP/Bluecat/{nah}.gif", filename=f"image.gif")
    embed.set_image(url=f"attachment://image.gif")
    await ctx.send(file=file, embed=embed)

#d
@bot.command()
async def d(ctx):
    await ctx.send("<:cicisrdicko:849285560832360531>")

#help
@bot.command(aliases=['HELP','Help'])
async def help(ctx):
    embed=discord.Embed(title="Help",description="ban - Zabanování uživatele\n bluecat - random bluecat gif\n help - tohle\n info - Info o botovi\n invite - Invite na bota\n kick - kick uživatele\nmute - dá uživateli muted roli buď na nějakou dobu, nebo dokud nepoužije unmute\n ping - latence bota\n setprefix - Nastavení prefixu bota, jen pro **Administratory**\n sudo - mluvení za bota, jen pro **Administrátory**\n support - Invite na server majitele bota, kde najedete podporu bota\n twitch - Odkaz na twitch majitele\n unban - Unban uživatele\n unmute - odeberele uživately mute\n\n\n**Roleplay commands**\nbite,blush,bored,cry,cuddle,dance,facepalm,feed,happy,highfive,hug,kiss,laugh,pat,\npoke,pout,shrug,slap,sleep,smile,smug,stare,think,thumbsup,tickle,wave,wink\n\n\n **Slash commands**\n RPS - hra kámen, nůžky, papír s pc\n Linky - Odkazy na soc sítě majitele bota\n\n\n **Economy**\n balance - zobrazení účtu\nbeg - příjem peněz\n withdraw - vybrat peníze z banky\ngive - daruj někomu peníže\n rob - okraď někoho o peníze\n deposite - ulož peníze do banky\n slots - automaty\n shop - obchod s věcmi\n buy - kup nějakou věc z shopu\n bag - seznam vlastněných věcí", color=0x000000)
    await ctx.send(embed=embed)

#info
@bot.command(aliases=['Info','INFO'])
async def info(ctx):
    await ctx.send(f"Bot vzniká jako moje dlouhodobá maturitní práce :)\nDatum vydání první alpha verze: 5.9.2021 \nDatum vydání první beta verze: 30.9.2021\nPlánované vydaní plné verze bota: ||1.3 - 29.4.2022|| \nNaprogramováno v pythonu \nPokud máte jakékoliv poznámky, rady či nápady pro bota, můžete je napsat na !support server. ;)\nPočet serverů, na kterých jsem: {len(bot.guilds)}\nVerze bota: Beta 0.2.3 \nDeveloper: 𝓑𝓵𝓾𝓮𝓬𝓪𝓽#1973")

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
            embed.description += f"**Warning {i}** od: {admin.mention} z důvodu: *'{reason}'*.\n"
            i += 1

        await ctx.send(embed=embed)
    
    except KeyError: #no warnings
        await ctx.send("Tento uživatel nemá žádné warny") 

#|Roleplay|

#bite
@bot.command(aliases=['Bite','BITE'])
async def bite(ctx,member : discord.User = None):
    if member is None:
        await ctx.send('Musíš někoho označit/zadat ID')
    else:
        nah = random.randint(1,13)
        await ctx.message.delete()
        embed=discord.Embed(description=f"{ctx.author.mention} kouše {member.mention}",color=0xadd8e6)
        embed.set_image(url=f"https://nekos.best/public/bite/{nah:03}.gif")
        await ctx.send(embed=embed)

#blush
@bot.command(aliases=['Blush','BLUSH'])
async def blush(ctx):
    nah = random.randint(1,13)
    await ctx.message.delete()
    embed=discord.Embed(description=f"{ctx.author.mention} se červená",color=0xadd8e6)
    embed.set_image(url=f"https://nekos.best/public/blush/{nah:03}.gif")
    await ctx.send(embed=embed)

#bored
@bot.command(aliases=['Bored','BORED'])
async def bored(ctx):
    nah = random.randint(1,15)
    await ctx.message.delete()
    embed=discord.Embed(description=f"{ctx.author.mention} se nudí",color=0xadd8e6)
    embed.set_image(url=f"https://nekos.best/public/bored/{nah:03}.gif")
    await ctx.send(embed=embed)

#cry
@bot.command(aliases=['Cry','CRY'])
async def cry(ctx):
    nah = random.randint(1,40)
    await ctx.message.delete()
    embed=discord.Embed(description=f"{ctx.author.mention} brečí",color=0xadd8e6)
    embed.set_image(url=f"https://nekos.best/public/cry/{nah:03}.gif")
    await ctx.send(embed=embed)

#cuddle
@bot.command(aliases=['Cuddle','CUDDLE'])
async def cuddle(ctx,member : discord.User = None):
    if member is None:
        await ctx.send('Musíš někoho označit/zadat ID')
    else:
        nah = random.randint(1,28)
        await ctx.message.delete()
        embed=discord.Embed(description=f"{ctx.author.mention} se mazlí s {member.mention}",color=0xadd8e6)
        embed.set_image(url=f"https://nekos.best/public/cuddle/{nah:03}.gif")
        await ctx.send(embed=embed)

#dance
@bot.command(aliases=['Dance','DANCE'])
async def dance(ctx):
    nah = random.randint(1,21)
    await ctx.message.delete()
    embed=discord.Embed(description=f"{ctx.author.mention} tancuje",color=0xadd8e6)
    embed.set_image(url=f"https://nekos.best/public/dance/{nah:03}.gif")
    await ctx.send(embed=embed)

#facepalm
@bot.command(aliases=['Facepalm','FACEPALM'])
async def facepalm(ctx):
    nah = random.randint(1,11)
    await ctx.message.delete()
    embed=discord.Embed(description=f"{ctx.author.mention} facepalm",color=0xadd8e6)
    embed.set_image(url=f"https://nekos.best/public/facepalm/{nah:03}.gif")
    await ctx.send(embed=embed)

#feed
@bot.command(aliases=['Feed','FEED'])
async def feed(ctx,member : discord.User = None):
    if member is None:
        await ctx.send('Musíš někoho označit/zadat ID')
    else:
        nah = random.randint(1,23)
        await ctx.message.delete()
        embed=discord.Embed(description=f"{ctx.author.mention} krmí {member.mention}",color=0xadd8e6)
        embed.set_image(url=f"https://nekos.best/public/feed/{nah:03}.gif")
        await ctx.send(embed=embed)

#happy
@bot.command(aliases=['Happy','HAPPY'])
async def happy(ctx):
    nah = random.randint(1,12)
    await ctx.message.delete()
    embed=discord.Embed(description=f"{ctx.author.mention} je šťastný",color=0xadd8e6)
    embed.set_image(url=f"https://nekos.best/public/happy/{nah:03}.gif")
    await ctx.send(embed=embed)

#highfive
@bot.command(aliases=['Highfive','HIGHFIVE'])
async def highfive(ctx,member : discord.User = None):
    if member is None:
        await ctx.send('Musíš někoho označit/zadat ID')
    else:
        nah = random.randint(1,13)
        await ctx.message.delete()
        embed=discord.Embed(description=f"{ctx.author.mention} highfive {member.mention}",color=0xadd8e6)
        embed.set_image(url=f"https://nekos.best/public/highfive/{nah:03}.gif")
        await ctx.send(embed=embed)

#hug
@bot.command(aliases=['Hug','HUG'])
async def hug(ctx,member : discord.User = None):
    if member is None:
        await ctx.send('Musíš někoho označit/zadat ID')
    else:
        nah = random.randint(1,100)
        await ctx.message.delete()
        embed=discord.Embed(description=f"{ctx.author.mention} objímá {member.mention}", color=0xadd8e6)
        file = discord.File(f"C:/Users/User/Desktop/škola/DMP/Childe-DMP/hug/{nah}.gif", filename=f"image.gif")
        embed.set_image(url=f"attachment://image.gif")
        await ctx.send(file=file, embed=embed)

#kiss
@bot.command(aliases=['Kiss','KISS'])
async def kiss(ctx,member : discord.User = None):
    if member is None:
        await ctx.send('Musíš někoho označit/zadat ID')
    else:
        nah = random.randint(1,100)
        await ctx.message.delete()
        embed=discord.Embed(description=f"{ctx.author.mention} líbá {member.mention}", color=0xadd8e6)
        file = discord.File(f"C:/Users/User/Desktop/škola/DMP/Childe-DMP/kiss/{nah}.gif", filename=f"image.gif")
        embed.set_image(url=f"attachment://image.gif")
        await ctx.send(file=file, embed=embed)

#laugh
@bot.command(aliases=['Laugh','LAUGH'])
async def laugh(ctx):
    nah = random.randint(1,19)
    await ctx.message.delete()
    embed=discord.Embed(description=f"{ctx.author.mention} se směje",color=0xadd8e6)
    embed.set_image(url=f"https://nekos.best/public/laugh/{nah:03}.gif")
    await ctx.send(embed=embed)

#pat
@bot.command(aliases=['Pat','PAT'])
async def pat(ctx,member : discord.User = None):
    if member is None:
        await ctx.send('Musíš někoho označit/zadat ID')
    else:
        nah = random.randint(1,38)
        await ctx.message.delete()
        embed=discord.Embed(description=f"{ctx.author.mention} hladí {member.mention}",color=0xadd8e6)
        embed.set_image(url=f"https://nekos.best/public/pat/{nah:03}.gif")
        await ctx.send(embed=embed)

#poke
@bot.command(aliases=['Poke','POKE'])
async def poke(ctx,member : discord.User = None):
    if member is None:
        await ctx.send('Musíš někoho označit/zadat ID')
    else:
        nah = random.randint(1,21)
        await ctx.message.delete()
        embed=discord.Embed(description=f"{ctx.author.mention} strká {member.mention}",color=0xadd8e6)
        embed.set_image(url=f"https://nekos.best/public/poke/{nah:03}.gif")
        await ctx.send(embed=embed)

#pout
@bot.command(aliases=['Pout','POUT'])
async def pout(ctx):
    nah = random.randint(1,8)
    await ctx.message.delete()
    embed=discord.Embed(description=f"{ctx.author.mention} pout",color=0xadd8e6)
    embed.set_image(url=f"https://nekos.best/public/pout/{nah:03}.gif")
    await ctx.send(embed=embed)

#shrug
@bot.command(aliases=['Shrug','SHRUG'])
async def shrug(ctx):
    nah = random.randint(1,8)
    await ctx.message.delete()
    embed=discord.Embed(description=f"{ctx.author.mention} krčí rameny",color=0xadd8e6)
    embed.set_image(url=f"https://nekos.best/public/shrug/{nah:03}.gif")
    await ctx.send(embed=embed)

#slap
@bot.command(aliases=['Slap','SLAP'])
async def slap(ctx,member : discord.User = None):
    if member is None:
        await ctx.send('Musíš někoho označit/zadat ID')
    else:
        nah = random.randint(1,31)
        await ctx.message.delete()
        embed=discord.Embed(description=f"{ctx.author.mention} dává facku {member.mention}",color=0xadd8e6)
        embed.set_image(url=f"https://nekos.best/public/slap/{nah:03}.gif")
        await ctx.send(embed=embed)

#sleep
@bot.command(aliases=['Sleep','SLEEP'])
async def sleep(ctx):
    nah = random.randint(1,12)
    await ctx.message.delete()
    embed=discord.Embed(description=f"{ctx.author.mention} spí",color=0xadd8e6)
    embed.set_image(url=f"https://nekos.best/public/sleep/{nah:03}.gif")
    await ctx.send(embed=embed)

#smile
@bot.command(aliases=['Smile','SMILE'])
async def smile(ctx):
    nah = random.randint(1,23)
    await ctx.message.delete()
    embed=discord.Embed(description=f"{ctx.author.mention} usmívá se",color=0xadd8e6)
    embed.set_image(url=f"https://nekos.best/public/smile/{nah:03}.gif")
    await ctx.send(embed=embed)

#smug
@bot.command(aliases=['Smug','SMUG'])
async def smug(ctx):
    nah = random.randint(1,15)
    await ctx.message.delete()
    embed=discord.Embed(description=f"{ctx.author.mention} smug",color=0xadd8e6)
    embed.set_image(url=f"https://nekos.best/public/smug/{nah:03}.gif")
    await ctx.send(embed=embed)

#stare
@bot.command(aliases=['Stare','STARE'])
async def stare(ctx,member : discord.User = None):
    if member is None:
        await ctx.send('Musíš někoho označit/zadat ID')
    else:
        nah = random.randint(1,14)
        await ctx.message.delete()
        embed=discord.Embed(description=f"{ctx.author.mention} civí na {member.mention}",color=0xadd8e6)
        embed.set_image(url=f"https://nekos.best/public/stare/{nah:03}.gif")
        await ctx.send(embed=embed)

#think
@bot.command(aliases=['Think','THINK'])
async def think(ctx):
    nah = random.randint(1,11)
    await ctx.message.delete()
    embed=discord.Embed(description=f"{ctx.author.mention} přemýšlí",color=0xadd8e6)
    embed.set_image(url=f"https://nekos.best/public/think/{nah:03}.gif")
    await ctx.send(embed=embed)

#thumbsup
@bot.command(aliases=['Thumbsup','THUMBSUP'])
async def thumbsup(ctx):
    nah = random.randint(1,16)
    await ctx.message.delete()
    embed=discord.Embed(description=f"{ctx.author.mention} thumbsup",color=0xadd8e6)
    embed.set_image(url=f"https://nekos.best/public/thumbsup/{nah:03}.gif")
    await ctx.send(embed=embed)

#tickle
@bot.command(aliases=['Tickle','TICKLE'])
async def tickle(ctx,member : discord.User = None):
    if member is None:
        await ctx.send('Musíš někoho označit/zadat ID')
    else:
        nah = random.randint(1,21)
        await ctx.message.delete()
        embed=discord.Embed(description=f"{ctx.author.mention} lechtá {member.mention}",color=0xadd8e6)
        embed.set_image(url=f"https://nekos.best/public/tickle/{nah:03}.gif")
        await ctx.send(embed=embed)

#wave
@bot.command(aliases=['Wave','WAVE'])
async def wave(ctx):
    nah = random.randint(1,27)
    await ctx.message.delete()
    embed=discord.Embed(description=f"{ctx.author.mention} mává",color=0xadd8e6)
    embed.set_image(url=f"https://nekos.best/public/wave/{nah:03}.gif")
    await ctx.send(embed=embed)

#wink
@bot.command(aliases=['Wink','WINK'])
async def wink(ctx):
    nah = random.randint(1,15)
    await ctx.message.delete()
    embed=discord.Embed(description=f"{ctx.author.mention} mrká",color=0xadd8e6)
    embed.set_image(url=f"https://nekos.best/public/wink/{nah:03}.gif")
    await ctx.send(embed=embed)
  
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

bot.run(TOKEN)