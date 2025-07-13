import discord, json, os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix="n!", intents=intents)

# Load commands from JSON
def load_custom_commands():
    if not os.path.exists("commands.json"):
        return {}
    with open("commands.json") as f:
        return json.load(f)

# Save custom commands to JSON
def save_custom_commands(commands_data):
    with open("commands.json", "w") as f:
        json.dump(commands_data, f, indent=4)

@bot.event
async def on_ready():
    print(f" Nova Bot is online as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    custom_commands = load_custom_commands()
    content = message.content.lower()

    if content in custom_commands:
        await message.channel.send(custom_commands[content])
        return

    await bot.process_commands(message)

# Command to list current custom commands
@bot.command()
async def commandslist(ctx):
    commands = load_custom_commands()
    if not commands:
        await ctx.send("No custom commands have been set.")
        return
    msg = "**Custom Commands:**\n" + "\n".join([f"`{cmd}` ➜ {resp}" for cmd, resp in commands.items()])
    await ctx.send(msg)

# Command to add custom command (admin only)
@bot.command()
@commands.has_permissions(administrator=True)
async def addcmd(ctx, name: str, *, response: str):
    commands = load_custom_commands()
    commands[name.lower()] = response
    save_custom_commands(commands)
    await ctx.send(f"✅ Added command `{name}`")

# Command to delete custom command
@bot.command()
@commands.has_permissions(administrator=True)
async def delcmd(ctx, name: str):
    commands = load_custom_commands()
    if name.lower() in commands:
        del commands[name.lower()]
        save_custom_commands(commands)
        await ctx.send(f"🗑️ Deleted command `{name}`")
    else:
        await ctx.send("⚠️ Command not found.")

# Basic moderation commands
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.kick(reason=reason)
    await ctx.send(f"👢 Kicked {member.mention} | Reason: {reason}")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 Banned {member.mention} | Reason: {reason}")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int = 10):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f" Purged {amount} messages", delete_after=3)

bot.run(TOKEN)
