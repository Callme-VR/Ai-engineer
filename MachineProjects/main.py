# =========================
# Imports
# =========================

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


# =========================
# Environment Setup
# =========================

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE = "https://api.themoviedb.org/3"
TMDB_IMG_500 = "https://image.tmdb.org/t/p/w500"

if not TMDB_API_KEY:
    raise ValueError("TMDB_API_KEY is missing in the .env file")


# =========================
# FastAPI App + CORS
# =========================

app = FastAPI(
    title="Movie Recommendation System",
    description="Movie Recommendation System",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# File Paths
# =========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DF_PATH = os.path.join(BASE_DIR, "df.pkl")
INDICES_PATH = os.path.join(BASE_DIR, "indices.pkl")
TFIDF_MATRIX_PATH = os.path.join(BASE_DIR, "tfidf_matrix.pkl")
TFIDF_OBJECT_PATH = os.path.join(BASE_DIR, "tfidf.pkl")


# =========================
# Global Objects (loaded once)
# =========================

df: Optional[pd.DataFrame] = None
indices_obj: Any = None
tfidf_matrix: Any = None
tfidf_object: Any = None

TITLE_TO_INDEX: Optional[Dict[str, int]] = None


# =========================
# Pydantic Models
# =========================

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


# =========================
# Utility Functions
# =========================

def _norm_TITLE(t: str) -> str:
    return str(t).strip().lower()


def MAKE_IMAGE_URL(path: Optional[str]) -> Optional[str]:
    if not path:
        return None
    return f"{TMDB_IMG_500}{path}"


# =========================
# TMDB API Helpers
# =========================

async def TMDB_get(path: str, params: Dict[str, Any]) -> Dict[str, Any]:
    q = dict(params)
    q["api_key"] = TMDB_API_KEY

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(f"{TMDB_BASE}{path}", params=q)
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=500,
            detail=f"TMDB request error: {type(e).__name__} | {repr(e)}"
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail=f"TMDB error {response.status_code}: {response.text}"
        )

    return response.json()


async def TMDB_CARD_FROM_RESULT(
    results: List[Dict],
    limit: int = 30
) -> List[TMDBMOVIES_CARD]:

    out: List[TMDBMOVIES_CARD] = []

    for m in (results or [])[:limit]:
        out.append(
            TMDBMOVIES_CARD(
                tmdb_id=int(m.get("id")),
                title=m.get("title") or m.get("name") or "",
                poster_url=MAKE_IMAGE_URL(m.get("poster_path")),
                release_date=m.get("release_date"),
                vote_average=m.get("vote_average"),
            )
        )

    return out


async def TMDB_MOVIE_DETAILS(movie_id: int) -> TMDBMOVIESDETAILS:
    data = await TMDB_get(f"/movie/{movie_id}", {"language": "en-US"})

    return TMDBMOVIESDETAILS(
        tmdb_id=int(data["id"]),
        title=data.get("title") or data.get("name") or "",
        overview=data.get("overview") or "",
        release_date=data.get("release_date"),
        poster_url=MAKE_IMAGE_URL(data.get("poster_path")),
        backdrop_url=MAKE_IMAGE_URL(data.get("backdrop_path")),
        genres=data.get("genres") or [],
    )


async def TMDB_SEARCH_MOVIES(query: str, page: int = 1) -> Dict[str, Any]:
    return await TMDB_get(
        "/search/movie",
        {
            "query": query,
            "page": page,
            "language": "en-US",
            "include_adult": "false",
        },
    )


async def TMDB_SEARCH_FIRST(query: str) -> Optional[Dict]:
    data = await TMDB_SEARCH_MOVIES(query=query, page=1)
    results = data.get("results", [])
    return results[0] if results else None


# =========================
# TF-IDF Helpers
# =========================

def Build_TITLE_TO_INDEX_MAP(indices: Any) -> Dict[str, int]:
    title_to_idx: Dict[str, int] = {}

    if isinstance(indices, dict):
        for k, v in indices.items():
            title_to_idx[_norm_TITLE(k)] = int(v)
        return title_to_idx

    try:
        for k, v in indices.items():
            title_to_idx[_norm_TITLE(k)] = int(v)
        return title_to_idx
    except Exception as e:
        raise RuntimeError(f"Failed to build title-index map: {e}")


def get_local_IDX_BY_title(title: str) -> int:
    global TITLE_TO_INDEX

    if TITLE_TO_INDEX is None:
        raise HTTPException(
            status_code=500,
            detail="Title-to-index mapping not loaded"
        )

    key = _norm_TITLE(title)
    if key not in TITLE_TO_INDEX:
        raise HTTPException(
            status_code=404,
            detail=f"Movie '{title}' not found in dataset"
        )

    return TITLE_TO_INDEX[key]


def Tfidf_RECOMMEND_TITLES(
    query_title: str,
    top_n: int = 10
) -> List[Tuple[str, float]]:

    global df, tfidf_matrix

    if df is None or tfidf_matrix is None:
        raise HTTPException(
            status_code=500,
            detail="TF-IDF model not loaded"
        )

    idx = get_local_IDX_BY_title(query_title)

    qv = tfidf_matrix[idx]
    scores = (tfidf_matrix @ qv.T).toarray().ravel()

    order = np.argsort(scores)[::-1]

    out: List[Tuple[str, float]] = []

    for i in order:
        if int(i) == int(idx):
            continue

        try:
            title_i = str(df.iloc[int(i)]["title"])
        except Exception:
            continue

        out.append((title_i, float(scores[i])))

        if len(out) >= top_n:
            break

    return out


async def ATTACH_TMDB_CARD_BY_TITLE(title: str) -> Optional[TMDBMOVIES_CARD]:

    try:
        m = await TMDB_SEARCH_FIRST(title)
        if not m:
            return None

        return TMDBMOVIES_CARD(
            tmdb_id=int(m["id"]),
            title=m.get("title") or m.get("name") or "",
            poster_url=MAKE_IMAGE_URL(m.get("poster_path")),
            release_date=m.get("release_date"),
            vote_average=m.get("vote_average"),
        )
    except Exception:
        return None
    # end try


# ================================== #
# startup:LOAD PICKLES
# ======================================#

# ==================================
# Startup: LOAD PICKLES
# ==================================

@app.on_event("startup")
def Load_pickel():
    global df, indices_obj, tfidf_matrix, tfidf_object, TITLE_TO_INDEX

    # Load dataframe
    with open(DF_PATH, "rb") as f:
        df = pickle.load(f)

    # Load indices
    with open(INDICES_PATH, "rb") as f:
        indices_obj = pickle.load(f)

    # Load TF-IDF matrix (scipy sparse matrix)
    with open(TFIDF_MATRIX_PATH, "rb") as f:
        tfidf_matrix = pickle.load(f)

    # Load TF-IDF vectorizer (optional)
    with open(TFIDF_OBJECT_PATH, "rb") as f:
        tfidf_object = pickle.load(f)

    # Build normalized title → index map
    TITLE_TO_INDEX = Build_TITLE_TO_INDEX_MAP(indices_obj)

    # Sanity check
    if df is None or "title" not in df.columns:
        raise RuntimeError(
            "df.pkl must contain a DataFrame with a 'title' column"
        )

# ============================#
# routes
# ============================#


@app.get("/health")
#  for example taken as enpoint is health
async def health():
    return {"status": "ok"}


# ======================================#
# for the homes feed
# =====================================#
