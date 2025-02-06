import pandas as pd
df = pd.read_csv(r'C:\Users\rauna\Downloads\CSV-01-12 (1)\01-12\DrDoS_DNS.csv', dtype={85: str})
print(df.shape[0])
#dropped tables 
df = df.dropna()
print(df.shape[0])

# Remove columns with zero variance
df = df.loc[:, df.nunique() > 1]  # Keeps only columns with more than 1 unique value

print(df.shape[0])




#Select SourceIP and SourcePort for entropy-based filtering
entropy_features = df[['SourceIP', 'SourcePort']]

'''
from sklearn.ensemble import ExtraTreesClassifier
import numpy as np

# Assuming 'Label' column contains attack/benign labels
X = df.drop(columns=['Label'])  # Drop target variable
y = df['Label']

# Train an Extra Trees Classifier
model = ExtraTreesClassifier()
model.fit(X, y)

# Select top 20 features based on importance scores
feature_importance = model.feature_importances_
important_features = np.argsort(feature_importance)[-20:]  # Get indices of top 20 features
selected_features = X.columns[important_features]

# Keep only the selected features
df = df[selected_features]
'''

'''
# Filter attack samples
dns_attacks = df[df['Label'] == 'DNS']
snmp_attacks = df[df['Label'] == 'SNMP']
tftp_attacks = df[df['Label'] == 'TFTP']

# Randomly sample from large classes
dns_sample = dns_attacks.sample(frac=0.25, random_state=42)  # 25% of DNS samples
snmp_sample = snmp_attacks.sample(frac=0.25, random_state=42)  # 25% of SNMP samples
tftp_sample = tftp_attacks.sample(frac=0.05, random_state=42)  # 5% of TFTP samples

# Combine with remaining data
df = pd.concat([df[~df['Label'].isin(['DNS', 'SNMP', 'TFTP'])], dns_sample, snmp_sample, tftp_sample])

'''