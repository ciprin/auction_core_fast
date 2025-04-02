from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from models.auction_model import Base, Auction  # Make sure to import Base from your models
from models.auction_model import User

# Base = declarative_base()

DATABASE_URL = "sqlite+aiosqlite:///./auction.db"
engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    async with AsyncSessionLocal() as db:
        yield db


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

        # Hardcodăm 2 useri pentru testare
        async with AsyncSessionLocal() as db:
            if not (await db.execute(select(User))).scalars().first():
                db.add_all([
                    User(username="test_user1"),
                    User(username="test_user2"),
                    Auction(
                        item_name="Test Item",
                        current_bid=100,
                        version_id=1,
                        end_time=datetime.utcnow() + timedelta(days=1),
                        is_closed=False
                    )
                ])
                await db.commit()
