import requests
#import os
from dotenv import load_dotenv
import json
from pymongo import MongoClient

cs_base_url = "https://csfloat.com/api/v1/listings"

def get_float_info(name):
    with open("config.json") as f:
        config = json.load(f)
    
    API_KEY = config["API_KEY"]
    headers = {"Authorization": API_KEY}
    response = requests.get(cs_base_url, headers = headers)
    if response.status_code == 200:
        data = response.json()
        print(data)
        return data
    else:
        print(f"Failed to retrieve data {response.status_code}")
    return cs_base_url
    pass