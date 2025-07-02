from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib 
import os

def train_model(X_train, y_train):
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(stop_words="english", max_df=0.7)),
        ("clf", LogisticRegression(max_iter=1000))
    ])
    pipeline.fit(X_train, y_train)
    return pipeline

import os
import joblib

def save_model(model, path="models/phishnet_model.pkl"):
    # This line ensures the 'models/' folder exists
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(model, path)
    



