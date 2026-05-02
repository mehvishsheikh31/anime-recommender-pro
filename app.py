import streamlit as st
import pickle
import pandas as pd
import os

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="ANI-MIND | Crimson Onyx",
    page_icon="👹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;600;700&display=swap');

    .stApp { background-color: #000000; }
    html, body, [class*="st-"] { color: #FFFFFF !important; font-family: 'Inter', sans-serif !important; }

    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background-color: #080808 !important;
        border-right: 2px solid #ff0000 !important;
    }
    [data-testid="collapsedControl"], [data-testid="stSidebarCollapsedControl"] {
        color: #ff0000 !important;
        background-color: #111111 !important;
        border: 1px solid #ff0000 !important;
        border-radius: 5px !important;
    }
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p {
        color: #FFFFFF !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    [data-testid="stSidebar"] div[data-testid="stMetricValue"],
    [data-testid="stSidebar"] span { color: #ff0000 !important; }

    /* DROPDOWNS */
    div[data-baseweb="select"] > div {
        background-color: #1a1a1a !important;
        border: 1px solid #ff0000 !important;
    }
    div[data-baseweb="select"] div { color: #FFFFFF !important; }
    [data-baseweb="popover"] ul { background-color: #1a1a1a !important; }
    [data-baseweb="popover"] li { color: #FFFFFF !important; }
    [data-baseweb="popover"] li:hover { background-color: #ff0000 !important; }

    /* HERO */
    .hero-container {
        padding: 50px 20px;
        text-align: center;
        background: linear-gradient(180deg, #450000 0%, #000000 100%);
        border-bottom: 3px solid #ff0000;
        margin-bottom: 30px;
    }
    .hero-title {
        font-family: 'Bebas Neue', sans-serif !important;
        font-size: 6rem;
        letter-spacing: 20px;
        color: white;
        margin: 0;
        text-shadow: 0 0 40px #ff0000, 2px 2px 20px #ff0000;
    }
    .hero-sub {
        color: #aaaaaa;
        font-weight: 300;
        letter-spacing: 5px;
        font-size: 0.9rem;
        margin-top: 8px;
    }

    /* TABS */
    .stTabs [data-baseweb="tab-list"] { border-bottom: 1px solid #330000 !important; }
    .stTabs [aria-selected="true"] { color: #ff0000 !important; border-bottom: 2px solid #ff0000 !important; }
    .stTabs [aria-selected="false"] { color: #888 !important; }

    /* BUTTON */
    .stButton > button {
        background: linear-gradient(135deg, #cc0000, #ff0000) !important;
        color: white !important;
        font-weight: 700 !important;
        font-family: 'Bebas Neue', sans-serif !important;
        font-size: 1.1rem !important;
        letter-spacing: 2px !important;
        width: 100% !important;
        height: 3.5rem !important;
        border-radius: 8px !important;
        border: none !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(255,0,0,0.4) !important;
    }

    /* ANIME CARD */
    .anime-card {
        background: #0d0d0d;
        border: 1px solid #1f1f1f;
        border-radius: 12px;
        overflow: hidden;
        transition: all 0.3s ease;
        margin-bottom: 20px;
        position: relative;
    }
    .anime-card:hover {
        border-color: #ff0000;
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(255, 0, 0, 0.25);
    }
    .anime-card img {
        width: 100%;
        height: 320px;
        object-fit: cover;
        display: block;
    }
    .card-body {
        padding: 12px 15px 15px 15px;
    }
    .card-title {
        font-weight: 700;
        color: white;
        font-size: 0.95rem;
        height: 42px;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        margin-bottom: 8px;
    }
    .card-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 4px;
    }
    .badge {
        background: #1a1a1a;
        border: 1px solid #333;
        border-radius: 20px;
        padding: 2px 10px;
        font-size: 0.75rem;
        color: #ccc;
    }
    .badge.red { border-color: #ff0000; color: #ff4444; background: #1f0000; }
    .badge.gold { border-color: #ffd700; color: #ffd700; background: #1a1500; }

    .watchlist-btn {
        background: transparent !important;
        border: 1px solid #333 !important;
        border-radius: 6px !important;
        color: #888 !important;
        font-size: 0.75rem !important;
        padding: 3px 10px !important;
        height: auto !important;
        width: auto !important;
        transition: all 0.2s !important;
    }
    .watchlist-btn:hover {
        border-color: #ff0000 !important;
        color: #ff0000 !important;
    }

    /* DETAIL PANEL */
    .detail-panel {
        background: #0d0d0d;
        border: 1px solid #ff0000;
        border-radius: 12px;
        padding: 25px;
        margin-bottom: 20px;
    }
    .detail-title {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 2.2rem;
        color: white;
        letter-spacing: 3px;
        margin-bottom: 10px;
    }

    /* SEARCH INPUT */
    .stTextInput input {
        background-color: #111 !important;
        border: 1px solid #333 !important;
        color: white !important;
        border-radius: 8px !important;
    }
    .stTextInput input:focus {
        border-color: #ff0000 !important;
    }

    /* WATCHLIST EMPTY */
    .empty-watchlist {
        text-align: center;
        padding: 60px 20px;
        color: #444;
    }
    .empty-watchlist h3 { color: #333; font-size: 2rem; }

    /* SECTION HEADER */
    .section-header {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 1.6rem;
        color: #ff0000;
        letter-spacing: 4px;
        margin-bottom: 20px;
        border-bottom: 1px solid #1f1f1f;
        padding-bottom: 10px;
    }

    /* SELECTBOX */
    .stSelectbox label { color: #aaa !important; font-size: 0.85rem !important; }

    /* SCORE MATCH */
    .match-score {
        font-size: 0.7rem;
        color: #888;
        text-align: center;
        margin-top: 4px;
    }
</style>
""", unsafe_allow_html=True)


# --- SESSION STATE ---
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = []
if 'selected_detail' not in st.session_state:
    st.session_state.selected_detail = None


# --- LOAD DATA ---
@st.cache_resource
def load_data():
    base_path = os.path.dirname(__file__)
    folder_name = 'models'
    if not os.path.exists(os.path.join(base_path, folder_name)):
        folder_name = 'Models'

    anime_list_path = os.path.join(base_path, folder_name, 'anime_list.pkl')
    similarity_path = os.path.join(base_path, folder_name, 'similarity_matrix.pkl')

    if not os.path.exists(anime_list_path):
        st.error(f"Error: Could not find {anime_list_path}.")
        st.stop()

    df = pickle.load(open(anime_list_path, 'rb'))
    sim = pickle.load(open(similarity_path, 'rb'))

    df['genres_text'] = df['genres_text'].fillna('').astype(str)
    df['rate'] = pd.to_numeric(df['rate'], errors='coerce').fillna(0)
    if 'votes' in df.columns:
        df['votes'] = pd.to_numeric(df['votes'], errors='coerce').fillna(0)
    else:
        df['votes'] = 0

    popular_favorites = [
        "Attack on Titan", "Naruto", "Death Note", "One Piece",
        "Vinland Saga", "Spy x Family", "Demon Slayer", "Jujutsu Kaisen"
    ]
    top_picks = df[df['name'].isin(popular_favorites)].sort_values(by='rate', ascending=False)
    remaining = df[~df['name'].isin(popular_favorites)]
    ordered_df = pd.concat([top_picks, remaining]).reset_index(drop=True)

    all_genres = set()
    for g_string in ordered_df['genres_text']:
        if g_string:
            all_genres.update(g_string.split())

    return ordered_df, sim, sorted(list(all_genres))


anime_df, similarity, unique_genres = load_data()


# --- HELPER: RENDER ANIME CARD ---
def render_card(col, info, score=None, show_watchlist_btn=True):
    """Renders a single anime card into a given column."""
    name = info['name']
    rate = info['rate']
    img = info.get('image_url', '')
    genres = info.get('genres_text', '')
    votes = int(info.get('votes', 0))

    # Fallback image
    if not img or str(img) == 'nan':
        img = f"https://via.placeholder.com/400x600/1a1a1a/ed1c24?text={name[:10]}"

    genre_list = genres.split()[:3]
    genre_badges = " ".join([f'<span class="badge">{g}</span>' for g in genre_list])

    votes_str = f"{votes/1000:.1f}K" if votes >= 1000 else str(votes)
    score_html = f'<div class="match-score">MATCH SCORE: {score:.0%}</div>' if score is not None else ""

    with col:
        st.markdown(f"""
            <div class="anime-card">
                <img src="{img}" onerror="this.src='https://via.placeholder.com/400x600/1a1a1a/ed1c24?text=No+Image'" />
                <div class="card-body">
                    <div class="card-title">{name}</div>
                    <div class="card-meta">
                        <span class="badge gold">⭐ {rate:.2f}</span>
                        <span class="badge">🗳 {votes_str}</span>
                    </div>
                    <div style="margin-top:8px; display:flex; flex-wrap:wrap; gap:4px;">{genre_badges}</div>
                    {score_html}
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Watchlist toggle
        if show_watchlist_btn:
            in_wl = name in st.session_state.watchlist
            btn_label = "❤️ Remove" if in_wl else "🤍 Watchlist"
            if st.button(btn_label, key=f"wl_{name}_{id(info)}"):
                if in_wl:
                    st.session_state.watchlist.remove(name)
                else:
                    st.session_state.watchlist.append(name)
                st.rerun()

        # Detail view toggle
        if st.button("📋 Details", key=f"det_{name}_{id(info)}"):
            if st.session_state.selected_detail == name:
                st.session_state.selected_detail = None
            else:
                st.session_state.selected_detail = name
            st.rerun()


# --- HELPER: RENDER DETAIL PANEL ---
def render_detail_panel(name):
    rows = anime_df[anime_df['name'] == name]
    if rows.empty:
        return
    info = rows.iloc[0]

    img = info.get('image_url', '')
    if not img or str(img) == 'nan':
        img = f"https://via.placeholder.com/400x600/1a1a1a/ed1c24?text={name[:10]}"

    genres = info.get('genres_text', '').split()
    genre_badges = " ".join([f'<span class="badge red">{g}</span>' for g in genres])
    votes = int(info.get('votes', 0))
    votes_str = f"{votes:,}"

    col_img, col_info = st.columns([1, 3])
    with col_img:
        st.markdown(f'<img src="{img}" style="width:100%; border-radius:10px; border:2px solid #ff0000;">', unsafe_allow_html=True)
    with col_info:
        st.markdown(f"""
            <div class="detail-panel">
                <div class="detail-title">{name}</div>
                <div style="margin-bottom:12px; display:flex; gap:8px; flex-wrap:wrap;">
                    <span class="badge gold">⭐ {info['rate']:.2f} / 5.0</span>
                    <span class="badge">🗳 {votes_str} votes</span>
                </div>
                <div style="margin-bottom:12px;">{genre_badges}</div>
                <div style="color:#888; font-size:0.85rem; line-height:1.6;">
                    <b style="color:#fff;">Tags:</b> {info.get('tags', info.get('genres_text', 'N/A'))}
                </div>
            </div>
        """, unsafe_allow_html=True)

        in_wl = name in st.session_state.watchlist
        if st.button("❤️ Remove from Watchlist" if in_wl else "🤍 Add to Watchlist", key=f"wl_detail_{name}"):
            if in_wl:
                st.session_state.watchlist.remove(name)
            else:
                st.session_state.watchlist.append(name)
            st.rerun()

        if st.button("✖ Close Details", key=f"close_detail_{name}"):
            st.session_state.selected_detail = None
            st.rerun()


# ─── SIDEBAR ───────────────────────────────────────────────
with st.sidebar:
    st.markdown("<h2 style='color:#ff0000; font-family:Bebas Neue,sans-serif; letter-spacing:3px;'>CRIMSON CONTROLS</h2>", unsafe_allow_html=True)
    st.write("---")

    sel_genres = st.multiselect("🎭 FILTER BY GENRE:", unique_genres, key="genre_filter")
    min_rate = st.slider("⭐ MINIMUM RATING:", 0.0, 5.0, 3.5, step=0.1, key="rating_slider")

    sort_by = st.selectbox(
        "📊 SORT DISCOVERY BY:",
        options=["Rating ↓", "Rating ↑", "Votes ↓", "Name A→Z"],
        key="sort_by"
    )

    st.write("---")
    st.metric("📦 DB CAPACITY", len(anime_df))
    wl_count = len(st.session_state.watchlist)
    st.metric("❤️ WATCHLIST", wl_count)


# ─── HERO ───────────────────────────────────────────────────
st.markdown("""
    <div class="hero-container">
        <div class="hero-title">ANI-MIND</div>
        <p class="hero-sub">CRIMSON PROTOCOL · NEURAL RECOMMENDATION ENGINE</p>
    </div>
""", unsafe_allow_html=True)


# ─── TABS ───────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🎯 NEURAL RECOMMEND", "🔍 LIBRARY DISCOVERY", f"❤️ WATCHLIST ({wl_count})"])


# ══════════════════════════════════════════════════════════
# TAB 1 — NEURAL RECOMMEND
# ══════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-header">SELECT TARGET ANIME</div>', unsafe_allow_html=True)

    selected_name = st.selectbox("", anime_df['name'].values, label_visibility="collapsed", key="main_search_box")

    num_results = st.slider("Number of recommendations:", 6, 18, 9, step=3, key="num_results")

    if st.button("⚡ EXECUTE NEURAL SCAN", key="scan_btn"):
        # Clear any open detail panel on new scan
        st.session_state.selected_detail = None

        idx = anime_df[anime_df['name'] == selected_name].index[0]
        distances = sorted(list(enumerate(similarity[idx])), reverse=True, key=lambda x: x[1])[1:num_results + 1]

        st.markdown(f'<div class="section-header">RECOMMENDATIONS FOR: {selected_name.upper()}</div>', unsafe_allow_html=True)

        cols = st.columns(3)
        for i, (item_idx, score) in enumerate(distances):
            info = anime_df.iloc[item_idx]
            render_card(cols[i % 3], info, score=score)

    # Detail panel (shown below grid)
    if st.session_state.selected_detail:
        st.write("---")
        render_detail_panel(st.session_state.selected_detail)


# ══════════════════════════════════════════════════════════
# TAB 2 — LIBRARY DISCOVERY
# ══════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-header">FILTERED DISCOVERY</div>', unsafe_allow_html=True)

    # Text search
    search_query = st.text_input("🔎 Search by name:", placeholder="e.g. Attack on Titan...", key="discovery_search")

    # Filter pipeline
    discovery_df = anime_df[anime_df['rate'] >= min_rate].copy()

    if sel_genres:
        discovery_df = discovery_df[
            discovery_df['genres_text'].apply(lambda x: any(g in x for g in sel_genres))
        ]

    if search_query.strip():
        discovery_df = discovery_df[
            discovery_df['name'].str.contains(search_query.strip(), case=False, na=False)
        ]

    # Sort
    sort_map = {
        "Rating ↓": ("rate", False),
        "Rating ↑": ("rate", True),
        "Votes ↓": ("votes", False),
        "Name A→Z": ("name", True),
    }
    sort_col, sort_asc = sort_map[sort_by]
    results = discovery_df.sort_values(by=sort_col, ascending=sort_asc).head(24)

    # Stats row
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Results Found", len(results))
    col_b.metric("Avg Rating", f"{results['rate'].mean():.2f}" if not results.empty else "—")
    col_c.metric("Active Filters", len(sel_genres) + (1 if search_query.strip() else 0))

    st.write("---")

    if results.empty:
        st.markdown("""
            <div class="empty-watchlist">
                <h3>⛔ NO RESULTS</h3>
                <p>Adjust the sidebar filters or search query.</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        cols = st.columns(3)
        for i, (_, row) in enumerate(results.iterrows()):
            render_card(cols[i % 3], row)

    # Detail panel
    if st.session_state.selected_detail:
        st.write("---")
        render_detail_panel(st.session_state.selected_detail)


# ══════════════════════════════════════════════════════════
# TAB 3 — WATCHLIST
# ══════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-header">MY WATCHLIST</div>', unsafe_allow_html=True)

    if not st.session_state.watchlist:
        st.markdown("""
            <div class="empty-watchlist">
                <h3>📭 WATCHLIST EMPTY</h3>
                <p>Add anime from the Recommend or Discovery tabs using the 🤍 button.</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        wl_col1, wl_col2 = st.columns([4, 1])
        with wl_col2:
            if st.button("🗑 Clear All", key="clear_all_wl"):
                st.session_state.watchlist = []
                st.rerun()

        wl_df = anime_df[anime_df['name'].isin(st.session_state.watchlist)]

        # Summary stats
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Saved", len(wl_df))
        c2.metric("Avg Rating", f"{wl_df['rate'].mean():.2f}" if not wl_df.empty else "—")
        top_genre = ""
        if not wl_df.empty:
            all_g = []
            for g in wl_df['genres_text']:
                all_g.extend(g.split())
            if all_g:
                from collections import Counter
                top_genre = Counter(all_g).most_common(1)[0][0]
        c3.metric("Top Genre", top_genre or "—")

        st.write("---")

        cols = st.columns(3)
        for i, (_, row) in enumerate(wl_df.iterrows()):
            render_card(cols[i % 3], row, show_watchlist_btn=True)

        # Detail panel
        if st.session_state.selected_detail:
            st.write("---")
            render_detail_panel(st.session_state.selected_detail)