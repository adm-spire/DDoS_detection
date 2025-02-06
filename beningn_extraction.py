import pandas as pd

# Path to input and output files
input_file = r"C:\Users\rauna\Downloads\CSV-01-12 (1)\01-12\DrDoS_UDP.csv"
output_file = r"C:\Users\rauna\Downloads\benign_UDP_Normalized.csv"

# Define chunk size (adjust based on available RAM)
chunk_size = 100000  # Process 100,000 rows at a time

# Prepare output CSV with headers from the first chunk
first_chunk = True

# Process file in chunks
for chunk in pd.read_csv(input_file, dtype={85: str}, chunksize=chunk_size):
    # Filter only benign data
    benign_data = chunk[chunk[' Label'] == 'BENIGN']

    # Append to output CSV
    benign_data.to_csv(output_file, mode='a', index=False, header=first_chunk)

    # After first chunk, set `first_chunk = False` to avoid writing headers again
    first_chunk = False

print("Processing complete. Benign dataset saved.")
