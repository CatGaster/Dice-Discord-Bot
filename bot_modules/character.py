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
            intelligence INTEGER DEFAULT 0,
            level INTEGER DEFAULT 1
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
            "Уровень": row[7]  
        }
    else:
        return {"Сила": 0, "Ловкость": 0, "Стойкость": 0, "Мудрость": 0, "Харизма": 0, "Интеллект": 0, "Уровень": 1}

def set_user_stat(user_id, stat_name, value):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO user_stats (user_id, strength, dexterity, constitution, wisdom, charisma, intelligence, level)
        VALUES (?, 0, 0, 0, 0, 0, 0, 1)
        ON CONFLICT(user_id) DO NOTHING
        """,
        (user_id,)
    )

    stat_columns = {
        "сила": "strength",
        "ловкость": "dexterity",
        "стойкость": "constitution",
        "мудрость": "wisdom",
        "харизма": "charisma",
        "интеллект": "intelligence",
        "уровень": "level"  
    }
    column_name = stat_columns.get(stat_name.lower())

    if column_name:
        cursor.execute(f"UPDATE user_stats SET {column_name} = ? WHERE user_id = ?", (value, user_id))
    conn.commit()
    conn.close()

# Функция для отправки списка характеристик с кнопками
async def send_character_list(ctx):
    user_id = str(ctx.author.id)
    user_stats = get_user_stats(user_id)

    view = View(timeout=600)

    # Функция для создания кнопки изменения конкретной характеристики
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
                    if stat_name == "Уровень" and (value < 1 or value > 20):  # Уровень от 1 до 20
                        await modal_interaction.response.send_message("Уровень должен быть от 1 до 20!", ephemeral=True, delete_after=30)
                        return

                    set_user_stat(user_id, stat_name, value)
                    await modal_interaction.response.send_message(
                        f"Значение {stat_name} установлено: {value}", ephemeral=True, delete_after=30,
                    )
                except ValueError:
                    await modal_interaction.response.send_message("Введите числовое значение!", ephemeral=True, delete_after=30)

            stat_modal.on_submit = on_submit
            await interaction.response.send_modal(stat_modal)

        button.callback = stat_button_callback
        return button

    # Добавляем кнопки для всех характеристик, включая уровень
    for stat in user_stats:
        view.add_item(create_button(stat))

    
    show_stats_button = Button(label="Показать все характеристики", style=discord.ButtonStyle.secondary)

    async def show_stats_callback(interaction: discord.Interaction):
        if interaction.user.id != ctx.author.id:
            await interaction.response.send_message("Это не ваш профиль!", ephemeral=True)
            return

        stats = get_user_stats(str(ctx.author.id))
        stats_message = "\n".join([f"{key}: {value}" for key, value in stats.items()])
        await interaction.response.send_message(f"Ваши характеристики:\n{stats_message}", ephemeral=True)

    show_stats_button.callback = show_stats_callback
    view.add_item(show_stats_button)

    await ctx.send("Выберите характеристику для изменения или нажмите кнопку для просмотра всех характеристик:", view=view, delete_after=600)

# Инициализация базы данных при запуске
init_db()

def setup_character_commands(bot):
    @bot.command(name="character_list", aliases=["cl"])
    async def character_list(ctx):
        try:
            await ctx.message.delete()
        except discord.errors.Forbidden:
            pass

        await send_character_list(ctx)

    @app_commands.command(name="character_list", description="Просмотреть и изменить характеристики персонажа.")
    async def slash_character_list(interaction: discord.Interaction):
        class ContextShim:
            def __init__(self, interaction):
                self.author = interaction.user
                self.send = interaction.response.send_message
        
        ctx = ContextShim(interaction)
        await send_character_list(ctx)

    bot.tree.add_command(slash_character_list)
