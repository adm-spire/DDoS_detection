import pandas as pd

# File path
csv_file = r"C:\Users\rauna\OneDrive\Desktop\sampled_data\final2\twenty_columned.csv"
#r"C:\Users\rauna\OneDrive\Desktop\sampled_data\final2\part_1.csv"

# Count rows using chunks
row_count = sum(1 for _ in open(csv_file)) - 1  # Subtract 1 for header

print(f"Number of rows in {csv_file}: {row_count}")


