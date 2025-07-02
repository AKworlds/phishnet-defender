
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from url_features import extract_url_features
import joblib
import os

def prepare_url_data(urls, labels):
    feature_rows = []
    for url in urls:
        features = extract_url_features(url)
        feature_rows.append(features)
    df = pd.DataFrame(feature_rows)
    df["label"] = labels
    return df

def train_url_model(df):
    X = df.drop("label", axis=1)
    y = df["label"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    clf = RandomForestClassifier()
    clf.fit(X_train, y_train)
    print(classification_report(y_test, clf.predict(X_test)))
    return clf

def save_url_model(model, path="models/url_model.pkl"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(model, path)

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from url_features import extract_url_features
import joblib
import os

def prepare_url_data(urls, labels):
    feature_rows = []
    for url in urls:
        features = extract_url_features(url)
        feature_rows.append(features)
    df = pd.DataFrame(feature_rows)
    df["label"] = labels
    return df

def train_url_model(df):
    X = df.drop("label", axis=1)
    y = df["label"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    clf = RandomForestClassifier()
    clf.fit(X_train, y_train)
    print(classification_report(y_test, clf.predict(X_test)))
    return clf

def save_url_model(model, path="models/url_model.pkl"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(model, path)

