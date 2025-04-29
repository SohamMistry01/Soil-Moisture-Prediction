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
st.title("Visualizations on Category-Based Analysis")
st.divider()

# Violin/Box Plot: Distribution of soil moisture before and after watering, grouped by Time of Day
st.subheader("Box Plot: Soil Moisture by Time of Day")
fig1 = px.box(df, x='Time of Day', y=['Soil Moisture Morning (%)', 'Soil Moisture After X hours (%)'],
              title='Soil Moisture Levels Before and After Watering by Time of Day')
st.plotly_chart(fig1)
st.divider()

# Grouped Bar Chart: Average moisture levels at different times of the day
st.subheader("Grouped Bar Chart: Average Soil Moisture by Time of Day")
avg_moisture = df.groupby('Time of Day')[['Soil Moisture Morning (%)', 'Soil Moisture After X hours (%)']].mean().reset_index()
fig2 = px.bar(avg_moisture, x='Time of Day', y=['Soil Moisture Morning (%)', 'Soil Moisture After X hours (%)'], 
              barmode='group', title='Average Soil Moisture Before and After Watering by Time of Day')
st.plotly_chart(fig2)
st.divider()

# Stacked Bar Chart: Count of Watering Done vs Watering Needed Later
st.subheader("Stacked Bar Chart: Watering Done vs Watering Needed Later")
watering_counts = df.groupby(['Time of Day', 'Watering Done? (Y/N)']).size().reset_index(name='Count')
fig3 = px.bar(watering_counts, x='Time of Day', y='Count', color='Watering Done? (Y/N)',
              title='Watering Done vs Watering Needed Later by Time of Day', barmode='stack')
st.plotly_chart(fig3)

