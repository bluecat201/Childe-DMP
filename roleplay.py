import discord
from discord.ext import commands
import aiohttp

class Roleplay(commands.Cog, name="Roleplay"):
    """Příkazy pro roleplay interakce s ostatními uživateli."""

    def __init__(self, bot):
        self.bot = bot

    # Obecná funkce pro příkazy
    async def fetch_neko_action(self, ctx, description, endpoint, member=None):
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

    # Bite
    @commands.command(aliases=['Bite', 'BITE'], help="Kousne označeného uživatele.")
    async def bite(self, ctx, member: discord.User = None):
        if member is None:
            await ctx.send("Musíš někoho označit/zadat ID")
        else:
            description = f"{ctx.author.mention} kouše {member.mention}"
            await self.fetch_neko_action(ctx, description, "bite")

    #blush
    @commands.command(aliases=['Blush', 'BLUSH'], help="Začervenáš se")
    async def blush(self, ctx):
        description = f"{ctx.author.mention} se červená"
        await self.fetch_neko_action(ctx, description, "blush")

    #bored
    @commands.command(aliases=['Bored','BORED'], help='Nudíš se')
    async def bored(self, ctx):
        description = f"{ctx.author.mention} se nudí"
        await self.fetch_neko_action(ctx, description, "bored")

    #cry
    @commands.command(aliases=['Cry','CRY'], help='Brečíš')
    async def cry(self, ctx):
        description = f"{ctx.author.mention} brečí"
        await self.fetch_neko_action(ctx, description, "cry")

    #cuddle
    @commands.command(aliases=['Cuddle', 'CUDDLE'], help='Mazlíš se s označeným uživatelem')
    async def cuddle(self, ctx, member: discord.User = None):
        if member is None:
            await ctx.send("Musíš někoho označit/zadat ID")
        else:
            description = f"{ctx.author.mention} se mazlí s {member.mention}"
            await self.fetch_neko_action(ctx, description, "cuddle")

    #dance
    @commands.command(aliases=['Dance', 'DANCE'], help="Tancuješ")
    async def dance(self, ctx):
        description = f"{ctx.author.mention} tancuje"
        await self.fetch_neko_action(ctx, description, "dance")

    #facepalm
    @commands.command(aliases=['Facepalm','FACEPALM'], help="Dáváš si facepalm")
    async def facepalm(self, ctx):
        description = f"{ctx.author.mention} si dává facepalm"
        await self.fetch_neko_action(ctx, description, "facepalm")

    #feed
    @commands.command(aliases=['Feed','FEED'], help='Krmíš označeného uživatele')
    async def feed(self, ctx,member : discord.User = None):
        if member is None:
            await ctx.send("Musíš někoho označit/zadat ID")
        else:
            description = f"{ctx.author.mention} krmí {member.mention}"
            await self.fetch_neko_action(ctx, description, "feed")

    #happy
    @commands.command(aliases=['Happy','HAPPY'], help='Jseš šťastný')
    async def happy(self, ctx):
        description = f"{ctx.author.mention} je šťastný"
        await self.fetch_neko_action(ctx, description, "happy")

    #highfive
    @commands.command(aliases=['Highfive','HIGHFIVE'], help='Dáváš si placáka s označeným uživatelem')
    async def highfive(self, ctx,member : discord.User = None):
        if member is None:
            await ctx.send("Musíš někoho označit/zadat ID")
        else:
            description = f"{ctx.author.mention} si dává placáka s {member.mention}"
            await self.fetch_neko_action(ctx, description, "highfive")

    # Hug
    @commands.command(aliases=['Hug', 'HUG'], help="Objímá označeného uživatele.")
    async def hug(self, ctx, member: discord.User = None):
        if member is None:
            await ctx.send("Musíš někoho označit/zadat ID")
        else:
            description = f"{ctx.author.mention} objímá {member.mention}"
            await self.fetch_neko_action(ctx, description, "hug")

    # Kiss
    @commands.command(aliases=['Kiss', 'KISS'], help="Líbá označeného uživatele.")
    async def kiss(self, ctx, member: discord.User = None):
        if member is None:
            await ctx.send("Musíš někoho označit/zadat ID")
        else:
            description = f"{ctx.author.mention} líbá {member.mention}"
            await self.fetch_neko_action(ctx, description, "kiss")

    #laugh
    @commands.command(aliases=['Laugh','LAUGH'], help='Směješ se')
    async def laugh(self, ctx):
        description = f"{ctx.author.mention} se směje"
        await self.fetch_neko_action(ctx, description, "laugh")

    #pat
    @commands.command(aliases=['Pat','PAT'], help='Hladíš označeného uživatele')
    async def pat(self, ctx,member : discord.User = None):
        if member is None:
            await ctx.send("Musíš někoho označit/zadat ID")
        else:
            description = f"{ctx.author.mention} hladí {member.mention}"
            await self.fetch_neko_action(ctx, description, "pat")

    #poke
    @commands.command(aliases=['Poke','POKE'], help='Strkáš označeného uživatele')
    async def poke(self, ctx,member : discord.User = None):
        if member is None:
            await ctx.send("Musíš někoho označit/zadat ID")
        else:
            description = f"{ctx.author.mention} strká {member.mention}"
            await self.fetch_neko_action(ctx, description, "poke")

    #pout
    @commands.command(aliases=['Pout','POUT'], help='Mračíš se')
    async def pout(self, ctx):
        description = f"{ctx.author.mention} se mračí"
        await self.fetch_neko_action(ctx, description, "pout")

    #shrug
    @commands.command(aliases=['Shrug','SHRUG'], help='Krčíš rameny')
    async def shrug(self, ctx):
        description = f"{ctx.author.mention} krčí rameny"
        await self.fetch_neko_action(ctx, description, "shrug")

    #slap
    @commands.command(aliases=['Slap', 'SLAP'], help='Daváš facku označenému uživately')
    async def slap(self, ctx, member: discord.User = None):
        if member is None:
            await ctx.send("Musíš někoho označit/zadat ID")
        else:
            description = f"{ctx.author.mention} dává facku {member.mention}"
            await self.fetch_neko_action(ctx, description, "slap")

    #sleep
    @commands.command(aliases=['Sleep','SLEEP'], help='spíš')
    async def sleep(self, ctx):
        description = f"{ctx.author.mention} spí"
        await self.fetch_neko_action(ctx, description, "sleep")

    #smile
    @commands.command(aliases=['Smile','SMILE'], help='Usmíváš se')
    async def smile(self, ctx):
        description = f"{ctx.author.mention} usmívá se"
        await self.fetch_neko_action(ctx, description, "smile")

    #smug
    @commands.command(aliases=['Smug','SMUG'], help='Jseš samolibý')
    async def smug(self, ctx):
        description = f"{ctx.author.mention} je samolibý"
        await self.fetch_neko_action(ctx, description, "smug")

    #stare
    @commands.command(aliases=['Stare','STARE'], help='Civíš na označeného uživatele')
    async def stare(self, ctx,member : discord.User = None):
        if member is None:
            await ctx.send("Musíš někoho označit/zadat ID")
        else:
            description = f"{ctx.author.mention} civí na {member.mention}"
            await self.fetch_neko_action(ctx, description, "stare")

    #think
    @commands.command(aliases=['Think','THINK'], help='Přemýšlíš')
    async def think(self, ctx):
        description = f"{ctx.author.mention} přemýšlí"
        await self.fetch_neko_action(ctx, description, "think")

    #thumbsup
    @commands.command(aliases=['Thumbsup','THUMBSUP'], help='Dáváš palec nahoru')
    async def thumbsup(self, ctx):
        description = f"{ctx.author.mention} dává palec nahoru"
        await self.fetch_neko_action(ctx, description, "thumbsup")

    #tickle
    @commands.command(aliases=['Tickle','TICKLE'], help='Lechtáš označeného uživatele')
    async def tickle(self, ctx,member : discord.User = None):
        if member is None:
            await ctx.send("Musíš někoho označit/zadat ID")
        else:
            description = f"{ctx.author.mention} lechtá {member.mention}"
            await self.fetch_neko_action(ctx, description, "tickle")

    #wave
    @commands.command(aliases=['Wave','WAVE'], help='Máváš')
    async def wave(self, ctx):
        description = f"{ctx.author.mention} mává"
        await self.fetch_neko_action(ctx, description, "wave")

    #wink
    @commands.command(aliases=['Wink','WINK'], help='Mrkáš')
    async def wink(self, ctx):
        description = f"{ctx.author.mention} mrká"
        await self.fetch_neko_action(ctx, description, "wink")
  
