import pandas as pd

def clean_data():
    print("🚀 Processing Crunchyroll Dataset...")
    # Make sure your file is named 'crunchyroll.csv' in the data folder
    try:
        df = pd.read_csv('data/crunchyroll.csv')
    except FileNotFoundError:
        print("❌ Error: 'data/crunchyroll.csv' not found. Please check the filename.")
        return

    # 1. Map columns to consistent names
    df['name'] = df['anime']
    df['image_url'] = df['anime_img']
    
    # 2. Convert One-Hot Genres back to Text
    # Crunchyroll genres usually start from column index 12 onwards
    genre_columns = df.columns[12:] 
    
    def get_genre_list(row):
        genres = [col for col in genre_columns if row[col] == 1]
        return " ".join(genres)

    df['genres_text'] = df.apply(get_genre_list, axis=1)
    
    # 3. Create Tags for the AI (Fixed the .str.lower() error)
    # We combine name and genres, then convert to lowercase
    df['tags'] = (df['name'].astype(str) + " " + df['genres_text'].astype(str)).str.lower()
    
    # 4. Clean up and Save
    final_df = df[['name', 'image_url', 'rate', 'votes', 'genres_text', 'tags']]
    # Drop rows where critical data is missing
    final_df = final_df.dropna(subset=['name', 'image_url', 'tags'])
    
    final_df.to_csv('data/processed_anime.csv', index=False)
    print(f"✅ Processed {len(final_df)} Crunchyroll titles!")

if __name__ == "__main__":
    clean_data()