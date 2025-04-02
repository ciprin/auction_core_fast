import asyncio
from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import init_db, AsyncSessionLocal, engine
from models.auction_model import Auction, User, Base
from services.auction_service import place_bid_optimistic


async def setup_test_data():
    """Initialize database and create test data"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        if not (await db.execute(select(User.id).limit(1))).scalar_one_or_none():
            db.add_all([
                User(username="test_user1"),
                User(username="test_user2")
            ])
            await db.commit()

        auction = (await db.execute(select(Auction).limit(1))).scalar_one_or_none()
        if not auction:
            auction = Auction(
                item_name="Test Item",
                current_bid=100,
                version_id=1,
                end_time=datetime.utcnow() + timedelta(days=1),
                is_closed=False
            )
            db.add(auction)
            await db.commit()
        return auction


async def test_concurrent_bids():
    auction = await setup_test_data()

    async with AsyncSessionLocal() as db:
        auction = await db.get(Auction, auction.id)

        bid_requests = [
            {"auction_id": auction.id, "user_id": 1, "amount": 110 + i}
            for i in range(5)
        ]

        tasks = [place_bid_optimistic(db, bid) for bid in bid_requests]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        print("\n=== Test Results ===")
        for i, result in enumerate(results):
            status = "Success" if not isinstance(result, Exception) else f"Failed - {str(result)}"
            print(f"Bid {i + 1}: {status}")

        await db.refresh(auction)
        print(f"\nFinal auction state: {auction.current_bid} (Version: {auction.version_id})")


if __name__ == "__main__":
    asyncio.run(test_concurrent_bids())