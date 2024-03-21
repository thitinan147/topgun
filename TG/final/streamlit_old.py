import pymongo
import pandas as pd
import streamlit as st
import plotly.express as px
from pymongo import MongoClient

# st.set_page_config(layout="wide")

# Initialize connection.
# Uses st.cache_resource to only run once.
MONGO_DETAILS = "mongodb://TGR_GROUP51:RL533I@mongoDB:27017"
@st.cache_resource
def init_connection():
   return pymongo.MongoClient(MONGO_DETAILS)

client = init_connection()

# Pull data from the collection.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def get_data():
   db = client.water_data
   items = db.waters_collection.find()
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

#table
df = pd.DataFrame(items)


waterback_latest_value = df['waterback'].iloc[-1]
# print(latest_value)
waterback_previous_value = df['waterback'].iloc[-2]
waterback_delta = waterback_latest_value - waterback_previous_value

waterfront_latest_value = df['waterfront'].iloc[-1]
waterfront_previous_value = df['waterfront'].iloc[-2]
waterfront_delta = waterfront_latest_value - waterfront_previous_value

waterdrain_latest_value = df['waterdrain'].iloc[-1]
waterdrain_previous_value = df['waterdrain'].iloc[-2]
waterdrain_delta = waterdrain_latest_value - waterdrain_previous_value

col1, col2, col3 = st.columns(3)
col1.metric("น้ำหน้าเขื่อนล่าสุด", waterfront_latest_value, f"{waterfront_delta:.2f}")
col2.metric("น้ำหลังเขื่อนล่าสุด", waterback_latest_value, f"{waterback_delta:.2f}")
col3.metric("อัตราการปล่อยน้ำล่าสุด", waterdrain_latest_value, f"{waterdrain_delta:.2f}")

# st.write(df)
# st.dataframe(df.style.highlight_max(axis=0))
st.dataframe(df)

# year selector
selected_year = st.selectbox("เลือกปี", df['year'].unique())

# Filter DataFrame based on the selected year
filtered_df = df[df['year'] == selected_year]

col1, col2, col3 = st.columns(3)
# Metric 1: Average waterfront
average_water_front = filtered_df['waterfront'].mean()
col1.metric("น้ำหน้าเขื่อนเฉลี่ย", value=f"{average_water_front:.2f}")

# Metric 2: Average waterback
average_water_back = filtered_df['waterback'].mean()
col2.metric("น้ำหลังเขื่อนเฉลี่ย", value=f"{average_water_back:.2f}")

# Metric 3: Average waterdrain
average_drain_rate = filtered_df['waterdrain'].mean()
col3.metric("อัตราการปล่อยน้ำเฉลี่ย", value=f"{average_drain_rate:.2f}")


fig2 = px.bar(
    df,
    x='date',
    y=['waterfront', 'waterback'],
    title='เปรียบเทียบปริมาณน้ำหน้าเขื่อนและน้ำหลังเขื่อน',
    labels={'value': 'ปริมาณน้ำ', 'variable': 'Type'},
    template='plotly_dark',
    facet_col='year',  # Facet by year
)

# Display the plot
st.plotly_chart(fig2)

fig = px.line(df, x='year', y='waterback', title='อัตราการปล่อยน้ำเฉลี่ยในแต่ละปี')

# Display the plot
st.plotly_chart(fig)



