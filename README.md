# Discord Bot: Dice Roller and Character Manager

## Disclaimer

This is an unofficial bot for Dungeons & Dragons, not affiliated with Wizards of the Coast.

## Project Description <a name="project-description-en"></a>

For detailed information about the bot modules, visit the link:

[Bot Modules Documentation](bot_modules/README.md)

This Discord bot is designed to assist with tabletop role-playing games (such as Dungeons & Dragons). It includes the following main features:

1. **Dice Rolls**: Standard dice (1d2, 1d4, 1d6, 1d8, 1d12, 1d20), custom dice, and additional dice are supported.
2. **Character Attribute Management**: Users can create and modify their attributes (e.g., Strength, Dexterity, Wisdom, etc.).
3. **TTS (Text-to-Speech)**: The option to announce command results in voice chat.
4. **Bot message deletion:**: The ability to delete a specific number of bot messages, as well as the option to automatically remove bot messages to maintain chat cleanliness.

## Project Structure

- **`bot.py`**: The main file responsible for running the bot and registering commands.
- **`dice.py`**: Functionality for working with dice.
- **`character.py`**: Managing character attributes.
- **`clear.py`**: Deleting bot messages.

## Creating a Discord Bot
- **To create a Discord bot, follow these steps:**

    - [Go to the Discord Developer Portal.](https://discord.com/developers/docs/intro)
    
    - Click on New Application and create a new application.
    - In the left menu, select Bot, then click Add Bot.
    - Copy your bot's Token, which you will need to run the bot.
    - In the OAuth2 section, select bot under SCOPES, then set the necessary permissions for your bot under BOT PERMISSIONS.
    - Use the generated invitation link to add the bot to your server.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/CatGaster/Dice-Discord-Bot

   git checkout english-version

   cd <Dice-Discord-Bot>
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

#### `/roll_dice` or `!roll_dice` or `!rd`
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

#### `/character_list` or `!character_list` or `!cl`
- Displays the current user's attribute list.
- Supported attributes:
  - Strength, Dexterity, Constitution, Wisdom, Charisma, Intelligence, Level.

#### Modifying Attributes
- Click on an attribute button and enter a new value.
- Example:
  ```
  Strength set to: 15
  ```

### Bot Message Deletion Commands

#### `/clear_bot_messages` or `!clear_bot_messages` or `!clear_bot`
- Deletes a specified number of bot messages.
- Example:
  ```
  !clear_bot_messages 5
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
- `level`: Character level

## Dependencies

- `discord.py`: Interaction with the Discord API.
- `sqlite3`: Local database for storing attributes.
- `python-dotenv`: For managing environment variables.
- `random`: Random number generation for dice rolls.
- `re`: Input handling for additional dice modifiers.


## License

The project is distributed under the MIT license. For details, see the LICENSE file.



