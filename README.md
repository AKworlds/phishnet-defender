# 🛡️ PhishNet Defender

**PhishNet Defender** is a dual-layer phishing detection system that uses machine learning and Google Safe Browsing to identify phishing **emails** and **URLs** in real time. This project was created after completing the AWS AI & ML Scholars program, combining NLP, URL feature engineering, Streamlit, and automation to create a deployable phishing detection app.

---

## 🔍 Features

- 📨 **Email Classification** — ML-based model classifies raw email content as **Phishing** or **Legit**
- 🔗 **URL Safety Check** — Uses ML + Google Safe Browsing API to flag malicious or suspicious URLs
- 📊 **Explainable Predictions** — Displays confidence scores and reasons for classification
- 🔄 **Auto-Retraining Pipeline** — Automatically fetches new data and retrains models on demand
- 🧪 **Jupyter Integration** — Includes notebooks for training, evaluation, and data exploration
- 🚀 **Streamlit UI** — Clean, interactive web interface to test emails or URLs in real time

---

## 📂 Project Structure
phishnet_defender/
│
├── app/                  # Streamlit frontend
│   └── streamlit_app.py
│
├── data/                 # Datasets (emails and URLs)
│   ├── phishing_emails.csv
│   ├── legit_emails.csv
│   ├── urls_phishing.csv
│   └── urls_legit.csv
│
├── models/               # Trained ML models
│   ├── phishnet_model.pkl
│   └── url_model.pkl
│
├── notebooks/            # Jupyter Notebooks for experimentation
│   └── 01-train-eval.ipynb
│
├── src/                  # Core ML logic and feature extraction
│   ├── model.py
│   ├── preprocessing.py
│   ├── evaluate.py
│   ├── url_model.py
│   └── utils.py
│
├── train.all.py          # Auto-retraining script
├── requirements.txt      # Python dependencies
└── .env                  # API keys and secrets (excluded via .gitignore)



---

## 🧠 Models

- **Email model**: Logistic Regression trained on labeled phishing vs legit email content
- **URL model**: Logistic Regression trained on feature-engineered URLs (length, digits, subdomains, etc.)
- **External check**: Google Safe Browsing API adds an extra layer of real-time blacklist checking

---

## ▶️ Usage

### 🔬 Local Development

1. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2. **Run training pipeline**:
    ```bash
    python src/train.all.py
    ```

3. **Launch app**:
    ```bash
    streamlit run app/streamlit_app.py
    ```

---

## 📓 Jupyter Notebooks

Explore how the models were developed and evaluated:
- `notebooks/01-train-eval.ipynb` — Preprocessing, model training, and performance metrics
- Used to validate model logic before integrating into the retraining script

---

## 🌐 API Integration

- Google Safe Browsing API is used to supplement URL predictions
- Replace `SAFE_BROWSING_API_KEY` in your `.env` file with your own key

---

## 🤖 Automation

- `train.all.py` fetches fresh email/URL data, retrains models, and saves outputs
- Results are logged and models are versioned automatically

---

## 🧾 License

MIT License

---

## 🙌 Acknowledgments

- **AWS AI & ML Scholarship Program** – For foundational training
- **PhishTank**, **Google Safe Browsing API** – For providing phishing data sources
