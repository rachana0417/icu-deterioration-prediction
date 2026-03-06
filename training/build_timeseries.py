import pandas as pd

print("Loading vital signals dataset...")

df = pd.read_csv("data/vital_signs.csv")

print("Dataset loaded")

# Keep only important columns
df = df[["subject_id", "charttime", "itemid", "valuenum"]]

# Convert time column
df["charttime"] = pd.to_datetime(df["charttime"])

# Sort by patient and time
df = df.sort_values(by=["subject_id", "charttime"])

print("Creating patient time-series...")

# Group by patient
groups = df.groupby("subject_id")

time_series = []

for patient_id, group in groups:
    values = group["valuenum"].dropna().values
    
    if len(values) >= 10:
        sequence = values[:10]
        time_series.append(sequence)

print("Total sequences created:", len(time_series))

# Convert to dataframe
ts_df = pd.DataFrame(time_series)

ts_df.to_csv("data/timeseries_dataset.csv", index=False)

print("Saved as data/timeseries_dataset.csv")