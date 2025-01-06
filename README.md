# Discord Bot: Dice Roller and Character Manager

[RU](#описание-проекта)

[ENG](#project-description)

## Описание проекта <a name="ru_description"></a>

Этот бот для Discord предназначен для помощи в настольных ролевых играх (например, Dungeons & Dragons). Он включает в себя следующие основные функции:

1. **Броски кубиков**: Поддерживаются стандартные кубики (1d2, 1d4, 1d6, 1d8, 1d12, 1d20), кастомные кубики и дополнительные кубики.
2. **Управление характеристиками персонажей**: Пользователи могут создавать и изменять свои характеристики (например, Сила, Ловкость, Мудрость и т.д.).
3. **TTS (Text-to-Speech)**: Возможность озвучивать результаты команд в голосовом чате.

## Структура проекта

- **`bot.py`**: Основной файл, отвечающий за запуск бота и регистрацию команд.
- **`dice.py`**: Функционал для работы с кубиками.
- **`character.py`**: Управление характеристиками персонажей.

## Установка

1. Склонируйте репозиторий:

   ```bash
   git clone https://github.com/CatGaster/Dice-Discord-Bot
   cd <папка проекта>
   ```

2. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```

3. Создайте файл `.env` и добавьте в него токен вашего бота:

   ```env
   DISCORD_TOKEN=<ваш токен>
   ```

4. Убедитесь, что у вас установлен Python версии 3.8 или выше.

5. Запустите бота:

   ```bash
   python bot.py
   ```

## Использование

### Команды для управления кубиками

#### `!roll_dice` или `!rd`
- Выводит кнопки для выбора кубиков.
- Поддерживаемые стандартные кубики:
  - 1d2, 1d4, 1d6, 1d8, 1d12, 1d20.
- Поддерживается кастомный кубик:
  - Введите количество граней, число бросков и дополнительные модификаторы.

#### Пример
- Бросок 1d20:
  ```
  1d20: 15
  ```
- Дополнительные кубики, например, 1d4+1d8+2d50-1d100:
  ```
  1d4 (3) + 1d8 (6) + 2d50 (20, 45) - 1d100 (65) = 9
  ```
- Учет выбранной характеристики:
  ```
  1d6 (+2 сила) = 6
  ```

#### Управление TTS
- Кнопка для включения/отключения озвучивания результатов.

### Команды для управления характеристиками

#### `!character_list` или `!cl`
- Выводит список характеристик текущего пользователя.
- Поддерживаемые характеристики:
  - Сила, Ловкость, Стойкость, Мудрость, Харизма, Интеллект.

#### Изменение характеристики
- Нажмите кнопку с характеристикой и введите новое значение.
- Пример:
  ```
  Значение Сила установлено: 15
  ```

## База данных

Для хранения характеристик персонажей используется SQLite. База данных создается автоматически при первом запуске и сохраняется в файле `user_stats.db`.

### Структура таблицы
- `user_id`: Идентификатор пользователя.
- `strength`: Сила.
- `dexterity`: Ловкость.
- `constitution`: Стойкость.
- `wisdom`: Мудрость.
- `charisma`: Харизма.
- `intelligence`: Интеллект.

## Зависимости

- `discord.py`: Работа с Discord API.
- `sqlite3`: Локальная база данных для хранения характеристик.
- `python-dotenv`: Для управления переменными окружения.
- `random`: Генерация случайных чисел для бросков кубиков.
- `re`: Обработка ввода для дополнительных кубиков.


## Лицензия

Проект распространяется под лицензией MIT. Для подробностей см. файл LICENSE.

---

## Project Description <a name="en_description"></a>

This Discord bot is designed to assist in tabletop role-playing games (e.g., Dungeons & Dragons). It includes the following main features:

1. **Dice Rolls**: Supports standard dice (1d2, 1d4, 1d6, 1d8, 1d12, 1d20), custom dice, and additional modifiers.
2. **Character Attribute Management**: Users can create and modify their character attributes (e.g., Strength, Dexterity, Wisdom, etc.).
3. **TTS (Text-to-Speech)**: Option to announce command results in a voice channel.

## Project Structure

- **`bot.py`**: Main file for launching the bot and registering commands.
- **`dice.py`**: Functionality for dice rolls.
- **`character.py`**: Character attribute management.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/CatGaster/Dice-Discord-Bot
   cd <project_folder>
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file and add your bot token:

   ```env
   DISCORD_TOKEN=<your_token>
   ```

4. Ensure Python version 3.8 or higher is installed.

5. Run the bot:

   ```bash
   python bot.py
   ```

## Usage

### Dice Commands

#### `!roll_dice` or `!rd`
- Displays buttons to select dice.
- Supported standard dice:
  - 1d2, 1d4, 1d6, 1d8, 1d12, 1d20.
- Supports custom dice:
  - Enter the number of sides, rolls, and additional modifiers.

#### Example
- Rolling 1d20:
  ```
  1d20: 15
  ```
- Additional dice, such as 1d4+1d8+2d50-1d100:
  ```
  1d4 (3) + 1d8 (6) + 2d50 (20, 45) - 1d100 (65) = 9
  ```
- Accounting for selected attributes:
  ```
  1d6 (+2 strength) = 6
  ```

#### TTS Management
- Button to toggle announcing results.

### Character Commands

#### `!character_list` or `!cl`
- Displays the current user's attribute list.
- Supported attributes:
  - Strength, Dexterity, Constitution, Wisdom, Charisma, Intelligence.

#### Modifying Attributes
- Click on an attribute button and enter a new value.
- Example:
  ```
  Strength set to: 15
  ```

## Database

SQLite is used to store character attributes. The database is created automatically on the first run and saved in `user_stats.db`.

### Table Structure
- `user_id`: User identifier.
- `strength`: Strength.
- `dexterity`: Dexterity.
- `constitution`: Constitution.
- `wisdom`: Wisdom.
- `charisma`: Charisma.
- `intelligence`: Intelligence.

## Dependencies

- `discord.py`: Interaction with the Discord API.
- `sqlite3`: Local database for storing attributes.
- `python-dotenv`: For managing environment variables.
- `random`: Random number generation for dice rolls.
- `re`: Input handling for additional dice modifiers.


## License

The project is distributed under the MIT license. For details, see the LICENSE file.

