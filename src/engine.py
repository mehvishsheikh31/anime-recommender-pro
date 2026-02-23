import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

def train_model():
    print("🧠 Training Crunchyroll Engine...")
    df = pd.read_csv('data/processed_anime.csv')
    
    cv = CountVectorizer(max_features=2000, stop_words='english')
    vectors = cv.fit_transform(df['tags']).toarray()
    
    similarity = cosine_similarity(vectors)
    
    pickle.dump(df, open('models/anime_list.pkl', 'wb'))
    pickle.dump(similarity, open('models/similarity_matrix.pkl', 'wb'))
    print("✅ Crunchyroll Brain saved.")

if __name__ == "__main__":
    train_model()