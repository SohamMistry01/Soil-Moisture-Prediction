import streamlit as st
import pandas as pd
import plotly.express as px
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

# Load Data
def load_data():
    file_path = "updated_sample_soil_moisture_data.csv"
    df = pd.read_csv(file_path)
    return df

df = load_data()

# Streamlit App
st.title("Basic Data Visualizations")
st.divider()

# Histogram
st.subheader("Histogram of Temperature, Humidity, and Soil Moisture")
fig1 = px.histogram(df, x=['Temperature (°C)', 'Humidity (%)', 'Soil Moisture Morning (%)'], 
                    title='Distribution of Temperature, Humidity & Soil Moisture', 
                    barmode='overlay', opacity=0.6)
st.plotly_chart(fig1)
st.divider()

# Box Plot
st.subheader("Box Plot of Temperature, Humidity, and Soil Moisture")
fig2 = px.box(df, y=['Temperature (°C)', 'Humidity (%)', 'Soil Moisture Morning (%)'], 
              title='Box Plot of Temperature, Humidity & Soil Moisture')
st.plotly_chart(fig2)
st.divider()

# Scatter Plot: Moisture levels before and after watering over time
st.subheader("Scatter Plot of Soil Moisture Before and After Watering")
fig3 = px.scatter(df, x='Soil Moisture Morning (%)', y='Soil Moisture After X hours (%)',
                  title='Relationship Between Soil Moisture Before and After Watering',
                  trendline="ols")
st.plotly_chart(fig3)
st.divider()

# Pie Chart for Watering Needed Later?
st.subheader("Pie Chart for Watering Needed Later")
fig4 = px.pie(df, names='Watering Needed Later? (Y/N)', 
              title='Proportion of Times Watering was Needed Later',
              hole=0.3)
st.plotly_chart(fig4)

