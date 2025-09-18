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
        with open("config.json") as f:
            config = json.load(f)
        self.API_KEY =  config["STEAMDT_API_KEY"]
        self.headers = {"Authorization": self.API_KEY}
        self.url = f"https://open.steamdt.com"
        pass


    def get_float_info(self, name):
        #with open("config.json") as f:
            #config = json.load(f)
        
        #API_KEY = config["STEAMDT_API_KEY"]
        #headers = {"Authorization": API_KEY}
        #print(headers)
        response = requests.get(cs_base_url, headers = self.headers)
        if response.status_code == 200:
            #data = response.json()
            MHN =  "AK-47 | Aquamarine Revenge (Minimal Wear)" #Market Hash Name
            url = f"https://open.steamdt.com/open/cs2/v1/float?marketHashName={MHN}"

            payload={}
            response = requests.request("GET", url, headers = self.headers, data=payload)

            print(response.text)
            #print(response.status_code)
        else:
            print(f"Failed to retrieve data {response.status_code}")
        return cs_base_url
    

    def get_batch_price(self, marketHashNames):
        
        response = requests.get(cs_base_url, headers = self.headers)
        if response.status_code == 200:
            #data = response.json()
            url = "https://open.steamdt.com/open/cs2/v1/price/batch"

            payload = json.dumps({
              "marketHashNames": marketHashNames
            })
            headers = {
              'Authorization': self.API_KEY,
              'Content-Type': 'application/json'
            }
            response = requests.request("POST", url, headers=headers, data=payload)

            print(response.text)
            #print(response.status_code)
        else:
            print(f"Failed to retrieve data {response.status_code}")
        return cs_base_url
        pass

    

model = SteamDTModel()
MHN =  "AK-47 | Aquamarine Revenge (Minimal Wear)"
lst = [MHN]
#lst = ['AUG | Sweeper (Factory New)', 'Kilowatt Case', 'MAC-10 | Storm Camo (Minimal Wear)', 'Recoil Case', 'Prisma 2 Case', 'Chroma 2 Case', 'Snakebite Case', 'Clutch Case', 'MAC-10 | Sakkaku (Field-Tested)', 'StatTrak™ P2000 | Gnarled (Battle-Scarred)', 'StatTrak™ PP-Bizon | Runic (Battle-Scarred)', 'UMP-45 | Roadblock (Field-Tested)', 'Dual Berettas | Melondrama (Minimal Wear)', 'MAC-10 | Ensnared (Field-Tested)', 'USP-S | Ticket to Hell (Field-Tested)', 'Five-SeveN | Coolant (Field-Tested)', 'Five-SeveN | Orange Peel (Field-Tested)', 'PP-Bizon | Wood Block Camo (Minimal Wear)', 'UMP-45 | Facility Dark (Factory New)', 'Tec-9 | Blue Blast (Battle-Scarred)', 'Souvenir R8 Revolver | Desert Brush (Minimal Wear)', 'Souvenir P90 | Verdant Growth (Field-Tested)', 'Souvenir M249 | Midnight Palm (Minimal Wear)', 'Souvenir SG 553 | Bleached (Field-Tested)', 'Tec-9 | Rebel (Field-Tested)', 'FAMAS | Palm (Minimal Wear)', 'MP5-SD | Lime Hex (Field-Tested)', 'Dual Berettas | Royal Consorts (Minimal Wear)', 'FAMAS | Mecha Industries (Field-Tested)', 'MAC-10 | Pipe Down (Minimal Wear)', "M4A1-S | Chantico's Fire (Minimal Wear)", 'UMP-45 | K.O. Factory (Field-Tested)', 'Nova | Predator (Battle-Scarred)', 'Sawed-Off | Spirit Board (Battle-Scarred)', 'Zeus x27 | Swamp DDPAT (Battle-Scarred)', 'M4A1-S | Vaporwave (Field-Tested)', 'AK-47 | Neon Rider (Field-Tested)', 'StatTrak™ MAG-7 | Insomnia (Battle-Scarred)', 'UMP-45 | Facility Dark (Field-Tested)', 'AWP | Crakow! (Field-Tested)', 'Five-SeveN | Scrawl (Well-Worn)', 'Sticker | ENCE (Glitter) | Antwerp 2022', 'Sticker | Natus Vincere (Glitter) | Shanghai 2024', 'Desert Eagle | Crimson Web (Field-Tested)', 'Sticker | Kawaii Eyes (Glitter)', 'StatTrak™ Galil AR | Eco (Field-Tested)', 'MAC-10 | Saibā Oni (Minimal Wear)', 'StatTrak™ Five-SeveN | Hybrid (Minimal Wear)', 'StatTrak™ FAMAS | Rapid Eye Movement (Minimal Wear)', '★ Driver Gloves | Imperial Plaid (Field-Tested)', '★ Talon Knife | Ultraviolet (Field-Tested)', 'SG 553 | Basket Halftone (Minimal Wear)', 'Sawed-Off | Spirit Board (Well-Worn)', "StatTrak™ Music Kit | Neck Deep, Life's Not Out To Get You", 'Special Agent Ava | FBI', 'AK-47 | The Empress (Field-Tested)', 'StatTrak™ XM1014 | Mockingbird (Well-Worn)', 'Glock-18 | Shinobu (Well-Worn)', 'P250 | Visions (Field-Tested)', 'StatTrak™ Dual Berettas | Flora Carnivora (Battle-Scarred)', 'Zeus x27 | Tosai (Factory New)', 'Five-SeveN | Sky Blue (Field-Tested)', 'USP-S | The Traitor (Minimal Wear)', 'StatTrak™ XM1014 | Mockingbird (Field-Tested)', 'G3SG1 | VariCamo (Minimal Wear)', 'Nova | Rain Station (Minimal Wear)', 'MP9 | Starlight Protector (Minimal Wear)', 'Galil AR | Green Apple (Minimal Wear)', 'SSG 08 | Acid Fade (Factory New)', 'Trapper | Guerrilla Warfare', 'XM1014 | Blue Spruce (Battle-Scarred)', 'Tec-9 | Tiger Stencil (Field-Tested)', 'AUG | Storm (Battle-Scarred)', 'FAMAS | Meow 36 (Battle-Scarred)', 'MP7 | Forest DDPAT (Field-Tested)', 'MAG-7 | Insomnia (Battle-Scarred)', 'StatTrak™ SG 553 | Cyberforce (Battle-Scarred)', 'Glock-18 | Winterized (Well-Worn)', 'Tec-9 | Urban DDPAT (Field-Tested)', 'StatTrak™ P90 | Randy Rush (Battle-Scarred)', 'M4A4 | Poly Mag (Well-Worn)', 'Nova | Sand Dune (Battle-Scarred)', 'Sealed Graffiti | Ninja (SWAT Blue)', 'Sealed Graffiti | Worry (Desert Amber)', 'Sealed Graffiti | Chess King (Tracer Yellow)', 'SG 553 | Waves Perforated (Field-Tested)', 'Galil AR | VariCamo (Field-Tested)', 'Five-SeveN | Orange Peel (Battle-Scarred)']
model.get_batch_price(lst)