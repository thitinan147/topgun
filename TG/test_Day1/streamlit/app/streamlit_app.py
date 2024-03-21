# from collections import namedtuple
# import altair as alt
# import math
# import pandas as pd
import streamlit as st



import streamlit as st

st.title("TEST")
st.header("header")
st.text("Welcome to TGR2023")
st.metric(label="Temperature", value="70 °F", delta="1.2 °F")
import streamlit as st

# Using object notation
add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone")
)

# Using "with" notation
with st.sidebar:
    add_radio = st.radio(
        "Choose a shipping method",
        ("Standard (5-15 days)", "Express (2-5 days)")
    )

import streamlit as st
import streamlit as st

# Using object notation
add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone")
)

# Using "with" notation
with st.sidebar:
    add_radio = st.radio(
        "Choose a shipping method",
        ("Standard (5-15 days)", "Express (2-5 days)")
    )

st.title("TEST")
st.header("header")
col1, col2, col3 = st.columns(3)

# with col1:
#     st.metric(label="Temperature", value="70 °F", delt
# dvz-wuez-wvu)


