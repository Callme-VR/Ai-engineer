# NLP Notebook - Error Analysis & Fixes

## ✅ Current Status: FIXED

Your NLP.ipynb notebook is now working correctly! Here's what I found and fixed:

---

## 🔍 Error Analysis

### Main Error Fixed: `LookupError: punkt_tab not found`

**Location:** Cell 41-42 (when using `word_tokenize()`)

**Root Cause:**

- Your notebook was downloading `punkt` and `stopwords` (cell 37, lines 917-918)
- However, newer versions of NLTK (3.9+) now require `punkt_tab` for the `word_tokenize()` function
- The notebook was missing the download command for `punkt_tab`

**What I Did:**

1. Created `download_nltk_data.py` - a helper script to download all required NLTK resources
2. Ran the script successfully to download:
   - ✅ `punkt`
   - ✅ `punkt_tab` (this was the missing resource)
   - ✅ `stopwords`

---

## 📋 Code Issues Found (Minor/Informational)

### 1. **Typo in Function Name** (Line 584)

```python
def  remove_puncutation(text):  # ❌ Typo: "puncutation"
```

**Should be:**

```python
def remove_punctuation(text):  # ✅ Correct spelling
```

### 2. **Empty Code Cells**

There are several empty/incomplete code cells in your notebook:

- **Cell at line 777-781:** "apply the next function for the links removal and ursl"
- **Cell at line 793-797:** "remove the html tags from the text"
- **Cell at line 1325-1329:** Empty cell at the end

These cells have markdown descriptions but no implementation. This is normal if you're still developing, but here are implementations if you need them:

#### Remove URLs/Links:

```python
import re

def remove_urls(text):
    # Remove URLs
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    return re.sub(url_pattern, '', text)

data_frame['text'] = data_frame['text'].apply(remove_urls)
```

#### Remove HTML Tags:

```python
import re

def remove_html_tags(text):
    # Remove HTML tags
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

data_frame['text'] = data_frame['text'].apply(remove_html_tags)
```

### 3. **Inefficient Loop** (Line 282)

In cell 26 (execution_count: 26), this code appears inside a loop:

```python
for emotion in Uniques_emotion_array:
    emotion_number[emotion] = i
    i += 1
    data_frame['emotion'] = data_frame['Emotions'].map(emotion_number)  # ⚠️ This repeats unnecessarily
```

**Better approach:**

```python
for emotion in Uniques_emotion_array:
    emotion_number[emotion] = i
    i += 1

# Do the mapping once after the loop
data_frame['emotion'] = data_frame['Emotions'].map(emotion_number)
```

### 4. **Redundant Import** (Line 1189)

Cell 41 imports `word_tokenize` again, but it was already imported in cell 36 (line 884).

---

## 🎯 Notebook Workflow Summary

Your notebook successfully performs the following NLP preprocessing steps:

1. **Data Loading** - Reads emotion data from `train.txt` (16,000 rows)
2. **Label Encoding** - Maps emotions to numeric values (0-5)
3. **Lowercase Conversion** - Normalizes text case
4. **Number Removal** - Removes digits from text
5. **Emoji Removal** - Keeps only ASCII characters
6. **Stopword Removal** - Removes common English words using NLTK

### Data Transformations:

**Before Preprocessing:**

```
"i can go from feeling so hopeless to so damned hopeful just from being around someone who cares and is awake"
```

**After Preprocessing:**

```
"go feeling hopeless damned hopeful around someone cares awake"
```

---

## 📌 Recommendations

### 1. **Add `punkt_tab` to your notebook**

To make your notebook portable, add this to cell 37:

```python
nltk.download('punkt')
nltk.download('punkt_tab')  # ADD THIS LINE
nltk.download('stopwords')
```

### 2. **Apply Punctuation Removal**

You defined the `remove_puncutation` function (cell 30) but only tested it (cell 31). You should actually apply it:

```python
data_frame['text'] = data_frame['text'].apply(remove_puncutation)
```

### 3. **Complete the Missing Functions**

Implement the URL and HTML tag removal functions if your data needs them.

### 4. **Consider Using `clean_text` Column**

You created a `clean_text` column (cell 34) but then continued modifying the `text` column. Consider using `clean_text` for all preprocessing steps to preserve the original text.

### 5. **Add Stemming/Lemmatization** (Optional)

For better NLP results, consider adding:

```python
from nltk.stem import PorterStemmer
# or
from nltk.stem import WordNetLemmatizer

# Example with Lemmatization
lemmatizer = WordNetLemmatizer()
nltk.download('wordnet')

def lemmatize_text(text):
    words = text.split()
    return ' '.join([lemmatizer.lemmatize(word) for word in words])

data_frame['text'] = data_frame['text'].apply(lemmatize_text)
```

---

## ✨ Final Status

Your notebook is **fully functional** and ready to use! The NLTK error has been resolved, and all cells should execute without errors.

If you encounter any other issues, please let me know!

---

**Generated:** 2026-01-19  
**Python Version:** 3.13.7  
**NLTK Version:** Updated (requires punkt_tab)
