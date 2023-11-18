
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

@st.cache_data
def load_data():
    day_data = pd.read_csv('day.csv')
    hour_data = pd.read_csv('hour.csv')
    return day_data, hour_data

day_df, hour_df = load_data()

st.title('Bike Sharing Demand Dashboard')
st.caption('Made By: Rava Radithya Razan')

tab1, tab2, tab3 = st.tabs(['Seasonality', 'Weather', 'Peak Hours'])

seasonal_agg = day_df.groupby('season')['cnt'].sum().reset_index()

weather_agg = day_df.groupby('weathersit')['cnt'].sum().reset_index()

hour_df['is_weekend'] = hour_df['weekday'].apply(lambda x: 1 if x in [0, 6] else 0)
peak_hours_weekday = hour_df[hour_df['is_weekend'] == 0].groupby('hr')['cnt'].mean().reset_index()
peak_hours_weekend = hour_df[hour_df['is_weekend'] == 1].groupby('hr')['cnt'].mean().reset_index()

with tab1:
    st.subheader('Total Bike Rentals per Season')
    fig, ax = plt.subplots()
    color = [
        "#83c5be",
        "#83c5be",
        "#006d77",
        "#83c5be",
    ]

    sns.barplot(x='season', y='cnt', data=seasonal_agg, ax=ax, palette=color, hue='season', legend=False)
    ax.set_title('Total Bike Rentals per Season')
    ax.set_xlabel('Season')
    ax.set_ylabel('Total Rentals')
    ax.set_xticklabels(['Spring', 'Summer', 'Fall', 'Winter'])
    st.pyplot(fig)

with tab2:
    st.subheader('Total Bike Rentals per Weather Situation')
    fig, ax = plt.subplots()
    color = [
        "#006d77",
        "#83c5be",
        "#83c5be",
    ]

    sns.barplot(x='weathersit', y='cnt', data=weather_agg, ax=ax, palette=color, hue='weathersit')
    ax.set_title('Total Bike Rentals per Weather Situation')
    ax.set_xlabel('Weather Situation')
    ax.set_ylabel('Total Rentals')
    ax.set_xticklabels(['Clear', 'Mist + Cloudy', 'Light Snow/Rain', 'Heavy Rain/Ice Pellets'])
    st.pyplot(fig)
with tab3:
    st.subheader('Average Bike Rentals per Hour')

    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(peak_hours_weekday['hr'], peak_hours_weekday['cnt'], label='Weekday', color='#219ebc')
    ax.plot(peak_hours_weekend['hr'], peak_hours_weekend['cnt'], label='Weekend', color='#fb8500')
    ax.set_title('Average Bike Rentals per Hour')
    ax.set_xlabel('Hour of the Day')
    ax.set_ylabel('Average Rentals')
    ax.legend()
    ax.set_xticks(range(0, 24))
    ax.grid(True)
    st.pyplot(fig)
