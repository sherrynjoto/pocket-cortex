from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os, httpx

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://hirvwvmctmgsjweedonk.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

def headers():
    return {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json", "Prefer": "return=representation"}

@app.get("/")
def root():
    return {"status": "Pocket Cortex API is running"}

@app.get("/trades")
async def get_trades():
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{SUPABASE_URL}/rest/v1/trades?order=open_time.asc&limit=10000", headers=headers())
    return res.json()

@app.post("/trade")
async def add_trade(request: Request):
    trade = await request.json()
    trade.pop("id", None)
    async with httpx.AsyncClient() as client:
        res = await client.post(f"{SUPABASE_URL}/rest/v1/trades", headers=headers(), json=trade)
    return {"message": "Trade saved", "data": res.json()}

@app.delete("/trades")
async def clear_trades():
    async with httpx.AsyncClient() as client:
        await client.delete(f"{SUPABASE_URL}/rest/v1/trades?id=neq.0", headers=headers())
    return {"message": "Cleared"}
