import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Define Ontario civic holidays
ontario_civic_holidays = [
    # 2019
    '2019-01-01',  # New Year's Day
    '2019-02-18',  # Family Day
    '2019-04-19',  # Good Friday
    '2019-05-20',  # Victoria Day
    '2019-07-01',  # Canada Day
    '2019-08-05',  # Civic Holiday
    '2019-09-02',  # Labour Day
    '2019-10-14',  # Thanksgiving Day
    '2019-12-25',  # Christmas Day
    '2019-12-26',  # Boxing Day

    # 2020
    '2020-01-01',  # New Year's Day
    '2020-02-17',  # Family Day
    '2020-04-10',  # Good Friday
    '2020-05-18',  # Victoria Day
    '2020-07-01',  # Canada Day
    '2020-08-03',  # Civic Holiday
    '2020-09-07',  # Labour Day
    '2020-10-12',  # Thanksgiving Day
    '2020-12-25',  # Christmas Day
    '2020-12-26',  # Boxing Day

    # 2021
    '2021-01-01',  # New Year's Day
    '2021-02-15',  # Family Day
    '2021-04-02',  # Good Friday
    '2021-05-24',  # Victoria Day
    '2021-07-01',  # Canada Day
    '2021-08-02',  # Civic Holiday
    '2021-09-06',  # Labour Day
    '2021-10-11',  # Thanksgiving Day
    '2021-12-25',  # Christmas Day
    '2021-12-26',  # Boxing Day

    # 2022
    '2022-01-01',  # New Year's Day
    '2022-02-21',  # Family Day
    '2022-04-15',  # Good Friday
    '2022-05-23',  # Victoria Day
    '2022-07-01',  # Canada Day
    '2022-08-01',  # Civic Holiday
    '2022-09-05',  # Labour Day
    '2022-10-10',  # Thanksgiving Day
    '2022-12-25',  # Christmas Day
    '2022-12-26',  # Boxing Day

    # 2023
    '2023-01-01',  # New Year's Day
    '2023-02-20',  # Family Day
    '2023-04-07',  # Good Friday
    '2023-05-22',  # Victoria Day
    '2023-07-01',  # Canada Day
    '2023-08-07',  # Civic Holiday
    '2023-09-04',  # Labour Day
    '2023-10-09',  # Thanksgiving Day
    '2023-12-25',  # Christmas Day
    '2023-12-26',  # Boxing Day

    # 2024
    '2024-01-01',  # New Year's Day
    '2024-02-19',  # Family Day
    '2024-03-29',  # Good Friday
    '2024-05-20',  # Victoria Day
    '2024-07-01',  # Canada Day
    '2024-08-05',  # Civic Holiday
    '2024-09-02',  # Labour Day
    '2024-10-14',  # Thanksgiving Day
    '2024-12-25',  # Christmas Day
    '2024-12-26',  # Boxing Day
]


def filter_data(data):
    st.sidebar.title("Filters")
    st.sidebar.markdown("Select the Date options and Room:")

    # Select Date Range
    date_range = st.sidebar.date_input("Select Date Range:", [data['ScheduledDate'].min(), data['ScheduledDate'].max()])

    # Select Room
    rooms = sorted(data['Roomdescription'].unique().tolist())
    selected_room = st.sidebar.selectbox("Select Room:", rooms)

    # Filter data
    filtered_data = data[
        (data['ScheduledDate'] >= pd.to_datetime(date_range[0])) & 
        (data['ScheduledDate'] <= pd.to_datetime(date_range[1])) &
        (data['Roomdescription'] == selected_room)
    ]

    return filtered_data, pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1]), selected_room

def app(data):
    st.title("Room Drill Down")

    # Apply filters
    filtered_data, start_date, end_date, selected_room = filter_data(data)

    # Add buttons for removing weekends and civic holidays
    remove_weekends = st.sidebar.checkbox("Remove Weekends")
    remove_civic_holidays = st.sidebar.checkbox("Remove Ontario Civic Holidays")

    if remove_weekends:
        filtered_data['DayOfWeek'] = filtered_data['ScheduledDate'].dt.day_name()
        filtered_data = filtered_data[~filtered_data['DayOfWeek'].isin(['Saturday', 'Sunday'])]

    if remove_civic_holidays:
        filtered_data = filtered_data[~filtered_data['ScheduledDate'].isin(ontario_civic_holidays)]

    # Display the selected room and the date range
    st.write(f"### Room: {selected_room}")
    st.write(f"### Date Range: {start_date.date()} to {end_date.date()}")

    # Distribution of Surgery Types
    surgery_type_dist = filtered_data['ProcedureSpecialtyDescription'].value_counts()

    fig, ax = plt.subplots(figsize=(10, 6))
    surgery_type_dist.plot(kind='bar', ax=ax)
    ax.set_title('Distribution of Surgery Types')
    ax.set_xlabel('Surgery Type')
    ax.set_ylabel('Count')
    plt.xticks(rotation=45)
    ax.grid(True)
    st.pyplot(fig)

    # Distribution of Surgery Durations
    fig, ax = plt.subplots(figsize=(10, 6))
    filtered_data['book_dur'].plot(kind='hist', bins=20, ax=ax)
    ax.set_title('Distribution of Surgery Durations')
    ax.set_xlabel('Duration (minutes)')
    ax.set_ylabel('Frequency')
    ax.grid(True)
    st.pyplot(fig)

    # Calculate and display statistics for surgery durations
    st.write("### Surgery Duration Statistics")
    st.write(filtered_data['book_dur'].describe())

    # Utilization by Day of the Week
    filtered_data['DayOfWeek'] = filtered_data['ScheduledDate'].dt.day_name()
    day_of_week_utilization = filtered_data.groupby('DayOfWeek')['book_dur'].sum()

    fig, ax = plt.subplots(figsize=(10, 6))
    day_of_week_utilization.plot(kind='bar', ax=ax)
    ax.set_title('Utilization by Day of the Week')
    ax.set_xlabel('Day of the Week')
    ax.set_ylabel('Total Duration (minutes)')
    plt.xticks(rotation=45)
    ax.grid(True)
    st.pyplot(fig)

    # Distribution of surgeries by surgeon ID
    surgeon_id_dist = filtered_data['surgeonID'].value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(10, 6))
    surgeon_id_dist.plot(kind='bar', ax=ax)
    ax.set_title('Distribution of Surgeries by Surgeon ID')
    ax.set_xlabel('Surgeon ID')
    ax.set_ylabel('Count')
    plt.xticks(rotation=45)
    ax.grid(True)
    st.pyplot(fig)

    # Utilization by Surgeon ID
    surgeon_id_utilization = filtered_data.groupby('surgeonID')['book_dur'].sum().sort_index()

    fig, ax = plt.subplots(figsize=(10, 6))
    surgeon_id_utilization.plot(kind='bar', ax=ax)
    ax.set_title('Utilization by Surgeon ID')
    ax.set_xlabel('Surgeon ID')
    ax.set_ylabel('Total Duration (minutes)')
    plt.xticks(rotation=45)
    ax.grid(True)
    st.pyplot(fig)