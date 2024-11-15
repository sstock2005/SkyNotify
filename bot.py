from typing import Optional
from discord import app_commands
from datetime import datetime
from numerize import numerize
import configparser
import aiohttp
import discord
import logging
import aiohttp
import asyncio
import time
import os

log_file = f'./logs/{time.ctime().split(":")[0].replace(" ", "_")}.log'

if os.path.exists("./logs") == False:
    os.mkdir("./logs")

if os.path.exists("./player_data") == False:
    os.mkdir("./player_data")

if os.path.exists("./discord_data") == False:
    os.mkdir("./discord_data")

if os.path.isfile(log_file) == False:
    open(log_file, 'a').close()

logger = logging.getLogger(__name__)
logging.basicConfig(encoding='utf-8',
                    format=('%(filename)s:%(levelname)s:%(funcName)s():%(lineno)d:\t%(message)s'),
                    level=logging.ERROR,
                    handlers=[
                        logging.FileHandler(log_file),
                        logging.StreamHandler()])

config = configparser.ConfigParser()

config.read("config.secret")

api_token = config["API"]["TOKEN"]
discord_token = config["DISCORD"]["TOKEN"]
admin_id = config["DISCORD"]["ADMIN"]

async def uuid(username) -> Optional[str]:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"https://api.mojang.com/users/profiles/minecraft/{username}") as response:
                if response.status == 204:
                    return None
                    
                if response.status != 200:
                    logger.error(f"Failed to get UUID for {username}. Status: {response.status}")
                    return None
                    
                json = await response.json()
                return json["id"]
                
        except aiohttp.ClientError as e:
            logger.error(f"Network error while getting UUID for {username}: {e}")
            return None
        except KeyError as e:
            logger.error(f"Invalid response format for {username}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error while getting UUID for {username}: {e}")
            return None

async def username(uuid) -> Optional[str]:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}") as response:
                if response.status == 204:
                    return None
                    
                if response.status != 200:
                    logger.error(f"Failed to get username for {uuid}. Status: {response.status}")
                    return None
                    
                json = await response.json()
                return json["name"]
                
        except aiohttp.ClientError as e:
            logger.error(f"Network error while getting username for {uuid}: {e}")
            return None
        except KeyError as e:
            logger.error(f"Invalid response format for {uuid}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error while getting username for {uuid}: {e}")
            return None

async def update(players, api_token):
    async with aiohttp.ClientSession() as session:
        for player in players:
            if player is None:
                continue

            # Fetch auction data
            async with session.get(
                f"https://api.hypixel.net/v2/skyblock/auction?player={player}",
                headers={"API-Key": api_token}
            ) as response:
                json = await response.json()
        
        player_auctions = []

        for auction in json["auctions"]:
            uuid = auction["uuid"]
            claimed = auction["claimed"]

            player_auctions.append(f"{uuid}:{claimed}")

        if os.path.isfile(f"./player_data/{player}.data") == False:
            with open(f"./player_data/{player}.data", "w") as f:
                for b in player_auctions:
                    f.write(b + "\n")
        else:
            saved_auction_list = []
            with open(f"./player_data/{player}.data", "r") as f:
                saved_auctions = f.readlines()
                
                for saved_auction in saved_auctions:
                    saved_auction_list.append(saved_auction.strip())

            updated_saved_auction_list = []
            for new in player_auctions:
                new_uuid = new.split(":")[0]
                new_claimed = new.split(":")[1]

                for old in saved_auction_list:

                    old_uuid = old.split(":")[0]
                    old_claimed = old.split(":")[1]

                    if new_uuid == old_uuid:
                        if old_claimed != new_claimed:
                            await client.notify(player, new_uuid)
                        else:
                            updated_saved_auction_list.append(f"{new_uuid}:{new_claimed}")
                        break
            
            with open(f"./player_data/{player}.data", 'w') as f:
                for u in updated_saved_auction_list:
                    f.write(u + '\n')

async def get_auction_info(auction_uuid):
    async with aiohttp.ClientSession() as session:
        url = f"https://api.hypixel.net/v2/skyblock/auction?uuid={auction_uuid}"
        headers = {"API-Key": api_token}
        
        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                return "NA", 0
            
            json_data = await response.json()
            
            if not json_data.get("success", False):
                return "NA", 0
            
            if not json_data.get("auctions"):
                return "NA", 0
            
            auction = json_data["auctions"][0]
            item_name = auction["item_name"]
            bid = auction["highest_bid_amount"]
            
            return item_name, bid

class SkyNotifier(discord.Client):
    def __init__(self, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.should_run = True
        self.u_task = None

    async def setup_hook(self):
        await self.tree.sync()
        self.u_task = self.loop.create_task(self.update_task())

    async def update_task(self):
        await self.wait_until_ready()

        while self.should_run:
            try:
                print("[#] Background Task Started!")

                players = []

                files = os.listdir("./discord_data")

                files = [f for f in files if os.path.isfile("./discord_data"+'/'+f)]

                for file in files:
                    player = file.replace(".data", "")
                    players.append(player)

                await update(players, api_token)

                await asyncio.sleep(300)
            except Exception as e:
                logger.error(f"Error in the update task: {str(e)}")
                await asyncio.sleep(5)

    async def notify(self, player: str, uuid: str):

        if os.path.isfile(f"./discord_data/{player}.data") == False:
            return

        with open(f"./discord_data/{player}.data", "r") as f:
            lines = f.readlines()
        
        for line in lines:
            print(f"[DEBUG] player = {line}")
            user = await client.fetch_user(int(line.strip()))
            if user == None:
                logger.error(f"Could not find user {user}")
                return
            
            item_name, highest_bid = await get_auction_info(uuid)

            embed = discord.Embed(title="An Auction Sold!", url=f"https://sky.coflnet.com/auction/{uuid}", description="An auction from a tracked player has sold!", timestamp=datetime.now())
            embed.add_field(name="Item Name", value=item_name, inline=True)
            embed.add_field(name="Highest Bid", value=numerize.numerize(highest_bid), inline=False)
            embed.add_field(name="Auction ID", value=uuid, inline=False)
            embed.set_footer(text="Made By Sam Stockstrom", icon_url="https://avatars.githubusercontent.com/u/144393153?v=4")

            await user.send(embed=embed)

            logger.info(f"Notified {line} about {player}'s auction ({uuid})")

    async def close(self):
        self.should_run = False
        if self.u_task:
            self.u_task.cancel()
        await super().close()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = SkyNotifier(intents=intents)

@client.event
async def on_ready():
    print(f"[#] {client.user} (ID: {client.user.id}) ONLINE")

@client.tree.command()
async def help(interaction: discord.Interaction):
    """Displays valid commands"""
    await interaction.response.send_message(
        "**/help** displays this page\n" +
        "**/track** *username* adds the given username to the list of tracked players",
        ephemeral=True)
    
@client.tree.command()
@app_commands.describe(username='The minecraft username of the player you want to track')
async def track(interaction: discord.Interaction, username: str):
    """Adds the given username to the list of tracked players"""

    discord_user = str(interaction.user.id)
    minecraft_user = await uuid(username)

    if minecraft_user == None:
        await interaction.response.send_message("Could not find a minecraft player with that username!", ephemeral=True)
        return
    
    print(f"User {discord_user} added {username} to tracking")

    if os.path.isfile(f"./discord_data/{minecraft_user}.data") == False:
        with open(f"./discord_data/{minecraft_user}.data", "w") as f:
            f.write(discord_user + "\n")
    else:
        with open(f"./discord_data/{minecraft_user}.data", "a") as f:
            f.write(discord_user + "\n")

    await interaction.response.send_message(f"Added {username} to your tracking list!", ephemeral=True)

async def main_test():
    players = [await uuid("TimeCandy")]

    await update(players, api_token)

if __name__ == '__main__':
    try:
        client.run(discord_token)
        # asyncio.run(main_test())

    except KeyboardInterrupt:
        client.loop.run_until_complete(client.close())