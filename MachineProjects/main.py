import os
import pickle
from typing import Optional, List, Dict, Any, Tuple

import numpy as np
import pandas as pd
import httpx
import streamlit as st

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel, Field
from dotenv import load_dotenv

# load the env variables from env
# using the this below function


load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE = "https://api.themoviedb.org/3"
TMDB_IMG_500 = "https://image.tmdb.org/t/p/w500"

# for the failure realted issue

if not TMDB_API_KEY:
    raise ValueError("TMDB_API_KEY is Missing in the .env file")

# for the cors issue

app = FastAPI(title="Movie Recommendation System",
              description="Movie Recommendation System", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=[
                   "*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


# pickle for the global variables


# for the path of the files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
df_Path = os.path.join(BASE_DIR, "df.pkl")
INDICES_PATH = os.path.join(BASE_DIR, "indices.pkl")
TFIDF_MATRIX_PATH = os.path.join(BASE_DIR, "tfidf.pkl")
TFIDF_PATH = os.path.join(BASE_DIR, "tfidf.pkl")


# why is this used below->

df: Optional[pd.DataFrame] = None
indices_obj: Any = None
tdidf_matrix: Any = None
tfidf_object: Any = None

TITLE_TO_INDEX: Optional[Dict[str, int]] = None


# for the models and it working and fetching


class TMDBMOVIES_CARD(BaseModel):
    tmdb_id: int
    title: str
    poster_url: Optional[str] = None
    release_date: Optional[str] = None
    vote_average: Optional[float] = None


class TMDBMOVIESDETAILS(BaseModel):
    tmdb_id: int
    title: str
    overview: str
    release_date: Optional[str] = None
    poster_url: Optional[str] = None
    backdrop_url: Optional[str] = None
    genres: List[Dict] = Field(default_factory=list)


class TFIDFRECITEM(BaseModel):
    title: str
    score: float
    tmdb: Optional[TMDBMOVIES_CARD] = None


class SEARCHBUNDLERESPONSE(BaseModel):
    query: str
    movies_details: TMDBMOVIESDETAILS
    TFIDF_RECOMMENDATIONS: List[TFIDFRECITEM]
    GENRE_RECOMMENDATIONS: List[TMDBMOVIES_CARD]


# some major utility functions for the actions
# for the loading the files

def _norm_TITLE(t: str) -> str:
    return str(t).strip().lower()


def MAKE_IMAGE_URL(path: Optional[str]) -> Optional[str]:
    if path is None:
        return None
    return f'{TMDB_IMG_500}{path}'


async def TMDB_get(path: str, params: Dict[str, Any]) -> Dict[str, Any]:
    q = dict(params)
    q["api_key"] = TMDB_API_KEY

    # try block for better error handling

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(f'{TMDB_BASE}{path}', params=q)

    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=500, detail=f'TMDB REQUEST ERROR:{type(e).__name__}|{repr(e)}')

    if response.status_code != 200:
        raise HTTPException(
            status_code=502, detail=f'TMDB Error {response.status_code}:{response.text}')

    return response.json()


async def TMDB_CARD_FROM_RESULT(results: List[Dict], limit: int = 30) -> List[TMDBMOVIES_CARD]:
    # out is here an object which stores the data of the movies
    out: List[TMDBMOVIES_CARD] = []

    for m in (results or [])[:limit]:
        out.append(
            TMDBMOVIES_CARD(
                tmdb_id=int(m.get("id")),
                title=m.get("title") or m.get("name") or " ",
                poster_url=MAKE_IMAGE_URL(m.get("poster_path")),
                release_date=m.get("release_date"),
                vote_average=m.get("vote_average")
            )
        )

    return out


async def TBDM_MOVIES_DETAILS(movies_id: int) -> TMDBMOVIESDETAILS:

    data = await TMDB_get(f'/movie/{movies_id}', {"language": "en-US"})
    return TMDBMOVIESDETAILS(
        tmdb_id=int(data["id"]),
        title=data.get("title") or data.get("name") or " ",
        overview=data.get("overview") or " ",
        release_date=data.get("release_date"),
        poster_url=MAKE_IMAGE_URL(data.get("poster_path")),
        backdrop_url=MAKE_IMAGE_URL(data.get("backdrop_path")),
        genres=data.get("genres") or []
    )


async def TMDB_SEARCH_MOVIES(Query: str, page: int = 1) -> List[str, Any]:

    return await TMDB_get('/search/movie', {"query": Query, "page": page, "language": "en-US", include_Adult: "false"})


async def TMDB_SEARCH_FIRST(Query: str) -> Optional[dict]:
    data = await TMDB_SEARCH_MOVIES(query=Query, page=1)
    result = data.get("results", [])
    return result[0] if result else None
