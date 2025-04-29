import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
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

# Exclude non-numeric columns for correlation analysis
columns_to_exclude = ['Date', 'Time', 'Watering Done? (Y/N)', 'Watering Needed Later? (Y/N)', 'Time of Day']
numeric_df = df.drop(columns=columns_to_exclude, errors='ignore')

# Streamlit App
st.title("Visualizations on Comparisons & Correlations")
st.divider()

# Scatter Plot: Relationship between Temperature and Soil Moisture
st.subheader("Scatter Plot: Temperature vs Soil Moisture")
fig1 = px.scatter(df, x='Temperature (°C)', y='Soil Moisture Morning (%)',
                  title='Relationship Between Temperature and Soil Moisture',
                  trendline="ols")
st.plotly_chart(fig1)
st.divider()

# Heatmap: Correlation Matrix using Plotly
st.subheader("Heatmap: Correlation Between Features")
corr_matrix = numeric_df.corr().round(2)
fig2 = ff.create_annotated_heatmap(
    z=corr_matrix.values,
    x=list(corr_matrix.columns),
    y=list(corr_matrix.index),
    colorscale='Viridis',
    showscale=True
)
st.plotly_chart(fig2)
st.divider()

# Pair Plot: Pairwise relationships between numerical variables
st.subheader("Pair Plot: Relationships Between Variables")
st.write("Displaying pairwise scatter plots between numerical features.")
fig3 = px.scatter_matrix(df, dimensions=['Temperature (°C)', 'Humidity (%)',
                                         'Soil Moisture Morning (%)', 'Soil Moisture After X hours (%)'],
                         title='Pairwise Relationships Between Variables')
st.plotly_chart(fig3)


