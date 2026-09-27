import pandas as pd

URL = "https://raw.githubusercontent.com/martj42/international_results/master/results.csv"

print("Downloading football dataset...")

df = pd.read_csv(URL)

print("\nDataset downloaded successfully!")
print("Rows:", len(df))
print("Columns:", list(df.columns))

print("\nFirst 5 matches:")
print(df.head())

df.to_csv("../data/international_results.csv", index=False)

print("\nDataset saved to:")
print("../data/international_results.csv")