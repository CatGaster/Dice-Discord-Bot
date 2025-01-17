import discord
from discord.ext import commands
import asyncio


def setup_clear_commands(bot: commands.Bot):
    MAX_LIMIT = 100  # Максимальное количество сообщений для проверки за один раз
    DELETE_LIMIT = 20  # Максимальное количество сообщений для удаления за один раз

    # Команда Slash
    @bot.tree.command(name="clear_bot_messages", description="Удаляет сообщения, отправленные этим ботом.")
    async def clear_bot_messages_slash(interaction: discord.Interaction, limit: int = 20):
        if limit > DELETE_LIMIT:
            await interaction.response.send_message(f"Вы можете удалить не более {DELETE_LIMIT} сообщений за один раз.", ephemeral=True)
            return

        # Начинаем процесс удаления сообщений
        await clear_bot_messages(interaction.channel, min(limit, DELETE_LIMIT), interaction.response.send_message)

    # Префиксная команда
    @bot.command(name="clear_bot_messages", aliases=["clear_bot"])
    async def clear_bot_messages_prefix(ctx: commands.Context, limit: int = 10):

        try:
            await ctx.message.delete()
        except discord.errors.Forbidden:
            pass  # Игнорируем ошибку, если у бота нет прав на удаление сообщений 
        
        if limit > DELETE_LIMIT:
            await ctx.send(f"Вы можете удалить не более {DELETE_LIMIT} сообщений за один раз.", ephemeral=True)
            return
        await clear_bot_messages(ctx.channel, min(limit, DELETE_LIMIT), ctx.send)

    async def clear_bot_messages(channel, limit, send_message):
        if not channel:
            await send_message("Эту команду можно использовать только в текстовом канале.", ephemeral=True)
            return

        deleted_count = 0 # Счётчик удалённых сообщений
        total_messages = 0  # Для подсчёта количества сообщений

        # Подсчёт сообщений бота в канале
        async for message in channel.history(limit=MAX_LIMIT):
            if message.author == bot.user:
                total_messages += 1

        if total_messages < limit:
            await send_message(f"В чате недостаточно сообщений для удаления. Всего {total_messages} сообщений от бота.", ephemeral=True)
            return

        try:
            # Поиск всех сообщений в канале, проверка их до удаления нужного количества
            async for message in channel.history(limit=MAX_LIMIT):
                if message.author == bot.user:  # Если сообщение отправлено ботом
                    await message.delete()
                    deleted_count += 1
                    if deleted_count >= limit:  # Если удалено нужное количество сообщений
                        break

            # Отправка только итогового сообщения
            if deleted_count > 0:
                await send_message(f"Удалено {deleted_count} сообщений от бота.", ephemeral=True, delete_after=10) 
            else:
                await send_message("Сообщения не были удалены.", ephemeral=True)

        except discord.errors.Forbidden:
            await send_message("У меня нет прав для удаления сообщений в этом канале.", ephemeral=True)
        
        except discord.errors.HTTPException as e:
            if e.code == 429:  # Обработка ошибки 'Слишком много запросов'
                await send_message("Превышен лимит запросов. Попробуйте позже.", ephemeral=True)
            else:
                await send_message("Произошла ошибка при удалении сообщений.", ephemeral=True)