import pymongo
import math
import pandas as pd
import streamlit as st
import plotly.express as px

st.title("Water Data")

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
   items = list(items)  # make hashable for st.cache_data
   return items

items = get_data()

# Convert data to DataFrame for easier manipulation.
df = pd.DataFrame(items)
# st.dataframe(df.style.highlight_max(axis=0))

# Print results.
# st.write("## Raw Data")
st.write(df)

# Create metrics and display them.
st.write("## Metrics")

# Metric 1: Average WaterDataFront
average_water_front = df['WaterDataFront'].mean()
st.metric("Average WaterDataFront", value=f"{average_water_front:.2f}")

# Metric 2: Average WaterDataBack
average_water_back = df['WaterDataBack'].mean()
st.metric("Average WaterDataBack", value=f"{average_water_back:.2f}")

# Metric 3: Average WaterDrainRate
average_drain_rate = df['WaterDrainRate'].mean()
st.metric("Average WaterDrainRate", value=f"{average_drain_rate:.2f}")


# # Convert data to DataFrame for easier manipulation.
# df = pd.DataFrame(items)

# # Print results.
# st.write("## Raw Data")
# st.write(df)