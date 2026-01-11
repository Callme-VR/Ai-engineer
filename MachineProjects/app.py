import requests
import streamlit as st

# config files
API_BASE = "http://127.0.0.1:8000"
TMDB_IMG = "https://image.tmdb.org/t/p/w500"

st.set_page_config(
    page_title="Movie Recommendation",
    layout="wide",
    page_icon="🎬"
)

# styles and markdown with python on streamlit
st.markdown(
    """
<style>
.block-container { padding-top: 1rem; padding-bottom: 2rem; max-width: 1400px; }
.small-muted { color:#6b7280; font-size: 0.92rem; }
.movie-title { font-size: 0.9rem; line-height: 1.15rem; height: 2.3rem; overflow: hidden; }
.card { border: 1px solid rgba(0,0,0,0.08); border-radius: 16px; padding: 14px; background: rgba(255,255,255,0.7); }
</style>
""",
    unsafe_allow_html=True,
)

# state and routing (single-file pages)
if "view" not in st.session_state:
    st.session_state.view = "home"

if "selected_tmdb_id" not in st.session_state:
    st.session_state.selected_tmdb_id = None

qp_view = st.query_params.get("view")
qp_id = st.query_params.get("id")

if qp_view in ("home", "details"):
    st.session_state.view = qp_view
    if qp_id:
        try:
            st.session_state.selected_tmdb_id = int(qp_id)
            st.session_state.view = "details"
        except:
            pass


def goto_home():
    st.session_state.view = "home"
    st.query_params["view"] = "home"
    if "id" in st.query_params:
        del st.query_params["id"]
    st.rerun()


def goto_details(tmdb_id: int):
    st.session_state.view = "details"
    st.session_state.selected_tmdb_id = int(tmdb_id)
    st.query_params["view"] = "details"
    st.query_params["id"] = str(int(tmdb_id))
    st.rerun()


# api helper functions
@st.cache_data(ttl=300)
def api_get_json(path: str, params: dict | None = None):
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=25)
        if r.status_code >= 400:
            return None, f"{r.status_code}:{r.text[:300]}"
        return r.json(), None
    except Exception as e:
        return None, f"Request failed: {e}"


def poster_grid(cards, cols=6, key_prefix="grid"):
    if not cards:
        st.info("NO movies to Show")
        return

    rows = (len(cards) + cols - 1) // cols
    idx = 0

    for r in range(rows):
        colset = st.columns(cols)
        for c in range(cols):
            if idx >= len(cards):
                break

            m = cards[idx]
            idx += 1

            tmdb_id = m.get("tmdb_id")
            title = m.get("title", "Unknown")
            poster = m.get("poster_url", "")

            with colset[c]:
                if poster:
                    st.image(poster, width='stretch')
                else:
                    st.write("No poster available")

                if st.button("Open", key=f"{key_prefix}_{r}_{c}_{idx}_{tmdb_id}"):
                    if tmdb_id:
                        goto_details(tmdb_id)

                st.markdown(
                    f"<div class='movie-title'>{title}</div>",
                    unsafe_allow_html=True,
                )


def to_cards_From_Tfidf_items(tfidf_items):
    cards = []
    for X in tfidf_items or []:
        tmdb = X.get("tmdb") or {}
        if tmdb.get("tmdb_id"):
            cards.append(
                {
                    "tmdb_id": tmdb.get("tmdb_id"),
                    "title": tmdb.get("title"),
                    "poster_url": tmdb.get("poster_url"),
                }
            )
    return cards


def parse_tmdb_search_to_cards(data, keyword: str, limit: int = 25):
    keyword_l = keyword.strip().lower()

    if isinstance(data, dict) and "results" in data:
        results = data.get("results", [])
        raw_items = []
        for m in results:
            title = (m.get("title") or "").strip()
            tmdb_id = m.get("id")
            poster_path = m.get("poster_path")
            if not title or not tmdb_id:
                continue

            raw_items.append(
                {
                    "tmdb_id": int(tmdb_id),
                    "title": title,
                    "poster_url": TMDB_IMG + poster_path if poster_path else "",
                    "release_date": m.get("release_date", ""),
                }
            )

    elif isinstance(data, list):
        raw_items = data
    else:
        raw_items = []

    matches = [x for x in raw_items if keyword_l in x["title"].lower()][:limit]
    final_list = matches if matches else raw_items[:limit]

    suggestions = []
    for x in final_list[:10]:
        year = (x.get("release_date") or "").split("-")[0]
        suggestions.append((f"{x['title']} ({year})", x["tmdb_id"]))

    cards = [
        {
            "tmdb_id": x["tmdb_id"],
            "title": x["title"],
            "poster_url": x["poster_url"],
            "release_date": x["release_date"],
        }
        for x in final_list
    ]

    return suggestions, cards


# sidebar
with st.sidebar:
    st.title("🎬 Menu")

    if st.button("🏡 Home"):
        goto_home()

    st.markdown("---")
    st.markdown("Home Feed (only home)")

    home_category = st.selectbox(
        "Category",
        ["Trending", "Popular", "Top_Rated", "Now_Playing", "Upcoming"],
        index=0,
    )

    grid_cols = st.slider("Grid Columns", 4, 8, 6)


# header
st.title("🎬 Movie Explorer")
st.markdown(
    "<div style='color: #666;'>Discover trending, popular, and top-rated movies with ease.</div>",
    unsafe_allow_html=True,
)

st.divider()

# HOME VIEW
if st.session_state.view == "home":
    typed = st.text_input("Search Movies", placeholder="Enter movie name")
    st.divider()

    if typed.strip():
        if len(typed.strip()) < 2:
            st.caption("Please enter at least 2 characters to search.")
        else:
            data, err = api_get_json("/tmdb/search", params={"query": typed.strip()})
            if err or data is None:
                st.error(f"Failed to fetch movies: {err}")
            else:
                suggestions, cards = parse_tmdb_search_to_cards(
                    data, typed.strip(), limit=24
                )

                if suggestions:
                    labels = ["Select a Movie--"] + [s[0] for s in suggestions]
                    selected = st.selectbox("Suggestions", labels, index=0)

                    if selected != "Select a Movie--":
                        label_to_id = {s[0]: s[1] for s in suggestions}
                        goto_details(label_to_id[selected])
                else:
                    st.info("No suggestions found, please try again")

                st.markdown("### Results")
                poster_grid(cards, cols=grid_cols, key_prefix="search_results")

    else:
        st.markdown(f"### 🏠 Home — {home_category.replace('_', ' ').title()}")

        home_cards, err = api_get_json(
            "/home", params={"category": home_category, "limit": 24}
        )

        if err or not home_cards:
            st.error(f"Home feed failed: {err or 'Unknown error'}")
        else:
            poster_grid(home_cards, cols=grid_cols, key_prefix="home_feed")

# DETAILS VIEW
if st.session_state.view == "details":
    tmdb_id = st.session_state.selected_tmdb_id

    if not tmdb_id:
        st.warning("No selected movie found")
        goto_home()
        st.stop()

    a, b = st.columns([3, 1])
    with a:
        st.markdown("## 🎬 Movie Details")
    with b:
        if st.button("← Back to Home"):
            goto_home()

    data, err = api_get_json(f"/movie/id/{tmdb_id}")
    if err or not data:
        st.error(f"Failed to fetch movie details: {err}")
        st.stop()

    left, right = st.columns([1, 2], gap="large")

    with left:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        if data.get("poster_url"):
            st.image(data["poster_url"], width='stretch')
        else:
            st.write("🌆 NO poster available for this movie")
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"## {data.get('title','')}")
        release = data.get("release_date") or "-"
        genres = ", ".join([g["name"] for g in data.get("genres", [])]) or "-"
        st.markdown(
            f"<div class='small-muted'>Release: {release}</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<div class='small-muted'>Genres: {genres}</div>",
            unsafe_allow_html=True,
        )
        st.markdown("---")
        st.markdown("### Overview")
        st.write(data.get("overview") or "No overview available.")
        st.markdown("</div>", unsafe_allow_html=True)

    if data.get("backdrop_url"):
        st.markdown("#### Backdrop")
        st.image(data["backdrop_url"], width='stretch')

    st.divider()
    st.markdown("### ✅ Recommendations")
    
    # for fetching the recommendations
    
    title=(data.get("title") or "").strip()
    if title:
        bundle, err2 = api_get_json("/movie/search", params={"query": title, "genre_limit": 12, "tfidf_top_n": 12})
        if not err2 and bundle:
            st.markdown("### 🔍 Similar Movies (TF-IDF)")
            tfidf_cards = to_cards_From_Tfidf_items(bundle.get("TFIDF_RECOMMENDATIONS"))
            if tfidf_cards:
                poster_grid(
                    tfidf_cards,
                    cols=grid_cols,
                    key_prefix="Detailed_TFIDF_genre"
                )
            else:
                st.info("No TF-IDF recommendations found.")

            st.markdown("### 🎭 Similar Movies (Genre)")
            genre_cards = bundle.get("GENRE_RECOMMENDATIONS", [])
            if genre_cards:
                poster_grid(
                    genre_cards,
                    cols=grid_cols,
                    key_prefix="Detailed_Genre"
                )
            else:
                st.info("No genre recommendations found.")
        else:
            st.warning("Could not fetch recommendations.")
