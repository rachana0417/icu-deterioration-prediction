import pandas as pd

file_path = "data/mimic-iv-clinical-database-demo-2.2/icu/chartevents.csv"

print("Loading dataset...")
df = pd.read_csv(file_path)

print("Filtering vital signs...")

# Vital sign item IDs
vital_ids = [220045, 220277, 220210, 223761]

vitals = df[df["itemid"].isin(vital_ids)]

print("Vital signals extracted")

print(vitals.head())

print("Total vital measurements:", len(vitals))

# Save cleaned dataset
vitals.to_csv("data/vital_signs.csv", index=False)

print("Saved as data/vital_signs.csv")