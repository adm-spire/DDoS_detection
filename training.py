import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# List of feature CSV files
feature_files = [
    r"C:\Users\rauna\OneDrive\Desktop\sampled_data\final2\part_1.csv",
    r"C:\Users\rauna\OneDrive\Desktop\sampled_data\final2\part_2.csv",
    r"C:\Users\rauna\OneDrive\Desktop\sampled_data\final2\part_3.csv",
    r"C:\Users\rauna\OneDrive\Desktop\sampled_data\final2\normal_traffic.csv"
]

# Initialize the Decision Tree model
dt_model = DecisionTreeClassifier(
    criterion="gini",
    splitter="best",
    max_depth=None,
    min_samples_split=2,
    min_samples_leaf=1
)

# Train model sequentially on each dataset
for i, feature_file in enumerate(feature_files, start=1):
    print(f"Training on {feature_file}...")

    # Load dataset with forced data types and disable memory warnings
    df = pd.read_csv(feature_file, low_memory=False)

    # Ensure "Label" column exists
    if "Label" not in df.columns:
        raise ValueError(f"Column 'Label' not found in {feature_file}")

    # Extract features and target
    X = df.drop(columns=["Label"])  # Features
    y = df["Label"]  # Target

    # Convert numeric columns properly
    for col in X.columns:
        X[col] = pd.to_numeric(X[col], errors="coerce")  # Convert non-numeric to NaN

    # Fill missing values with median
    X.fillna(X.median(), inplace=True)

    # Drop columns with more than 50% missing values
    X.dropna(axis=1, thresh=int(0.5 * len(X)), inplace=True)

    # Identify categorical columns
    cat_cols = X.select_dtypes(include=["object"]).columns

    # Convert categorical columns using label encoding (avoiding too many features)
    for col in cat_cols:
        X[col] = X[col].astype("category").cat.codes  # Convert to integer codes

    # Split into train-test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Check if this is the first dataset or not
    if i == 1:
        # Train model from scratch on the first dataset
        dt_model.fit(X_train, y_train)
    else:
        # Incrementally train model by fitting on new data
        dt_model.fit(X_train, y_train)

    # Save the continuously updated model
    joblib.dump(dt_model, "sequential_decision_tree_model.joblib")
    print(f"Model updated and saved as sequential_decision_tree_model.joblib")

    # Predict on test set
    y_pred = dt_model.predict(X_test)

    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy after training on {feature_file}: {accuracy:.4f}\n")

print("Training complete!")

