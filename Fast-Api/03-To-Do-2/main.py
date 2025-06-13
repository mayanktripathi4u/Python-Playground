from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class ItemCls(BaseModel):
    text: str = None
    is_done: bool = False


items = []

@app.get("/")
def root():
    return {"Displaying all Items": items}

@app.post("/items")
def create_item(item: ItemCls):
    items.append(item)
    # return {"item": item}
    return {"message": "Item {item} created successfully", "Final items List": items}


@app.get("/items/{item_id}", response_model=ItemCls)
def read_item(item_id: int) -> ItemCls:
    if item_id < len(items):
        return {"item": items[item_id]}
    else:
        # return {"error": "Item not found"}
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")

@app.get("/items", response_model=list[ItemCls])
def list_items(limit: int = 10, offset: int = 0):
    return {"items": items[offset:offset + limit]}


 