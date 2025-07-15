import discord
import json
import os
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
    with open("commands.json", "r") as f:
        return json.load(f)

# Save custom commands to JSON
def save_custom_commands(commands_data):
    with open("commands.json", "w") as f:
        json.dump(commands_data, f, indent=4)

@bot.event
async def on_ready():
    print(f"Nova Bot is online as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    custom_commands = load_custom_commands()
    content = message.content.lower()

    if content in custom_commands:
        await message.channel.send(custom_commands[content])
    else:
        await bot.process_commands(message)

# List custom commands
@bot.command(name="commandslist")
async def commandslist(ctx):
    commands = load_custom_commands()
    if not commands:
        await ctx.send("No custom commands have been set.")
        return
    msg = "**Custom Commands:**\n" + "\n".join([f"`{cmd}` ➜ {resp}" for cmd, resp in commands.items()])
    await ctx.send(msg)

# Add custom command (admin only)
@bot.command(name="addcmd")
@commands.has_permissions(administrator=True)
async def addcmd(ctx, name: str, *, response: str):
    commands = load_custom_commands()
    commands[name.lower()] = response
    save_custom_commands(commands)
    await ctx.send(f"✅ Added command `{name}`")

# Delete custom command (admin only)
@bot.command(name="delcmd")
@commands.has_permissions(administrator=True)
async def delcmd(ctx, name: str):
    commands = load_custom_commands()
    if name.lower() in commands:
        del commands[name.lower()]
        save_custom_commands(commands)
        await ctx.send(f"🗑️ Deleted command `{name}`")
    else:
        await ctx.send("⚠️ Command not found.")

# Kick command (kick_members permission)
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    try:
        await member.kick(reason=reason)
        await ctx.send(f"👢 Kicked {member.mention} | Reason: {reason}")
    except discord.Forbidden:
        await ctx.send("I don't have permission to kick that user.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

# Ban command (ban_members permission)
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    try:
        await member.ban(reason=reason)
        await ctx.send(f"🔨 Banned {member.mention} | Reason: {reason}")
    except discord.Forbidden:
        await ctx.send("I don't have permission to ban that user.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

# Purge command (manage_messages permission)
@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int = 10):
    try:
        deleted = await ctx.channel.purge(limit=amount)
        await ctx.send(f"🧹 Purged {len(deleted)} messages.", delete_after=3)
    except discord.Forbidden:
        await ctx.send("I don't have permission to delete messages.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

bot.run(TOKEN)

