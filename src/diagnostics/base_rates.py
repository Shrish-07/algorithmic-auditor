import pandas as pd

df = pd.read_csv("data/processed/clean_loans.csv")

rates = (
    df.groupby("race_group")["approved"]
      .mean()
      .sort_values(ascending=False)
)

print("=== TRUE APPROVAL RATES BY RACE ===")
print(rates)
