import re
from sklearn.feature_extraction.text import TfidfVectorizer

STOPWORDS = {
    "the","and","or","of","in","to","for","a","an","with","be","on","is","at",
    "that","this","by","as","are","from","it","will","has","have","not","but",
    "their","they","them","your","our","you","we","new","per","etc","more"
}

def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s\-]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_candidate_tokens(text: str):
    """
    Extract potential skill tokens (single + multi-word).
    """
    text = clean_text(text)

    words = text.split()
    words = [w for w in words if len(w) > 2 and w not in STOPWORDS]

    # Unigrams
    candidates = words.copy()

    # Bigrams
    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i+1]
        if w1 not in STOPWORDS and w2 not in STOPWORDS:
            candidates.append(f"{w1} {w2}")

    # Trigrams
    for i in range(len(words) - 2):
        w1, w2, w3 = words[i], words[i+1], words[i+2]
        if w1 not in STOPWORDS and w2 not in STOPWORDS and w3 not in STOPWORDS:
            candidates.append(f"{w1} {w2} {w3}")

    return list(set(candidates))  # unique list


def extract_skills_from_jd(jd_text: str, top_n: int = 20) -> list:
    """
    Automatically extract top meaningful tokens using TF-IDF ranking.
    No hardcoded skill lists.
    """
    cleaned = clean_text(jd_text)
    candidates = extract_candidate_tokens(jd_text)

    if not candidates:
        return []

    # Use JD text as corpus
    vectorizer = TfidfVectorizer(vocabulary=candidates)
    tfidf_matrix = vectorizer.fit_transform([cleaned])
    scores = tfidf_matrix.toarray()[0]

    # Rank candidates by TF-IDF score
    ranked = sorted(
        zip(candidates, scores),
        key=lambda x: x[1],
        reverse=True
    )

    skills = [token for token, score in ranked if score > 0]

    return skills[:top_n]


def extract_years_requirement(jd_text: str):
    """
    Extract number of years of experience from JD.
    """
    match = re.search(r"(\d{1,2})\+?\s*(years|year|yrs)", jd_text, re.IGNORECASE)
    if match:
        try:
            return int(match.group(1))
        except:
            return None
    return None
