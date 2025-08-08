import streamlit as st
import requests

API_KEY = "0f5ee829057c4b736b714b402f2baf37"

# Get weather data
def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        rainfall = data.get('rain', {}).get('1h', 0)  # Safe fallback
        return temp, humidity, rainfall
    else:
        return None, None, None

# Enhanced prediction logic
def predict_crop(N, P, K, temp, humidity, ph, rainfall):
    if not (0 <= ph <= 14):
        return "Invalid pH value"
    if not (0 <= N <= 140 and 5 <= P <= 145 and 5 <= K <= 205):
        return "NPK values out of range"

    explanation = f"🌡️ Temperature: {temp}°C | 💧 Humidity: {humidity}% | 🌧️ Rainfall: {rainfall}mm"

    # Basic conditions for specific crops (example logic)
    if 6.0 <= ph <= 7.5:
        if temp > 25 and rainfall > 100:
            crop = "Rice"
        elif 20 <= temp <= 28 and 40 <= humidity <= 70:
            crop = "Wheat"
        elif temp > 27 and rainfall < 50:
            crop = "Cotton"
        elif 20 <= temp <= 30 and humidity >= 50:
            crop = "Sugarcane"
        else:
            crop = "Maize"
    else:
        crop = "Millets or pulses (less pH-sensitive)"

    return f"✅ Recommended Crop: **{crop}**\n\n📊 Based on weather:\n{explanation}"

# Streamlit UI
st.title("🌾 PrediCrop: Smart Crop Prediction")

city = st.text_input("Enter your city to fetch weather")

weather_data_ready = False

if st.button("Fetch Weather"):
    if city:
        temp, humidity, rainfall = get_weather(city)
        if temp is not None:
            st.success(f"Weather Fetched: Temp: {temp}°C, Humidity: {humidity}%, Rainfall: {rainfall}mm")
            weather_data_ready = True
        else:
            st.error("Could not fetch weather data. Check city name.")
    else:
        st.warning("Please enter a city.")

st.write("### Enter Soil Parameters")

N = st.slider("Nitrogen (N)", 0, 140, 50)
P = st.slider("Phosphorus (P)", 5, 145, 50)
K = st.slider("Potassium (K)", 5, 205, 50)
ph = st.slider("pH Level", 0.0, 14.0, 6.5)

if st.button("Predict"):
    if city:
        temp, humidity, rainfall = get_weather(city)
        if temp is None:
            st.error("Weather data not found. Please check the city name.")
        else:
            result = predict_crop(N, P, K, temp, humidity, ph, rainfall)
            st.markdown(result)
    else:
        st.warning("Please enter a city and click 'Fetch Weather' before predicting.")
