"""
Member 2 - Data Preprocessing
Handles: lowercasing, punctuation removal, tokenization, stopword removal, stemming
"""

import re
import string


# Simple English stopwords list (no external download needed)
STOPWORDS = {
    'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'is', 'it', 'this', 'that', 'was', 'are',
    'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
    'will', 'would', 'could', 'should', 'may', 'might', 'shall', 'can',
    'i', 'me', 'my', 'we', 'our', 'you', 'your', 'he', 'she', 'they',
    'them', 'his', 'her', 'its', 'their', 'what', 'which', 'who', 'whom',
    'when', 'where', 'why', 'how', 'if', 'so', 'as', 'up', 'out', 'about',
    'into', 'through', 'during', 'before', 'after', 'above', 'below',
    'between', 'each', 'all', 'both', 'few', 'more', 'most', 'other',
    'some', 'such', 'no', 'not', 'only', 'same', 'than', 'then', 'there',
    's', 't', 'just', 'also', 'very', 'too', 'much', 'many'
}

# Basic suffix-stripping stemmer (replaces NLTK PorterStemmer)
def simple_stem(word):
    """Simple rule-based stemmer for common English suffixes."""
    if len(word) <= 3:
        return word
    # Order matters: longer suffixes first
    suffixes = ['ings', 'ing', 'tion', 'tions', 'ness', 'ment', 'ments',
                'ers', 'er', 'est', 'ed', 'es', 'ly', 'ies', 'ied']
    for suffix in suffixes:
        if word.endswith(suffix) and len(word) - len(suffix) >= 3:
            return word[:-len(suffix)]
    if word.endswith('ies') and len(word) > 4:
        return word[:-3] + 'y'
    return word


def preprocess_text(text):
    """
    Full preprocessing pipeline:
    1. Lowercase
    2. Remove punctuation
    3. Tokenize (split into words)
    4. Remove stopwords
    5. Stem words
    Returns: cleaned string ready for TF-IDF
    """
    # Step 1: Lowercase
    text = text.lower()

    # Step 2: Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))

    # Step 3: Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    # Step 4: Tokenize
    tokens = text.split()

    # Step 5: Remove stopwords
    tokens = [t for t in tokens if t not in STOPWORDS and len(t) > 1]

    # Step 6: Stem
    tokens = [simple_stem(t) for t in tokens]

    return ' '.join(tokens)


def preprocess_batch(texts):
    """Preprocess a list of texts."""
    return [preprocess_text(t) for t in texts]


if __name__ == "__main__":
    # Demo / test
    samples = [
        "What should I do if someone is choking?",
        "How do I treat a burn?",
        "The person stopped breathing!",
    ]
    print("=== Preprocessing Demo ===")
    for s in samples:
        print(f"  Original : {s}")
        print(f"  Processed: {preprocess_text(s)}")
        print()
