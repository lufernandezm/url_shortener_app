from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from models import Url
from utils import is_valid_url
from controllers import find_url, generate_short_url, add_url, get_url, increment_visitis_counter, get_visits_counter

BASE_URL = "http://localhost:8000"

router = APIRouter() 


@router.post("/shorten")
def create_short_url(url: Url):
    if not is_valid_url(url.url):
        raise HTTPException(status_code=400, detail="Invalid URL provided.")
    try:
        short_url = find_url(url.url)
        if not short_url:
            short_url = generate_short_url()
            add_url(short_url, url.url)
        return JSONResponse(status_code=200, content={"shortUrl": f"{BASE_URL}/{short_url}"})
    except KeyError as e:
        raise HTTPException(status_code=400, detail="Invalid URL provided.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")


@router.get("/{short_url}")
def redirect(short_url: str):
    try:
        shortened_url = get_url(short_url)
        if shortened_url is None:
            raise HTTPException(status_code=404, detail="Short URL not found")
        increment_visitis_counter(short_url)
        return RedirectResponse(url=shortened_url)
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"message": e.detail})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

@router.get("/short_url_visits/{short_url}")
def get_visits(short_url: str):
    try:
        visits = get_visits_counter(short_url)
        return JSONResponse(status_code=200, content={"visits": f"{visits}"})
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"message": e.detail})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})
    