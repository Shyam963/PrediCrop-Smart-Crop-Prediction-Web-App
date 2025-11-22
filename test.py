import pickle
import pandas as pd
from sklearn.metrics import accuracy_score

# --- A. Load the Model ---
try:
    with open('model.pkl', 'rb') as f:
        loaded_model = pickle.load(f)
    print("Model loaded successfully.")
except FileNotFoundError:
    print("Error: 'model.pkl' not found. Make sure it's in the same folder.")
    exit()

# --- B. Define Test Data (Example: Optimal Rice Conditions) ---
# NOTE: The columns MUST match the training data used to create the model.
# Example data for testing (N, P, K, temp, humidity, ph, rainfall)
test_input = [
    [80, 50, 40, 29.5, 82, 6.8, 150],  # Test case 1: Should predict Rice
    [30, 70, 20, 15.0, 60, 6.0, 40]   # Test case 2: Should predict a cool-weather crop
]

# Create a DataFrame with the column names expected by your model
# (Adjust these column names if your original crop_recommendation.csv used different names)
column_names = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
X_test_data = pd.DataFrame(test_input, columns=column_names)

# --- C. Make Predictions ---
predictions = loaded_model.predict(X_test_data)

# --- D. Print Results ---
print("\n--- TEST RESULTS ---")
for i, prediction in enumerate(predictions):
    input_values = X_test_data.iloc[i].values
    print(f"Input: {input_values}")
    print(f"Predicted Crop: **{prediction}**\n")