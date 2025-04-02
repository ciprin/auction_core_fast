# tasks/scheduler.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select

from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from models.auction_model import Auction
from datetime import datetime

scheduler = AsyncIOScheduler()


async def close_expired_auctions():
    async for db in get_db():  # Proper async iteration
        stmt = select(Auction).where(
            Auction.end_time <= datetime.utcnow(),
            Auction.is_closed == False
        )
        result = await db.execute(stmt)
        auctions = result.scalars().all()
        for auction in auctions:
            auction.is_closed = True
        await db.commit()
        break  # Only need one session


def start_scheduler():
    scheduler.add_job(close_expired_auctions, 'interval', minutes=1)
    scheduler.start()
