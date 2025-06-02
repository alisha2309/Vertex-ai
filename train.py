import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import os

# Load data from Cloud Storage
data_path = "/gcs/chatbot-data01/customers.csv"
df = pd.read_csv(data_path)

# Preprocess and train
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["message"])
y = df["response"]
model = LogisticRegression()
model.fit(X, y)

# Save model artifacts
model_dir = os.getenv("AIP_MODEL_DIR", "/tmp/model")
joblib.dump(model, f"{model_dir}/model.pkl")
joblib.dump(vectorizer, f"{model_dir}/vectorizer.pkl")
