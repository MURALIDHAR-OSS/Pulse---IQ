from fastapi import FastAPI

app = FastAPI()
@app.get("/")
def home():
    return {"message": "PulseIQ Backend is running!"}