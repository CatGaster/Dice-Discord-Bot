import discord
from discord.ext import commands
import asyncio

# Function to register the message clearing command
def setup_clear_commands(bot: commands.Bot):
    MAX_LIMIT = 100  # Maximum number of messages to check at once
    DELETE_LIMIT = 20  # Maximum number of messages to delete at once

    # Slash command
    @bot.tree.command(name="clear_bot_messages", description="Deletes messages sent by this bot.")
    async def clear_bot_messages_slash(interaction: discord.Interaction, limit: int = 20):
        if limit > DELETE_LIMIT:
            await interaction.response.send_message(f"You can delete no more than {DELETE_LIMIT} messages at a time.", ephemeral=True)
            return

        # Directly proceed with deletion without a start message
        await clear_bot_messages(interaction.channel, min(limit, DELETE_LIMIT), interaction.response.send_message)

    # Prefix command
    @bot.command(name="clear_bot_messages", aliases=["clear_bot"])
    async def clear_bot_messages_prefix(ctx: commands.Context, limit: int = 10):

        try:
            await ctx.message.delete()  # Delete the user's message
        except discord.errors.Forbidden:
            pass  # Ignore the error if the bot does not have permission to delete messages

        if limit > DELETE_LIMIT:
            await ctx.send(f"You can delete no more than {DELETE_LIMIT} messages at a time.", ephemeral=True)
            return
        await clear_bot_messages(ctx.channel, min(limit, DELETE_LIMIT), ctx.send)

    async def clear_bot_messages(channel, limit, send_message):
        if not channel:
            await send_message("This command can only be used in a text channel.", ephemeral=True)
            return

        deleted_count = 0
        total_messages = 0  # To count the number of messages

        # Count the bot's messages in the channel
        async for message in channel.history(limit=MAX_LIMIT):
            if message.author == bot.user:
                total_messages += 1

        if total_messages < limit:
            await send_message(f"There are not enough messages in the chat to delete. Total {total_messages} bot messages.", ephemeral=True)
            return

        try:
            # Search all messages in the channel, checking them until the desired number is deleted
            async for message in channel.history(limit=MAX_LIMIT):
                if message.author == bot.user:  # If the message was sent by the bot
                    await message.delete()
                    deleted_count += 1
                    if deleted_count >= limit:  # If the desired number of messages is deleted
                        break

            # Send only the final result message
            if deleted_count > 0:
                await send_message(f"Deleted {deleted_count} bot messages.", ephemeral=True, delete_after=10)
            else:
                await send_message("No messages were deleted.")

        except discord.errors.Forbidden:
            await send_message("I don't have permission to delete messages in this channel.", ephemeral=True)
        
        except discord.errors.HTTPException as e:
            if e.code == 429:  # Handling 'Too Many Requests' error
                await send_message("Request limit exceeded. Please try again later.", ephemeral=True)
            else:
                await send_message("An error occurred while deleting messages.", ephemeral=True)