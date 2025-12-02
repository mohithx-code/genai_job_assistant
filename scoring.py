import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def keyword_match_score(jd_skills: list, resume_text: str):
    """
    Simple keyword overlap scoring.
    Returns:
    - score (0 to 1)
    - list of matched skills
    """
    resume_l = resume_text.lower()

    if not jd_skills:
        return 0.0, []

    matched = [skill for skill in jd_skills if skill.lower() in resume_l]

    score = len(matched) / max(1, len(jd_skills))
    return score, matched


def semantic_similarity_score(jd_text: str, resume_text: str):
    """
    Falls back to TF-IDF semantic similarity.
    (This is local and does not rely on Gemini embeddings.)
    """
    vec = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    docs = [jd_text, resume_text]

    try:
        matrix = vec.fit_transform(docs)
        similarity = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]
        return float(similarity)
    except:
        return 0.0


def compute_match_score(jd_text: str, resume_text: str, jd_skills: list,
                        jd_years=None, resume_years=None):
    """
    Combines:
    - Semantic similarity (60%)
    - Keyword score (30%)
    - Experience factor (10%)
    """

    # (1) Keyword match
    K, matched_skills = keyword_match_score(jd_skills, resume_text)

    # (2) Semantic similarity
    S = semantic_similarity_score(jd_text, resume_text)  # between 0–1

    # (3) Experience factor
    Exp = 1.0
    if jd_years and resume_years:
        diff = jd_years - resume_years
        if diff > 0:
            Exp = max(0.5, 1 - 0.07 * diff)

    # Final weighted score
    score_raw = 0.6 * S + 0.3 * K + 0.1 * Exp
    score_pct = round(score_raw * 100, 1)

    details = {
        "semantic_score": round(S, 3),
        "keyword_score": round(K, 3),
        "experience_factor": round(Exp, 3),
        "matched_skills": matched_skills,
    }

    return score_pct, details
