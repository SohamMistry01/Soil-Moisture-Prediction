import streamlit as st
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

st.title("Implementation of Stacking Regressor and XGBoost Classifier⚡")

st.divider()
st.info("Stacking Regressor performs well with accuracy of 98.83% - Combining the highly accurate predictions of Random Forest Regressor and XGBoost Regressor.")
st.info("XGBoost Classifier performs well with accuracy of 96.50%")

st.divider()
html_path = os.path.join("pages", "soil_moisture_prediction.html")
with open(html_path, "r", encoding="utf-8") as f: # Provide full path
    html_content = f.read()

st.components.v1.html(html_content, height=800, scrolling=True)