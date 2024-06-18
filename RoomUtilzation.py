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
    st.sidebar.markdown("Select the Date options and Rooms:")

    # Select Date Range
    date_range = st.sidebar.date_input("Select Date Range:", [data['ScheduledDate'].min(), data['ScheduledDate'].max()])

    # Select Rooms
    rooms = sorted(data['Roomdescription'].unique().tolist())
    selected_rooms = st.sidebar.multiselect("Select Rooms:", rooms, default=rooms)

    if st.sidebar.button("Select All Rooms"):
        selected_rooms = rooms

    # Filter data
    filtered_data = data[
        (data['ScheduledDate'] >= pd.to_datetime(date_range[0])) & 
        (data['ScheduledDate'] <= pd.to_datetime(date_range[1])) &
        (data['Roomdescription'].isin(selected_rooms))
    ]

    return filtered_data, pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])

def app(data):
    st.title("Room Utilization")

    # Apply filters
    filtered_data, start_date, end_date = filter_data(data)

    # Day Calculations
    total_days = (end_date - start_date).days + 1

    remove_weekends = st.sidebar.checkbox("Remove Weekends")
    remove_civic_holidays = st.sidebar.checkbox("Remove Ontario Civic Holidays")

    if remove_weekends:
        filtered_data['DayOfWeek'] = filtered_data['ScheduledDate'].dt.day_name()
        filtered_data = filtered_data[~filtered_data['DayOfWeek'].isin(['Saturday', 'Sunday'])]
        total_days -= len(pd.date_range(start_date, end_date, freq='W-SAT')) + len(pd.date_range(start_date, end_date, freq='W-SUN'))

    if remove_civic_holidays:
        filtered_data = filtered_data[~filtered_data['ScheduledDate'].isin(pd.to_datetime(ontario_civic_holidays))]
        total_days -= sum(start_date <= pd.to_datetime(holiday) <= end_date for holiday in ontario_civic_holidays)

    room_speciality_group = filtered_data.groupby(['Roomdescription', 'ProcedureSpecialtyDescription'])['book_dur'].sum().unstack().fillna(0)
    total_available_minutes = total_days * 8 * 60
    utilization_percentage = (room_speciality_group / total_available_minutes) * 100

    room_total_utilization = utilization_percentage.sum(axis=1)

    # Visualization of room utilization percentage by speciality (stacked bar chart)
    fig, ax = plt.subplots(figsize=(10, 6))
    utilization_percentage.plot(kind='bar', stacked=True, ax=ax)
    ax.set_title('Room Utilization Percentage by Speciality')
    ax.set_xlabel('Room')
    ax.set_ylabel('Utilization Percentage (%)')
    plt.xticks(rotation=45)
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(True)
    st.pyplot(fig)

    # Formatting utilization percentages for display
    utilization_percentage = utilization_percentage.applymap(lambda x: f"{x:.2f}%")
    room_total_utilization_disp = room_total_utilization.apply(lambda x: f"{x:.2f}%")
    
    st.write("### Total Utilization Percentage by Room")
    st.dataframe(room_total_utilization_disp.reset_index().rename(columns={0: 'Total Utilization Percentage'}))

    st.write("### Room Utilization Data")

    # Calculate ratio of specialty usage in each room (on a scheduled minutes basis)
    total_minutes_per_room_speciality = filtered_data.pivot_table(values='book_dur', index='Roomdescription', columns='ProcedureSpecialtyDescription', aggfunc='sum', fill_value=0)
    total_minutes_per_room = total_minutes_per_room_speciality.sum(axis=1)
    speciality_percentage_per_room = total_minutes_per_room_speciality.div(total_minutes_per_room, axis=0) * 100

    # Formatting to percent for display
    speciality_percentage_per_room = speciality_percentage_per_room.applymap(lambda x: f"{x:.2f}%")

    st.write("### Speciality Utilization as Percentage of Total Minutes Scheduled per Room")
    st.dataframe(speciality_percentage_per_room)

    total_minutes_per_room_priority = filtered_data.pivot_table(values='book_dur', index='Roomdescription', columns='SurgicalPriority', aggfunc='sum', fill_value=0)
    total_minutes_per_room = total_minutes_per_room_priority.sum(axis=1)
    priority_percentage_per_room_graph = total_minutes_per_room_priority.div(total_available_minutes, axis=0) * 100
    
    st.write("### Surgical Priority Utilization as Percentage of Total Minutes Scheduled per Room")
  
    # Visualization of room utilization percentage by surgical priority (stacked bar chart)
    fig, ax = plt.subplots(figsize=(10, 6))
    priority_percentage_per_room_graph.plot(kind='bar', stacked=True, ax=ax)
    ax.set_title('Room Utilization Percentage by Surgical Priority')
    ax.set_xlabel('Room')
    ax.set_ylabel('Utilization Percentage (%)')
    plt.xticks(rotation=45)
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(True)
    st.pyplot(fig)

    # Formatting the percentages for display
    priority_percentage_per_room = total_minutes_per_room_priority.div(total_minutes_per_room, axis=0) * 100
    priority_percentage_per_room_disp = priority_percentage_per_room.applymap(lambda x: f"{x:.2f}%")
    st.dataframe(priority_percentage_per_room_disp)

    # Writing total Utilization Percentage
    room_usage = room_total_utilization.mean()
    st.title(f"Total OR Utilization: {room_usage:.2f}%")

