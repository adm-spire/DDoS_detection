import pandas as pd

# Input and output file paths
input_file = r"C:\Users\rauna\OneDrive\Desktop\sampled_data\final2\part_1.csv"
output_file = r"C:\Users\rauna\OneDrive\Desktop\sampled_data\final2\part1_target.csv"

# Columns to extract
columns_to_extract = [
    "Label"
]

# Read in chunks
chunksize = 10000  # Adjust based on available memory
first_chunk = True  # Flag to write headers only once

for chunk in pd.read_csv(input_file, usecols=columns_to_extract, chunksize=chunksize):
    # Append to output file, write header only for the first chunk
    chunk.to_csv(output_file, mode='a', index=False, header=first_chunk)
    first_chunk = False  # Ensure headers are written only once