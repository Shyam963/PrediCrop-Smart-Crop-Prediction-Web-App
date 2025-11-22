import streamlit as st
import requests
import pickle
import pandas as pd
from sklearn.exceptions import NotFittedError

# --- Configuration (REPLACE with your key) ---
# NOTE: This API Key is exposed in a public code block. Use a secure method 
# like Streamlit Secrets for a real-world app.
API_KEY = "0f5ee829057c4b736b714b402f2baf37" 

# --- 1. Model Loading ---
@st.cache_resource # Caches the model so it loads only once
def load_ml_model():
    """Loads the trained Random Forest model."""
    try:
        with open('model.pkl', 'rb') as f:
            model = pickle.load(f)
        return model
    except FileNotFoundError:
        st.error("ERROR: model.pkl not found. Please run 'train_model.py' first.")
        return None
    except NotFittedError:
        st.error("ERROR: Model found but not fitted. Retrain the model.")
        return None

# --- 2. Data Fetching ---
def get_weather(city):
    """Fetches temperature, humidity, and rainfall from OpenWeatherMap."""
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        # Rainfall in the last hour, defaulting to 0 if not present
        rainfall = data.get('rain', {}).get('1h', 0) 
        
        return temp, humidity, rainfall
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            st.error(f"City not found: {city}. Please check the spelling.")
        else:
            st.error(f"Weather API Error: {e}")
        return None, None, None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None, None, None

# --- 3. Prediction Logic (Using ML Model) ---
def predict_crop(model, N, P, K, ph, temp, humidity, rainfall):
    """Uses the loaded ML model to predict the crop."""
    
    # Create a DataFrame row for prediction
    # NOTE: Columns MUST match the training data order!
    input_data = pd.DataFrame([[N, P, K, temp, humidity, ph, rainfall]], 
                              columns=['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall'])
    
    # Make the prediction
    prediction = model.predict(input_data)[0]
    
    return prediction

# --- Streamlit UI (Simulating ESP32 Input) ---
st.set_page_config(page_title="PrediCrop Dashboard", layout="wide")
st.title("🌾 PrediCrop: Smart Crop Prediction Dashboard")

model = load_ml_model()

if model is None:
    st.stop() # Stop if the model could not be loaded

# --- Input Section ---
col1, col2 = st.columns(2)

with col1:
    st.header("🌦️ Live Weather Input")
    city = st.text_input("Enter City Name:", "New Delhi")
    
    # Fetch weather on button click
    if st.button("Fetch & Predict", type="primary"):
        temp, humidity, rainfall = get_weather(city)
        if temp is not None:
            st.session_state['weather_data'] = (temp, humidity, rainfall)
            st.success(f"Weather Fetched for {city}!")
        
with col2:
    st.header("🧪 Soil Parameters (Simulated ESP32 Input)")
    st.info("Since the ESP32 is not connected, use the sliders to simulate data.")
    
    # Simulation: Replace these sliders with data fetched from the ESP32 in a real app
    sim_N = st.slider("Nitrogen (N) - ppm", 0, 140, 90)
    sim_P = st.slider("Phosphorus (P) - ppm", 5, 145, 42)
    sim_K = st.slider("Potassium (K) - ppm", 5, 205, 43)
    sim_ph = st.slider("pH Level", 0.0, 14.0, 6.5)

# --- Prediction and Results ---
st.markdown("---")
st.header("✨ Prediction & Current Readings")

if 'weather_data' in st.session_state:
    temp, humidity, rainfall = st.session_state['weather_data']
    
    # Run the Prediction
    predicted_crop = predict_crop(model, sim_N, sim_P, sim_K, sim_ph, temp, humidity, rainfall)

    # --- Display Data ---
    data_cols = st.columns(7)
    
    data_cols[0].metric("Nitrogen (N)", f"{sim_N} ppm")
    data_cols[1].metric("Phosphorus (P)", f"{sim_P} ppm")
    data_cols[2].metric("Potassium (K)", f"{sim_K} ppm")
    data_cols[3].metric("pH Level", f"{sim_ph:.1f}")
    
    data_cols[4].metric("Temperature", f"{temp:.1f} °C")
    data_cols[5].metric("Humidity", f"{humidity}%")
    data_cols[6].metric("Rainfall (1hr)", f"{rainfall} mm")
    
    st.markdown("---")
    
    # --- Final Prediction Display ---
    st.subheader("Final Crop Recommendation")
    st.success(f"The best crop based on current conditions is:")
    st.markdown(f"**<p style='font-size:40px; color: #1e8449;'>{predicted_crop.upper()}</p>**", unsafe_allow_html=True)
else:
    st.info("Enter a city and click 'Fetch & Predict' to see the results.")