import streamlit as st
import pandas as pd
import numpy as np

github_url = "https://github.com/Hellojustjoe/"
badge_url = "https://img.shields.io/badge/-hellojustjoe-black?style=flat-square&logo=github"

st.set_page_config(layout="wide")

st.markdown(f"""
        <div style="display: flex; justify-content: center; align-items: center;">
            <h1 style="margin-right: 10px;">Simple Data Science Dashboard</h1>
            <a href="{github_url}">
                <img src="{badge_url}" alt="GitHub Badge" style="height: 40px;">
            </a>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<h3 style='text-align: center;'>A basic dashboard using Streamlit and Pandas</h3>", unsafe_allow_html=True)
