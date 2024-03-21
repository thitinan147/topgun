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






height_latest_value = df['height'].iloc[-1]
# print(latest_value)

height_previous_value = df['height'].iloc[-2]

height_delta = height_latest_value - height_previous_value

# waterfront_latest_value = df['waterfront'].iloc[-1]
# waterfront_previous_value = df['waterfront'].iloc[-2]
# waterfront_delta = waterfront_latest_value - waterfront_previous_value

# waterdrain_latest_value = df['waterdrain'].iloc[-1]
# waterdrain_previous_value = df['waterdrain'].iloc[-2]
# waterdrain_delta = waterdrain_latest_value - waterdrain_previous_value

# col1, col2, col3 = st.columns(3)
st.metric("ระดับความสูงน้ำล่าสุด", f"{height_delta:.2f}", f"{height_delta:.2f}")
# col2.metric("น้ำหลังเขื่อนล่าสุด", waterback_latest_value, f"{waterback_delta:.2f}")
# col3.metric("อัตราการปล่อยน้ำล่าสุด", waterdrain_latest_value, f"{waterdrain_delta:.2f}")

# st.write(df)
# st.dataframe(df.style.highlight_max(axis=0))

# ระดับน้ำล่าสุด
latest_water_level = df['height'].iloc[-1]

# ระดับน้ำท่วม (ตัวอย่างเช่น 100 เป็นตัวเลขที่คำนวณจากข้อมูลหรือมีค่าจากทางท้องถิ่น)
flood_level = 112

# คำนวณอัตราเปอร์เซ็นต์น้ำท่วม
flooding_percentage = (latest_water_level / flood_level) * 100

# แสดงผล
st.write(f"อัตราเปอร์เซ็นต์น้ำท่วม: {flooding_percentage:.2f}%")

chart_data = px.line(df.groupby(by = ["day"])[["discharge","day"]].mean(), x="day",y="discharge", title="discharge of water")
st.plotly_chart(chart_data)


chart_data = px.line(df.groupby(by = ["day"])[["height","day"]].mean(), x="day",y="height", title="height of water")
st.plotly_chart(chart_data)

chart_data = px.line(df.groupby(by = ["day"])[["discharge","height","day"]].mean(), x="day",y=["discharge","height"], title="เปรียบเทียบระดับน้ำกับอัตราการปล่อยน้ำ")
st.plotly_chart(chart_data)

chart_data = px.line(df.groupby(by = ["day"])[["discharge","height","day"]].mean(), x="day",y=["discharge","height"], title="เปรียบเทียบระดับน้ำกับอัตราการปล่อยน้ำ")
st.plotly_chart(chart_data)



grouped_data = df.groupby(by="day")[["discharge", "height"]].mean()
# สร้างกราฟแท่ง
average_values = df.groupby(by = ["day"])[["discharge", "height","day"]].mean()
melted_data = pd.melt(average_values, id_vars='day', value_vars=["discharge", "height"],
                      var_name='WaterSource', value_name='AverageValue')
chart_data = px.bar(melted_data,
    x='day',
    y='AverageValue',
    color='WaterSource',
    barmode='group',  # Use 'group' to place bars side by side
    title='Comparison of discharge and height',
    labels={"AverageValue": "Average Water Level"},)
st.plotly_chart(chart_data)






# Plot discharge and height with different markers or colors to represent the likelihood of flooding
fig = px.scatter(df, x='discharge', y='height',
                 title='Discharge vs height Wมater ',
                 labels={'discharge': 'Discharge', 'height': 'Height'},
                 size_max=20,color_discrete_sequence=['green'])

# Display the plot
st.plotly_chart(fig)