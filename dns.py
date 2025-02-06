import pandas as pd

# Load dataset with dtype specification for column 85
df = pd.read_csv(r'C:\Users\rauna\Downloads\CSV-01-12 (1)\01-12\DrDoS_DNS.csv', dtype={85: str})
print(f"Original DataFrame size: {df.shape[0]}")

# Drop rows with missing values
df = df.dropna()
print(f"After dropping NaN: {df.shape[0]}")

# Remove columns with zero variance
df = df.loc[:, df.nunique() > 1]  # Keeps only columns with more than 1 unique value
print(f"After removing zero-variance columns: {df.shape[0]}")




# Select SourceIP and SourcePort for entropy-based filtering
entropy_features = df[[' Source IP', ' Source Port' , ' Label']]

# Select 25% random samples
df_sampled = entropy_features.sample(frac=0.5, random_state=42)
print(f"Sampled DataFrame size: {df_sampled.shape[0]}")

# Save to CSV
df_sampled.to_csv(r'C:\Users\rauna\Downloads\DrDoS_DNS_sampled_new.csv', index=False)

print("Sampled data saved successfully.")


