import pandas as pd
import numpy as np
from scipy.stats import entropy
import matplotlib.pyplot as plt

# Load Source IP and Source Port CSV
df = pd.read_csv(r"C:\Users\rauna\OneDrive\Desktop\sampled_data\final\combined2.csv")

# Ensure column names are correctly formatted
df.columns = df.columns.str.strip()

# Window size for entropy calculation
WINDOW_SIZE = 40000

def calculate_entropy(column_values):
    value_counts = column_values.value_counts(normalize=True)  # Probability of each occurrence
    return entropy(value_counts, base=2)  # Using log base 2 for entropy

# Store entropy values for all windows
entropy_values = []
for start in range(0, len(df), WINDOW_SIZE):
    end = min(start + WINDOW_SIZE, len(df))
    window = df.iloc[start:end]

    entropy_ip = calculate_entropy(window['Source IP'])
    entropy_port = calculate_entropy(window['Source Port'])

    entropy_values.append((entropy_ip, entropy_port))

entropy_values = np.array(entropy_values)
lower_threshold = np.quantile(entropy_values, 0.25)
upper_threshold = np.quantile(entropy_values, 0.75)

# Define ground truth based on entropy behavior
ground_truth = []
for entropy_ip, entropy_port in entropy_values:
    if entropy_ip < lower_threshold and entropy_port < lower_threshold:
        ground_truth.append("Benign")
    elif entropy_ip > upper_threshold or entropy_port > upper_threshold:
        ground_truth.append("Attack")
    else:
        ground_truth.append("Uncertain")

# Now classify windows using entropy-based detection
attack_results = []
for i, (entropy_ip, entropy_port) in enumerate(entropy_values):
    start, end = i * WINDOW_SIZE, min((i + 1) * WINDOW_SIZE, len(df))
    
    if entropy_ip < lower_threshold or entropy_port < lower_threshold:
        attack_results.append((start, end, "DoS Attack Detected"))
    elif entropy_ip > upper_threshold or entropy_port > upper_threshold:
        attack_results.append((start, end, "DDoS Attack Detected"))
    else:
        attack_results.append((start, end, "Normal Traffic"))

# Convert results to DataFrame
attack_df = pd.DataFrame(attack_results, columns=["Start", "End", "Attack Type"])
attack_df["Ground Truth"] = ground_truth  # Add ground truth column for comparison

# Save results to CSV
attack_df.to_csv(r'C:\Users\rauna\Downloads\attack_detection_results.csv', index=False)

print("Attack detection completed and saved to CSV.")

# ===================== Plot Comparison =====================

plt.figure(figsize=(12, 6))

# Plot entropy values
plt.plot(range(len(entropy_values)), entropy_values[:, 0], label="Entropy (Source IP)", marker='o', linestyle='-')
plt.plot(range(len(entropy_values)), entropy_values[:, 1], label="Entropy (Source Port)", marker='s', linestyle='-')

# Plot threshold lines
plt.axhline(y=lower_threshold, color='r', linestyle='--', label="Lower Threshold")
plt.axhline(y=upper_threshold, color='g', linestyle='--', label="Upper Threshold")

# Annotate attack types (Predicted vs Ground Truth)
for i, (_, _, attack_type) in enumerate(attack_results):
    plt.text(i, entropy_values[i, 0], attack_type, fontsize=9, color='black', rotation=45)
    plt.text(i, entropy_values[i, 1], ground_truth[i], fontsize=9, color='blue', rotation=45)

# Labels and legend
plt.xlabel("Window Number")
plt.ylabel("Entropy Value")
plt.title("Entropy-Based Attack Detection vs Ground Truth")
plt.legend()
plt.grid(True)
plt.show()
