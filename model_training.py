import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Load dataset
df = pd.read_csv("assets/data/loan_data.csv")

# Drop non-feature columns if they exist
if "loan_id" in df.columns:
    df = df.drop(columns=["loan_id"])

# Ensure column names are all lowercase for consistency
df.columns = [col.lower() for col in df.columns]

# Encode categorical features
label_encoders = {}
categorical_columns = ["gender", "married", "dependents", "education", "self_employed", "property_area"]

for column in categorical_columns:
    if column in df.columns:
        le = LabelEncoder()
        df[column] = le.fit_transform(df[column])
        label_encoders[column] = le

# Define features and target
X = df.drop(columns=["loan_status"])
y = df["loan_status"]

# Print feature columns for debugging
print("Feature columns:", X.columns.tolist())

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model and encoders
with open("assets/data/trained_model.pkl", "wb") as model_file:
    pickle.dump(model, model_file)

with open("assets/data/label_encoders.pkl", "wb") as encoder_file:
    pickle.dump(label_encoders, encoder_file)

print("✅ Model training completed & saved successfully!")