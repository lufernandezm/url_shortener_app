from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse
from pydantic import BaseModel
import string
import random
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

class Url(BaseModel):
    url: str

url_mapping = {}

def find_url(url_mapping, url_to_check):

    for short_url, url_info in url_mapping.items():
        if url_info['url'] == url_to_check:
            return short_url
    return None

def generate_short_url():
    """Generate a random short URL of fixed length."""
    while True:
        short_url = ''.join(random.choices(string.ascii_uppercase + string.digits, k=LENGTH_SHORT_URL))
        if short_url not in url_mapping:
            return short_url

@app.post("/shorten")
def create_short_url(url: Url):
    try:
        short_url = find_url(url_mapping, url.url)
        print(short_url)
        print(url_mapping)
        if not short_url:
            short_url = generate_short_url()
            url_mapping[short_url] = {'url': url.url, 'visits': 0}
        return JSONResponse(status_code=200, content={"shortUrl": f"{BASE_URL}/{short_url}"})
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})

@app.get("/{short_url}")
def redirect(short_url: str):
    try:
        if short_url not in url_mapping:
            raise HTTPException(status_code=404, detail="Short URL not found")
        url_mapping[short_url]['visits'] += 1
        return RedirectResponse(url=url_mapping[short_url]['url'])
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"message": e.detail})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})