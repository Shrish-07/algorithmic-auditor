import pandas as pd
from sklearn.model_selection import train_test_split  
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
import joblib
import os

os.makedirs("models", exist_ok=True)

df = pd.read_csv("data/processed/clean_loans.csv")

X = df.drop(columns=["approved", "race_group"])
y = df["approved"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=8,
    min_samples_leaf=200,
    random_state=42
)

model.fit(X_train, y_train)

preds = model.predict_proba(X_test)[:, 1]
print("AUC:", roc_auc_score(y_test, preds))

joblib.dump(model, "models/approval_model.joblib")
print("Model saved to models/approval_model.joblib")