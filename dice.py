import discord
from discord.ext import commands
from discord.ui import Button, View, Modal, TextInput
import random
import re
from character import get_user_stats  

# Function for rolling dice
def roll_dice(sides, rolls=1):
    return [random.randint(1, sides) for _ in range(rolls)]

tts_enabled = False  # TTS is off by default

# Function to calculate the stat modifier
def calculate_modifier(stat_value):
    return (stat_value - 10) // 2

def setup_dice_commands(bot):
    @bot.command(name="roll_dice", aliases=["rd"])
    async def roll_dice_buttons(ctx):
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

        view = View()
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
                extra_dice_input = TextInput(label="Additional dice", placeholder="For example: 1d4+1d6", required=False)

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

                        # Additional dice (line 4)
                        extra_dice = extra_dice_input.value.strip() if extra_dice_input.value else ""

                        # Main dice (lines 1 and 2)
                        if sides_input.value:
                            sides = int(sides_input.value)
                            rolls = int(rolls_input.value) if rolls_input.value else 1
                            results = roll_dice(sides, rolls)
                            total += sum(results)
                            result_message += f"{rolls}d{sides}: {', '.join(map(str, results))}"

                        # Stat modifier (line 3)
                        stat_name = stat_input.value.strip().lower()  # Convert input to lowercase
                        modifier = 0
                        user_stats_lower = {key.lower(): value for key, value in user_stats.items()}

                        if stat_name in user_stats_lower:
                            stat_value = user_stats_lower[stat_name]
                            modifier = calculate_modifier(stat_value)
                            total += modifier

                        # Additional dice (line 4)
                        if extra_dice:
                            extra_result_strings = []
                            for dice in re.finditer(r"([+-]?)\s*(\d+)d(\d+)", extra_dice):
                                sign = dice.group(1) or "+"
                                extra_rolls = int(dice.group(2))
                                extra_sides = int(dice.group(3))
                                extra_roll_results = roll_dice(extra_sides, extra_rolls)
                                subtotal = sum(extra_roll_results)
                                if sign == "-":
                                    total -= subtotal 
                                    extra_result_strings.append(f"- {extra_rolls}d{extra_sides}: {', '.join(map(str, extra_roll_results))}")
                                else:
                                    total += subtotal
                                    formatted_sign = "" if not result_message and sign == "+" else "+"
                                    extra_result_strings.append(f"{formatted_sign} {extra_rolls}d{extra_sides}: {', '.join(map(str, extra_roll_results))}")

                            if extra_result_strings:
                                if result_message:
                                    result_message += " "
                                result_message += " ".join(extra_result_strings)

                        # Add modifier to the result if it exists
                        if modifier != 0:
                            result_message += f" (+{modifier} {stat_name})" if modifier > 0 else f" ({modifier} {stat_name})"

                        result_message += f" = {total}"
                        await modal_interaction.response.send_message(result_message, tts=tts_enabled)
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
                        await interaction.response.send_message(f"{custom_id}: {results[0]}", tts=tts_enabled)
                    else:
                        await interaction.response.send_message(f"{custom_id}: {', '.join(map(str, results))} = {total}", tts=tts_enabled)

        async def tts_button_callback(interaction: discord.Interaction):
            global tts_enabled
            tts_enabled = not tts_enabled
            tts_button.label = "Disable TTS 🔇" if tts_enabled else "Enable TTS 🔊"
            tts_button.style = discord.ButtonStyle.danger if tts_enabled else discord.ButtonStyle.success
            await interaction.response.edit_message(content="Settings updated.", view=view)

        for button in dice_buttons:
            button.callback = dice_button_callback
        tts_button.callback = tts_button_callback

        await ctx.send("Choose a dice to roll:", view=view)