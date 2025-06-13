from fastapi import FastAPI, HTTPException

app = FastAPI()

items = []

@app.get("/")
def root():
    return {"Displaying all Items": items}

@app.post("/items")
def create_item(item: str):
    items.append(item)
    # return {"item": item}
    return {"message": "Item {item} created successfully", "Final items List": items}


@app.get("/items/{item_id}")
def read_item(item_id: int) -> str:
    if item_id < len(items):
        return {"item": items[item_id]}
    else:
        # return {"error": "Item not found"}
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")

@app.get("/items")
def list_items(limit: int = 10, offset: int = 0):
    return {"items": items[offset:offset + limit]}


 