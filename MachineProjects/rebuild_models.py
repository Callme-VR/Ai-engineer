import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
import os


def rebuild():
    print("Loading MoviesData.csv...")
    # Load dataset
    try:
        df = pd.read_csv('MoviesData.csv')
    except FileNotFoundError:
        print("Error: MoviesData.csv not found!")
        return

    print(f"Loaded {len(df)} rows.")

    # Data Cleaning
    # Ensure titles and overviews are strings and handle missing values
    df['title'] = df['title'].fillna('')
    df['overview'] = df['overview'].fillna('')

    # Create TF-IDF Matrix
    print("Generating TF-IDF Matrix...")
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['overview'])

    # Create Indices Map
    # Drop duplicates just in case, keeping the first occurrence
    df = df.drop_duplicates(
        subset='title', keep='first').reset_index(drop=True)
    # Re-calculate matrix after dropping duplicates to keep indices aligned
    tfidf_matrix = tfidf.fit_transform(df['overview'])

    indices = pd.Series(df.index, index=df['title']).drop_duplicates()

    # Save files
    print("Saving pickles...")

    with open('df.pkl', 'wb') as f:
        pickle.dump(df, f)

    with open('indices.pkl', 'wb') as f:
        pickle.dump(indices, f)

    with open('tfidf_matrix.pkl', 'wb') as f:
        # Saving just the sparse matrix, not the vectorizer
        pickle.dump(tfidf_matrix, f)

    print("Success! All models rebuilt compatible with scikit-learn 1.8.0")


if __name__ == "__main__":
    rebuild()
