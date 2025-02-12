# Documentation for Discord Bot Modules

## Contents
- [dice.py module](#dicepy-module)
- [character.py module](#characterpy-module)
- [clear.py module](#clearpy-module)
- [wise_wizardpy-module](#wise_wizardpy-module)
---

# <a name="dicepy-module"></a>dice.py module

The `dice.py` module provides functionality for rolling dice, including standard types, custom settings, and using user attributes for modifiers. This module supports both prefix (`!`) and slash commands.

### Main Features

1. **Rolling Standard Dice**  
   Standard dice supported: 1d2, 1d4, 1d6, 1d8, 1d12, 1d20. The user can choose the dice using buttons.

2. **Custom Dice**  
   The user can specify the number of sides and rolls for custom dice. Additional dice and numeric modifiers in the format `1d6+2d8-5` are also supported.

3. **Attribute Modifiers**  
   The module can take into account user attribute modifiers (e.g., "Strength" or "Dexterity"). The modifier value is calculated as `(value - 10) // 2`.

4. **Text-to-Speech Notifications (TTS)**  
   Users can enable or disable text-to-speech (TTS) notifications.

### Main Functions

#### `roll_dice(sides, rolls=1)`
- **Description:** Rolls a dice with the specified number of sides and returns the results.
- **Parameters:**
  - `sides` (int): Number of sides on the dice.
  - `rolls` (int): Number of rolls (default is 1).
- **Returns:** A list of results for each roll.

#### `calculate_modifier(stat_value)`
- **Description:** Calculates the modifier for an attribute.
- **Parameters:**
  - `stat_value` (int): The value of the attribute.
- **Returns:** The modifier (int).

### Commands

1. **`/roll_dice` (slash command)**  
   **Description:** Allows the user to select a dice to roll through interactive buttons.  
   **Interaction:** Displays buttons for standard dice and custom rolls.

2. **`!roll_dice` or `!rd` (prefix command)**  
   **Description:** Equivalent functionality for users who prefer text commands.  
   **Interaction:** Displays buttons for selecting the dice.

### Interactive Elements

- **Buttons for Standard Dice:**  
  Dice: 1d2, 1d4, 1d6, 1d8, 1d12, 1d20.  
  **Action:** Rolls the selected dice and outputs the results.

- **Button for Custom Dice:**  
  **Action:** Opens a modal for entering the following parameters:
  - Number of sides.
  - Number of rolls.
  - Attribute for modifiers.
  - Additional dice and modifiers.

- **Button for TTS Control:**  
  **Action:** Enables or disables text-to-speech notifications.

### Custom Dice Logic
1. The user enters parameters in the modal window.
2. The main roll is calculated using `roll_dice`.
3. If an attribute is specified, the module retrieves its value through the `get_user_stats` function.
4. Additional dice and modifiers are parsed using regular expressions.
5. The final result is calculated and displayed to the user.

### Example Interaction

1. The user enters the command `/roll_dice`.
2. The bot displays buttons for selecting dice.
3. The user clicks the `1d20` button.
4. The bot rolls the dice and sends a message: `1d20: 15`.

### Dependencies
- **Libraries:**
  - `discord`
  - `discord.ext.commands`
  - `discord.ui`
  - `random`
  - `re`
- **Other Modules:**
  - `character.get_user_stats` for retrieving user attribute data.

### Limitations
- The maximum number of rolls for a dice is not limited, but very large values may cause delays.
- The format for additional dice should follow the pattern `NdM+NdM-...` (e.g., `2d6+1d8-5`).

---

# <a name="characterpy-module"></a>character.py module

The `character.py` module provides functionality for managing user attributes in Discord. It allows viewing, changing, and saving attributes through interactive elements like buttons and modals. Both prefix (`!`) and slash commands are supported.

### Main Features

1. **Viewing Attributes**  
   The user can get a list of their attributes in a convenient format. For each value, a button is created that allows changing the attribute value.

2. **Changing Attributes**  
   Attributes can be changed by selecting the corresponding button and entering a new value in a modal window.

3. **Storing Data**  
   User data is stored in an SQLite database. Each user has a record with the following attributes:
   - Strength
   - Dexterity
   - Constitution
   - Wisdom
   - Charisma
   - Intelligence
   - Level

### Main Functions

#### `init_db()`
- **Description:** Initializes the SQLite database by creating the `user_stats` table if it does not exist.
- **Table Contains:**
  - `user_id` (str): User ID.
  - `strength`, `dexterity`, `constitution`, `wisdom`, `charisma`, `intelligence`, `Level`. (int): Attribute values.

#### `get_user_stats(user_id)`
- **Description:** Returns the current attributes of the user as a dictionary.
- **Parameters:**
  - `user_id` (str): User ID.
- **Returns:** A dictionary of attributes. If the user is not in the database, all values will be 0.

#### `set_user_stat(user_id, stat_name, value)`
- **Description:** Sets a new value for the specified user attribute.
- **Parameters:**
  - `user_id` (str): User ID.
  - `stat_name` (str): Attribute name (e.g., "Strength").
  - `value` (int): New attribute value.

#### `send_character_list(ctx)`
- **Description:** Sends the user a list of buttons for changing their attributes.
- **Parameters:**
  - `ctx`: Command context (for prefix commands) or interaction (for slash commands).

### Commands

1. **`!character_list` or `!cl` (prefix command)**  
   **Description:** Allows the user to view and change their attributes.  
   **Interaction:** Sends a message with buttons for changing attributes.

2. **`/character_list` (slash command)**  
   **Description:** Similar to the prefix command but used through the slash command interface.  
   **Interaction:** Creates a list of buttons for changing attributes.

### Interactive Elements

- **Buttons for Changing Attributes:**  
  **Action:** Allows the user to change the value of an attribute through a modal window.  
  **Workflow:**
  1. The user clicks a button for the attribute.
  2. The bot opens a modal with an input field.
  3. The user enters a new value.
  4. The value is saved in the database.

### Example Interaction

1. The user enters the command `!character_list` or `/character_list`.
2. The bot sends a message with buttons: "Strength", "Dexterity", "Constitution", "Wisdom", "Charisma", "Intelligence", "Level".
3. The user clicks the "Strength" button.
4. The bot opens a modal for entering the new value.
5. The user enters the value, for example, `12`.
6. The bot saves the value in the database and confirms the change.

### Dependencies
- **Libraries:**
  - `discord`
  - `discord.ext.commands`
  - `discord.ui`
  - `sqlite3`
- **Related Modules:**
  - `dice.py` — for dice related to attributes.

### Limitations
- Only registered users can change their attributes.
- Attribute names are case-sensitive in code but are processed in lowercase when interacting.
- The SQLite database is limited to a single `user_stats` table.

### Expandability
- To add new attributes:
  1. Update the `user_stats` table in the database.
  2. Add the new attribute to the `stat_columns` dictionary in the `set_user_stat` function.
  3. Add a button and handling logic in the `send_character_list` function.

---

## <a name="clearpy-module"></a>clear.py module

The `clear.py` module provides functionality for deleting messages sent by the bot using both prefix (`!`) and slash commands. This is useful for clearing the chat from spam or outdated bot messages.

### Main Features

1. **Deleting Bot Messages**  
   The command allows deleting a specified number of messages sent by the bot from the text channel.

2. **Deletion Limits**  
   The maximum number of messages checked at once: 100.  
   The maximum number of messages deleted at once: 20.

### Main Functions

#### `setup_clear_commands(bot)`
- **Description:** Registers commands for deleting messages.
- **Parameters:**
  - `bot` (commands.Bot): Bot instance.

#### `clear_bot_messages(channel, limit, send_message)`
- **Description:** Deletes the specified number of bot messages from the given text channel.
- **Parameters:**
  - `channel` (discord.TextChannel): The text channel for deleting messages.
  - `limit` (int): The number of messages to delete.
  - `send_message` (Callable): A function to send notifications to the user.
- **Error Handling:**
  - If the bot does not have permission to delete messages, a notification is sent.
  - If the Discord API rate limit is exceeded, an appropriate message is sent.

### Commands

1. **`/clear_bot_messages` (slash command)**  
   **Description:** Deletes messages sent by the bot.  
   **Parameters:**
   - `limit` (int): The number of messages to delete (default is 20, max is 20).  
   **Example usage:** `/clear_bot_messages limit:10` — deletes the last 10 bot messages.

2. **`!clear_bot_messages` or `!clear_bot` (prefix command)**  
   **Description:** Similar to the slash command, but used with the prefix.  
   **Parameters:**
   - `limit` (int): The number of messages to delete (default is 10, max is 20).  
   **Example usage:** `!clear_bot_messages 15` — deletes the last 15 bot messages.

### Example Interaction

1. The user enters the command `/clear_bot_messages limit:10`.
2. The bot checks for bot messages in the channel.
3. If there are fewer than 10 bot messages, the bot notifies the user.
4. If there are enough messages, the bot deletes them and sends a message: `Deleted 10 bot messages`.

### Dependencies
- **Libraries:**
  - `discord`
  - `discord.ext.commands`

### Limitations
- The maximum number of messages that can be deleted in a single operation is 20.
- The bot must have the `Manage Messages` permission in the channel.

-----


# <a name="wise_wizardpy-module"></a>wise_wizard.py module

The wise_wizard.py module provides functionality for interacting with the ancient mage Baltazar, who answers questions in the style of Dungeons & Dragons using archaic language, proverbs, and metaphors via OpenAI.

## Main Features

### **Ask the Ancient Mage Baltazar the Wise**

- **Addressing the Wise Mage Baltazar:**
The module sends questions to the OpenRouter API with a predefined system prompt that sets the response style as if spoken by the ancient wizard Baltazar.

### 1. **/wise_wizard (Slash Command)**
- **Description:** Allows you to interact with the bot.
- **Usage Example:**
  - "/wise_wizard Tell me about a shortsword" — Ah, a shortsword! A weapon worthy of the nimble and cunning warriors. It is light in weight, swift in battle like a snake in the grass. Its damage is 1d6, and if the hand wielding it is skillful, the Dexterity modifier is added to the damage. For it is not brute strength but skill that decides the outcome of a duel.
  
### 2. !wise_wizard or !ask (Prefix Command)
- **Description:** Functions similarly to the slash command but is invoked using a prefix.


### Dependencies
- Libraries:
- discord
- discord.ext.commands
- asyncio
- dotenv
- os
- openai


### Environment Variables:
- `OPENROUTER_API_KEY – the key to access the OpenRouter API`.