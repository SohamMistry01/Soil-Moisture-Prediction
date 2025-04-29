import pandas as pd
import streamlit as st
import base64

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

st.title("Smart Plant Monitoring System 🌱")
st.divider()

st.subheader("About our Project:")
st.info("""An IOT based project which helps in tracking the Temperature, Humidity and Soil Moisture
         using Temperture, Humidity and Soil Moisture sensors.
         Arduino tracks the real-time readings and records it in Excel Data Streamer.
         We water the plant every morning and record these parameters on a daily basis.
         We integrate a machine learning model, XGBoost in this project to predict the increase/decrease
         in the level of soil moisture content after few hours.
         XGBoost Regressor helps in predicting the future soil moisture.
         XGBoost Classifier helps in stating whether additional watering would be needed or not.""")

st.divider()

st.subheader("Quick Links:")
st.page_link("pages/PREDICT_SOIL_MOISTURE.py", label="🔎Determine Soil Moisture")
st.page_link("pages/RUN_NOTEBOOK.py", label="🔎View the ML Model Training Process")
st.divider()

st.subheader("Explore a variety of visualizations:")
st.page_link("pages/Basic_Visualizations.py", label="📊Basic Visualizations")
st.page_link("pages/Category_Based_Analysis.py", label="📊Category Based Visualizations")
st.page_link("pages/Comparisons_and_Correlations.py", label="📊Comparison & Correlation Charts")
st.divider()

st.subheader("Dataset: ")
values_count = st.slider("Select the number of entries you want to display: ",0,1000)
df = pd.read_csv("updated_sample_soil_moisture_data.csv")
values_displayed = df.head(values_count)
st.write(values_displayed)

