import streamlit as st
import pickle
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="ANI-MIND | Crimson Onyx", page_icon="👹", layout="wide")

# --- HIGH-CONTRAST CRIMSON & PURE WHITE CSS ---
st.markdown("""
<style>
    /* Full Black Background */
    .stApp {
        background-color: #000000;
    }
    
    /* Global Text Color - Forced Pure White */
    html, body, [class*="st-"] {
        color: #FFFFFF !important;
    }

    /* Sidebar Fix: Make all text visible */
    [data-testid="stSidebar"] {
        background-color: #050505 !important;
        border-right: 1px solid #330000;
    }
    [data-testid="stSidebar"] .stText, [data-testid="stSidebar"] label, [data-testid="stSidebar"] p {
        color: #FFFFFF !important;
        font-weight: bold !important;
    }
    
    /* Metrics in Sidebar */
    [data-testid="stMetricValue"] {
        color: #ff0000 !important;
        font-size: 1.8rem !important;
    }

    /* Hero Header */
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
        margin: 0;
    }

    /* Recommendation Cards */
    .anime-card {
        background: #0f0f0f;
        border: 2px solid #222;
        border-radius: 15px;
        overflow: hidden;
        transition: 0.3s;
        height: 460px;
        margin-bottom: 25px;
    }
    .anime-card:hover {
        border-color: #ff0000;
        box-shadow: 0 0 20px rgba(255, 0, 0, 0.6);
    }

    .poster-img {
        width: 100%;
        height: 360px;
        object-fit: cover;
    }

    .card-content { padding: 15px; text-align: center; }
    .card-title { 
        font-size: 1.2rem; 
        font-weight: 800; 
        color: #FFFFFF !important; 
        margin-bottom: 10px;
        height: 30px;
        overflow: hidden;
    }
    
    .status-badge {
        background: #ff0000;
        color: white !important;
        padding: 4px 15px;
        border-radius: 5px;
        font-size: 0.9rem;
        font-weight: 900;
    }

    /* Selectbox Styling */
    .stSelectbox label {
        color: #FFFFFF !important;
        font-size: 1.2rem !important;
        margin-bottom: 10px !important;
    }

    /* Master Button */
    .stButton>button {
        background: #ff0000 !important;
        color: white !important;
        border: none !important;
        font-weight: 900 !important;
        font-size: 1.1rem !important;
        height: 3.5rem !important;
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- LOAD DATA ---
@st.cache_resource
def load_data():
    df = pickle.load(open('models/anime_list.pkl', 'rb'))
    sim = pickle.load(open('models/similarity_matrix.pkl', 'rb'))
    return df, sim

anime_df, similarity = load_data()

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color: #ff0000;'>SYSTEM LOGS</h2>", unsafe_allow_html=True)
    st.write("---")
    st.metric("DATABASE", "CRUNCHYROLL")
    st.metric("CAPACITY", len(anime_df))
    st.write("---")
    st.write("STATUS: **OPTIMIZED**")
    st.write("USER: **MEHVISH**")

# --- MAIN UI ---
st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">ANI-MIND</h1>
        <p style="color: #FFFFFF; font-weight: bold; letter-spacing: 3px;">CRIMSON PROTOCOL ACTIVATED</p>
    </div>
""", unsafe_allow_html=True)

# Search Logic
selected_name = st.selectbox("SELECT TARGET ANIME:", anime_df['name'].values)

if st.button("EXECUTE NEURAL SCAN 🚀"):
    idx = anime_df[anime_df['name'] == selected_name].index[0]
    distances = sorted(list(enumerate(similarity[idx])), reverse=True, key=lambda x: x[1])[1:10]
    
    st.markdown(f"<h3 style='color: #ff0000; text-align:center;'>TOP MATCHES FOUND</h3>", unsafe_allow_html=True)
    
    cols = st.columns(3)
    for i, (item_idx, score) in enumerate(distances):
        info = anime_df.iloc[item_idx]
        with cols[i % 3]:
            # Clean Card: Only Image, Title, and Score
            st.markdown(f"""
                <div class="anime-card">
                    <img src="{info['image_url']}" class="poster-img">
                    <div class="card-content">
                        <div class="card-title">{info['name']}</div>
                        <span class="status-badge">⭐ {info['rate']}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)