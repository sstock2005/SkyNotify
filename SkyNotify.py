from discord_webhook import DiscordWebhook
import configparser
from numerize import numerize
import requests
import logging
import time
import os

log_file = f'./logs/{time.ctime().split(":")[0].replace(" ", "_")}.log'

if os.path.exists("./logs") == False:
    os.mkdir("./logs")

if os.path.exists("./player_data") == False:
    os.mkdir("./player_data")

if os.path.isfile(log_file) == False:
    open(log_file, 'a').close()

logger = logging.getLogger(__name__)
logging.basicConfig(filename=log_file, encoding='utf-8', level=logging.ERROR)

config = configparser.ConfigParser()

config.read("config.secret")

api_token = config["API"]["TOKEN"]
discord_webhook = config["DISCORD"]["WEBHOOK"]

def uuid(username) -> str:
    json = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}").json()

    try:
        return json["id"]
    except:
        logger.error(json["errorMessage"])
        return None

def username(uuid) -> str:
    json = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}").json()

    try:
        return json["name"]
    except:
        logger.error(json["errorMessage"])
        return None
    
def update(players, api_token):
    for player in players:

        if player == None:
            continue

        json = requests.get(f"https://api.hypixel.net/v2/skyblock/auction?player={player}", headers={"API-Key":api_token}).json()
        
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
                            notify(player, new_uuid)
                        else:
                            updated_saved_auction_list.append(f"{new_uuid}:{new_claimed}")
                        break
            
            with open(f"./player_data/{player}.data", 'w') as f:
                for u in updated_saved_auction_list:
                    f.write(u + '\n')

def get_auction_info(auction_uuid):
    json = requests.get(f"https://api.hypixel.net/v2/skyblock/auction?uuid={auction_uuid}", headers={"API-Key":api_token}).json()

    item_name = json["auctions"][0]["item_name"]
    bid = json["auctions"][0]["highest_bid_amount"]

    return item_name, bid

def notify(player_uuid, auction_uuid):

    item_name, bid = get_auction_info(auction_uuid)

    content = f"{username(player_uuid)}, your {item_name} has sold for {numerize.numerize(bid)}!"

    webhook = DiscordWebhook(url=discord_webhook, content=content)

    webhook.execute()

if __name__ == '__main__':

    while(True):
        players = [uuid("USERNAME HERE")]
        update(players, api_token)
        time.sleep(300)
