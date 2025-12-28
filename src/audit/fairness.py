import pandas as pd
import joblib
import os

MODEL_PATH = "models/approval_model.joblib"

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        f"Model not found at {MODEL_PATH}. "
        "Please run src/model/train_model.py first to train and save the model."
    )

df = pd.read_csv("data/processed/clean_loans.csv")
model = joblib.load(MODEL_PATH)

X = df.drop(columns=["approved", "race_group"])
df["score"] = model.predict_proba(X)[:, 1]

THRESHOLD = 0.7
df["pred"] = (df["score"] >= THRESHOLD).astype(int)

def demographic_parity(df):
    return df.groupby("race_group")["pred"].mean()

def equal_opportunity(df):
    return (
        df[df["approved"] == 1]
        .groupby("race_group")["pred"]
        .mean()
    )

print("=== DEMOGRAPHIC PARITY ===")
print(demographic_parity(df))

print("\n=== EQUAL OPPORTUNITY ===")
print(equal_opportunity(df))