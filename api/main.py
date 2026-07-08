from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ==========================================
# GOD-MODE CORS
# ==========================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "ak_kzh26w17kjlek0fs09teeq34"
USER_EMAIL = "24f2002227@ds.study.iitm.ac.in"

# ==========================================
# BULLETPROOF ROUTING
# ==========================================
@app.post("/")
@app.post("/analytics")
@app.post("/api/analytics")
async def analytics(request: Request):
    # --- 1. AUTHENTICATION ---
    # FastAPI automatically lowercases header names for lookup
    client_key = request.headers.get("x-api-key")
    if client_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # --- 2. PARSE BODY ---
    try:
        body = await request.json()
    except Exception:
        body = {}
        
    events = body.get("events", [])
    
    # --- 3. AGGREGATION LOGIC ---
    total_events = len(events)
    unique_users = set()
    revenue = 0.0
    user_revenue = {}

    for event in events:
        u = event.get("user", "")
        amt = float(event.get("amount", 0.0))
        
        unique_users.add(u)
        
        # Only process positive amounts per instructions
        if amt > 0:
            revenue += amt
            user_revenue[u] = user_revenue.get(u, 0.0) + amt
    
    # --- 4. FIND TOP USER ---
    top_user = ""
    max_rev = -1.0
    for u, r in user_revenue.items():
        if r > max_rev:
            max_rev = r
            top_user = u
            
    # --- 5. RETURN RESPONSE ---
    return {
        "email": USER_EMAIL,
        "total_events": total_events,
        "unique_users": len(unique_users),
        "revenue": revenue,
        "top_user": top_user
    }
