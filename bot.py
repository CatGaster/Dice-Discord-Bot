import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os

from bot_modules.character import setup_character_commands
from bot_modules.dice import setup_dice_commands
from bot_modules.clear import setup_clear_commands
from bot_modules.wise_wizard import setup_wise_wizard

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Функция для регистрации слэш-команд
async def register_slash_commands(bot):
    await bot.tree.sync()
    print("Слэш-команды успешно зарегистрированы.")

# Регистрируем все команды бота
setup_character_commands(bot)
setup_dice_commands(bot)
setup_clear_commands(bot)
setup_wise_wizard(bot)


@bot.event
async def on_ready():
    print(f"Бот {bot.user.name} успешно запущен!")
    await register_slash_commands(bot)

if __name__ == "__main__":
    bot.run(TOKEN)
