from fastapi import FastAPI, UploadFile, File
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome from the API"}

@app.post("/{style}")
def get_image(style: str, file:UploadFile = File(...)):
    pass


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)


     