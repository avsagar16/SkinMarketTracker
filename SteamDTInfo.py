import requests
#import os
from dotenv import load_dotenv
import json
from pymongo import MongoClient
from SteamInfo import SteamInventoryModel

#cs_base_url = "https://csfloat.com/api/v1/listings"
cs_base_url = "	https://open.steamdt.com/open/cs2/v1/base"
class SteamDTModel:
    def __init__(self):
        pass
    def get_float_info(self, name):
        with open("config.json") as f:
            config = json.load(f)
        
        API_KEY = config["STEAMDT_API_KEY"]
        headers = {"Authorization": API_KEY}
        print(headers)
        response = requests.get(cs_base_url, headers = headers)
        if response.status_code == 200:
            #data = response.json()
            MHN =  "AK-47 | Aquamarine Revenge (Minimal Wear)" #Market Hash Name
            url = f"https://open.steamdt.com/open/cs2/v1/price/avg?marketHashName={MHN}"

            payload={}
            response = requests.request("GET", url, headers=headers, data=payload)

            print(response.text)
            #print(response.status_code)
        else:
            print(f"Failed to retrieve data {response.status_code}")
        return cs_base_url
        pass

model = SteamDTModel()
model.get_float_info("check")