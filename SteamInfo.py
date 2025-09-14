import requests
#import os
from dotenv import load_dotenv
import json
from pymongo import MongoClient

#url = "https://cat-fact.herokuapp.com"
#url = "https://csfloat.com/api/v1/listings/<ID>"

class SteamInventoryModel:
    def __init__(self, steam_id, app_id = 730, context_id = 2):
        self.steam_id = steam_id
        self.app_id = app_id
        self.context_id = context_id

        pass
    def get_steam_inventory(self):

        #Args:
        # steam_id (str): The Steam ID of the user whose inventory you want to fetch. ex. 742348293472
        # app_id (int, optional): The App ID of the game whose inventory you want to fetch. Default is 730 (CS:GO/CS2).

        #Returns:
        # dict: A dictionary containing the user's inventory data if successful, otherwise None.
        url = f"https://steamcommunity.com/inventory/{self.steam_id}/{self.app_id}/{self.context_id}"
        results = {}
        print(f"Fetching inventory for Steam ID: {self.steam_id}, App ID: {self.app_id}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            inventory_data = response.json()
            #print(data)
            #return data
            assets = inventory_data.get('assets', [])
            print(assets)
            return assets
        else:
            print(f"Failed to retrieve inventory: {response.status_code}")
        
        return None

with open("config.json") as f:
    config = json.load(f) #STEAM_ID
STEAM_ID = config["STEAM_ID"]
steam_inventory_model = SteamInventoryModel(steam_id=STEAM_ID)
steam_inventory_model.get_steam_inventory(STEAM_ID)

#get_float_info("check")

