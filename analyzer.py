#importing libraries
import re
import numpy as np
import joblib
from sklearn.metrics.pairwise import cosine_similarity

#loading of saved models
model = joblib.load("models/hybrid_model.pkl")
tfidf = joblib.load("models/tfidf_vectorizer.pkl")
scaler = joblib.load("models/feature_scaler.pkl")
embedding_model = joblib.load("models/embedding_model.pkl")

#text cleaning function
def clean_text(text):

    text = str(text)

    text = text.lower()

    # Remove URLs
    text = re.sub(
        r"http\S+|www\S+",
        "",
        text
    )

    # Keep letters and spaces
    text = re.sub(
        r"[^a-zA-Z\s]",
        " ",
        text
    )

    # Remove extra spaces
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()

def analyze_news(headline, body):

    headline = str(headline)
    body = str(body)

    clean_headline = clean_text(headline)
    clean_body = clean_text(body)
#calculating the TF-IDF similarity

    headline_tfidf = tfidf.transform(
        [clean_headline]
    )

    body_tfidf = tfidf.transform(
        [clean_body]
    )

    lexical_similarity = cosine_similarity(
        headline_tfidf,
        body_tfidf
    )[0][0]

#performing semantic similarity

    headline_embedding = embedding_model.encode(
        [clean_headline]
    )

    body_embedding = embedding_model.encode(
        [clean_body]
    )

    semantic_similarity = cosine_similarity(
        headline_embedding,
        body_embedding
    )[0][0]

    title_words = len(
        clean_headline.split()
    )

    body_words = len(
        clean_body.split()
    )

    if body_words > 0:
        length_ratio = title_words / body_words
    else:
        length_ratio = 0


    question_marks = headline.count("?")

    exclamation_marks = headline.count("!")

#creating features
    features = np.array([[
        lexical_similarity,
        semantic_similarity,
        title_words,
        body_words,
        length_ratio,
        question_marks,
        exclamation_marks
    ]])

#scaling of features

    features_scaled = scaler.transform(
        features
    )

#real and fake prediction

    prediction = model.predict(
        features_scaled
    )[0]

    probabilities = model.predict_proba(
        features_scaled
    )[0]


    fake_probability = probabilities[0] * 100

    real_probability = probabilities[1] * 100

    lexical_score = lexical_similarity * 100

    semantic_score = semantic_similarity * 100

    hybrid_match = (
        lexical_score + semantic_score
    ) / 2

    discrepancy_score = (
        100 - hybrid_match
    )

    return {

        "prediction": prediction,

        "fake_probability": fake_probability,

        "real_probability": real_probability,

        "lexical_similarity": lexical_score,

        "semantic_similarity": semantic_score,

        "hybrid_match": hybrid_match,

        "discrepancy_score": discrepancy_score,

        "title_words": title_words,

        "body_words": body_words,

        "length_ratio": length_ratio,

        "question_marks": question_marks,

        "exclamation_marks": exclamation_marks
    }