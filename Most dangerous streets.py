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
import seaborn as sns
import matplotlib.pyplot as plt

st.set_option('deprecation.showPyplotGlobalUse', False)

st.title("Top 0.1% most dangerous streets")


path = "C:/Users/darii/OneDrive - Bentley University/Courses/2023 Fall/CS 230/Final Ivakhnenkova/pages/"

def read_data():
    return pd.read_csv(path + 'bostoncrime2023_7000_sample.csv')

data = read_data()
#found on https://www.w3schools.com/python/pandas/ref_df_nlargest.asp
top_streets = data.groupby('STREET').size().sort_values(ascending=False).nlargest(int(0.001 * len(data)))

# Bar plot using Seaborn found on https://seaborn.pydata.org/examples/histogram_stacked.html
sns.set_theme(style="whitegrid")
plt.figure(figsize=(12, 6))
sns.barplot(x=top_streets.index, y=top_streets.values, palette="Blues_d")
plt.xticks(rotation=45, ha='right', fontsize=10)

plt.xlabel("Streets", fontsize=14)
plt.ylabel("Crime Counts", fontsize=14)
plt.title("Top 0.1% Crime Counts per Street", fontsize=16)

plt.yticks(fontsize=10)
plt.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot()

st.success("Information about the top streets:")
for street, count in top_streets.items():
    st.write(f"Street: {street}, Crime Counts: {count}")
