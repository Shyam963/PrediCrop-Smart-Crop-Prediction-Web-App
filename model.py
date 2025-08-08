import streamlit as st
import requests
import pickle

# Load the trained model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# OpenWeatherMap API key
API_KEY = "0f5ee829057c4b736b714b402f2baf37"

# Function to get weather
def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        rainfall = data.get('rain', {}).get('1h', 0)  # fallback if no rain data
        return temp, humidity, rainfall
    else:
        return None, None, None

# UI
st.title("🌾 PrediCrop: Smart Crop Prediction using ML")

city = st.text_input("Enter your city to fetch weather data")

if st.button("Fetch Weather"):
    if city:
        temp, humidity, rainfall = get_weather(city)
        if temp is not None:
            st.success(f"✅ Weather: {temp}°C | Humidity: {humidity}% | Rainfall: {rainfall}mm")
            st.session_state.weather_fetched = True
            st.session_state.temp = temp
            st.session_state.humidity = humidity
            st.session_state.rainfall = rainfall
        else:
            st.error("❌ Could not fetch weather data. Check the city name.")
    else:
        st.warning("⚠️ Please enter a city name.")

st.write("### 🧪 Enter Soil Parameters")

N = st.slider("Nitrogen (N)", 0, 140, 50)
P = st.slider("Phosphorus (P)", 5, 145, 50)
K = st.slider("Potassium (K)", 5, 205, 50)
ph = st.slider("pH Level", 0.0, 14.0, 6.5)

if st.button("Predict Crop"):
    if city and st.session_state.get('weather_fetched', False):
        input_data = [[
            N,
            P,
            K,
            st.session_state.temp,
            st.session_state.humidity,
            ph,
            st.session_state.rainfall
        ]]

        prediction = model.predict(input_data)[0]
        st.success(f"🌱 Recommended Crop: **{prediction}**")
    else:
        st.warning("⚠️ Please fetch weather data first.")
