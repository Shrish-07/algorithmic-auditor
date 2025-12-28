import pandas as pd
import os

RAW_DIR = "data/raw"
OUT_PATH = "data/processed/clean_loans.csv"

os.makedirs("data/processed", exist_ok=True)

def clean_dti(val):
    if pd.isna(val):
        return None
    if isinstance(val, (int, float)):
        return float(val)
    if isinstance(val, str):
        # Remove %, <, and >, then strip whitespace
        cleaned = val.replace("%", "").replace("<", "").replace(">", "").strip()
        # Handle ranges like "30-35" by taking the lower bound
        parts = cleaned.split("-")
        try:
            return float(parts[0])
        except ValueError:
            return None
    return None

raw_files = [f for f in os.listdir(RAW_DIR) if f.endswith(".csv")]
if not raw_files:
    raise FileNotFoundError("No raw HMDA CSV found in data/raw")

RAW_PATH = os.path.join(RAW_DIR, raw_files[0])
print("Using raw file:", RAW_PATH)


use_cols = [
    "action_taken",
    "loan_purpose",
    "loan_amount",
    "combined_loan_to_value_ratio",
    "property_value",
    "occupancy_type",
    "income",
    "debt_to_income_ratio",
    "applicant_race_1"
]


chunks = []
CHUNK_SIZE = 250_000

for chunk in pd.read_csv(
    RAW_PATH,
    usecols=use_cols,
    low_memory=False,
    chunksize=CHUNK_SIZE
):
  
    chunk = chunk[chunk["action_taken"].isin([1, 3])]
    chunks.append(chunk)

 
    if sum(len(c) for c in chunks) >= 120_000:
        break

df = pd.concat(chunks, ignore_index=True)
print("Rows after early filtering:", len(df))


df["approved"] = (df["action_taken"] == 1).astype(int)
df = df.drop(columns=["action_taken"])


df = df.replace("Exempt", pd.NA)

df["debt_to_income_ratio"] = df["debt_to_income_ratio"].apply(clean_dti)

df = df.dropna()


race_map = {
    1: "American Indian or Alaska Native",
    2: "Asian",
    3: "Black",
    4: "Native Hawaiian or Pacific Islander",
    5: "White",
    6: "Other"
}

df["race_group"] = df["applicant_race_1"].map(race_map)
df = df[df["race_group"].notna()]
df = df.drop(columns=["applicant_race_1"])


df = (
    df.groupby("race_group", group_keys=False)
      .apply(lambda x: x.sample(min(len(x), 12_000), random_state=42))
)

print("Final dev rows:", len(df))


df.to_csv(OUT_PATH, index=False)
print("Saved dev dataset →", OUT_PATH)