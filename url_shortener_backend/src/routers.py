from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from models import Url
import string
import random
from urllib.parse import urlparse

router = APIRouter()

LENGTH_SHORT_URL = 6
BASE_URL = "http://localhost:8000"
url_mapping = {}

def find_url(url_mapping, url_to_check):
    for short_url, url_info in url_mapping.items():
        if url_info['url'] == url_to_check:
            return short_url
    return None

def generate_short_url():
    while True:
        short_url = ''.join(random.choices(string.ascii_uppercase + string.digits, k=LENGTH_SHORT_URL))
        if short_url not in url_mapping:
            return short_url
        
def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

@router.post("/shorten")
def create_short_url(url: Url):
    if not is_valid_url(url.url):
        raise HTTPException(status_code=400, detail="Invalid URL provided.")
    try:
        short_url = find_url(url_mapping, url.url)
        if not short_url:
            short_url = generate_short_url()
            url_mapping[short_url] = {'url': url.url, 'visits': 0}
        return JSONResponse(status_code=200, content={"shortUrl": f"{BASE_URL}/{short_url}"})
    except KeyError as e:
        raise HTTPException(status_code=400, detail="Invalid URL provided.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")


@router.get("/{short_url}")
def redirect(short_url: str):
    try:
        if short_url not in url_mapping:
            raise HTTPException(status_code=404, detail="Short URL not found")
        url_mapping[short_url]['visits'] += 1
        print(url_mapping)
        return RedirectResponse(url=url_mapping[short_url]['url'])
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"message": e.detail})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})