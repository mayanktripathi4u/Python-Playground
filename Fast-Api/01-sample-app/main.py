from fastapi import FastAPI

app = FastAPI()

@app.get("/") # App Decorator
def read_root():
    return {"Hello": "World"}


