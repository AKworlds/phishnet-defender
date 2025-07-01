import re
import pandas as pd
from sklearn.model_selection import train_test_split

def clean_email(text):
    if pd.isnull(text):
        return ""
    text = re.sub(r"http\S+", " URL ", text)
    text = re.sub(r"\S+@\S+", " EMAIL ", text)
    text = re.sub(r"<.*?>", "", text)
    text = re.sub(r"[^a-zA-Z]", " ", text)
    text = text.lower()
    return text.strip()

def load_and_prepare(phish_path, legit_path):
    df_phish = pd.read_csv(phish_path)
    df_legit = pd.read_csv(legit_path)

    df_phish["label"] = 1
    df_legit["label"] = 0

    df = pd.concat([df_phish, df_legit])
    df["text"] = df["text"].apply(clean_email)

    return train_test_split(df["text"], df["label"], test_size=0.2, random_state=42)
