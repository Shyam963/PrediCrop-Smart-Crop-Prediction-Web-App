# 🌾 PrediCrop: Smart Crop Prediction Web App
A smart crop recommendation system powered by Machine Learning and real-time weather data 🌦️. 

Given soil parameters and city, it predicts the most suitable crop to grow.


## 🔍 Features
📈 Trains a machine learning model (Random Forest)

## 📊 Takes user input for:

### Nitrogen (N)

### Phosphorus (P)

### Potassium (K)

### pH Level

### ☁️ Fetches live weather data (temperature, humidity, rainfall) from OpenWeatherMap API

### 🌱 Predicts the most suitable crop for farming

### 🚀 Live Demo
You can run the app locally using Streamlit (see instructions below).

### 🧠 Model Accuracy
The trained Random Forest model achieves ~99% accuracy on the test data.

### 📁 Dataset
Used dataset: Crop Recommendation Dataset (Kaggle)

## 🛠️ Installation
### 1. Clone the Repository
git clone https://github.com/your-username/predicrop.git

cd predicrop

### 2. Install Dependencies
pip install -r requirements.txt

If requirements.txt is missing, install manually:

pip install pandas scikit-learn streamlit requests

### 3. Add API Key
Replace the value of API_KEY in the app.py (or wherever your Streamlit code is) with your OpenWeatherMap API key:

API_KEY = "your_api_key_here"

Get a free API key from https://openweathermap.org/

### 4.🖥️ Run the Streamlit App
streamlit run app.py

This will launch the web app at localhost:8501

### 📸 Screenshots
UI	Prediction

### 📂 Project Structure

predicrop/

├── Crop_recommendation.csv   # Dataset

├── app.py                    # Streamlit app

├── README.md                 # This file

├── requirements.txt          # Dependencies

└── screenshots/              # UI screenshots

### 🙌 Acknowledgements
OpenWeatherMap

Kaggle - Crop Dataset

Built using Streamlit

### OUTPUT
<img width="1920" height="1080" alt="Screenshot (94)" src="https://github.com/user-attachments/assets/e8140fd3-da24-4b01-960f-3ddc8ab7cbb2" />
<img width="1262" height="206" alt="Screenshot 2025-08-08 213652" src="https://github.com/user-attachments/assets/10933a5a-9f62-4611-acdb-91b76cdf5bb5" />

