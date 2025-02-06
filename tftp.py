

import pandas as pd

# Process the file in chunks of 100,000 rows at a time
chunksize = 100_000  
sample_fraction = 0.15  # Take 15% sample from each chunk

dfs = []  # List to store sampled data

for chunk in pd.read_csv(r'C:\Users\rauna\Downloads\CSV-01-12 (1)\01-12\TFTP.csv', 
                         dtype={85: str}, chunksize=chunksize):
    
    chunk.columns = chunk.columns.str.strip()  # Remove spaces from column names
    chunk = chunk.dropna()  # Remove NaN values
    chunk = chunk.loc[:, chunk.nunique() > 1]  # Remove zero-variance columns
    
    # Ensure required columns exist
    required_columns = {'Source IP', 'Source Port', 'Label'}
    if required_columns.issubset(set(chunk.columns)):
        sampled_chunk = chunk[['Source IP', 'Source Port', 'Label']].sample(frac=sample_fraction, random_state=42)
        dfs.append(sampled_chunk)  # Store sampled data
    else:
        print("Missing columns:", required_columns - set(chunk.columns))

# Combine all sampled chunks
if dfs:  # Ensure there's data before concatenating
    df_sampled = pd.concat(dfs, ignore_index=True)
    df_sampled.to_csv(r'C:\Users\rauna\Downloads\Dr_TFTP_sampled_2.csv', index=False)
    print(f"Sampled {df_sampled.shape[0]} rows and saved successfully.")
else:
    print("No valid data found for sampling.")
