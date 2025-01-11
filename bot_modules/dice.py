import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Button, View, Modal, TextInput
import random
import re
from bot_modules.character import get_user_stats

# Function to roll the dice
def roll_dice(sides, rolls=1):
    return [random.randint(1, sides) for _ in range(rolls)]

tts_enabled = False  # TTS is disabled by default

# Function to calculate the modifier of a stat
def calculate_modifier(stat_value):
    return (stat_value - 10) // 2

def setup_dice_commands(bot):
    @bot.command(name="roll_dice", aliases=["rd"])
    async def roll_dice_buttons(ctx):
        try:
            await ctx.message.delete()  # Delete the user's requst message
        except discord.errors.Forbidden:
            pass  # Ignore the error if the bot does not have permission to delete messages

        await send_dice_buttons(ctx)  # Send the message with buttons

    # Registering slash command
    @app_commands.command(name="roll_dice", description="Choose a dice to roll 🎲")
    async def slash_roll_dice(interaction: discord.Interaction):
        class ContextShim:
            def __init__(self, interaction):
                self.author = interaction.user
                self.send = interaction.response.send_message
        
        ctx = ContextShim(interaction)
        await send_dice_buttons(ctx)

    # Helper function to create buttons
    async def send_dice_buttons(ctx):
        global tts_enabled

        dice_buttons = [
            Button(label="1d2 🎲", style=discord.ButtonStyle.primary, custom_id="1d2"),
            Button(label="1d4 🎲", style=discord.ButtonStyle.primary, custom_id="1d4"),
            Button(label="1d6 🎲", style=discord.ButtonStyle.primary, custom_id="1d6"),
            Button(label="1d8 🎲", style=discord.ButtonStyle.primary, custom_id="1d8"),
            Button(label="1d12 🎲", style=discord.ButtonStyle.primary, custom_id="1d12"),
            Button(label="1d20 🎲", style=discord.ButtonStyle.primary, custom_id="1d20"),
            Button(label="Custom Dice", style=discord.ButtonStyle.secondary, custom_id="custom_dice"),
        ]

        tts_button = Button(
            label="Disable TTS 🔇" if tts_enabled else "Enable TTS 🔊",
            style=discord.ButtonStyle.danger if tts_enabled else discord.ButtonStyle.success,
            custom_id="tts_toggle",
        )

        view = View(timeout=3600) #The buttons will disappear and the message will be deleted after 1 hour
        for button in dice_buttons:
            view.add_item(button)
        view.add_item(tts_button)

        async def dice_button_callback(interaction: discord.Interaction):
            custom_id = interaction.data["custom_id"]
            if custom_id == "custom_dice":
                custom_modal = Modal(title="Custom Dice")
                sides_input = TextInput(label="Number of sides", placeholder="For example: 10", required=False)
                rolls_input = TextInput(label="Number of rolls", placeholder="Default: 1", required=False)
                stat_input = TextInput(label="Stat for modifier", placeholder="For example: Strength", required=False)
                extra_dice_input = TextInput(label="Extra dice", placeholder="For example: 1d4+1d6", required=False)

                custom_modal.add_item(sides_input)
                custom_modal.add_item(rolls_input)
                custom_modal.add_item(stat_input)
                custom_modal.add_item(extra_dice_input)

                async def on_submit(modal_interaction):
                    try:
                        user_id = str(ctx.author.id)
                        user_stats = get_user_stats(user_id)  # Get data from the database
                        total = 0
                        result_message = ""

                        # Extra dice (line 4)
                        extra_dice = extra_dice_input.value.strip() if extra_dice_input.value else ""

                        # Main dice (lines 1 and 2)
                        if sides_input.value:
                            sides = int(sides_input.value)
                            rolls = int(rolls_input.value) if rolls_input.value else 1
                            results = roll_dice(sides, rolls)
                            total += sum(results)
                            result_message += f"{rolls}d{sides}: {', '.join(map(str, results))}"

                        # Modifier from stat (line 3)
                        stat_name = stat_input.value.strip().lower()  # Convert input to lowercase
                        modifier = 0
                        user_stats_lower = {key.lower(): value for key, value in user_stats.items()}

                        if stat_name in user_stats_lower:
                            stat_value = user_stats_lower[stat_name]
                            modifier = calculate_modifier(stat_value)
                            total += modifier

                        # Extra dice (line 4)
                        if extra_dice:
                            extra_result_strings = []
                            for item in re.finditer(r"([+-]?)\s*(\d+d\d+|\d+)", extra_dice):
                                sign = item.group(1) or "+"
                                value = item.group(2)

                                if "d" in value:  # Dice roll, e.g., 2d8
                                    extra_rolls, extra_sides = map(int, value.split("d"))
                                    extra_roll_results = roll_dice(extra_sides, extra_rolls)
                                    subtotal = sum(extra_roll_results)

                                    if sign == "-":
                                        total -= subtotal
                                        extra_result_strings.append(f"- {extra_rolls}d{extra_sides}: {', '.join(map(str, extra_roll_results))}")
                                    else:
                                        total += subtotal
                                        extra_result_strings.append(f"+ {extra_rolls}d{extra_sides}: {', '.join(map(str, extra_roll_results))}")

                                else:  # Numeric modifier, e.g., +5
                                    numeric_modifier = int(value)
                                    if sign == "-":
                                        total -= numeric_modifier
                                        extra_result_strings.append(f"- {numeric_modifier}")
                                    else:
                                        total += numeric_modifier
                                        extra_result_strings.append(f"+ {numeric_modifier}")

                            # Build result string for extra dice
                            if extra_result_strings:
                                if result_message:
                                    result_message += " "
                                result_message += " ".join(extra_result_strings).lstrip("+ ")

                        # Add stat modifier if present
                        if modifier != 0:
                            result_message += f" (+{modifier} {stat_name})" if modifier > 0 else f" ({modifier} {stat_name})"

                        # Output
                        result_message += f" = {total}"
                        await modal_interaction.response.send_message(result_message.strip(), tts=tts_enabled, delete_after=1800)
                    except ValueError:
                        await modal_interaction.response.send_message("Please enter valid values!", ephemeral=True)

                custom_modal.on_submit = on_submit
                await interaction.response.send_modal(custom_modal)
            else:
                match = re.match(r"(\d+)d(\d+)", custom_id)
                if match:
                    sides = int(match.group(2))
                    rolls = int(match.group(1))
                    results = roll_dice(sides, rolls)
                    total = sum(results)

                    if rolls == 1:
                        await interaction.response.send_message(f"{custom_id}: {results[0]}", tts=tts_enabled, delete_after=1800)
                    else:
                        await interaction.response.send_message(f"{custom_id}: {', '.join(map(str, results))} = {total}", tts=tts_enabled, delete_after=1800)

        async def tts_button_callback(interaction: discord.Interaction):
            global tts_enabled
            tts_enabled = not tts_enabled
            tts_button.label = "Disable TTS 🔇" if tts_enabled else "Enable TTS 🔊"
            tts_button.style = discord.ButtonStyle.danger if tts_enabled else discord.ButtonStyle.success
            await interaction.response.edit_message(content="Settings updated.", view=view)

        for button in dice_buttons:
            button.callback = dice_button_callback
        tts_button.callback = tts_button_callback

        await ctx.send("Choose a dice to roll:", view=view, delete_after=3600)

    bot.tree.add_command(slash_roll_dice)