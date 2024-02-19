import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

dataURL = "./data/Motor_Vehicle_Collisions_-_Crashes.csv"

github_url = "https://github.com/Hellojustjoe/"
badge_url = "https://img.shields.io/badge/-hellojustjoe-black?style=flat-square&logo=github"

st.set_page_config(layout="wide")


st.markdown(f"""
        <div style="display: flex; justify-content: center; align-items: center;">
            <h1 style="margin-right: 10px;">🗽 NYC Motor Vehicle Collisions 🚗</h1>
            <a href="{github_url}">
                <img src="{badge_url}" alt="GitHub Badge" style="height: 40px;">
            </a>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<h4 style='text-align: center;'>Geospatial dashboard to visualize NYC Motor Vehicle Collisions - Built with Numpy, Pandas and Plotly.</h4>", unsafe_allow_html=True)

@st.cache_data(persist=True)
def load_data(nrows):
    data = pd.read_csv(dataURL, nrows=nrows, parse_dates=[['CRASH_DATE', 'CRASH_TIME']])
    data.dropna(subset=['LATITUDE', 'LONGITUDE'], inplace=True)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data.rename(columns={'crash_date_crash_time': 'date/time'}, inplace=True)
    return data

data = load_data(10000)

injured = data['injured_persons'].sum()
st.markdown(f'<h5 style="text-align: center;">Total number of people injured in NYC: {injured}</h5>', unsafe_allow_html=True)

st.header("Where are the most people injured in NYC?")
injured_people = st.slider("People injured in a collision:", 0, 19)
st.map(data.query("injured_persons >= @injured_people")[["latitude", "longitude"]].dropna(how="any"))


st.header("How many collisions occur during a given time of day?")
hour = st.slider('Hour:', 0, 23)
data = data[data['date/time'].dt.hour == hour]

st.markdown("Collisions between %i:00 and %i:00" % (hour, (hour+1) % 24))


if st.checkbox("Show Raw Data", False):
    st.subheader('Raw data')
    st.write(data)
