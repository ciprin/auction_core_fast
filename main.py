from fastapi import FastAPI
from api.controller import router as auction_router
from tasks.scheduler import start_scheduler
from database import engine, get_db, init_db

app = FastAPI()
app.include_router(auction_router)

@app.on_event("startup")
async def startup():
    # db = next(get_db())
    await init_db()
    start_scheduler()
