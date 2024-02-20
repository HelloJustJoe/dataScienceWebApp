import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import pydeck as pdk

dataURL = "./data/Motor_Vehicle_Collisions_-_Crashes.csv"

github_url = "https://github.com/Hellojustjoe/"
badge_url = "https://img.shields.io/badge/-hellojustjoe-black?style=flat-square&logo=github"

st.set_page_config(layout="wide")


st.markdown(f"""
        <div style="display: flex; justify-content: center; align-items: center;">
            <h1 style="margin-right: 10px;">🗽 NYC Motor Vehicle Collisions 🚗</h1>
            <a href="{github_url}">
                <img src="{badge_url}" alt="GitHub Badge" style="height: 40px; border-radius: 10px;">
            </a>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<h4 style='text-align: center;'>Geospatial dashboard visualizing NYC Motor Vehicle Collisions - Built with Numpy, Pandas and Plotly.</h4>", unsafe_allow_html=True)



@st.cache_data(persist=True)
def load_data(nrows):
    data = pd.read_csv(dataURL, nrows=nrows, parse_dates=[['CRASH_DATE', 'CRASH_TIME']])
    data.dropna(subset=['LATITUDE', 'LONGITUDE'], inplace=True)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data.rename(columns={'crash_date_crash_time': 'date/time'}, inplace=True)
    return data

data = load_data(100000)

injured = int(data['injured_persons'].sum())
st.markdown(f'<h5 style="text-align: center;">Total number of people injured in NYC: {injured}</h5>', unsafe_allow_html=True)

st.markdown('<hr style="border:1px solid #FFD700;"/>', unsafe_allow_html=True)


st.header("Where are the most people injured in NYC?")
injured_people = st.slider("People injured in a collision:", 0, 19)
filtered_data = data.query("injured_persons >= @injured_people")[["latitude", "longitude"]].dropna(how="any")

initial_view_state = pdk.ViewState(
    latitude=data['latitude'].median(),
    longitude=data['longitude'].median(),
    zoom=10,
    pitch=0,
)

layer = pdk.Layer(
    "ScatterplotLayer",
    filtered_data,
    get_position='[longitude, latitude]',
    get_color='[200, 30, 0, 160]',
    get_radius=100,
)

st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/dark-v9',
    initial_view_state=initial_view_state,
    layers=[layer],
))

st.header("How many collisions occur during a given time of day?")
hour = st.slider('Hour:', 0, 23)
data = data[data['date/time'].dt.hour == hour]

col1, col2, = st.columns(2)
with col1:
    st.subheader("By the Hour: %i:00 - %i:00" % (hour, (hour+1) % 24))

    st.write(pdk.Deck(
        map_style="mapbox://styles/mapbox/dark-v9",
        initial_view_state=pdk.ViewState(
            latitude=data['latitude'].median(),
            longitude=data['longitude'].median(),
            zoom=10,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                'HexagonLayer',
                data=data[['date/time', 'latitude', 'longitude']],
                get_position=['longitude', 'latitude'],
                radius=150,
                elevation_scale=5,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            )
        ]
    ))

with col2:
    st.subheader("Minute by Minute: %i:00 - %i:00" % (hour, (hour+1) % 24))
    filtered = data[
        (data['date/time'].dt.hour >= hour) & (data['date/time'].dt.hour < (hour + 1))
    ]

    hist = np.histogram(filtered['date/time'].dt.minute, bins=60, range=(0, 60))[0]
    chart_data = pd.DataFrame({'minute': range(60), 'crashes': hist})
    fig = px.bar(chart_data, x='minute', y='crashes', hover_data=['minute', 'crashes'], height=400)
    st.plotly_chart(fig, use_container_width=True)


st.header("Top 5 dangerous streets by affected type")
selected_types = st.multiselect(
    'Affected Type',
    ['Pedestrians', 'Cyclists', 'Motorists'],
    ['Pedestrians', 'Cyclists', 'Motorists']
)

if len(selected_types) > 0:
    query_conditions = " | ".join([f"injured_{affected_type.lower()} >= 1" for affected_type in selected_types])
    filtered_data = data.query(query_conditions)

    top_dangerous = filtered_data.nlargest(5, 'injured_persons')[["on_street_name",
                                                                  "injured_pedestrians",
                                                                  "injured_cyclists",
                                                                  "injured_motorists"]]

    st.write(top_dangerous)
else:
    st.write("Please select at least one affected type to display the top 5 dangerous streets.")


if st.checkbox("Show Raw Data", False):
    st.subheader('Raw data')
    st.write(data)
