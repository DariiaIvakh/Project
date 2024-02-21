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
import matplotlib.pyplot as plt
from PIL import Image

st.set_option('deprecation.showPyplotGlobalUse', False)

path = "C:/Users/darii/OneDrive - Bentley University/Courses/2023 Fall/CS 230/Final Ivakhnenkova/pages/"
st.title("Crime Trends Analysis")

st_image = Image.open("C:/Users/darii/OneDrive - Bentley University/Courses/2023 Fall/CS 230/Final Ivakhnenkova/pages/crimes.jpg")

# Show your image using st.image()

st.image(st_image, width=800)


def read_data():
    return pd.read_csv(path + 'bostoncrime2023_7000_sample.csv')

data = read_data()

#found on https://docs.streamlit.io/library/api-reference/layout/st.tabs
tab1, tab2, tab3 = st.tabs(["Crime specific Trends for Chosen Month", "Details of Selected Crime", "Time of the day"])


crime = st.sidebar.selectbox('Select Crime Type', data['OFFENSE_DESCRIPTION'].unique())

with tab1:
    st.title('Monthly statistics')
    st.text("Select Month Range: Use the sliders to choose the start and end months for the analysis.")
    st.write("You'll see a bar chart illustrating the trends of the chosen crime over the selected months. Hover over each bar to view the exact number of incidents.")
    st.success("If no data is available based on your chosen criteria, an error message will be displayed.")


    filtered = data[(data['MONTH'] >= st.slider('Start month', 1, 12, 1)) & (data['MONTH'] <= st.slider('End Month', 1, 12, 1))]
    filtered = filtered[filtered['OFFENSE_DESCRIPTION'] == crime]


    if not filtered.empty:
        cnt = filtered.groupby('MONTH').size()
        # Customizing the appearance, info found on https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.subplots.html
        figure, ax = plt.subplots()
        cnt.plot(kind='bar', ax=ax, color='pink', edgecolor='black')
        ax.set_title(f"Crime Trends for {crime}")
        ax.set_xlabel("Month")
        ax.set_ylabel("Number of Crimes")
        st.pyplot(figure)

        st.subheader(f"Details of Incidents for {crime}")
        column_no_need = ['OFFENSE_CODE_GROUP', 'UCR_PART']
        filtered_wthout = filtered.drop(columns=column_no_need, errors='ignore')
        selected_distr = st.select_slider("Please select districts", data['DISTRICT'].unique())
        filtered_by_distr = filtered_wthout[filtered_wthout['DISTRICT'].isin([selected_distr])]
        for month, value in cnt.items():
            ax.text(month, value, str(value), ha='center', va='bottom', fontsize=8, color='black')
        st.write(f"Showing information for selected districts:")
        st.table(filtered_by_distr)

    else:
        # found on https://docs.streamlit.io/library/api-reference/status/st.error
        st.error('Error: Please input a valid range of months', icon="🚨")
        st.write("No data to display.")

with tab2:
    st.title('Crime Trends for Chosen Month')
    st.write("The line graph displays the number of crimes for the chosen primary and secondary crime types for each day of the week for chosen month.")

    selected_month = st.slider('Select Month', 1, 12, 1)
    filter_month = data[(data['MONTH'] == selected_month) & (data['OFFENSE_DESCRIPTION'].isin([crime]))]

    crime_two = st.selectbox('Select Second Crime Type', data['OFFENSE_DESCRIPTION'].unique())
    filter_month_two = data[(data['MONTH'] == selected_month) & (data['OFFENSE_DESCRIPTION'].isin([crime_two]))]

    weekdays_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    cnt_by_day = filter_month.groupby('DAY_OF_WEEK').size().reindex(weekdays_order)
    cnt_by_day_two = filter_month_two.groupby('DAY_OF_WEEK').size().reindex(weekdays_order)

    figure_line, ax_line = plt.subplots(figsize=(12, 8))
    cnt_by_day.plot(marker='o',label=crime, color='blue', ax=ax_line)
    cnt_by_day_two.plot(marker='o', label=crime_two, color='red', ax=ax_line)
    ax_line.set_title(f"Crime Trends for {crime} and {crime_two}")
    ax_line.set_xlabel("Day of the Week")
    ax_line.set_ylabel("Number of Crimes")
    ax_line.legend()

    st.pyplot(figure_line)

with tab3:
    st.title('Crime Trends by Time of the Day')
    st.write("The scatter chart shows the number of crimes at different hours of the day.")
    selected_month_three = st.slider('Select', 1, 12, 1)
    selected_month_three = data[(data['MONTH'] == selected_month_three) & (data['OFFENSE_DESCRIPTION'].isin([crime]))]

    #found on https://docs.streamlit.io/library/api-reference/charts/st.scatter_chart
    hour_count = selected_month_three.groupby('HOUR').size().reset_index(name='Number of Crimes')
    st.scatter_chart(hour_count, x='HOUR', y='Number of Crimes', use_container_width=True, size='Number of Crimes')
