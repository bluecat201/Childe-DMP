from quart import Quart, render_template, request, session, redirect, url_for
from quart_discord import DiscordOAuth2Session
from discord.ext import ipc

app = Quart(__name__)
ipc_client = ipc.Client(secret_key = "Bluecat")

app.config["SECRET_KEY"] = "test123"
app.config["DISCORD_CLIENT_ID"] = 883325865474269192
app.config["DISCORD_CLIENT_SECRET"] = ""
app.config["DISCORD_REDIRECT_URI"] = "http://127.0.0.1:5000/callback"

discord = DiscordOAuth2Session(app)

@app.route("/")
async def home():
    return await render_template("index.html", authorized = await discord.authorized)

@app.route("/css.css")
async def css():
    return await render_template("index.css")

@app.route("/login")
async def login():
    return await discord.create_session()


@app.route("/callback")
async def callback():
    try:
        await discord.callback()
    except Exception:
        pass

    return redirect(url_for("dashboard"))


@app.route("/dashboard")
async def dashboard():
    if not await discord.authorized:
        return redirect(url_for("login"))

    guild_count = await ipc_client.request("get_guild_count")
    guild_ids = await ipc_client.request("get_guild_ids")

    user_guilds = await discord.fetch_guilds()

    guilds = []
    for guild in user_guilds:
        if guild.permissions.administrator:
            guild.class_color = "blue-border" if guild.id in guild_ids else "grey-border"
            guilds.append(guild)

    guilds.sort(key = lambda x: x.class_color == "grey-border")
    name = (await discord.fetch_user()).name
    render_template("index.css")
    return await render_template("dashboard.html", guild_count = guild_count, guilds = guilds, username=name)

@app.route("/dashboard/<int:guild_id>")
async def dashboard_server(guild_id):
    if not await discord.authorized:
        return redirect(url_for("login"))

    guild = await ipc_client.request("get_guild", guild_id = guild_id)
    if guild is None:
	    return redirect(f'https://discord.com/oauth2/authorize?&client_id={app.config["DISCORD_CLIENT_ID"]}&scope=bot&permissions=8&guild_id={guild_id}&response_type=code&redirect_uri={app.config["DISCORD_REDIRECT_URI"]}')
    return guild["name"]

if __name__ == "__main__":
    app.run(debug=True)