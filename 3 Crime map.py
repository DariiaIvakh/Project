"""
Name:       Dariia Ivakhnenkova
CS230:      Section 6
Data:       Boston Crime 2023

Description:
This Program analyzes crime data in Boston for the year 2023, providing interactive visualizations and insights.
It includes features such as filtering crime trends based on selected months, exploring top crime locations, visualizing crime distribution on a map,
and displaying detailed information about specific incidents. The application has various charts, plots, and interactive components to enhance user
engagement and understanding of the dataset.
"""
import streamlit as st
import pydeck as pdk
import pandas as pd

st.set_option('deprecation.showPyplotGlobalUse', False)

# Title
st.title("Boston Crime Map Analysis")

st.write("""This interactive map allows users to explore reported crimes across different districts in Boston

Select Districts: Use the dropdown to choose one or more districts for analysis

Crime Map: The map displays reported crimes with icons differentiating between the ones with shootings and without

Search by Incident Number: Explore specific incidents by selecting an incident number from the dropdown

Incident Details: Further explore incident details by choosing information types

""")

st.success("""Map Legend:

Red flags: Shootings

Other Icons: No Shootings
""")

path = "C:/Users/darii/OneDrive - Bentley University/Courses/2023 Fall/CS 230/Final Ivakhnenkova/pages/"

def read_data():
    return pd.read_csv(path + 'bostoncrime2023_7000_sample.csv')

data_wthout_distr = read_data()
data_wthout_distr.dropna(subset=['DISTRICT'], inplace=True)
data_wthout_distr.rename(columns={"Lat": "lat", "Long": "lon"}, inplace=True)

unique_distr = sorted(data_wthout_distr['DISTRICT'].unique())

selected_distr = st.multiselect("Please select a district", unique_distr)


data = data_wthout_distr[data_wthout_distr['DISTRICT'].isin(selected_distr)]

ICON_SHOOTING_URL = "https://upload.wikimedia.org/wikipedia/commons/1/1c/Flag_icon_red_4.svg"
ICON_NON_SHOOTING_URL = "https://upload.wikimedia.org/wikipedia/commons/c/cf/Icon_Shield_72x72%5Es_BLACK%2C_TotK.svg"

data["icon_data"] = None

data["icon_data"] = [
    {"url": ICON_SHOOTING_URL, "width": 25, "height": 25, "anchorY": 1}
    if shooting == 1 else
    {"url": ICON_NON_SHOOTING_URL, "width": 25, "height": 25, "anchorY": 1}
    for shooting in data["SHOOTING"]]

view_state = pdk.ViewState(
    latitude=data["lat"].mean(),
    longitude=data["lon"].mean(),
    zoom=15,
    pitch=0
)

tool_tip = {
    "html": "Crime:<br/> <b>{OFFENSE_DESCRIPTION}</b>",
    "style": {"backgroundColor": "green", "color": "white"}
}

icon_layer = pdk.Layer(type="IconLayer",
                       data=data,
                       get_icon="icon_data",
                       get_position='[lon,lat]',
                       get_size=4,
                       size_scale=10,
                       pickable=True)

icon_map = pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v11',
    initial_view_state=view_state,
    layers=[icon_layer],
    tooltip=tool_tip
)

st.pydeck_chart(icon_map)

st.header("Search Incident by Number")

numbers = sorted(data["INCIDENT_NUMBER"])
select_num = st.selectbox("Select Incident Number", numbers, None)

if select_num:
    select_inc = data[data["INCIDENT_NUMBER"] == select_num]

    selected_view_state = pdk.ViewState(
        latitude=select_inc["lat"].mean(),
        longitude=select_inc["lon"].mean(),
        zoom=15,
        pitch=0
    )

    select_icon = pdk.Layer(
        type="IconLayer",
        data=select_inc,
        get_icon="icon_data",
        get_position='[lon,lat]',
        get_size=4,
        size_scale=10,
        pickable=True
    )

    select_icon = pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v11',
        initial_view_state=selected_view_state,
        layers=[select_icon],
        tooltip=tool_tip
    )

    st.pydeck_chart(select_icon)
    st.header("Select Information Type")

    info_type = st.radio("Select Information Type", ["OFFENSE_CODE", "OFFENSE_DESCRIPTION", "DISTRICT", "SHOOTING",
                                                     "OCCURRED_ON_DATE", "YEAR", "MONTH", "DAY_OF_WEEK", "HOUR",
                                                     "STREET"])

    if info_type:
        st.write(f"Showing information for {info_type}:")
        st.write(select_inc[info_type].iloc[0])