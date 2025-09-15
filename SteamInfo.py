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
            #with open("latest_inventory.json", "w") as f:
                #json.dump(assets, f, indent=4)
            print(f"Retrieved {len(assets)} assets from inventory.")
            return inventory_data
        else:
            print(f"Failed to retrieve inventory: {response.status_code}")
        
        return None
    
    def get_all_market_hash_names(self):
        """
        Get market_hash_name for all marketable items in a Steam inventory
        
        Returns:
            List of dictionaries containing asset_id and market_hash_name of all marketable items
        """
        # Get full inventory data
        inventory_data = self.get_steam_inventory()
        if not inventory_data:
            return []
        
        assets = inventory_data.get('assets', [])
        #with open("inventory_assets.json", "w") as f:
            #json.dump(assets, f, indent=4)
        descriptions = inventory_data.get('descriptions', [])
        #with open("inventory_description.json", "w") as f:
            #json.dump(descriptions, f, indent=4)
        
        # Create lookup dictionary for descriptions
        desc_lookup = {}
        for desc in descriptions:
            key = f"{desc['classid']}_{desc['instanceid']}"
            desc_lookup[key] = desc
        
        # Extract market_hash_name for each asset
        items = []
        for asset in assets:
            key = f"{asset['classid']}_{asset['instanceid']}"
            description = desc_lookup.get(key, {})
            is_marketable = description.get('marketable', 0) == 1
            if is_marketable:
                item = {
                    'asset_id': asset['assetid'],
                    'market_hash_name': description.get('market_hash_name', 'Unknown'),
                    'market_name': description.get('market_name', 'Unknown'),
                    'name': description.get('name', 'Unknown'),
                    'type': description.get('type', ''),
                    'tradable': description.get('tradable', 0),
                    'marketable': description.get('marketable', 0),
                    'instance_id': asset['instanceid'],
                    'class_id': asset['classid'],
                    'amount': int(asset.get('amount', 1))
                }
                items.append(item)
        items = self.group_all_items_simple(items)
        print(f"Found {len(items)} marketable items in inventory.")
        return items
    
    def group_all_items_simple(self, items):
        """
        Simple version - group all items by market_hash_name
        """
        """ITEMS GROUPED WILL MOST LIKELY HAVE INCORRECT INSTANCE_ID AND CLASS_ID"""
        item_groups = {}
        
        for item in items:
            market_hash_name = item.get('market_hash_name', '')
            
            if market_hash_name in item_groups:
                # Just increment the amount
                item_groups[market_hash_name]['amount'] += item.get('amount', 1)
            else:
                # Store the item (copy to avoid reference issues)
                item_groups[market_hash_name] = item.copy()
        
        return list(item_groups.values())

#with open("config.json") as f:
    #config = json.load(f) #STEAM_ID
#STEAM_ID = config["STEAM_ID"]
#steam_inventory_model = SteamInventoryModel(steam_id=STEAM_ID)
#inventory = steam_inventory_model.get_all_market_hash_names()
#get_float_info("check")

