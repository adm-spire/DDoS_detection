import pandas as pd
import joblib
import matplotlib.pyplot as plt
from collections import Counter

# Load the trained model
model_path = "sequential_decision_tree_model.joblib"
dt_model = joblib.load(model_path)

# Path to the new data file
new_data_file = r"C:\Users\rauna\OneDrive\Desktop\sampled_data\final\twenty_columned.csv"

# Load new data
new_df = pd.read_csv(new_data_file, low_memory=False)

# Ensure "Label" column is not present in inference data
if "Label" in new_df.columns:
    new_df = new_df.drop(columns=["Label"])

# Convert numeric columns properly
for col in new_df.columns:
    new_df[col] = pd.to_numeric(new_df[col], errors="coerce")  # Convert non-numeric to NaN

# Fill missing values with median
new_df.fillna(new_df.median(), inplace=True)

# Drop columns with more than 50% missing values
new_df.dropna(axis=1, thresh=int(0.5 * len(new_df)), inplace=True)

# Identify categorical columns
cat_cols = new_df.select_dtypes(include=["object"]).columns

# Convert categorical columns using label encoding
for col in cat_cols:
    new_df[col] = new_df[col].astype("category").cat.codes  # Convert to integer codes

# Make predictions
predictions = dt_model.predict(new_df)

# Save predictions to a CSV file
output_file = r"C:\Users\rauna\OneDrive\Desktop\sampled_data\final2\predictions.csv"
pd.DataFrame(predictions, columns=["Predicted_Label"]).to_csv(output_file, index=False)

print(f"Predictions saved to {output_file}")

# Define window size
window_size = 40000
num_windows = (len(predictions) // window_size) + 1

# Compute majority label per window
majority_labels = []
for i in range(num_windows):
    start_idx = i * window_size
    end_idx = min((i + 1) * window_size, len(predictions))
    window_preds = predictions[start_idx:end_idx]
    
    if len(window_preds) == 0:
        continue  # Skip empty windows
    
    majority_label = Counter(window_preds).most_common(1)[0][0]  # Get most frequent label
    majority_labels.append(majority_label)
    print(f"Window {i + 1}: Majority Label = {majority_label}")

# Plot majority labels per window
plt.figure(figsize=(10, 5))
plt.plot(range(1, len(majority_labels) + 1), majority_labels, marker='o', linestyle='-', color='b')
plt.xlabel("Window Number")
plt.ylabel("Majority Predicted Label")
plt.title("Majority Predicted Label Per Window")
plt.xticks(range(1, len(majority_labels) + 1))
plt.grid()
plt.show()



