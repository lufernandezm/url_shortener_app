from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse
from pydantic import BaseModel
from routers import router as url_router
import os

LENGTH_SHORT_URL = 6
BASE_URL = "http://localhost:8000"

app = FastAPI()
app.include_router(url_router)

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

