from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import router as url_router
import os

LENGTH_SHORT_URL = 6
BASE_URL = "http://localhost:8000"

app = FastAPI()


origins = [
    os.getenv("CLIENT_ORIGIN", "http://localhost:3000"),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(url_router)