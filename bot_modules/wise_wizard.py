import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
import os
from openai import OpenAI

# Загружаем переменные окружения (если они ещё не загружены в основном файле)
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Инициализируем клиента OpenRouter (OpenAI)
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

def format_question(user_question: str) -> str:
    """
    Форматирование вопроса с дополнительными указаниями.
    """
    return f"{user_question}\n\n⚠️ В ответе не размышляй, сразу отвечай, как если бы истина была известна тебе изначально."

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
        # Проверка на наличие ответа
        if completion and completion.choices and completion.choices[0].message:
            return completion.choices[0].message.content
        else:
            return "🌪️ Бальтозар не смог извлечь мудрость из космоса!"
    except Exception as e:
        print(f"Ошибка при обращении к OpenAI: {e}")
        return "🌪️ Бальтозар не может ответить из-за магического сбоя!"

async def get_baltazar_response(question: str) -> str:
    """
    Асинхронное получение ответа от "Бальтазара" с использованием run_in_executor.
    """
    system_prompt = (
        "Ты Бальтозар Мудрый - древний архимаг из мира Dungeons & Dragons. "
        "Отвечай, используя архаичную лексику, пословицы и метафоры. "
        "Отвечай сразу, без размышлений, анализов и пояснений процесса мышления. "
        "Вплетай в ответы упоминания древних рун, магических артефактов и судеб. "
        "Перепроверяй правильно ли ты указал нужную характеристику"
        "Не используй китайские буквы и слова"
        "Если у предмета или существа есть характеристики(по типу урона длинного лука 1d8 +ловкость) обязательно расскажи о них"
        "Сохраняй тон мудрого наставника. Говори на русском языке."
    )
    try:
        loop = asyncio.get_running_loop()
        formatted_question = format_question(question)
        return await loop.run_in_executor(None, sync_openai_request, formatted_question, system_prompt)
    except Exception as e:
        print(f"Ошибка API: {e}")
        return "🌪️ Бальтозар истощил магическую энергию! Подожди немного и спроси снова."

def setup_wise_wizard(bot: commands.Bot) -> None:
    """
    Регистрирует команды для работы с древним магом Бальтазаром:
      - Префиксная команда: !wise_wizard
      - Слэш-команда: /wise_wizard
    """
    # Префиксная команда
    @bot.command(name="wise_wizard", help="Задать вопрос древнему магу Бальтозару Мудрому", aliases=["ask"])
    async def ask_baltazar_prefix(ctx: commands.Context, *, вопрос: str):
        try:
            message = await ctx.send("🧙‍♂️ Бальтозар внимает твоему вопросу...")
            response = await get_baltazar_response(вопрос)
            embed = discord.Embed(
                description=(
                    f"**🧙‍♂️ Бальтозар Мудрый внемлет твоему вопросу:**\n\n"
                    f"*{response}*\n\n~ Произнёс мудрый маг ~"
                ),
                color=0x6a0dad
            )
            embed.set_thumbnail(url="https://memepedia.ru/wp-content/uploads/2021/12/pondering-my-orb-mem.jpg")
            await message.edit(content=None, embed=embed)
        except Exception as e:
            print(f"Ошибка в префиксной команде !wise_wizard: {e}")
            await ctx.send("Произошла ошибка при выполнении команды. Попробуйте позже.")

    # Слэш-команда
    @bot.tree.command(name="wise_wizard", description="Задать вопрос древнему магу Бальтозару Мудрому")
    async def ask_baltazar(interaction: discord.Interaction, вопрос: str):
        try:
            await interaction.response.defer()  # Отложенный ответ для учета задержек
            response = await get_baltazar_response(вопрос)
            embed = discord.Embed(
                description=(
                    f"**🧙‍♂️ Бальтозар Мудрый внемлет твоему вопросу:**\n\n"
                    f"*{response}*\n\n~ Произнёс мудрый маг ~"
                ),
                color=0x6a0dad
            )
            embed.set_thumbnail(url="https://memepedia.ru/wp-content/uploads/2021/12/pondering-my-orb-mem.jpg")
            await interaction.followup.send(embed=embed)
        except Exception as e:
            print(f"Ошибка в слэш-команде /wise_wizard: {e}")
            await interaction.followup.send(
                "Произошла ошибка при выполнении команды. Попробуйте позже.",
                ephemeral=True
            )
