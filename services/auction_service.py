from select import select

from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import StaleDataError

from models.auction_model import Auction, Bid, User


async def create_auction(db: AsyncSession, auction_data: dict):
    db_auction = Auction(**auction_data)
    db.add(db_auction)
    await db.commit()
    return db_auction


async def place_bid_optimistic(db: AsyncSession, bid_data: dict):
    user = await db.get(User, bid_data["user_id"])
    if not user:
        raise ValueError("User not found")

    stmt = select(Auction).where(
        Auction.id == bid_data["auction_id"],
        Auction.is_closed == False
    )
    result = await db.execute(stmt)
    auction = result.scalar_one_or_none()

    if not auction:
        raise ValueError("Auction not found or already closed")

    if bid_data["amount"] <= auction.current_bid:
        raise ValueError("Bid amount must be higher than current bid")

    update_stmt = (
        update(Auction)
        .where(
            Auction.id == bid_data["auction_id"],
            Auction.version_id == auction.version_id  # Verificare versiune
        )
        .values(
            current_bid=bid_data["amount"],
            version_id=Auction.version_id + 1
        )
    )

    try:
        result = await db.execute(update_stmt)
        if result.rowcount == 0:  # Dacă niciun rând nu a fost actualizat
            await db.rollback()
            raise ValueError("Concurrent modification detected")

        db.add(Bid(
            auction_id=auction.id,
            user_id=user.id,
            amount=bid_data["amount"]
        ))
        await db.commit()

        return {
            "auction_id": auction.id,
            "bid_amount": bid_data["amount"],
            "new_version": auction.version_id + 1,
            "status": "bid_accepted"
        }

    except SQLAlchemyError as e:
        await db.rollback()
        raise ValueError(f"Database error: {str(e)}")

#
# async def place_bid_optimistic(db: AsyncSession, bid_data: dict):
#     # Check if user exists
#     user = await db.get(User, bid_data["user_id"])
#     if not user:
#         raise ValueError("User not found")
#
#     # Check if auction exists
#     auction = await db.get(Auction, bid_data["auction_id"])
#     if not auction:
#         raise ValueError("Auction not found")
#
#     if auction.is_closed:
#         raise ValueError("Auction is already closed")
#
#     if bid_data["amount"] <= auction.current_bid:
#         raise ValueError("Bid amount must be higher than current bid")
#
#     try:
#         auction.current_bid = bid_data["amount"]
#         auction.version_id += 1
#         # Create bid record
#         db.add(Bid(
#             auction_id=auction.id,
#             user_id=user.id,
#             amount=bid_data["amount"]
#         ))
#         await db.commit()
#         return {"auction_id": auction.id, "bid_amount": bid_data["amount"], "status": "bid_accepted"}
#
#     except StaleDataError:
#         await db.rollback()
#         raise ValueError("Auction updated by another user. Please try again.")
