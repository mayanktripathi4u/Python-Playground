from fastapi import FastAPI
# import uvicorn

app = FastAPI()

@app.get("/") # App Decorator
# This decorator defines a route for the root URL ("/") of the application.
# When a GET request is made to this URL, the function `read_root` will be executed.
# The function returns a JSON response with a greeting message.
# The response will be in the format: {"Hello": "World"}
def read_root():
    return {"Hello": "World - other than main.py"}

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)


# # This script creates a simple FastAPI application that returns a JSON response with a greeting message.
# # The application runs on the default host and port (8000).

