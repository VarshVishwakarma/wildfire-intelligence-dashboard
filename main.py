import pandas as pd
import glob
import os

# Create data folder
os.makedirs("data", exist_ok=True)

# Load files
files = glob.glob("viirs-jpss1/2024/*.csv")

df_list = []
for f in files:
    temp = pd.read_csv(f)
    temp['country'] = f.split("_")[-1].replace(".csv", "")
    df_list.append(temp)

df = pd.concat(df_list, ignore_index=True)

# Keep needed columns
df = df[['latitude', 'longitude', 'bright_ti4', 'acq_date', 'frp', 'country']]

df['acq_date'] = pd.to_datetime(df['acq_date'])

# Balanced sampling
sample = df.groupby('country').apply(lambda x: x.sample(min(300, len(x))))
sample = sample.reset_index(drop=True)

# Save
sample.to_csv("data/sample.csv", index=False)

print("✅ Sample dataset created at data/sample.csv")