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
import pandas as pd
from streamlit_echarts import st_echarts

st.set_option('deprecation.showPyplotGlobalUse', False)

path = "C:/Users/darii/OneDrive - Bentley University/Courses/2023 Fall/CS 230/Final Ivakhnenkova/pages/"

st.title("Top Three Crimes Analysis")
st.text("Select Month: Adjust the slider to choose the month you want to analyze.")
st.write("The table shows the top three crimes based on their occurrence in the selected month.The pie chart represents the distribution of these crimes.")

def read_data():
    return pd.read_csv(path + 'bostoncrime2023_7000_sample.csv')

data = read_data()
selected_month = st.slider('Select Month', 1, 12, 1)
filter = data[data['MONTH'] == selected_month]
crime_cnt = filter.groupby('OFFENSE_DESCRIPTION').size().sort_values(ascending=False)
#found on https://www.w3schools.com/python/pandas/ref_df_nlargest.asp
top_cr = crime_cnt.nlargest(3)
st.table(top_cr.reset_index().rename(columns={"index": "Crime", "OFFENSE_DESCRIPTION": "Count"}))

#taken from https://discuss.streamlit.io/t/a-dashboard-based-on-streamlit-and-echarts/15142

options = {
    # Legend
    "legend": {"top": 'top'},
    "series": [
        {
            "name": 'Crime Distribution',
            "type": 'pie',
            "radius": ["30%", "70%"],  # Inner and outer radius
            "center": ['50%', '50%'],  # Center position
            "roseType": 'area',
            "itemStyle": {
                "borderRadius": "8"  # Border radius for rounded corners
            },

            # Data
            "data": [{"value": value, "name": crime} for crime, value in top_cr.items()]
        }
    ],

    "tooltip": {"show": "true"},

    "label": {"show": "true"}
}

st_echarts(options=options, key="3")

