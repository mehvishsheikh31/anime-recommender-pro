import requests
import streamlit as st

@st.cache_data(show_spinner=False)
def get_anime_poster(title):
    try:
        # Reduced timeout for faster skipping if API is slow
        url = f"https://api.jikan.moe/v4/anime?q={title}&limit=1"
        res = requests.get(url, timeout=3)
        if res.status_code == 200:
            data = res.json()
            if data['data']:
                return data['data'][0]['images']['jpg']['large_image_url']
    except:
        pass
    return "https://via.placeholder.com/400x600/1a1a1a/ed1c24?text=Poster+Unavailable"