import os
import sys
import joblib
import pandas as pd
from datetime import datetime

# === Fix Python path so "src" is importable ===
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from src.url_model import prepare_url_data, train_url_model
from src.model import train_model
from src.preprocessing import clean_email

# === 1. Fetch Phishing URLs from PhishTank ===
def fetch_phishing_urls():
    print("⚠️ Live phishing URL fetch skipped. Using backup list...")
    phishing_urls = [
        "https://paypal.com-login.secure-verify.net",
        "http://192.168.1.1/login",
        "https://tinyurl.com/secure-access",
        "https://verify-apple.com-reset-password.co",
        "https://login-instagram-help.com",
        "https://secure.amaz0n-login.info",
        "https://plala.voxel6.com/login",
        "https://jaergfv3.duckdns.org/",
        "http://secure-apple-login.com",
        "http://amaz0n-support-mail.ru",
        "http://login-verify-instagram-help.info"
    ]
    df = pd.DataFrame({"url": phishing_urls})
    save_path = os.path.join(BASE_DIR, "data", "urls_phishing.csv")
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    df.to_csv(save_path, index=False)
    print(f"✅ Backup phishing URLs saved to {save_path}")


# === 2. Save Static Legit URLs ===
def fetch_legit_urls():
    urls = [
        "https://www.google.com/", "https://www.amazon.com/",
        "https://www.github.com/", "https://www.nytimes.com/",
        "https://www.microsoft.com/", "https://www.apple.com/",
        "https://www.reddit.com/", "https://www.wikipedia.org/",
        "https://www.stackoverflow.com/", "https://www.linkedin.com/"
    ]
    df = pd.DataFrame({"url": urls})
    df.to_csv(os.path.join(BASE_DIR, "data", "urls_legit.csv"), index=False)
    print("✅ Legit URLs saved.")

# === 3. Write Sample Emails ===
def fetch_emails():
    legit = [
        "Your invoice is attached. Thanks for your business.",
        "Your package has shipped. Track it here: https://ups.com/tracking",
        "Reminder: Your appointment with Dr. Smith is Monday at 10AM.",
    ]
    phish = [
        "Your PayPal account has been locked. Log in here: http://secure-paypal.co/login",
        "You’ve won an Amazon gift card! Click here to claim: http://bit.ly/fakeclaim",
        "Immediate action required: confirm your Apple ID at http://apple.verify.com",
    ]

    with open(os.path.join(BASE_DIR, "data", "emails_legit.txt"), "w") as f:
        f.write("\n".join(legit))
    with open(os.path.join(BASE_DIR, "data", "emails_phishing.txt"), "w") as f:
        f.write("\n".join(phish))

    print("✅ Sample phishing and legit emails saved.")

# === 4. Train URL Model ===
def train_url_detector():
    legit_path = os.path.join(BASE_DIR, "data", "urls_legit.csv")
    phish_path = os.path.join(BASE_DIR, "data", "urls_phishing.csv")
    df_legit = pd.read_csv(legit_path)
    df_phish = pd.read_csv(phish_path)

    df_legit["label"] = 0
    df_phish["label"] = 1
    df = pd.concat([df_legit, df_phish], ignore_index=True)

    url_features = prepare_url_data(df["url"].tolist(), df["label"].tolist())
    model = train_url_model(url_features)

    os.makedirs(os.path.join(BASE_DIR, "models"), exist_ok=True)
    joblib.dump(model, os.path.join(BASE_DIR, "models", "url_model.pkl"))
    print("✅ URL model trained and saved.")

# === 5. Train Email Model ===
def train_email_detector():
    legit_path = os.path.join(BASE_DIR, "data", "emails_legit.txt")
    phish_path = os.path.join(BASE_DIR, "data", "emails_phishing.txt")

    with open(legit_path, "r") as f:
        legit = [{"text": line.strip(), "label": 0} for line in f if line.strip()]
    with open(phish_path, "r") as f:
        phish = [{"text": line.strip(), "label": 1} for line in f if line.strip()]

    df = pd.DataFrame(legit + phish)
    df["text"] = df["text"].apply(clean_email)

    model = train_model(df["text"], df["label"])

    joblib.dump(model, os.path.join(BASE_DIR, "models", "phishnet_model.pkl"))
    print("✅ Email model trained and saved.")

# === 6. Log Completion ===
def log_completion():
    log_path = os.path.join(BASE_DIR, "train_log.txt")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} - Model training complete ✅\n")
    print("📜 Training run logged.")


# === 🚀 Run Everything ===
if __name__ == "__main__":
    print("\n=== 🚧 Starting PhishNet Auto-Training Pipeline ===\n")
    fetch_phishing_urls()
    fetch_legit_urls()
    fetch_emails()
    train_url_detector()
    train_email_detector()
    log_completion()
    print("\n🎉 All models updated and ready for use.\n")
