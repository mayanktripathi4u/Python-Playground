import json
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
import redis

app = FastAPI(title="Exchange Rate API")
r = redis.Redis(host="redis", port=6379, db=0)
"""
In Redis, db=0 specifies that you want to use database number 0.
Redis supports multiple logical databases, numbered from 0 (default) up to a configurable limit (usually 15).
Each database is independent and isolated from the others.
"""

class Currency(BaseModel):
    name: str
    value: float

class DB(BaseModel):
    data: List[Currency]


db = DB(data=[])
data = json.load(open('all_currenc.json', "r"))

@app.get("/")
def index():
    try:
        history = r.execute_command("GET", "counter1")
        return {"history":history}
    except:
        return {'key': 'value'}
    
@app.post('/currency')
def create_currency(currency: Currency):
    db.data.append(currency)
    return currency.dict() # Return last object from db list


@app.get('/currency/{currency_id}')
def get_currency_by_id(currency_id: str):
    r.incr("counter1")
    try:
        return data[currency_id]
    except:
        return {"error": "no data"}
    
@app.get('/currency/')
def get_all_currency():
    return data

@app.delete('/currency/{currency_id}')
def delete_currency(currency_id: str):
    for index, key in enumerate(db.data):
        for k, v in key:
            if k == 'name' and v == currency_id:
                db.data.opo(index)
                return {"deleted": "successfully"}
    return {"error": "no data"}
