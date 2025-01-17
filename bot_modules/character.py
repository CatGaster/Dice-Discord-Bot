import discord
from discord.ext import commands
from discord.ui import Button, View, Modal, TextInput
from discord import app_commands
import sqlite3

# Инициализация базы данных
DB_FILE = "user_stats.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS user_stats (
            user_id TEXT PRIMARY KEY,
            strength INTEGER DEFAULT 0,
            dexterity INTEGER DEFAULT 0,
            constitution INTEGER DEFAULT 0,
            wisdom INTEGER DEFAULT 0,
            charisma INTEGER DEFAULT 0,
            intelligence INTEGER DEFAULT 0
        )
        """
    )
    conn.commit()
    conn.close()

# Функции для работы с базой данных
def get_user_stats(user_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_stats WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "Сила": row[1],
            "Ловкость": row[2],
            "Стойкость": row[3],
            "Мудрость": row[4],
            "Харизма": row[5],
            "Интеллект": row[6],
        }
    else:
        return {"Сила": 0, "Ловкость": 0, "Стойкость": 0, "Мудрость": 0, "Харизма": 0, "Интеллект": 0}

def set_user_stat(user_id, stat_name, value):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO user_stats (user_id, strength, dexterity, constitution, wisdom, charisma, intelligence)
        VALUES (?, 0, 0, 0, 0, 0, 0)
        ON CONFLICT(user_id) DO NOTHING
        """,
        (user_id,)
    )

    # Приводим stat_name к нижнему регистру
    stat_columns = {
        "сила": "strength",
        "ловкость": "dexterity",
        "стойкость": "constitution",
        "мудрость": "wisdom",
        "харизма": "charisma",
        "интеллект": "intelligence",
    }
    column_name = stat_columns.get(stat_name.lower())  # Приведение к нижнему регистру

    if column_name:
        cursor.execute(f"UPDATE user_stats SET {column_name} = ? WHERE user_id = ?", (value, user_id))
    conn.commit()
    conn.close()

# Функция для отправки списка характеристик
async def send_character_list(ctx):
    user_id = str(ctx.author.id)
    user_stats = get_user_stats(user_id)

    view = View(timeout=600) # сообщение перестанет работать и удалиться через 10 минут

    # Функция для создания кнопок с уникальными callback
    def create_button(stat_name):
        button = Button(label=stat_name, style=discord.ButtonStyle.primary)

        async def stat_button_callback(interaction: discord.Interaction):
            if interaction.user.id != ctx.author.id:
                await interaction.response.send_message("Это не ваш список характеристик!", ephemeral=True)
                return

            stat_modal = Modal(title=f"Установить {stat_name}")
            stat_input = TextInput(label=f"{stat_name}", placeholder="Введите значение", required=True)
            stat_modal.add_item(stat_input)

            async def on_submit(modal_interaction):
                try:
                    value = int(stat_input.value)
                    set_user_stat(user_id, stat_name, value)
                    await modal_interaction.response.send_message(
                        f"Значение {stat_name} установлено: {value}", ephemeral=True
                    )
                except ValueError:
                    await modal_interaction.response.send_message("Введите числовое значение!", ephemeral=True)

            stat_modal.on_submit = on_submit
            await interaction.response.send_modal(stat_modal)

        button.callback = stat_button_callback
        return button

    # Создание кнопок для всех характеристик
    for stat in user_stats:
        view.add_item(create_button(stat))

    await ctx.send("Выберите характеристику для изменения:", view=view, delete_after=600)  

# Инициализация базы данных при запуске
init_db()

def setup_character_commands(bot):
    @bot.command(name="character_list", aliases=["cl"])
    async def character_list(ctx):
        try:
            await ctx.message.delete() # Удаляем сообщение пользователя, вызвавшего команду
        except discord.errors.Forbidden:
            pass  # Игнорируем ошибку, если у бота нет прав на удаление сообщений

        await send_character_list(ctx)

    # Регистрация слэш-команды
    @app_commands.command(name="character_list", description="Просмотреть и изменить характеристики персонажа.")
    async def slash_character_list(interaction: discord.Interaction):
        class ContextShim:
            def __init__(self, interaction):
                self.author = interaction.user
                self.send = interaction.response.send_message
        
        ctx = ContextShim(interaction)
        await send_character_list(ctx)

    bot.tree.add_command(slash_character_list)