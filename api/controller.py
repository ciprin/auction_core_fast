from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.auction_model import Auction, Bid, User
from schemas.auction_schema import AuctionCreate, BidCreate
from services.auction_service import create_auction, place_bid_optimistic
from database import get_db

router = APIRouter()

@router.post("/auctions/")
async def create_new_auction(auction: AuctionCreate, db: AsyncSession = Depends(get_db)):
    return await create_auction(db, auction.dict())

@router.post("/bids/")
async def place_bid(bid: BidCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await place_bid_optimistic(db, bid.dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/users/")
async def list_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    return result.scalars().all()

# get all bids from database
@router.get("/bids/")
async def list_bids(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Bid))
    return result.scalars().all()

#  ge tall auctions from database
@router.get("/auctions/")
async def list_auctions(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Auction))
    return result.scalars().all()

@router.get("/debug/")
async def debug(db: AsyncSession = Depends(get_db)):
    return {
        "users": (await db.execute(select(User))).scalars().all(),
        "auctions": (await db.execute(select(Auction))).scalars().all(),
        "bids": (await db.execute(select(Bid))).scalars().all()
    }