import streamlit as st
import pickle
import pandas as pd
import os

# --- PAGE CONFIG (FORCE SIDEBAR OPEN) ---
st.set_page_config(
    page_title="ANI-MIND | Crimson Onyx", 
    page_icon="👹", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- THE BRUTE FORCE CSS FIX ---
st.markdown("""
<style>
    /* 1. Global Background */
    .stApp { background-color: #000000; }
    html, body, [class*="st-"] { color: #FFFFFF !important; }

    /* 2. SIDEBAR FORCE-VISIBLE STYLE */
    [data-testid="stSidebar"] { 
        background-color: #0a0a0a !important; 
        border-right: 2px solid #ff0000 !important;
        visibility: visible !important;
        display: block !important;
    }
    
    /* Make the tiny 'Collapse/Expand' arrow visible and Red */
    [data-testid="collapsedControl"], [data-testid="stSidebarCollapsedControl"] {
        color: #ff0000 !important;
        background-color: #111111 !important;
        border: 1px solid #ff0000 !important;
        border-radius: 5px !important;
    }

    /* 3. SIDEBAR TEXT & FILTERS */
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p {
        color: #FFFFFF !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
    }
    
    /* Metrics and Slider Colors */
    [data-testid="stSidebar"] div[data-testid="stMetricValue"], 
    [data-testid="stSidebar"] span {
        color: #ff0000 !important;
    }

    /* 4. DROPDOWN FIXES */
    div[data-baseweb="select"] > div {
        background-color: #1a1a1a !important;
        border: 1px solid #ff0000 !important;
    }
    div[data-baseweb="select"] div { color: #FFFFFF !important; }
    [data-baseweb="popover"] ul { background-color: #1a1a1a !important; }
    [data-baseweb="popover"] li { color: #FFFFFF !important; }
    [data-baseweb="popover"] li:hover { background-color: #ff0000 !important; }

    /* 5. HERO & TABS */
    .hero-container {
        padding: 50px 20px; text-align: center;
        background: linear-gradient(180deg, #450000 0%, #000000 100%);
        border-bottom: 3px solid #ff0000; margin-bottom: 40px;
    }
    .stTabs [aria-selected="true"] { color: #ff0000 !important; border-bottom: 2px solid #ff0000 !important; }

    /* 6. BUTTON */
    .stButton>button {
        background: #ff0000 !important; color: white !important;
        font-weight: 900 !important; width: 100% !important;
        height: 3.5rem !important; border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- LOAD DATA ---
@st.cache_resource
def load_data():
    # Get the current directory of app.py
    base_path = os.path.dirname(__file__)
    
    # Check for 'models' or 'Models' (Handling Linux case-sensitivity)
    folder_name = 'models'
    if not os.path.exists(os.path.join(base_path, folder_name)):
        folder_name = 'Models'

    # Create the full path to your files
    anime_list_path = os.path.join(base_path, folder_name, 'anime_list.pkl')
    similarity_path = os.path.join(base_path, folder_name, 'similarity_matrix.pkl')
    
    # Final check before loading
    if not os.path.exists(anime_list_path):
        st.error(f"Error: Could not find {anime_list_path}. Please check your GitHub folder name.")
        st.stop()

    # Load the files
    df = pickle.load(open(anime_list_path, 'rb'))
    sim = pickle.load(open(similarity_path, 'rb'))
    
    # Process Genres
    df['genres_text'] = df['genres_text'].fillna('').astype(str)
    
    popular_favorites = ["Attack on Titan", "Naruto", "Death Note", "One Piece", "Vinland Saga", "Spy x Family", "Demon Slayer", "Jujutsu Kaisen"]
    top_picks = df[df['name'].isin(popular_favorites)].sort_values(by='rate', ascending=False)
    remaining = df[~df['name'].isin(popular_favorites)]
    ordered_df = pd.concat([top_picks, remaining]).reset_index(drop=True)
    
    all_genres = set()
    for g_string in ordered_df['genres_text']:
        if g_string:
            all_genres.update(g_string.split())
    
    return ordered_df, sim, sorted(list(all_genres))

# Execute Load
anime_df, similarity, unique_genres = load_data()

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color: #ff0000;'>CRIMSON CONTROLS</h2>", unsafe_allow_html=True)
    st.write("---")
    sel_genres = st.multiselect("FILTER BY GENRE:", unique_genres, key="genre_filter_unique")
    min_rate = st.slider("MINIMUM RATING:", 0.0, 5.0, 3.5, key="rating_slider_unique")
    st.write("---")
    st.metric("DB CAPACITY", len(anime_df))
    st.write("USER: **MEHVISH**")

# --- MAIN UI ---
st.markdown("""
    <div class="hero-container">
        <h1 style="font-size: 5.5rem; letter-spacing: 15px; color: white; margin:0; text-shadow: 2px 2px 20px #ff0000;">ANI-MIND</h1>
        <p style="color: #FFFFFF; font-weight: bold; letter-spacing: 3px;">CRIMSON PROTOCOL ACTIVATED</p>
    </div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🎯 NEURAL RECOMMEND", "🔍 LIBRARY DISCOVERY"])

with tab1:
    st.markdown("<p style='font-size:1.1rem; font-weight:bold;'>SELECT TARGET ANIME:</p>", unsafe_allow_html=True)
    selected_name = st.selectbox("", anime_df['name'].values, label_visibility="collapsed", key="main_search_box")
    
    if st.button("EXECUTE NEURAL SCAN 🚀"):
        idx = anime_df[anime_df['name'] == selected_name].index[0]
        distances = sorted(list(enumerate(similarity[idx])), reverse=True, key=lambda x: x[1])[1:10]
        
        cols = st.columns(3)
        for i, (item_idx, score) in enumerate(distances):
            info = anime_df.iloc[item_idx]
            with cols[i % 3]:
                st.markdown(f"""
                    <div class="anime-card">
                        <img src="{info['image_url']}" style="width:100%; height:350px; object-fit:cover;">
                        <div style="padding:15px; text-align:center;">
                            <div style="font-weight:bold; color:white; height:40px; overflow:hidden;">{info['name']}</div>
                            <span class="status-badge">⭐ {info['rate']}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

with tab2:
    st.markdown("<h3 style='color: #ff0000; text-align:center;'>FILTERED DISCOVERY</h3>", unsafe_allow_html=True)
    discovery_df = anime_df[anime_df['rate'] >= min_rate]
    if sel_genres:
        discovery_df = discovery_df[discovery_df['genres_text'].apply(lambda x: any(g in x for g in sel_genres))]

    results = discovery_df.sort_values(by='rate', ascending=False).head(12)
    
    if results.empty:
        st.warning("No matches found. Adjust the filters in the sidebar.")
    else:
        cols = st.columns(3)
        for i, (idx, row) in enumerate(results.iterrows()):
            with cols[i % 3]:
                st.markdown(f"""
                    <div class="anime-card">
                        <img src="{row['image_url']}" style="width:100%; height:350px; object-fit:cover;">
                        <div style="padding:15px; text-align:center;">
                            <div style="font-weight:bold; color:white; height:40px; overflow:hidden;">{row['name']}</div>
                            <span class="status-badge">⭐ {row['rate']}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)