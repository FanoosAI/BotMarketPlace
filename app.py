from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# handle corse
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
async def root():
    return {"message": "Welcome to the BOT Marketplace backend server. See /docs for api documentations."}

@app.get("/public-bots")
async def public_bots():
    pass

@app.post("/register")
async def register_bot():
    pass
