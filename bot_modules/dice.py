import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Button, View, Modal, TextInput
import random
import re
from bot_modules.character import get_user_stats

# Функция для броска кубика
def roll_dice(sides, rolls=1):
    return [random.randint(1, sides) for _ in range(rolls)]

tts_enabled = False  # По умолчанию TTS отключен
bonus_mastery = False  # По умолчанию бонус мастерства выключен

# Функция расчёта бонуса мастерства
def get_proficiency_bonus(level):
    proficiency_table = {
        range(1, 5): 2,
        range(5, 9): 3,
        range(9, 13): 4,
        range(13, 17): 5,
        range(17, 21): 6
    }
    return next(bonus for levels, bonus in proficiency_table.items() if level in levels)

# Функция для расчёта модификатора характеристики
def calculate_modifier(stat_value):
    return (stat_value - 10) // 2

def setup_dice_commands(bot):
    @bot.command(name="roll_dice", aliases=["rd"])
    async def roll_dice_buttons(ctx):
        try:
            await ctx.message.delete()  # Удаляем сообщение пользователя
        except discord.errors.Forbidden:
            pass  # Игнорируем ошибку, если у бота нет прав на удаление сообщений

        await send_dice_buttons(ctx)  # Отправляем сообщение с кнопками

    # Регистрация слэш-команды
    @app_commands.command(name="roll_dice", description="Выбери кубик для броска 🎲")
    async def slash_roll_dice(interaction: discord.Interaction):
        class ContextShim:
            def __init__(self, interaction):
                self.author = interaction.user
                self.send = interaction.response.send_message
        
        ctx = ContextShim(interaction)
        await send_dice_buttons(ctx)

    # Помощьная функция для создания кнопок
    async def send_dice_buttons(ctx):
        global tts_enabled, bonus_mastery

        dice_buttons = [
            Button(label="1d2 🎲", style=discord.ButtonStyle.primary, custom_id="1d2"),
            Button(label="1d4 🎲", style=discord.ButtonStyle.primary, custom_id="1d4"),
            Button(label="1d6 🎲", style=discord.ButtonStyle.primary, custom_id="1d6"),
            Button(label="1d8 🎲", style=discord.ButtonStyle.primary, custom_id="1d8"),
            Button(label="1d12 🎲", style=discord.ButtonStyle.primary, custom_id="1d12"),
            Button(label="1d20 🎲", style=discord.ButtonStyle.primary, custom_id="1d20"),
            Button(label="Кастомный кубик", style=discord.ButtonStyle.secondary, custom_id="custom_dice"),
        ]

        # Кнопка бонуса мастерства
        mastery_button = Button(
            label=f"Бонус мастерства {'✅' if bonus_mastery else '⬜'}",
            style=discord.ButtonStyle.secondary,
            custom_id="toggle_mastery",
        )

        tts_button = Button(
            label="Отключить TTS 🔇" if tts_enabled else "Включить TTS 🔊",
            style=discord.ButtonStyle.danger if tts_enabled else discord.ButtonStyle.success,
            custom_id="tts_toggle",
        )

        view = View(timeout=3600)  # Кнопки пропадут и сообщение удалиться через 1 час
        for button in dice_buttons:
            view.add_item(button)
        view.add_item(tts_button)
        view.add_item(mastery_button)

        async def dice_button_callback(interaction: discord.Interaction):
            custom_id = interaction.data["custom_id"]
            if custom_id == "custom_dice":
                custom_modal = Modal(title="Кастомный кубик")
                sides_input = TextInput(label="Количество граней", placeholder="Например: 10", required=False)
                rolls_input = TextInput(label="Количество бросков", placeholder="По умолчанию: 1", required=False)
                stat_input = TextInput(label="Характеристика для модификатора", placeholder="Например: Сила", required=False)
                extra_dice_input = TextInput(label="Дополнительные кубики", placeholder="Например: 1d4+1d6", required=False)

                custom_modal.add_item(sides_input)
                custom_modal.add_item(rolls_input)
                custom_modal.add_item(stat_input)
                custom_modal.add_item(extra_dice_input)

                async def on_submit(modal_interaction):
                    try:
                        user_id = str(ctx.author.id)
                        user_stats = get_user_stats(user_id)  # Получаем данные из базы данных
                        total = 0
                        result_message = ""

                        # Дополнительные кубики (4 строка)
                        extra_dice = extra_dice_input.value.strip() if extra_dice_input.value else ""

                        # Основной кубик (1 и 2 строки)
                        if sides_input.value:
                            sides = int(sides_input.value)
                            rolls = int(rolls_input.value) if rolls_input.value else 1
                            results = roll_dice(sides, rolls)
                            total += sum(results)
                            result_message += f"{rolls}d{sides}: {', '.join(map(str, results))}"

                        # Модификатор от характеристики (3 строка)
                        stat_name = stat_input.value.strip().lower()  # Преобразуем ввод в нижний регистр
                        modifier = 0
                        user_stats_lower = {key.lower(): value for key, value in user_stats.items()}

                        if stat_name in user_stats_lower:
                            stat_value = user_stats_lower[stat_name]
                            if stat_name == "уровень":
                                modifier = stat_value  # Уровень добавляется как есть
                            else:
                                modifier = calculate_modifier(stat_value)  # Остальные характеристики используют модификатор
                            total += modifier

                        # Дополнительные кубики (4 строка)
                        if extra_dice:
                            extra_result_strings = []
                            for item in re.finditer(r"([+-]?)\s*(\d+d\d+|\d+)", extra_dice):
                                sign = item.group(1) or "+"
                                value = item.group(2)

                                if "d" in value:  # Это бросок кубиков, например, 2d8
                                    extra_rolls, extra_sides = map(int, value.split("d"))
                                    extra_roll_results = roll_dice(extra_sides, extra_rolls)
                                    subtotal = sum(extra_roll_results)

                                    if sign == "-":
                                        total -= subtotal
                                        extra_result_strings.append(f"- {extra_rolls}d{extra_sides}: {', '.join(map(str, extra_roll_results))}")
                                    else:
                                        total += subtotal
                                        extra_result_strings.append(f"+ {extra_rolls}d{extra_sides}: {', '.join(map(str, extra_roll_results))}")

                                else:  # Это числовой модификатор, например, +5
                                    numeric_modifier = int(value)
                                    if sign == "-":
                                        total -= numeric_modifier
                                        extra_result_strings.append(f"- {numeric_modifier}")
                                    else:
                                        total += numeric_modifier
                                        extra_result_strings.append(f"+ {numeric_modifier}")

                            # Формируем строку результата дополнительных кубиков
                            if extra_result_strings:
                                if result_message:
                                    result_message += " "
                                result_message += " ".join(extra_result_strings).lstrip("+ ")

                        # Добавляем модификатор от характеристики, если есть
                        if modifier != 0:
                            result_message += f" (+{modifier} {stat_name})" if modifier > 0 else f" ({modifier} {stat_name})"

                        # Если бонус мастерства активен, добавляем его к общему результату
                        if bonus_mastery:
                            level = user_stats.get("Уровень", 1)
                            proficiency_bonus = get_proficiency_bonus(level)
                            total += proficiency_bonus
                            result_message += f" (+{proficiency_bonus} БМ)"

                        # вывод
                        result_message += f" = {total}"
                        await modal_interaction.response.send_message(result_message.strip(), tts=tts_enabled, delete_after=1800)
                    except ValueError:
                        await modal_interaction.response.send_message("Введите корректные значения!", ephemeral=True)

                custom_modal.on_submit = on_submit
                await interaction.response.send_modal(custom_modal)
            else:
                match = re.match(r"(\d+)d(\d+)", custom_id)
                if match:
                    sides = int(match.group(2))
                    rolls = int(match.group(1))
                    results = roll_dice(sides, rolls)
                    total = sum(results)
                    
                    # Добавляем проверку на бонус мастерства
                    if bonus_mastery:
                        user_id = str(interaction.user.id)
                        user_stats = get_user_stats(user_id)
                        level = user_stats.get("Уровень", 1)
                        proficiency_bonus = get_proficiency_bonus(level)
                        total += proficiency_bonus
                    
                    # Формируем сообщение с учетом бонуса
                    if rolls == 1:
                        message = f"{custom_id}: {results[0]}"
                    else:
                        message = f"{custom_id}: {', '.join(map(str, results))} = {total}"
                    
                    # Добавляем информацию о бонусе если он активен
                    if bonus_mastery:
                        message += f" +{proficiency_bonus} (БМ) = {total}"
                    
                    await interaction.response.send_message(message, tts=tts_enabled, delete_after=1800)

        async def toggle_mastery_callback(interaction: discord.Interaction):
            global bonus_mastery
            bonus_mastery = not bonus_mastery
            mastery_button.label = f"Бонус мастерства {'✅' if bonus_mastery else '⬜'}"
            await interaction.response.edit_message(content="Настройки обновлены.", view=view)

        async def tts_button_callback(interaction: discord.Interaction):
            global tts_enabled
            tts_enabled = not tts_enabled
            tts_button.label = "Отключить TTS 🔇" if tts_enabled else "Включить TTS 🔊"
            tts_button.style = discord.ButtonStyle.danger if tts_enabled else discord.ButtonStyle.success
            await interaction.response.edit_message(content="Настройки обновлены.", view=view)

        # Обработчики кнопок
        for button in dice_buttons:
            button.callback = dice_button_callback
        mastery_button.callback = toggle_mastery_callback
        tts_button.callback = tts_button_callback

        await ctx.send("Выберите кубик для броска:", view=view, delete_after=3600)

    bot.tree.add_command(slash_roll_dice)