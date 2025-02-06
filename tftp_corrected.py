import pandas as pd

# Path to input and output files
input_file = r"C:\Users\rauna\Downloads\CSV-01-12 (1)\01-12\TFTP.csv"
output_file = r"C:\Users\rauna\Downloads\balanced_TFTP_Normalized.csv"

# Define chunk size (adjust based on available RAM)
chunk_size = 100000  # Process 100,000 rows at a time

# Prepare output CSV with headers from the first chunk
first_chunk = True

# Process file in chunks
for chunk in pd.read_csv(input_file, dtype={85: str}, chunksize=chunk_size):
    # Separate benign and attack data
    benign_data = chunk[chunk[' Label'] == 'BENIGN']
    attack_data = chunk[chunk[' Label'] != 'BENIGN']

    # Randomly sample attack data (e.g., 5% of attacks)
    attack_data_sampled = attack_data.sample(frac=0.05, random_state=42)

    # Combine benign and sampled attack data
    balanced_chunk = pd.concat([benign_data, attack_data_sampled])

    # Append to output CSV
    balanced_chunk.to_csv(output_file, mode='a', index=False, header=first_chunk)

    # After first chunk, set `first_chunk = False` to avoid writing headers again
    first_chunk = False

print("Processing complete. Balanced dataset saved.")