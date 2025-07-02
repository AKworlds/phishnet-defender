
import streamlit as st
import pandas as pd
import joblib
import os
import re
import requests
import json

# === Utility Functions ===
def clean_email(text):
    text = re.sub(r"http\S+", " URL ", text)
    text = re.sub(r"\S+@\S+", " EMAIL ", text)
    text = re.sub(r"<.*?>", "", text)
    text = re.sub(r"[^a-zA-Z]", " ", text)
    return text.lower().strip()

def get_latest_model(pattern):
    model_dir = os.path.join(os.path.dirname(__file__), "..", "models")
    files = sorted([f for f in os.listdir(model_dir) if f.startswith(pattern.replace("*.pkl", ""))], reverse=True)
    if files:
        return joblib.load(os.path.join(model_dir, files[0]))
    return None

def get_reason_summary(content_type, input_text, prediction):
    if content_type == "email":
        if prediction == 1:
            reasons = []
            if any(w in input_text.lower() for w in ["verify", "urgent", "click", "update", "account"]):
                reasons.append("Contains urgent or manipulative language.")
            if "http" in input_text.lower() or "www." in input_text.lower():
                reasons.append("Contains suspicious links.")
            if "@" in input_text and not input_text.lower().endswith("@company.com"):
                reasons.append("Email sender domain is unfamiliar.")
            return " ".join(reasons) or "Detected phishing-like patterns."
        else:
            return "No suspicious keywords or links found. Structure matches legitimate emails."
    elif content_type == "url":
        if prediction == 1:
            reasons = []
            if "-" in input_text or any(tld in input_text.lower() for tld in [".ru", ".cn", ".info"]):
                reasons.append("Uses uncommon or deceptive domain patterns.")
            if input_text.count("/") > 3:
                reasons.append("URL path is unusually long or obfuscated.")
            if any(p in input_text.lower() for p in ["login", "secure", "verify"]):
                reasons.append("Contains phishing-related keywords.")
            if "@" in input_text or input_text.startswith("http://"):
                reasons.append("Uses risky formatting like IP-based or user-info URLs.")
            return " ".join(reasons) or "URL matches phishing behavior."
        else:
            return "Domain and structure appear clean and typical of known legitimate sources."

# === Load Models ===
model_dir = os.path.join(os.path.dirname(__file__), "..", "models")
email_model_path = os.path.join(model_dir, "phishnet_model.pkl")
url_model_path = os.path.join(model_dir, "url_model.pkl")

email_model = joblib.load(email_model_path) if os.path.exists(email_model_path) else None
url_model = joblib.load(url_model_path) if os.path.exists(url_model_path) else None

# === Streamlit UI ===
st.set_page_config(page_title="PhishNet Defender", page_icon="🛡️")
st.title(":shield: PhishNet Defender")

st.subheader("Paste an email to detect phishing", divider="gray")
user_input = st.text_area("Enter email content below:")

if st.button("Analyze Email"):
    if user_input.strip() == "":
        st.warning("Please paste some email content first.")
    elif not email_model:
        st.error("❌ Email model not found. Please run the training pipeline first.")
    else:
        cleaned = clean_email(user_input)
        prediction = email_model.predict([cleaned])[0]
        proba = email_model.predict_proba([cleaned])[0]

        label = "Phishing" if prediction == 1 else "Legit"
        color = "red" if prediction == 1 else "green"
        confidence = round(proba[prediction] * 100, 2)
        reason = get_reason_summary("email", user_input, prediction)

        st.markdown(f"### Result: **:{color}[{label}]**")
        st.markdown(f"Confidence: `{confidence}%`")
        st.markdown(f"**Reason Summary:** {reason}")

st.markdown("---")
st.subheader("🔗 Check a URL for safety", divider="gray")
url_input = st.text_input("Enter a URL")

if st.button("Analyze URL"):
    if not url_input.strip():
        st.warning("Please enter a URL.")
    elif not url_model:
        st.error("❌ URL model not found. Please run the training pipeline first.")
    else:
        try:
            from url_features import extract_url_features
            features_df = pd.DataFrame([extract_url_features(url_input)])
            prediction = url_model.predict(features_df)[0]
            proba = url_model.predict_proba(features_df)[0]

            label = "URL not safe" if prediction == 1 else "Legit"
            color = "red" if prediction == 1 else "green"
            confidence = round(proba[prediction] * 100, 2)
            reason = get_reason_summary("url", url_input, prediction)

            st.markdown(f"### Result: **:{color}[{label}]**")
            st.markdown(f"Confidence: `{confidence}%`")
            st.markdown(f"**Reason Summary:** {reason}")

        except Exception as e:
            st.error(f"Error during URL analysis: {e}")

import streamlit as st
import pandas as pd
import joblib
import os
import re
import requests
import json

# === Utility Functions ===
def clean_email(text):
    text = re.sub(r"http\S+", " URL ", text)
    text = re.sub(r"\S+@\S+", " EMAIL ", text)
    text = re.sub(r"<.*?>", "", text)
    text = re.sub(r"[^a-zA-Z]", " ", text)
    return text.lower().strip()

def get_latest_model(pattern):
    model_dir = os.path.join(os.path.dirname(__file__), "..", "models")
    files = sorted([f for f in os.listdir(model_dir) if f.startswith(pattern.replace("*.pkl", ""))], reverse=True)
    if files:
        return joblib.load(os.path.join(model_dir, files[0]))
    return None

def get_reason_summary(content_type, input_text, prediction):
    if content_type == "email":
        if prediction == 1:
            reasons = []
            if any(w in input_text.lower() for w in ["verify", "urgent", "click", "update", "account"]):
                reasons.append("Contains urgent or manipulative language.")
            if "http" in input_text.lower() or "www." in input_text.lower():
                reasons.append("Contains suspicious links.")
            if "@" in input_text and not input_text.lower().endswith("@company.com"):
                reasons.append("Email sender domain is unfamiliar.")
            return " ".join(reasons) or "Detected phishing-like patterns."
        else:
            return "No suspicious keywords or links found. Structure matches legitimate emails."
    elif content_type == "url":
        if prediction == 1:
            reasons = []
            if "-" in input_text or any(tld in input_text.lower() for tld in [".ru", ".cn", ".info"]):
                reasons.append("Uses uncommon or deceptive domain patterns.")
            if input_text.count("/") > 3:
                reasons.append("URL path is unusually long or obfuscated.")
            if any(p in input_text.lower() for p in ["login", "secure", "verify"]):
                reasons.append("Contains phishing-related keywords.")
            if "@" in input_text or input_text.startswith("http://"):
                reasons.append("Uses risky formatting like IP-based or user-info URLs.")
            return " ".join(reasons) or "URL matches phishing behavior."
        else:
            return "Domain and structure appear clean and typical of known legitimate sources."

# === Load Models ===
model_dir = os.path.join(os.path.dirname(__file__), "..", "models")
email_model_path = os.path.join(model_dir, "phishnet_model.pkl")
url_model_path = os.path.join(model_dir, "url_model.pkl")

email_model = joblib.load(email_model_path) if os.path.exists(email_model_path) else None
url_model = joblib.load(url_model_path) if os.path.exists(url_model_path) else None

# === Streamlit UI ===
st.set_page_config(page_title="PhishNet Defender", page_icon="🛡️")
st.title(":shield: PhishNet Defender")

st.subheader("Paste an email to detect phishing", divider="gray")
user_input = st.text_area("Enter email content below:")

if st.button("Analyze Email"):
    if user_input.strip() == "":
        st.warning("Please paste some email content first.")
    elif not email_model:
        st.error("❌ Email model not found. Please run the training pipeline first.")
    else:
        cleaned = clean_email(user_input)
        prediction = email_model.predict([cleaned])[0]
        proba = email_model.predict_proba([cleaned])[0]

        label = "Phishing" if prediction == 1 else "Legit"
        color = "red" if prediction == 1 else "green"
        confidence = round(proba[prediction] * 100, 2)
        reason = get_reason_summary("email", user_input, prediction)

        st.markdown(f"### Result: **:{color}[{label}]**")
        st.markdown(f"Confidence: `{confidence}%`")
        st.markdown(f"**Reason Summary:** {reason}")

st.markdown("---")
st.subheader("🔗 Check a URL for safety", divider="gray")
url_input = st.text_input("Enter a URL")

if st.button("Analyze URL"):
    if not url_input.strip():
        st.warning("Please enter a URL.")
    elif not url_model:
        st.error("❌ URL model not found. Please run the training pipeline first.")
    else:
        try:
            from url_features import extract_url_features
            features_df = pd.DataFrame([extract_url_features(url_input)])
            prediction = url_model.predict(features_df)[0]
            proba = url_model.predict_proba(features_df)[0]

            label = "URL not safe" if prediction == 1 else "Legit"
            color = "red" if prediction == 1 else "green"
            confidence = round(proba[prediction] * 100, 2)
            reason = get_reason_summary("url", url_input, prediction)

            st.markdown(f"### Result: **:{color}[{label}]**")
            st.markdown(f"Confidence: `{confidence}%`")
            st.markdown(f"**Reason Summary:** {reason}")

        except Exception as e:
            st.error(f"Error during URL analysis: {e}")

