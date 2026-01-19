"""
NLTK Data Downloader for NLP Project
=====================================
This script downloads all required NLTK data packages to fix the LookupError.
Run this script before running your NLP.ipynb notebook.
"""

import nltk

print("Downloading NLTK data packages...")
print("-" * 50)

# Download punkt tokenizer (older version)
print("\n1. Downloading 'punkt'...")
nltk.download('punkt')

# Download punkt_tab tokenizer (required for newer NLTK versions)
print("\n2. Downloading 'punkt_tab'...")
nltk.download('punkt_tab')

# Download stopwords
print("\n3. Downloading 'stopwords'...")
nltk.download('stopwords')

print("-" * 50)
print("\n✅ All NLTK data packages downloaded successfully!")
print("\nYou can now run your NLP.ipynb notebook without errors.")
