import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from character import setup_character_commands
from dice import setup_dice_commands

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Set up commands for character and dice
setup_character_commands(bot)
setup_dice_commands(bot)

# Start the bot
if __name__ == "__main__":
    bot.run(TOKEN)