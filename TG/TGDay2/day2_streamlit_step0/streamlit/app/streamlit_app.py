import pymongo
import pandas as pd
import streamlit as st
import plotly.express as px
from pymongo import MongoClient




# Initialize connection.
# Uses st.cache_resource to only run once.

MONGO_DETAILS = "mongodb://tesarally:contestor@mongoDB:27017"
@st.cache_resource
def init_connection():
   return pymongo.MongoClient(MONGO_DETAILS)

client = init_connection()

# Pull data from the collection.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def get_data():
   db = client.mockupdata
   items = db.waterdata.find()
#    print(items)
   items = list(items)  # make hashable for st.cache_data
   return items

items = get_data()

st.balloons()
# # Print results.
# for item in items:
#    st.write(f"{item['Name']} {item['Date']}")

st.markdown(
    """
    <style>
    .header {
        font-size: 2em;
        font-weight: bold;
        color: #00CCFF;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Header
st.markdown('<p class="header">Water Data Visualization Dashboard</p>', unsafe_allow_html=True)

df = pd.DataFrame(items)



WaterDataBack_latest_value = df['WaterDataBack'].iloc[-1]
# print(latest_value)
WaterDataBack_previous_value = df['WaterDataBack'].iloc[-2]
WaterDataBack_delta = WaterDataBack_latest_value - WaterDataBack_previous_value

WaterDataFront_latest_value = df['WaterDataFront'].iloc[-1]
WaterDataFront_previous_value = df['WaterDataFront'].iloc[-2]
WaterDataFront_delta = WaterDataFront_latest_value - WaterDataFront_previous_value

WaterDrainRate_latest_value = df['WaterDrainRate'].iloc[-1]
WaterDrainRate_previous_value = df['WaterDrainRate'].iloc[-2]
WaterDrainRate_delta = WaterDrainRate_latest_value - WaterDrainRate_previous_value



col1, col2, col3 = st.columns(3)
col1.metric("น้ำหน้าเขื่อนล่าสุด", WaterDataFront_latest_value, f"{WaterDataFront_delta:.2f}")
col2.metric("น้ำหลังเขื่อนล่าสุด", WaterDataBack_latest_value, f"{WaterDataBack_delta:.2f}")
col3.metric("อัตราการปล่อยน้ำล่าสุด", WaterDrainRate_latest_value, f"{WaterDrainRate_delta:.2f}")


# st.write(df)
st.dataframe(df.style.highlight_max(axis=0))

# # Metric 1: Average WaterDataFront
# average_water_front = df['WaterDataFront'].mean()
# st.metric("Average WaterDataFront", value=f"{average_water_front:.2f}")

# # Metric 2: Average WaterDataBack
# average_water_back = df['WaterDataBack'].mean()
# st.metric("Average WaterDataBack", value=f"{average_water_back:.2f}")

# # Metric 3: Average WaterDrainRate
# average_drain_rate = df['WaterDrainRate'].mean()
# st.metric("Average WaterDrainRate", value=f"{average_drain_rate:.2f}")

# Year selector
selected_year = st.selectbox("เลือกปี", df['Year'].unique())

# Filter DataFrame based on the selected year
filtered_df = df[df['Year'] == selected_year]

col1, col2, col3 = st.columns(3)
# Metric 1: Average WaterDataFront
average_water_front = filtered_df['WaterDataFront'].mean()
col1.metric("น้ำหน้าเขื่อนเฉลี่ย", value=f"{average_water_front:.2f}")

# Metric 2: Average WaterDataBack
average_water_back = filtered_df['WaterDataBack'].mean()
col2.metric("น้ำหลังเขื่อนเฉลี่ย", value=f"{average_water_back:.2f}")

# Metric 3: Average WaterDrainRate
average_drain_rate = filtered_df['WaterDrainRate'].mean()
col3.metric("อัตราการปล่อยน้ำเฉลี่ย", value=f"{average_drain_rate:.2f}")









# Custom CSS for a stylish header


# df = pd.DataFrame(items)

# # # Create a bar chart using Plotly Express
# fig = px.bar(
#     df,
#     x='Date',
#     y='WaterDataFront',
#     title='WaterDataFront over Time',
#     labels={'WaterDataFront': 'Water Level'},
#     facet_col='Year',  # Facet by Year
#     template='plotly_dark',  # Choose a dark template
#     height=400,
#     width=800,
# )

# # Customize the plot
# fig.update_layout(
#     title_text='WaterDataFront over Time',
#     xaxis_title='Date',
#     yaxis_title='Water Level',
#     showlegend=True,
# )

# # Display the plot
# st.plotly_chart(fig)

fig2 = px.bar(
    df,
    x='Date',
    y=['WaterDataFront', 'WaterDataBack'],
    title='เปรียบเทียบปริมาณน้ำหน้าเขื่อนและน้ำหลังเขื่อน',
    labels={'value': 'ปริมาณน้ำ', 'variable': 'Type'},
    template='plotly_dark',
    facet_col='Year',  # Facet by Year
)

# Display the plot
st.plotly_chart(fig2)

fig = px.line(df, x='Year', y='WaterDrainRate', title='อัตราการปล่อยน้ำเฉลี่ยในแต่ละปี')

# Display the plot
st.plotly_chart(fig)



