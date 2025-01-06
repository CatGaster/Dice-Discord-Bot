# Discord Bot: Dice Roller and Character Manager

## Disclaimer

This is an unofficial dice bot for Dungeons & Dragons, not affiliated with Wizards of the Coast.

## Project Description <a name="en_description"></a>

This Discord bot is designed to assist in tabletop role-playing games (e.g., Dungeons & Dragons). It includes the following main features:

1. **Dice Rolls**: Supports standard dice (1d2, 1d4, 1d6, 1d8, 1d12, 1d20), custom dice, and additional modifiers.
2. **Character Attribute Management**: Users can create and modify their character attributes (e.g., Strength, Dexterity, Wisdom, etc.).
3. **TTS (Text-to-Speech)**: Option to announce command results in a voice channel.

## Project Structure

- **`bot.py`**: Main file for launching the bot and registering commands.
- **`dice.py`**: Functionality for dice rolls.
- **`character.py`**: Character attribute management.

## Creating a Discord Bot

- **To create a Discord bot, follow these steps:**

    - [Go to the Discord Developer Portal.](https://discord.com/developers/docs/intro)

    - Click on "New Application" and create a new application.

    - In the left menu, select "Bot", then click "Add Bot".

    - Copy your bot's Token, which will be needed to run the bot.

    - Under OAuth2, select "bot" in the SCOPES section, then set the necessary permissions for your bot in the BOT PERMISSIONS section.

    - Use the generated invite link to add the bot to your server.

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



