Fake News Detector
A simple Machine Learning + NLP based web application that helps analyze whether a news article looks more like fake or real news.
The main idea behind this project is not just to classify an article using its words. The system also checks whether the headline actually matches the article body and whether the headline shows common clickbait patterns.
I built this project to understand how different NLP techniques can work together in a practical application.

What does this project do?

The application takes two inputs:
A news headline and the article body ,It then performs three main types of analysis:
-Fake/Real Prediction – a hybrid ML model predicts whether the article is more associated with fake or real news.
-Headline–Body Analysis – compares the headline and article body using both word-level and meaning-level similarity.
-Clickbait Detection – checks the headline for sensational wording, excessive punctuation, capitalization, and curiosity-gap phrases.
The results are displayed through an interactive Gradio web interface.

## Demo

![NewsLens Demo](images/demo.png)

Why did I use a hybrid approach?
A headline and an article can use different words but still talk about the same thing.
For example:

Headline: NASA scientists discover new evidence about Mars

The article might say:
Researchers studying the Martian surface have found evidence suggesting that water existed on Mars in the past.

The exact words are different, but the meaning is related.Because of this, the project uses two types of similarity:

TF-IDF + Cosine Similarity → checks lexical/word-level similarity
Sentence Transformers + Cosine Similarity → checks semantic/meaning-level similarity
These are combined with a few additional article features and given to a Logistic Regression model.

How the system works

Headline + Article Body
          |
          v
     Text Cleaning
          |
     -----+-----
     |         |
     v         v
   TF-IDF   Sentence
 Similarity Transformer
     |         |
     |         v
     |    Semantic Similarity
     |         |
     +----+----+
          |
          v
  Additional Features
          |
          v
     7 ML Features
          |
          v
   Feature Scaling
          |
          v
 Logistic Regression
          |
          v
    Fake / Real

At the same time, the headline is passed through a separate clickbait analyzer.

Features:

1. Fake / Real News Prediction

The hybrid Logistic Regression model predicts:Fake or Real
The application also displays the model's probability for both classes.

2. TF-IDF Similarity

TF-IDF is used to represent the headline and article body numerically.
Cosine similarity is then used to measure how much their words overlap.

3. Semantic Similarity

The project uses the all-MiniLM-L6-v2 Sentence Transformer model.
This helps compare the meaning of the headline and article body, even when they don't use exactly the same words.

4. Headline–Body Match

The TF-IDF similarity and semantic similarity are combined to calculate a headline-body match score.
A corresponding discrepancy score is also shown.
A high discrepancy means that the headline and article body should be reviewed more carefully.

5. Clickbait Detection

The clickbait analyzer looks for things such as:
Sensational words
"You won't believe..." type phrases
Excessive !, Excessive ? , Excessive capitalization
Curiosity-gap wording
It produces a score from 0 to 100.

6. Article Statistics

The application also displays:
-Number of words in the headline
-Number of words in the article
-Headline/body length ratio
-Number of question marks
-Number of exclamation marks

Dataset

The project uses the Fake and Real News Dataset containing separate fake and real news CSV files.
Original dataset:
Fake articles: 23,481

Real articles: 21,417

Total: 44,898
After removing duplicate articles: 39,105 articles

The main columns used are:
title
text
subject
date

For this project:

Fake news → label 0

Real news → label 1

Model Performance

The current hybrid model achieved approximately:

84.02% accuracy

Classification results:
Class   Precision   Recall     F1-Score
Fake      85%         79%        82%
Real      83%         88%        86%

The result is based on the dataset used for this project and should not be interpreted as proof that the system can determine the truth of every real-world news article.

Technologies Used:

-Python
-Pandas
-NumPy
-Scikit-learn
-Logistic Regression
-TF-IDF
-Cosine Similarity
-Sentence Transformers
-all-MiniLM-L6-v2
-Joblib
-Gradio

Project Structure:

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
├── analyzer.py
├── app.py
├── clickbait.py
├── train_model.py
├── requirements.txt
└── README.md

What the main files do

train_model.py
Cleans the dataset, creates the features, trains the hybrid Logistic Regression model, evaluates it, and saves the trained components.

analyzer.py
Loads the saved models and analyzes a new headline and article body.

clickbait.py
Contains the rule-based clickbait detection logic.

app.py
Creates the Gradio web interface and displays the analysis results.

requirements.txt
Contains the Python libraries needed to run the project.

Running the project locally

1. Clone the repository

git clone <your-repository-url>

2. Open the project folder

cd Fake_news_detector

3. Install the required libraries

pip install -r requirements.txt

4. Run the application

python app.py

Gradio will provide a local link in the terminal. Open that link in your browser.

Example tests

The application can be tested using different types of headlines.

Normal news

A headline that accurately represents the article should generally show better headline-body consistency.

Misleading headline

A headline that talks about something that is not actually discussed in the article should produce a higher discrepancy score.

Clickbait headline

A headline such as:

"YOU WON'T BELIEVE WHAT HAPPENED NEXT!!!"

should trigger several clickbait indicators.

Important limitation

This project is not a fact-checking system.

The Machine Learning model learns patterns from the training dataset. Therefore, a prediction such as "Likely Real" does not guarantee that the article is factually true.

Similarly, a high headline-body discrepancy does not automatically mean that the article itself is fake.

The purpose of this project is to provide multiple analytical signals that can help a user examine a news article more carefully.

Future Improvements

Some improvements I would like to explore in the future are:

Real-time news scraping

News source credibility analysis

Named Entity Recognition

Explainable AI for model predictions

Multilingual news detection

Transformer-based fake news classification

Fact-checking API integration

Browser extension for analyzing headlines while browsing

Project Goal

The main goal of this project was to build something that goes beyond a basic "Fake or Real" classifier.

By combining Machine Learning, NLP, lexical similarity, semantic similarity, and clickbait analysis, the project tries to give a more useful picture of why a headline might deserve a closer look.

Built as a Machine Learning and NLP project.