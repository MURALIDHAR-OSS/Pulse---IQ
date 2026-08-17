from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.products import router as products_router

app = FastAPI(title="PulseIQ API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(products_router, prefix="/api/v1")


@app.get("/")
def home() -> dict[str, str]:
    return {"message": "PulseIQ API is running."}
