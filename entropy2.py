import pandas as pd
import numpy as np
from scipy.stats import entropy
import matplotlib.pyplot as plt

# Load Source IP and Source Port CSV
df = pd.read_csv(r"C:\Users\rauna\OneDrive\Desktop\sampled_data\final2\twenty_columned_training.csv")

# Ensure column names are correctly formatted
df.columns = df.columns.str.strip()

# Window size for entropy calculation
WINDOW_SIZE = 40000

def calculate_entropy(column_values):
    value_counts = column_values.value_counts(normalize=True)  # Probability of each occurrence
    return entropy(value_counts, base=2)  # Using log base 2 for entropy

entropy_values = []  # Store entropy for all windows
windows = []  # Store DataFrames of normal traffic windows

for start in range(0, len(df), WINDOW_SIZE):
    end = min(start + WINDOW_SIZE, len(df))
    window = df.iloc[start:end]

    entropy_ip = calculate_entropy(window['Source IP'])
    entropy_port = calculate_entropy(window['Source Port'])

    entropy_values.append((entropy_ip, entropy_port))

entropy_values = np.array(entropy_values)
lower_threshold = np.quantile(entropy_values, 0.25)
upper_threshold = np.quantile(entropy_values, 0.75)

# Now reprocess the dataset using fixed thresholds
attack_results = []
for i, (entropy_ip, entropy_port) in enumerate(entropy_values):
    start, end = i * WINDOW_SIZE, min((i + 1) * WINDOW_SIZE, len(df))
    
    if entropy_ip < lower_threshold or entropy_port < lower_threshold:
        attack_results.append((start, end, "DoS Attack Detected"))
    elif entropy_ip > upper_threshold or entropy_port > upper_threshold:
        attack_results.append((start, end, "DDoS Attack Detected"))
    else:
        attack_results.append((start, end, "Normal Traffic"))
        # Append the normal traffic window to the list
        windows.append(df.iloc[start:end])

# Convert results to DataFrame
attack_df = pd.DataFrame(attack_results, columns=["Start", "End", "Attack Type"])

# Save attack classification results
attack_df.to_csv(r'C:\Users\rauna\Downloads\attack_detection_results.csv', index=False)

# Concatenate all normal traffic windows
if windows:
    normal_traffic_df = pd.concat(windows, ignore_index=True)
    normal_traffic_df.to_csv(r'C:\Users\rauna\Downloads\normal_traffic.csv', index=False)
    print("Normal traffic data saved to CSV.")

print("Attack detection completed and saved to CSV.")

# Plot entropy values for IP and Port
plt.figure(figsize=(12, 6))
plt.plot(range(len(entropy_values)), entropy_values[:, 0], label="Entropy (Source IP)", marker='o', linestyle='-')
plt.plot(range(len(entropy_values)), entropy_values[:, 1], label="Entropy (Source Port)", marker='s', linestyle='-')

# Plot threshold lines
plt.axhline(y=lower_threshold, color='r', linestyle='--', label="Lower Threshold")
plt.axhline(y=upper_threshold, color='g', linestyle='--', label="Upper Threshold")

# Annotate attack types
for i, (_, _, attack_type) in enumerate(attack_results):
    if attack_type != "Normal Traffic":
        plt.text(i, entropy_values[i, 0], attack_type, fontsize=9, color='black', rotation=45)

# Labels and legend
plt.xlabel("Window Number")
plt.ylabel("Entropy Value")
plt.title("Entropy Analysis for Attack Detection")
plt.legend()
plt.grid(True)
plt.show()
