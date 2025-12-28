from preprocessing import load_and_clean

df = load_and_clean()

print("=== DATA SNAPSHOT ===")
print(df.head())

print("\n=== ROW COUNT ===")
print(len(df))

print("\n=== APPROVAL RATE ===")
print(df["approved"].mean())

print("\n=== RACE DISTRIBUTION ===")
print(df["applicant_race_1"].value_counts(normalize=True))

print("\n=== FEATURE STATS ===")
print(df.describe())
