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

def load_data(nrows):
    data = pd.read_csv(dataURL, nrows=nrows, parse_dates=[['CRASH_DATE', 'CRASH_TIME']])
    data.dropna(subset=['LATITUDE', 'LONGITUDE'], inplace=True)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data.rename(columns={'crash_date_crash_time': 'date/time'}, inplace=True)
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done! (using st.cache_data)")
