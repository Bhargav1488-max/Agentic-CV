import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_ats_score(cv_text, jd_text):
    if not cv_text or not jd_text:
        return 0, [], []
        
    # Simple keyword extraction (simulating ATS)
    words_jd = set(re.findall(r'\b[A-Za-z0-9]+\b', jd_text.lower()))
    words_cv = set(re.findall(r'\b[A-Za-z0-9]+\b', cv_text.lower()))
    
    # Exclude common stop words (simplified list)
    stop_words = {'the', 'and', 'to', 'a', 'of', 'in', 'for', 'is', 'on', 'with', 'as', 'by', 'an'}
    words_jd = words_jd - stop_words
    words_cv = words_cv - stop_words
    
    matched = list(words_jd.intersection(words_cv))
    missing = list(words_jd - words_cv)
    
    # TF-IDF similarity
    try:
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform([cv_text, jd_text])
        cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        score = int(cosine_sim * 100)
    except Exception:
        score = 0
        
    return score, matched[:20], missing[:20]
