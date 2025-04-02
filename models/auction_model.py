from datetime import datetime

from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean, ForeignKey, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    bids = relationship("Bid", back_populates="user")


class Auction(Base):
    __tablename__ = "auctions"
    id = Column(Integer, primary_key=True)
    item_name = Column(String, nullable=False)
    current_bid = Column(Float, default=0.0)
    version_id = Column(Integer, default=1)
    end_time = Column(DateTime, nullable=False)
    is_closed = Column(Boolean, default=False)
    Index('ix_auction_version', id, version_id)  # Index compus


class Bid(Base):
    __tablename__ = "bids"
    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    auction_id = Column(Integer, ForeignKey("auctions.id"))
    user = relationship("User", back_populates="bids")
    auction = relationship("Auction")
