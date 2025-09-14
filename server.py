from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json

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
async def process_input(data: InputData):
    try:
        print(f"✅ Successfully received: {data}")
        print(f"Input text: '{data.input}'")
        print(f"Timestamp: {data.timestamp}")
        
        return {
            "status": "success", 
            "message": f"You typed: {data.input}",
            "received_timestamp": data.timestamp,
            "length": len(data.input)
        }
    except Exception as e:
        print(f"❌ Error processing data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Add this to debug what's actually being received
@app.middleware("http")
async def debug_requests(request, call_next):
    if request.method == "POST" and "/api/process" in str(request.url):
        body = await request.body()
        print(f"🔍 Raw request body: {body}")
        try:
            json_body = json.loads(body)
            print(f"🔍 Parsed JSON: {json_body}")
        except:
            print("❌ Could not parse JSON from request body")
    
    response = await call_next(request)
    return response

@app.get("/")
async def root():
    return {"message": "FastAPI server is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")