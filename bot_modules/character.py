import discord
from discord.ext import commands
from discord.ui import Button, View, Modal, TextInput
from discord import app_commands
import sqlite3

# Database initialization
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

# Functions for interacting with the database
def get_user_stats(user_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_stats WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "Strength": row[1],
            "Dexterity": row[2],
            "Constitution": row[3],
            "Wisdom": row[4],
            "Charisma": row[5],
            "Intelligence": row[6],
            "Level": row[7]  
        }
    else:
        return {"Strength": 0, "Dexterity": 0, "Constitution": 0, "Wisdom": 0, "Charisma": 0, "Intelligence": 0, "Level": 1}

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
        "strength": "strength",
        "dexterity": "dexterity",
        "constitution": "constitution",
        "wisdom": "wisdom",
        "charisma": "charisma",
        "intelligence": "intelligence",
        "level": "level"  
    }
    column_name = stat_columns.get(stat_name.lower())

    if column_name:
        cursor.execute(f"UPDATE user_stats SET {column_name} = ? WHERE user_id = ?", (value, user_id))
    conn.commit()
    conn.close()

# Function to send character list
async def send_character_list(ctx):
    user_id = str(ctx.author.id)
    user_stats = get_user_stats(user_id)

    view = View(timeout=600)

    def create_button(stat_name):
        button = Button(label=stat_name, style=discord.ButtonStyle.primary)

        async def stat_button_callback(interaction: discord.Interaction):
            if interaction.user.id != ctx.author.id:
                await interaction.response.send_message("This is not your character list!", ephemeral=True, )
                return

            stat_modal = Modal(title=f"Set {stat_name}")
            stat_input = TextInput(label=f"{stat_name}", placeholder="Enter value", required=True)
            stat_modal.add_item(stat_input)

            async def on_submit(modal_interaction):
                try:
                    value = int(stat_input.value)
                    if stat_name == "Level" and (value < 1 or value > 20):  # Level from 1 to 20
                        await modal_interaction.response.send_message("Level must be between 1 and 20!", ephemeral=True, delete_after=30)
                        return

                    set_user_stat(user_id, stat_name, value)
                    await modal_interaction.response.send_message(
                        f"{stat_name} set to: {value}", ephemeral=True, delete_after=30,
                    )
                except ValueError:
                    await modal_interaction.response.send_message("Please enter a numerical value!", ephemeral=True, delete_after=30)

            stat_modal.on_submit = on_submit
            await interaction.response.send_modal(stat_modal)

        button.callback = stat_button_callback
        return button

    # Add buttons for all stats, including level
    for stat in user_stats:
        view.add_item(create_button(stat))

    await ctx.send("Choose a stat to modify:", view=view, delete_after=600)

# Initialize the database at startup
init_db()

def setup_character_commands(bot):
    @bot.command(name="character_list", aliases=["cl"])
    async def character_list(ctx):
        try:
            await ctx.message.delete()
        except discord.errors.Forbidden:
            pass

        await send_character_list(ctx)

    @app_commands.command(name="character_list", description="View and modify character stats.")
    async def slash_character_list(interaction: discord.Interaction):
        class ContextShim:
            def __init__(self, interaction):
                self.author = interaction.user
                self.send = interaction.response.send_message
        
        ctx = ContextShim(interaction)
        await send_character_list(ctx)

    bot.tree.add_command(slash_character_list)
