# Fake News Detector

An AI-powered web application that analyzes news headlines and article bodies to identify potentially fake or misleading content.

The project combines **Machine Learning, NLP, TF-IDF similarity, semantic similarity, and rule-based clickbait detection** to provide multiple signals instead of relying on a single prediction.

> **Note:** This project is designed as an analytical tool and is not a fact-checking system.

---

## Demo

![NewsLens Demo](images/demo.png)

The application provides an interactive dashboard showing:

- Fake / Real prediction
- Fake and Real probabilities
- TF-IDF lexical similarity
- Semantic similarity
- Headline-body match
- Discrepancy score
- Clickbait score
- Article statistics
- Overall assessment

---

## How It Works

The system takes a **news headline and article body** as input and analyzes their relationship using multiple techniques.

```text
                  HEADLINE + ARTICLE BODY
                            │
                            ▼
                      TEXT CLEANING
                            │
                            ▼
                    FEATURE EXTRACTION
                            │
             ┌──────────────┴──────────────┐
             │                             │
             ▼                             ▼
       TF-IDF SIMILARITY          SEMANTIC SIMILARITY
       (Lexical Matching)         (Sentence Transformer)
             │                             │
             └──────────────┬──────────────┘
                            │
                            ▼
                    ADDITIONAL FEATURES
                            │
                            ▼
                     FEATURE SCALING
                            │
                            ▼
                  LOGISTIC REGRESSION
                            │
                            ▼
                     FAKE / REAL
                            │
                            │
        ┌───────────────────┘
        │
        ▼
   HEADLINE ANALYSIS
        │
        ▼
  CLICKBAIT DETECTION
        │
        ▼
  CLICKBAIT SCORE (0–100)
        │
        └──────────────┐
                       ▼
                 FINAL RESULTS
                       │
                       ▼
                   NEWSLENS UI
```

### Two Main Analysis Paths

**1. Hybrid ML Analysis**

The headline and article body are compared using:

- TF-IDF cosine similarity
- Sentence Transformer semantic similarity
- Headline and article length features
- Question and exclamation mark counts
- Headline-to-body length ratio

These features are scaled and passed to a **Logistic Regression classifier**.

**2. Clickbait Analysis**

The headline is separately analyzed for common clickbait patterns such as:

- Sensational words
- Curiosity-gap phrases
- Excessive `!`
- Excessive `?`
- Excessive capitalization

---

## Features

### 1. Fake / Real News Prediction

The hybrid Logistic Regression model predicts whether the submitted article is:

- **Fake**
- **Real**

The application also displays the model's probability for both classes.

---

### 2. TF-IDF Similarity

TF-IDF (**Term Frequency–Inverse Document Frequency**) represents the headline and article body numerically.

Cosine similarity is then used to measure their **lexical overlap**.

A higher score generally indicates that the headline and article body share more vocabulary.

---

### 3. Semantic Similarity

The project uses the **`all-MiniLM-L6-v2` Sentence Transformer** model.

Unlike simple word matching, semantic similarity helps identify whether the headline and article body discuss similar ideas even when different words are used.

---

### 4. Headline–Body Consistency

The TF-IDF and semantic similarity scores are combined to produce a **headline-body match score**.

The application also displays a **discrepancy score**:

```text
Discrepancy = 100 - Headline-Body Match
```

A high discrepancy indicates that the headline and article body may need closer examination.

---

### 5. Clickbait Detection

The rule-based clickbait analyzer checks for:

- Sensational vocabulary
- Curiosity-gap phrases
- Excessive exclamation marks
- Excessive question marks
- Excessive capitalization

The result is presented as a score from **0 to 100**.

The application categorizes the result as:

- **LOW CLICKBAIT**
- **MODERATE CLICKBAIT**
- **HIGH CLICKBAIT**

---

### 6. Article Statistics

The dashboard also displays:

- Number of words in the headline
- Number of words in the article
- Headline/body length ratio
- Number of question marks
- Number of exclamation marks

These statistics provide additional context for the analysis.

---

## Dataset

The project uses the **Fake and Real News Dataset**, containing separate CSV files for fake and real news articles.

### Original Dataset

| Category | Articles |
|---|---:|
| Fake | 23,481 |
| Real | 21,417 |
| **Total** | **44,898** |

After removing duplicate headline + article combinations:

**39,105 unique articles** were used.

### Main Columns

The dataset contains:

- `title`
- `text`
- `subject`
- `date`

For model training:

```text
Fake News → Label 0
Real News → Label 1
```

---

## Model Performance

The current hybrid model achieved approximately:

### Accuracy

**84.02%**

### Classification Report

| Class | Precision | Recall | F1-Score |
|---|---:|---:|---:|
| Fake | 85% | 79% | 82% |
| Real | 83% | 88% | 86% |

The performance is based on the dataset used for this project.

> A high test accuracy on this dataset does not mean the model can determine the factual truth of every real-world news article.

---

## Technologies Used

### Programming

- Python

### Data Processing

- Pandas
- NumPy

### Machine Learning

- Scikit-learn
- Logistic Regression
- Feature Scaling

### NLP

- TF-IDF
- Cosine Similarity
- Sentence Transformers
- `all-MiniLM-L6-v2`

### Application

- Gradio

### Model Persistence

- Joblib

---

## Project Structure

```text
Fake_news_detector/
│
├── data/
│   ├── Fake.csv
│   └── True.csv
│
├── models/
│   ├── embedding_model.pkl
│   ├── feature_scaler.pkl
│   ├── hybrid_model.pkl
│   └── tfidf_vectorizer.pkl
│
├── images/
│   └── demo.png
│
├── analyzer.py
├── app.py
├── clickbait.py
├── train_model.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## What the Main Files Do

### `train_model.py`

- Loads the fake and real news datasets
- Cleans the text
- Removes duplicate articles
- Creates headline-body features
- Calculates TF-IDF similarity
- Calculates semantic similarity
- Trains the Logistic Regression model
- Evaluates the model
- Saves the trained model components

### `analyzer.py`

Loads the saved models and analyzes a new headline and article body.

It calculates:

- Fake / Real probability
- TF-IDF similarity
- Semantic similarity
- Headline-body match
- Discrepancy
- Article statistics

### `clickbait.py`

Contains the rule-based clickbait detection logic.

### `app.py`

Creates the Gradio web interface and displays the analysis results in an interactive dashboard.

### `requirements.txt`

Contains the Python libraries required to run the project.

---

## Running the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/mvshre-m27/Fake_news_detector.git
```

### 2. Open the project folder

```bash
cd Fake_news_detector
```

### 3. Install the required libraries

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

Gradio will provide a local link in the terminal.

Open that link in your browser to use the application.

---

## Example Tests

The application can be tested using different types of headlines.

### Normal News

A headline that accurately represents the article should generally show better headline-body consistency and lower discrepancy.

### Misleading Headline

A headline discussing something that is not actually supported by the article body should produce a higher discrepancy score.

### Clickbait Headline

For example:

```text
YOU WON'T BELIEVE WHAT HAPPENED NEXT!!!
```

This should trigger multiple clickbait indicators such as:

- Curiosity-gap wording
- Sensational language
- Excessive capitalization
- Multiple exclamation marks

---

## Important Limitation

This project is **not a fact-checking system**.

The Machine Learning model learns statistical patterns from the training dataset. Therefore:

> **"Likely Real" does not guarantee that an article is factually true.**

Similarly:

> **A high headline-body discrepancy does not automatically mean that an article is fake.**

The project instead provides **multiple analytical signals** that can help a user examine a news article more carefully.

This distinction is important because fake-news detection and factual verification are different problems.

---

## Future Improvements

Possible future improvements include:

- Real-time news scraping
- News source credibility analysis
- Named Entity Recognition
- Explainable AI for model predictions
- Multilingual news detection
- Transformer-based fake news classification
- Fact-checking API integration
- Improved clickbait classification using machine learning
- Comparison with additional news datasets

---

## Project Goal

The goal of this project is to explore how **NLP and Machine Learning can be combined with headline-body consistency and clickbait analysis** to provide a more informative approach to news analysis.

Rather than giving users only a **Fake / Real** label, the system provides additional evidence such as similarity, discrepancy, clickbait indicators, and article statistics.

---

## Author

Developed as an academic Machine Learning and NLP project.
