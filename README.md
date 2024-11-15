# SkyNotify

A Discord bot that tracks Hypixel Skyblock auction sales and notifies users via DM when their tracked players complete an auction.

## Features

- Track specific Minecraft players' auction activities
- Receive real-time Discord DM notifications when tracked players sell items
- Detailed auction information including:
  - Item name
  - Final bid amount
  - Auction ID
  - Direct link to auction details
- Simple command interface
- Background monitoring system

## Installation
[Add the bot with this link!](https://sstock.dev/skynotify)  

## Prerequisites

- Python 3.7+
- [Discord Bot Token](https://discord.com/developers/applications)
- [Hypixel API Key](https://developer.hypixel.net/)

## Self-Host Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/skynotify.git
cd skynotify
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Edit `config.secret.example` file with your API tokens and save it as `config.secret`:
```ini
[API]
TOKEN=https://developer.hypixel.net/

[DISCORD]
TOKEN=https://discord.com/developers/applications
ADMIN=https://support.discord.com/hc/en-us/articles/4407571667351-How-to-Find-User-IDs-for-Law-Enforcement
```

## Usage

### Starting the Bot

Run the script:
```bash
python bot.py
```

### Commands

- `/help` - Displays available commands
- `/track <username>` - Adds a Minecraft username to your tracking list

## Todo
- Add `/remove <username>` - Removes the Minecraft username from your tracking list
- Add `/list` - Lists the Minecraft username from your tracking list

## Directory Structure

The bot automatically creates these directories if they don't exist:
- `./logs/` - Contains bot operation logs
- `./player_data/` - Stores auction data for tracked players
- `./discord_data/` - Maintains user tracking preferences

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[LICENSE](LICENSE)

## Acknowledgments

- Uses the Hypixel API for auction data
- Built with discord.py
- Auction links provided by CoflNet's Sky.Coflnet.com
