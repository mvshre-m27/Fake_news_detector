import pandas as pd
import numpy as np
import re
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
from sklearn.metrics.pairwise import cosine_similarity

from sentence_transformers import SentenceTransformer
print("\nLoading datasets...")

fake = pd.read_csv("data/Fake.csv")
true = pd.read_csv("data/True.csv")

print("Fake articles:", len(fake))
print("Real articles:", len(true))

#adding labels

fake["label"] = 0       # Fake
true["label"] = 1       # Real

data = pd.concat([fake, true],ignore_index=True)
#Handling Missing Values
data["title"] = data["title"].fillna("")
data["text"] = data["text"].fillna("")
data["title"] = data["title"].astype(str)
data["text"] = data["text"].astype(str)
before = len(data)
data = data.drop_duplicates(subset=["title", "text"]).reset_index(drop=True)
after = len(data)
print("Articles before duplicate removal:", before)
print("Articles after duplicate removal:", after)
def clean_text(text):
    text = str(text)
    # Convert to lowercase
    text = text.lower()
    # Remove URLs
    text = re.sub(r"http\S+|www\S+","",text)
    # Keep only letters and spaces
    text = re.sub(r"[^a-zA-Z\s]"," ",text)
    # Remove extra spaces
    text = re.sub( r"\s+", " ", text)
    return text.strip()

data["clean_title"] = data["title"].apply(clean_text)
data["clean_body"] = data["text"].apply(clean_text)
#Training and Splitting

print("\nSplitting dataset...")

train_data, test_data = train_test_split(data,test_size=0.20,random_state=42,stratify=data["label"])

train_data = train_data.reset_index(drop=True)
test_data = test_data.reset_index(drop=True)

print("Training articles:", len(train_data))
print("Testing articles:", len(test_data))

#Tf-IDF
print("\nCreating TF-IDF model...")

tfidf = TfidfVectorizer(max_features=10000,stop_words="english",ngram_range=(1, 2))

# TF-IDF is fitted ONLY on training data.
training_text = pd.concat([
    train_data["clean_title"],
    train_data["clean_body"]
])

tfidf.fit(training_text)

print("TF-IDF vocabulary size:",len(tfidf.get_feature_names_out()))


#Calculating TF-IDF similarity
def calculate_tfidf_similarity(title, body):

    title_vector = tfidf.transform([title])

    body_vector = tfidf.transform([body])

    similarity = cosine_similarity( title_vector, body_vector)[0][0]
    return similarity


print("\nCalculating lexical similarity...")


train_data["tfidf_similarity"] = train_data.apply(
    lambda row: calculate_tfidf_similarity(
        row["clean_title"],row["clean_body"] ),
    axis=1
)

test_data["tfidf_similarity"] = test_data.apply(
    lambda row: calculate_tfidf_similarity(
        row["clean_title"],row["clean_body"] ),
    axis=1
)
#Sentence Embedding

print("\nLoading sentence embedding model...")

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)
#Semantic Similarity

print("\nCreating semantic embeddings...")

train_title_embeddings = embedding_model.encode(
    train_data["clean_title"].tolist(),
    show_progress_bar=True
)

train_body_embeddings = embedding_model.encode(
    train_data["clean_body"].tolist(),
    show_progress_bar=True
)

test_title_embeddings = embedding_model.encode(
    test_data["clean_title"].tolist(),
    show_progress_bar=True
)

test_body_embeddings = embedding_model.encode(
    test_data["clean_body"].tolist(),
    show_progress_bar=True
)


def calculate_semantic_similarity(title_embedding,body_embedding):

    return cosine_similarity(
        [title_embedding],
        [body_embedding])[0][0]


print("\nCalculating semantic similarity...")


train_data["semantic_similarity"] = [
    calculate_semantic_similarity(
        train_title_embeddings[i],
        train_body_embeddings[i]
    )
    for i in range(len(train_data))
]


test_data["semantic_similarity"] = [
    calculate_semantic_similarity(
        test_title_embeddings[i],
        test_body_embeddings[i]
    )
    for i in range(len(test_data))
]


def word_count(text):

    return len(text.split())


def length_ratio(title, body):

    title_words = word_count(title)
    body_words = word_count(body)

    if body_words == 0:
        return 0

    return title_words / body_words


# Headline length
train_data["title_length"] = (
    train_data["clean_title"].apply(word_count)
)

test_data["title_length"] = (
    test_data["clean_title"].apply(word_count)
)


# Article body length
train_data["body_length"] = (
    train_data["clean_body"].apply(word_count)
)

test_data["body_length"] = (
    test_data["clean_body"].apply(word_count)
)


# Headline/body length ratio
train_data["length_ratio"] = train_data.apply(
    lambda row: length_ratio(
        row["clean_title"],
        row["clean_body"]
    ),
    axis=1
)

test_data["length_ratio"] = test_data.apply(
    lambda row: length_ratio(
        row["clean_title"],
        row["clean_body"]
    ),
    axis=1
)


# Question marks in headline
train_data["question_marks"] = (
    train_data["title"].str.count(r"\?")
)

test_data["question_marks"] = (
    test_data["title"].str.count(r"\?")
)


# Exclamation marks in headline
train_data["exclamation_marks"] = (
    train_data["title"].str.count("!")
)

test_data["exclamation_marks"] = (
    test_data["title"].str.count("!")
)


features = [
    "tfidf_similarity",
    "semantic_similarity",
    "title_length",
    "body_length",
    "length_ratio",
    "question_marks",
    "exclamation_marks"
]

X_train = train_data[features]
X_test = test_data[features]

y_train = train_data["label"]
y_test = test_data["label"]


print("\nFeatures used by hybrid model:")

for feature in features:
    print("-", feature)

#scaling of features

print("\nScaling features...")

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(
    X_train
)

X_test_scaled = scaler.transform(
    X_test
)

#training hybrid model

print("\nTraining hybrid model...")

model = LogisticRegression( max_iter=1000)

model.fit(X_train_scaled,y_train)


#evaluating the model
print("\nMaking predictions...")

y_pred = model.predict(X_test_scaled)

accuracy = accuracy_score(y_test,y_pred)
print("\n========================================")
print("       NEWSLENS HYBRID MODEL")
print("========================================")

print(f"\nAccuracy: {accuracy * 100:.2f}%")
print("\nClassification Report:")
print(classification_report(y_test,y_pred,target_names=["Fake", "Real"]))

print("\nSaving models...")

joblib.dump(
    model,
    "models/hybrid_model.pkl"
)

joblib.dump(
    tfidf,
    "models/tfidf_vectorizer.pkl"
)

joblib.dump(
    scaler,
    "models/feature_scaler.pkl"
)

joblib.dump(
    embedding_model,
    "models/embedding_model.pkl"
)

joblib.dump(
    features,
    "models/feature_names.pkl"
)


print("\n========================================")
print("All models saved successfully!")
print("========================================")

print("\nSaved files:")

print("✓ models/hybrid_model.pkl")
print("✓ models/tfidf_vectorizer.pkl")
print("✓ models/feature_scaler.pkl")
print("✓ models/embedding_model.pkl")
print("✓ models/feature_names.pkl")

print("\nTraining completed successfully!")