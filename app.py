import streamlit as st
import pickle
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="ANI-MIND | Crimson Onyx", page_icon="👹", layout="wide")

# --- THE "FIX EVERYTHING" CSS ---
st.markdown("""
<style>
    /* 1. Full Page & Sidebar */
    .stApp { background-color: #000000; }
    [data-testid="stSidebar"] { background-color: #050505 !important; border-right: 1px solid #330000; }
    
    /* 2. Global Text Force White */
    h1, h2, h3, h4, h5, h6, p, label, .stMetric, .stSelectbox p {
        color: #FFFFFF !important;
    }

    /* 3. THE DROPDOWN FIX (CRITICAL) */
    /* This targets the input box itself */
    div[data-baseweb="select"] > div {
        background-color: #111111 !important;
        border: 2px solid #ff0000 !important;
        color: #FFFFFF !important;
    }

    /* This targets the text INSIDE the box while you type */
    div[data-baseweb="select"] * {
        color: #FFFFFF !important;
    }

    /* This targets the POPUP list that appears when you click */
    ul[data-baseweb="listbox"] {
        background-color: #111111 !important;
    }
    
    ul[data-baseweb="listbox"] li {
        color: #FFFFFF !important;
        background-color: #111111 !important;
        border-bottom: 1px solid #222 !important;
    }

    /* This targets the hover effect in the list */
    ul[data-baseweb="listbox"] li:hover {
        background-color: #ff0000 !important;
        color: #FFFFFF !important;
    }

    /* 4. Hero & Cards */
    .hero-container {
        padding: 50px 20px;
        text-align: center;
        background: linear-gradient(180deg, #450000 0%, #000000 100%);
        border-bottom: 3px solid #ff0000;
        margin-bottom: 40px;
    }
    .hero-title {
        font-size: 5.5rem;
        font-weight: 900;
        letter-spacing: 15px;
        color: #FFFFFF !important;
        text-shadow: 2px 2px 20px #ff0000;
    }
    .anime-card {
        background: #0f0f0f;
        border: 2px solid #222;
        border-radius: 15px;
        overflow: hidden;
        transition: 0.3s;
        height: 460px;
        margin-bottom: 25px;
    }
    .anime-card:hover { border-color: #ff0000; box-shadow: 0 0 20px rgba(255, 0, 0, 0.6); }
    .poster-img { width: 100%; height: 360px; object-fit: cover; }
    .card-content { padding: 15px; text-align: center; }
    .card-title { font-size: 1.2rem; font-weight: 800; color: #FFFFFF !important; margin-bottom: 10px; height: 30px; overflow: hidden; }
    .status-badge { background: #ff0000; color: white !important; padding: 4px 15px; border-radius: 5px; font-weight: 900; }

    /* 5. Execution Button */
    .stButton>button {
        background: #ff0000 !important;
        color: white !important;
        border: none !important;
        font-weight: 900 !important;
        width: 100% !important;
        border-radius: 10px !important;
        height: 3.5rem !important;
    }
</style>
""", unsafe_allow_html=True)

# --- LOAD DATA ---
@st.cache_resource
def load_data():
    df = pickle.load(open('models/anime_list.pkl', 'rb'))
    sim = pickle.load(open('models/similarity_matrix.pkl', 'rb'))
    
    # --- POPULAR ANIME SORTING ---
    popular_favorites = [
        "Attack on Titan", "Naruto", "Death Note", "One Piece", 
        "Vinland Saga", "Spy x Family", "Demon Slayer", "Jujutsu Kaisen",
        "Naruto Shippuuden", "BLEACH"
    ]
    
    # Pull the favorites that actually exist in your Crunchyroll CSV
    top_picks = df[df['name'].isin(popular_favorites)].sort_values(by='rate', ascending=False)
    remaining = df[~df['name'].isin(popular_favorites)]
    
    # Combine them so favorites stay at the top (index 0, 1, 2...)
    ordered_df = pd.concat([top_picks, remaining]).reset_index(drop=True)
    
    return ordered_df, sim

anime_df, similarity = load_data()

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color: #ff0000;'>SYSTEM LOGS</h2>", unsafe_allow_html=True)
    st.write("---")
    st.metric("DATABASE", "CRUNCHYROLL")
    st.metric("CAPACITY", len(anime_df))
    st.write("---")
    st.write("USER: **MEHVISH**")

# --- MAIN UI ---
st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">ANI-MIND</h1>
        <p style="color: #FFFFFF; font-weight: bold; letter-spacing: 3px;">CRIMSON PROTOCOL ACTIVATED</p>
    </div>
""", unsafe_allow_html=True)

# Search Logic
st.markdown("<p style='font-size:1.2rem; font-weight:bold;'>SELECT TARGET ANIME:</p>", unsafe_allow_html=True)
selected_name = st.selectbox("", anime_df['name'].values, label_visibility="collapsed")

st.write("##") # Spacing

if st.button("EXECUTE NEURAL SCAN 🚀"):
    # Always locate by name to ensure we match the right vector
    idx = anime_df[anime_df['name'] == selected_name].index[0]
    distances = sorted(list(enumerate(similarity[idx])), reverse=True, key=lambda x: x[1])[1:10]
    
    st.markdown(f"<h3 style='color: #ff0000; text-align:center;'>TOP MATCHES FOUND</h3>", unsafe_allow_html=True)
    
    cols = st.columns(3)
    for i, (item_idx, score) in enumerate(distances):
        info = anime_df.iloc[item_idx]
        with cols[i % 3]:
            st.markdown(f"""
                <div class="anime-card">
                    <img src="{info['image_url']}" class="poster-img">
                    <div class="card-content">
                        <div class="card-title">{info['name']}</div>
                        <span class="status-badge">⭐ {info['rate']}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)