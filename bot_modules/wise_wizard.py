import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
import os
from openai import OpenAI


load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Initialize OpenRouter (OpenAI) client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

def format_question(user_question: str) -> str:
    """
    Format the question with additional instructions.
    """
    return f"{user_question}\n\n⚠️ Do not ponder in your response; answer immediately as if the truth was always known to you."

def sync_openai_request(question: str, system_prompt: str) -> str:
    try:
        completion = client.chat.completions.create(
            model="deepseek/deepseek-chat:free",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            temperature=0.5,
            max_tokens=800
        )
        # Check if a response is available
        if completion and completion.choices and completion.choices[0].message:
            return completion.choices[0].message.content
        else:
            return "🌪️ Baltazar failed to extract wisdom from the cosmos!"
    except Exception as e:
        print(f"Error when calling OpenAI: {e}")
        return "🌪️ Baltazar cannot respond due to a magical disturbance!"

async def get_baltazar_response(question: str) -> str:
    # if OPENROUTER_API_KEY is not set
    if not OPENROUTER_API_KEY:
        return "🧙‍♂️ Without the key, the gate to the wizard's tower will remain closed."

    """
    Asynchronously retrieve a response from "Baltazar" using run_in_executor.
    """
    system_prompt = (
        "You are Baltazar the Wise - an ancient archmage from the world of Dungeons & Dragons. "
        "Answer using archaic language, proverbs, and metaphors. "
        "Respond immediately, without reflection, analysis, or explanation of your thought process. "
        "Weave mentions of ancient runes, magical artifacts, and fates into your responses. "
        "Double-check if you correctly specified the required characteristic. "
        "If an item or creature has attributes (such as a longbow dealing 1d8 + Dexterity damage), be sure to mention them. "
        "Maintain the tone of a wise mentor. Speak in English."
    )
    try:
        loop = asyncio.get_running_loop()
        formatted_question = format_question(question)
        return await loop.run_in_executor(None, sync_openai_request, formatted_question, system_prompt)
    except Exception as e:
        print(f"API error: {e}")
        return "🌪️ Baltazar has exhausted his magical energy! Wait a bit and ask again."

def setup_wise_wizard(bot: commands.Bot) -> None:
    """
    Registers commands to interact with the ancient mage Baltazar:
      - Prefix command: !wise_wizard
      - Slash command: /wise_wizard
    """
    # Prefix command
    @bot.command(name="wise_wizard", help="Ask a question to the ancient mage Baltazar the Wise", aliases=["ask"])
    async def ask_baltazar_prefix(ctx: commands.Context, *, question: str):
        try:
            message = await ctx.send("🧙‍♂️ Baltazar is pondering your question...")
            response = await get_baltazar_response(question)
            embed = discord.Embed(
                description=(
                    f"**🧙‍♂️ Baltazar the Wise heeds your question:**\n\n"
                    f"*{response}*\n\n~ Spoke the wise mage ~"
                ),
                color=0x6a0dad
            )
            embed.set_thumbnail(url="https://memepedia.ru/wp-content/uploads/2021/12/pondering-my-orb-mem.jpg")
            await message.edit(content=None, embed=embed)
        except Exception as e:
            print(f"Error in prefix command !wise_wizard: {e}")
            await ctx.send("An error occurred while executing the command. Please try again later.")

    # Slash command
    @bot.tree.command(name="wise_wizard", description="Ask a question to the ancient mage Baltazar the Wise")
    async def ask_baltazar(interaction: discord.Interaction, question: str):
        try:
            await interaction.response.defer()  # Deferred response to account for delays
            response = await get_baltazar_response(question)
            embed = discord.Embed(
                description=(
                    f"**🧙‍♂️ Baltazar the Wise heeds your question:**\n\n"
                    f"*{response}*\n\n~ Spoke the wise mage ~"
                ),
                color=0x6a0dad
            )
            embed.set_thumbnail(url="https://memepedia.ru/wp-content/uploads/2021/12/pondering-my-orb-mem.jpg") # Paste your link here if you want to upload another photo
            await interaction.followup.send(embed=embed)
        except Exception as e:
            print(f"Error in slash command /wise_wizard: {e}")
            await interaction.followup.send(
                "An error occurred while executing the command. Please try again later.",
                ephemeral=True
            )
