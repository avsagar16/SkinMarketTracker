from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json
from SteamInfo import SteamInventoryModel
from processor import Processor

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class InputData(BaseModel):
    text: str
    timestamp: Optional[str] = None

@app.post("/api/process")
async def process_input(request: Request):
    try:
        # Get the raw JSON data
        body = await request.json()
        print(f"Received data: {body}")
        
        user_input = body.get("input", "")
        timestamp = body.get("timestamp", "")
        
        print(f"Processing: '{user_input}'")
        if Processor.verify_steam_id(user_input): #check if input is a valid steam id
            print("Valid Steam ID detected.")
            steam_model = SteamInventoryModel(steam_id=user_input)
            inventory = steam_model.get_all_market_hash_names()
            with open('json_outputs/latest_inventory.json', 'w') as f:
                json.dump(inventory, f, indent=4)

            if inventory is not None:
                return {
                    "status": "success",
                    "message": f"Inventory fetched for Steam ID: {user_input}",
                    "timestamp": timestamp,
                    "inventory": inventory
                }
            else:
                return {
                    "status": "error",
                    "message": f"Failed to fetch inventory for Steam ID: {user_input}",
                    "timestamp": timestamp
                }
        
        print(f"Invalid Steam ID '{user_input}'")
        return {
            "status": "error",
            "message": f"You typed an invalid Steam ID: {user_input}",
            "timestamp": timestamp,
            "length": len(user_input)
        }
    except Exception as e:
        print(f"Error: {e}")
        return {"status": "error", "message": str(e)}

# Add this to debug what's actually being received
#@app.middleware("http")
#async def debug_requests(request, call_next):
    #if request.method == "POST" and "/api/process" in str(request.url):
    #    body = await request.body()
    #    print(f"Raw request body: {body}")
    #    try:
    #        json_body = json.loads(body)
    #       print(f"Parsed JSON: {json_body}")
    #    except:
    #       print("Could not parse JSON from request body")
    
    #response = await call_next(request)
    #return response

@app.get("/")
async def root():
    return {"message": "FastAPI server is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")