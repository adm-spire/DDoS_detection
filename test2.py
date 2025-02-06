import pandas as pd

# Load the balanced dataset
output_file = r"C:\Users\rauna\OneDrive\Desktop\sampled_data\final\combined2.csv"
df_balanced = pd.read_csv(output_file)

# Count occurrences of each label
print(df_balanced['Label'].value_counts())

