import pandas as pd

# Input and output file paths
input_file = r"C:\Users\rauna\OneDrive\Desktop\sampled_data\final\sampled_30_percent.csv"
output_file = r"C:\Users\rauna\OneDrive\Desktop\sampled_data\final2\twenty_columned_training.csv"

# Columns to extract
columns_to_extract = [
    "Inbound", "URG Flag Count", "Destination IP", "Source IP", "CWE Flag Count",
    "RST Flag Count", "Fwd PSH Flags", "Bwd Packet Length Max", "Bwd Packet Length Mean",
    "Bwd Packet Length Min", "ACK Flag Count", "Destination Port", "Avg Bwd Segment Size",
    "Source Port", "Fwd Packet Length Min", "Init_Win_bytes_backward", "Down/Up Ratio",
    "Init_Win_bytes_forward", "min_seg_size_forward", "Protocol" , "Label"
]

# Read in chunks
chunksize = 10000  # Adjust based on available memory
first_chunk = True  # Flag to write headers only once

for chunk in pd.read_csv(input_file, usecols=columns_to_extract, chunksize=chunksize):
    # Append to output file, write header only for the first chunk
    chunk.to_csv(output_file, mode='a', index=False, header=first_chunk)
    first_chunk = False  # Ensure headers are written only once
