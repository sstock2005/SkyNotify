# SkyNotify

SkyNotify is a Python script that monitors Hypixel Skyblock player auctions and notifies a Discord channel when an item is sold. The script uses the Hypixel API and posts updates to a specified Discord webhook, making it easy for players to track their auctions in real-time. Currently, users can specify the usernames they wish to track, and notifications will be automatically sent to Discord. In future updates, SkyNotify aims to become a fully functional Discord bot for easier interaction.

## Features

- Tracks Hypixel Skyblock auctions for specified players.
- Sends a notification to a Discord webhook when an item is sold.
- Easy-to-use configuration with a simple `config.secret` file.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/sstock2005/SkyNotify.git
   cd SkyNotify
   ```

2. **Install the required Python packages:**

   Make sure you have [Python](https://www.python.org/downloads/) installed. Install the requirements with:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the API Token and Discord Webhook:**

   Create a `config.secret` file in the project directory and add your Hypixel API token and Discord webhook URL as follows:

   ```ini
   [API]
   TOKEN=your_hypixel_api_token

   [DISCORD]
   WEBHOOK=your_discord_webhook_url
   ```

4. **Add the Usernames to Track:**

   Open the main script (e.g., `SkyNotify.py`) and add the Minecraft usernames of players you want to track on **line 119**:

   ```python
   players = [uuid("USERNAME_HERE")]
   ```

## Usage

To start tracking auctions and sending notifications:

```bash
python SkyNotify.py
```

The script will run continuously, checking for auction updates every 5 minutes. Each time an item is sold, a message will be sent to your Discord channel via the specified webhook.

## Logging

SkyNotify creates log files to store errors and other information, which can be helpful for debugging. Logs are stored in the `logs/` directory.

## Future Plans

- Implementing SkyNotify as a Discord bot for easier setup and management.
- Allowing dynamic addition/removal of usernames to track without modifying the code.
- Improved auction data tracking and analytics.

## Contributing

Feel free to submit issues or pull requests to help improve SkyNotify. Your contributions are welcome!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
