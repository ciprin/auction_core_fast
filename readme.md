# 🏷️ Auction System (FastAPI + SQLAlchemy)

A high-performance auction platform with:
- ✅ Optimistic concurrency control

[//]: # (- 🔔 Real-time WebSocket notifications)
- ⏰ Automated auction closing
- 🧪 Concurrent bid testing

## 🚀 Quick Start

### 1. Installation
```bash
git clone https://github.com/yourrepo/auction-system.git
cd auction-system
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
pip install -r requirements.txt
```
### 2.Initialize Database

```bash
python -c "from database import init_db; import asyncio; asyncio.run(init_db())"
Creates auction.db with test users (test_user1, test_user2)
```

### 3. Run the Server

```bash
uvicorn main:app --reload
```
➡️ http://localhost:8000


## 🔍 API Endpoints

Method	Endpoint	Description

POST	/auctions/	Create new auction 

POST	/bids/	Place a bid

GET	/users/	Retrieve all users

GET	/bids/	Retrieve all bids

GET	/auctions/	Retrieve all auctions

GET	/debug/	View database state


🧪 Testing Concurrency

### 1. Run Concurrency Test

```bash
# First clean existing DB (optional)
rm auction.db

# Run the test
python tests/test_concurrency.py
```
Expected Output:

```
=== Test Results ===
Bid 1: ...
!! Not working... !!!

```

## 🛠️ Manual Testing (CURL)

```bash
# Create auction
curl -X POST "http://localhost:8000/auctions/" \
-H "Content-Type: application/json" \
-d '{"item_name":"Rare Painting", "end_time":"2025-12-31T23:59:59"}'

# Place bid
curl -X POST "http://localhost:8000/bids/" \
-H "Content-Type: application/json" \
-d '{"auction_id":1, "user_id":1, "amount":500}'

# View debug info
curl http://localhost:8000/debug/
```

## 🐛 Troubleshooting

Error	Solution

no such table	Run init_db() again

Concurrent modification	Expected behavior for failed bids

datetime format error	Use ISO format: YYYY-MM-DDTHH:MM:SS

## 📦 Dependencies

Python 3.9+
FastAPI
SQLAlchemy 2.0+
aiosqlite
WebSockets

## 🛡️ Concurrency Model

```
sequenceDiagram
    Bidder 1->>Server: POST /bids/ (Amount: 110)
    Bidder 2->>Server: POST /bids/ (Amount: 120)
    Server->>Database: Check version_id
    Database-->>Server: version_id=1
    Server->>Database: Update (version_id=2)
    Server->>Bidder 2: 409 Conflict (Version changed)
```
## Happy bidding! 🎟️