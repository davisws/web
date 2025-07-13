import discord, json, os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is ready: {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot: return
    if not os.path.exists("commands.json"): return
    with open("commands.json") as f:
        cmds = json.load(f)
    if message.content in cmds:
        await message.channel.send(cmds[message.content])
    await bot.process_commands(message)

bot.run(TOKEN)
