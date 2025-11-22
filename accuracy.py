import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# --- A. Load Data and Split (MUST match training script) ---
df = pd.read_csv("crop_recommendation.csv")
X = df.drop('label', axis=1)
y = df['label']

# Split the data into 80% training and 20% testing sets
# We use the same 'test_size=0.2' as the original training script
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# --- B. Load the Model ---
try:
    with open('model.pkl', 'rb') as f:
        loaded_model = pickle.load(f)
except FileNotFoundError:
    print("Error: 'model.pkl' not found. Cannot calculate accuracy.")
    exit()

# --- C. Test the Model on Unseen Data ---
# Use the test features (X_test) to get predictions
y_pred = loaded_model.predict(X_test)

# --- D. Calculate Accuracy ---
# Compare the model's predictions (y_pred) with the actual correct labels (y_test)
accuracy = accuracy_score(y_test, y_pred)

# --- E. Print Results ---
print("\n--- MODEL SUCCESS RATE (ACCURACY) ---")
print(f"Total Test Samples: {len(X_test)}")
print(f"Accuracy Score: {accuracy * 100:.2f}%")
print("\nThis score means the model correctly predicted the crop label")
print(f"**{accuracy * 100:.2f}%** of the time on the data it was trained to generalize to.")