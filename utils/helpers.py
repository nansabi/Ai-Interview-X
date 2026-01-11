# utils/helpers.py

import re

# -------------------------
# Text Cleaning / NLP Utilities
# -------------------------
def clean_text(text):
    """
    Clean text by:
    - Lowercasing
    - Removing special characters
    - Removing extra spaces
    """
    text = text.lower().strip()
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)  # Keep letters/numbers only
    text = re.sub(r"\s+", " ", text)  # Replace multiple spaces with single space
    return text

def count_words(text):
    """Return number of words in a string"""
    return len(text.split())

def check_keywords(answer, keywords):
    """
    Check if all required keywords are present in answer
    answer: string
    keywords: list of strings
    Returns: tuple (found_count, total_keywords, missing_keywords)
    """
    answer_clean = clean_text(answer)
    missing = [kw for kw in keywords if kw.lower() not in answer_clean]
    found_count = len(keywords) - len(missing)
    return found_count, len(keywords), missing

# -------------------------
# Example usage
# -------------------------
if __name__ == "__main__":
    sample = "This is a Sample Answer for AI Interview."
    print(clean_text(sample))
    print(count_words(sample))
    print(check_keywords(sample, ["AI", "Interview", "Python"]))
