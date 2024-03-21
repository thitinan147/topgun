import pymongo
import math
import pandas as pd
import streamlit as st
import plotly.express as px
from pymongo import MongoClient
import numpy as np
import time

# Initialize connection.
# Uses st.cache_resource to only run once.
st.set_page_config(
    layout="wide",
    page_title="Water Data Visualization Dashboard",
    page_icon="🏞️",    
    )




MONGO_DETAILS = "mongodb://TGR_GROUP51:RL533I@mongoDB:27017"
@st.cache_resource
def init_connection():
   return pymongo.MongoClient(MONGO_DETAILS)

client = init_connection()

# Pull data from the collection.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=10)
def get_data():
   db = client.water_data
   items = db.waters_collection_ml.find()
   print(items)
   items = list(items)  # make hashable for st.cache_data
   return items

items = get_data()

df = pd.DataFrame(items)
placeholder = st.empty()


# st.balloons() 

#height_latest_value
height_latest_value = df['height'].iloc[-1]
height_previous_value = df['height'].iloc[-2]
height_delta = height_latest_value - height_previous_value

#discharge_latest_value
discharge_latest_value = df['discharge'].iloc[-1]
discharge_previous_value = df['discharge'].iloc[-2]
discharge_delta = discharge_latest_value - discharge_previous_value



# st.sidebar.title("Navigation")
# st.sidebar.markdown("[Water Data Visualization Dashboard](#main1-page)")
# st.sidebar.markdown("[main3-page](#main2-page)")

#📈
#🗃
with placeholder.container():
      with st.sidebar:
         st.markdown(
            """
            <a style="text-decoration: none;" href="https://gear.kku.ac.th/" target="_blank">
            <div style="background-color: #1A73E8; padding: 10px; border-radius: 5px; text-align: center;">
                <span style="color: white; font-size: 18px;">About Us</span>
            </div>
         </a>
        """,
        unsafe_allow_html=True
       )
    #   st.markdown("<h1 style='color: skyblue;'>Water Data Visualization Dashboard</h1>", unsafe_allow_html=True)
      st.markdown("<h1 style='color: #1A73E8;text-align: left;'>ข้อมูลน้ำ🧊</h1>", unsafe_allow_html=True)
    #   job_filter = st.selectbox("Select the Job", pd.unique(df["day"]))
      kpi1, kpi2 = st.columns(2)
      kpi1.metric("ความสูงระดับน้ำล่าสุด (เมตร)", f"{height_latest_value:.1f}", delta=f"{height_delta:.1f}")
      kpi2.metric("อัตราการไหลของน้ำล่าสุด (ลูกบาศก์เมตรต่อวินาที)", f"{discharge_latest_value:.1f}", delta=f"{discharge_delta:.1f}")
      
      #day selector
      day = st.selectbox("เลือกวันที่", pd.unique(df["day"]))
      
      #filter Dataframe based on day
      filtered_df = df[df['day'] == day]
      # flood_warning_day_value = 'เสี่ยงน้ำท่วม' if filtered_df['height'].max() >= 112 else 'ปกติ'
      water_level_max = filtered_df['height'].max()
      flood_warning_day_value = 'น้ำท่วม' if water_level_max >= 112 else 'เสี่ยงน้ำท่วม' if 109 <= water_level_max <112 else 'ปกติ'

      col1_day, col2_day, col3_day= st.columns(3)
      #metric for height
      height_values = filtered_df['height']
      height_values_rounded = height_values.round(2)
      col1_day.metric(f"ความสูงระดับน้ำวันที่ {day} (เมตร)", value=height_values_rounded)
      #metric for discharge
      discharge_values = filtered_df['discharge']
      discharge_values_rounded = discharge_values.round(2)
      col2_day.metric(f"อัตราการไหลของน้ำวันที่ {day} (ลูกบาศก์เมตรต่อวินาที)", value=discharge_values_rounded )
      # col3_day.metric(f"สถานะของระดับน้ำวันที่ {day}", flood_warning_day_value)
      
      if flood_warning_day_value == "น้ำท่วม":
        color = 'red'
      elif flood_warning_day_value == 'เสี่ยงน้ำท่วม':
        color = 'blue'
      else:
        color = 'green'
      col3_day.markdown("<font style='color: black;text-align: center;'>สถานะของน้ำ</font>", unsafe_allow_html=True)
      col3_day.markdown(f"<font color='{color}'>{flood_warning_day_value}</font>", unsafe_allow_html=True)

      
      fig_col1, fig_col2 = st.columns(2)
      with fig_col1:
         chart_data = px.line(df.groupby(by = ["day"])[["height","day"]].mean(), x='day', y=["height"], title='📈ระดับความสูงของน้ำในแต่ละวัน (เมตร)',labels={"value": "Water Level"}, height=500, width=600)
         st.plotly_chart(chart_data)
         
      with fig_col2:
         average_values = df.groupby(by = ["day"])[["discharge","day"]].mean()
         melted_data = pd.melt(average_values, id_vars='day', value_vars=["discharge"],
                      var_name='WaterSource', value_name='AverageValue')
         chart_data = px.bar(melted_data,
            x='day', 
            y='AverageValue',
            color='WaterSource',
            barmode='group',  # Use 'group' to place bars side by side
            title='📈อัตราการไหลของน้ำในแต่วัน (ลูกบาศก์เมตรต่อวินาที)',
            labels={"AverageValue": "Water Discharge"},height=500, width=600)
         st.plotly_chart(chart_data)
      
    #   st.dataframe(df, height=10 * 30)
      st.markdown("<h3 style='color: black;text-align: left;'>รายละเอียดข้อมูลน้ำทั้งหมด📂</h3>", unsafe_allow_html=True)
      st.dataframe(df.style.set_properties(**{'background-color': 'lightyellow','border-color': 'darkblue','text-align': 'center', 'color': 'black'}), height=10 * 40, width=10 * 160)
      
      st.balloons() 
      
      time.sleep(10)
      st.experimental_rerun()