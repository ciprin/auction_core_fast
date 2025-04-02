from pydantic import BaseModel
from datetime import datetime

class AuctionCreate(BaseModel):
    item_name: str
    end_time: datetime

class BidCreate(BaseModel):
    auction_id: int
    user_id: int
    amount: float