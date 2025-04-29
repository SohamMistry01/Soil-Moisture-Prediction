import streamlit as st
import joblib
import pandas as pd
import numpy as np
import plotly.express as px
import base64
import os

# Background Image CSS
def set_bg(image_file):
    with open(image_file, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")

    bg_image_style = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{data}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """
    st.markdown(bg_image_style, unsafe_allow_html=True)

# Set Background
set_bg("leaf.jpg")

input_features = [
    "Temperature (°C)", "Humidity (%)", "Soil Moisture Morning (%)", 
    "Watering Done? (Y/N)", "Time of Day"
]

# Streamlit App for Soil Moisture Prediction
# Load trained models
def predict_soil_moisture(temp, humidity, soil_moisture_morning, watering_done, time_of_day, hours):
    model1_path = os.path.join("pages", "reg.pkl")
    model1 = joblib.load(model1_path)
    
    input_data = pd.DataFrame([[temp, humidity, soil_moisture_morning, watering_done, time_of_day]],
                              columns=input_features)
    base_prediction = model1.predict(input_data)[0]
    
    # Adjust prediction based on environmental factors and hours
    moisture_decay = (0.02 * hours * temp) - (0.015 * hours * humidity)
    adjusted_prediction = max(0, min(100, base_prediction - moisture_decay))
    
    return adjusted_prediction

def predict_watering_needed(temp, humidity, soil_moisture_morning, watering_done, time_of_day):
    model2_path = os.path.join("pages", "cls.pkl")
    model2 = joblib.load(model2_path)
    
    input_data = pd.DataFrame([[temp, humidity, soil_moisture_morning, watering_done, time_of_day]],
                              columns=input_features)
    return "Yes" if model2.predict(input_data)[0] == 1 else "No"

st.title("Soil Moisture Prediction")
st.divider()

# User inputs
temp = st.number_input("Temperature (°C)", 20.0, 40.0, step=0.1)
humidity = st.number_input("Humidity (%)", 10.0, 100.0, step=0.1)
soil_moisture_morning = st.number_input("Soil Moisture Morning (%)", 0.0, 100.0, step=0.1)
watering_done = st.selectbox("Watering Done?", ["No", "Yes"])
time_of_day = st.selectbox("Time of Day", ["Early Morning", "Morning", "Late Morning"])
hours = st.slider("Predict Soil Moisture After (hours)", 1, 12, 1)

# Convert categorical inputs
watering_done_encoded = 1 if watering_done == "Yes" else 0
time_of_day_encoded = ["Early Morning", "Morning", "Late Morning"].index(time_of_day)

# Predict button
if st.button("Predict Soil Moisture & Watering Need"):
    moisture_prediction = predict_soil_moisture(temp, humidity, soil_moisture_morning, watering_done_encoded, time_of_day_encoded, hours)
    watering_prediction = predict_watering_needed(temp, humidity, soil_moisture_morning, watering_done_encoded, time_of_day_encoded)
    st.success(f"Predicted Soil Moisture After {hours} hours: {moisture_prediction:.2f}%")
    st.success(f"Is Additional Watering Needed? {watering_prediction}")
    if moisture_prediction<5:
        st.warning("Soil moisture is CRITICALLY LOW! Immediate watering required.")
    
    # Generate moisture predictions over time
    time_range = np.arange(1, hours + 1)
    moisture_levels = [predict_soil_moisture(temp, humidity, soil_moisture_morning, watering_done_encoded, time_of_day_encoded, h) for h in time_range]
    
    # Plot 1: Moisture Level Over Time
    fig1 = px.line(x=time_range, y=moisture_levels, labels={"x": "Hours Ahead", "y": "Predicted Soil Moisture (%)"}, title="Predicted Soil Moisture Over Time")
    st.plotly_chart(fig1)
    
    # Plot 2: Watering Impact Comparison
    moisture_no_watering = predict_soil_moisture(temp, humidity, soil_moisture_morning, 0, time_of_day_encoded, hours)
    moisture_with_watering = predict_soil_moisture(temp, humidity, soil_moisture_morning, 1, time_of_day_encoded, hours)
    df_watering = pd.DataFrame({"Condition": ["Without Watering", "With Watering"], "Soil Moisture (%)": [moisture_no_watering, moisture_with_watering]})
    fig2 = px.bar(df_watering, x="Condition", y="Soil Moisture (%)", title="Effect of Watering on Soil Moisture")
    st.plotly_chart(fig2)
    
    # Plot 3: Temperature vs. Moisture Loss
    temp_range = np.linspace(20, 40, 10)
    moisture_loss = [(0.02 * hours * t) - (0.015 * hours * humidity) for t in temp_range]
    fig3 = px.scatter(x=temp_range, y=moisture_loss, labels={"x": "Temperature (°C)", "y": "Moisture Loss (%)"}, title="Impact of Temperature on Moisture Loss")
    st.plotly_chart(fig3)

