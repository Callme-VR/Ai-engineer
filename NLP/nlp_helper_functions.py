"""
NLP Helper Functions
====================
Additional preprocessing functions to complete your NLP pipeline.
Copy these into your notebook as needed.
"""

import re
from nltk.stem import PorterStemmer, WordNetLemmatizer
import nltk

# Make sure to download required NLTK data
# nltk.download('wordnet')
# nltk.download('omw-1.4')

# ============================================================
# URL REMOVAL
# ============================================================


def remove_urls(text):
    """Remove URLs from text"""
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    return re.sub(url_pattern, '', text)

# Usage:
# data_frame['text'] = data_frame['text'].apply(remove_urls)


# ============================================================
# HTML TAG REMOVAL
# ============================================================

def remove_html_tags(text):
    """Remove HTML tags from text"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

# Usage:
# data_frame['text'] = data_frame['text'].apply(remove_html_tags)


# ============================================================
# SPECIAL CHARACTERS REMOVAL
# ============================================================

def remove_special_chars(text):
    """Remove special characters, keep only letters and spaces"""
    return re.sub(r'[^a-zA-Z\s]', '', text)

# Usage:
# data_frame['text'] = data_frame['text'].apply(remove_special_chars)


# ============================================================
# EXTRA WHITESPACE REMOVAL
# ============================================================

def remove_extra_whitespace(text):
    """Remove extra whitespace and trim"""
    return ' '.join(text.split())

# Usage:
# data_frame['text'] = data_frame['text'].apply(remove_extra_whitespace)


# ============================================================
# STEMMING
# ============================================================

def stem_text(text):
    """Apply Porter Stemming to text"""
    stemmer = PorterStemmer()
    words = text.split()
    return ' '.join([stemmer.stem(word) for word in words])

# Usage:
# data_frame['text'] = data_frame['text'].apply(stem_text)

# Example: "running" -> "run", "flies" -> "fli"


# ============================================================
# LEMMATIZATION (Better than stemming for most cases)
# ============================================================

def lemmatize_text(text):
    """Apply Lemmatization to text"""
    lemmatizer = WordNetLemmatizer()
    words = text.split()
    return ' '.join([lemmatizer.lemmatize(word) for word in words])

# Usage:
# data_frame['text'] = data_frame['text'].apply(lemmatize_text)

# Example: "running" -> "running", "better" -> "good"


# ============================================================
# COMPLETE PREPROCESSING PIPELINE
# ============================================================

def preprocess_text_complete(text):
    """
    Complete text preprocessing pipeline.
    Applies all steps in order:
    1. Lowercase
    2. Remove URLs
    3. Remove HTML tags
    4. Remove special characters
    5. Remove extra whitespace
    6. Lemmatization
    """
    # Lowercase
    text = text.lower()

    # Remove URLs
    text = remove_urls(text)

    # Remove HTML tags
    text = remove_html_tags(text)

    # Remove special characters
    text = remove_special_chars(text)

    # Remove extra whitespace
    text = remove_extra_whitespace(text)

    # Lemmatize
    text = lemmatize_text(text)

    return text

# Usage:
# data_frame['cleaned_text'] = data_frame['text'].apply(preprocess_text_complete)


# ============================================================
# CONTRACTIONS EXPANSION (Optional but useful)
# ============================================================

CONTRACTIONS = {
    "ain't": "is not",
    "aren't": "are not",
    "can't": "cannot",
    "couldn't": "could not",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hadn't": "had not",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he would",
    "he'll": "he will",
    "he's": "he is",
    "i'd": "i would",
    "i'll": "i will",
    "i'm": "i am",
    "i've": "i have",
    "isn't": "is not",
    "it's": "it is",
    "let's": "let us",
    "shouldn't": "should not",
    "that's": "that is",
    "there's": "there is",
    "they'd": "they would",
    "they'll": "they will",
    "they're": "they are",
    "they've": "they have",
    "we'd": "we would",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "what's": "what is",
    "won't": "will not",
    "wouldn't": "would not",
    "you'd": "you would",
    "you'll": "you will",
    "you're": "you are",
    "you've": "you have"
}


def expand_contractions(text):
    """Expand contractions in text"""
    for contraction, expansion in CONTRACTIONS.items():
        text = text.replace(contraction, expansion)
    return text

# Usage:
# data_frame['text'] = data_frame['text'].apply(expand_contractions)


# ============================================================
# EXAMPLE: Complete workflow for your notebook
# ============================================================

if __name__ == "__main__":
    """
    Suggested order of operations for your NLP notebook:

    1. Load data
    2. Basic cleaning:
       - Lowercase
       - Expand contractions (optional)
       - Remove URLs
       - Remove HTML tags
       - Remove numbers
       - Remove special chars
       - Remove extra whitespace
    3. Tokenization and stopword removal
    4. Lemmatization or Stemming
    5. Final cleanup

    Example code for notebook:

    # Apply all basic cleaning
    data_frame['text'] = data_frame['text'].str.lower()
    data_frame['text'] = data_frame['text'].apply(expand_contractions)
    data_frame['text'] = data_frame['text'].apply(remove_urls)
    data_frame['text'] = data_frame['text'].apply(remove_html_tags)
    data_frame['text'] = data_frame['text'].apply(remove_number)
    data_frame['text'] = data_frame['text'].apply(remove_puncutation)
    data_frame['text'] = data_frame['text'].apply(remove_emojies)
    data_frame['text'] = data_frame['text'].apply(removestopwords)
    data_frame['text'] = data_frame['text'].apply(lemmatize_text)
    data_frame['text'] = data_frame['text'].apply(remove_extra_whitespace)
    """
    pass
