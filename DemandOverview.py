import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def filter_data(data):
    st.sidebar.title("Filters")
    st.sidebar.markdown("Select the Procedure Speciality, Surgical Priority, Date options, and Rooms:")

    # Select Speciality
    specialities = sorted(data['ProcedureSpecialtyDescription'].unique().tolist())
    all_specialities = st.sidebar.checkbox("Select all specialities", value=True)
    if all_specialities:
        selected_specialities = st.sidebar.multiselect("Select Speciality:", specialities, default=specialities)
    else:
        selected_specialities = st.sidebar.multiselect("Select Speciality:", specialities)

    # Initial filter to limit options
    if selected_specialities:
        filtered_data = data[data['ProcedureSpecialtyDescription'].isin(selected_specialities)]
    else:
        filtered_data = data.copy()

    # Select Surgical Priority
    surgical_priorities = sorted(filtered_data['SurgicalPriority'].unique().tolist())
    all_priorities = st.sidebar.checkbox("Select all priorities", value=True)
    if all_priorities:
        selected_priorities = st.sidebar.multiselect("Select Surgical Priorities:", surgical_priorities, default=surgical_priorities)
    else:
        selected_priorities = st.sidebar.multiselect("Select Surgical Priorities:", surgical_priorities)

    # Select Date Range
    date_range = st.sidebar.date_input("Select Date Range:", [filtered_data['ScheduledDate'].min(), filtered_data['ScheduledDate'].max()])

    # Select Years
    years = sorted(filtered_data['Surgery Year'].unique().tolist())
    all_years = st.sidebar.checkbox("Select all years", value=True)
    if all_years:
        selected_years = st.sidebar.multiselect("Select Years:", years, default=years)
    else:
        selected_years = st.sidebar.multiselect("Select Years:", years)

    # Select Rooms
    rooms = sorted(filtered_data['Roomdescription'].unique().tolist())
    all_rooms = st.sidebar.checkbox("Select all rooms", value=True)
    if all_rooms:
        selected_rooms = st.sidebar.multiselect("Select Rooms:", rooms, default=rooms)
    else:
        selected_rooms = st.sidebar.multiselect("Select Rooms:", rooms)

    # Select Surgeon IDs
    surgeon_ids = sorted(filtered_data['surgeonID'].unique().tolist())
    all_surgeons = st.sidebar.checkbox("Select all surgeons", value=True)
    if all_surgeons:
        selected_surgeons = st.sidebar.multiselect("Select Surgeon IDs:", surgeon_ids, default=surgeon_ids)
    else:
        selected_surgeons = st.sidebar.multiselect("Select Surgeon IDs:", surgeon_ids)

    # Filter data
    filtered_data = filtered_data[
        (filtered_data['ProcedureSpecialtyDescription'].isin(selected_specialities if selected_specialities else specialities)) &
        (filtered_data['surgeonID'].isin(selected_surgeons if selected_surgeons else surgeon_ids)) &
        (filtered_data['SurgicalPriority'].isin(selected_priorities if selected_priorities else surgical_priorities)) & 
        (filtered_data['ScheduledDate'] >= pd.to_datetime(date_range[0])) & 
        (filtered_data['ScheduledDate'] <= pd.to_datetime(date_range[1])) & 
        (filtered_data['Surgery Year'].isin(selected_years if selected_years else years)) & 
        (filtered_data['Roomdescription'].isin(selected_rooms if selected_rooms else rooms)) 
    ]

    return filtered_data

def app(data):
    st.title("Demand Overview")

    filtered_data = filter_data(data)

    # Create a date range covering the entire period
    full_date_range = pd.date_range(start=filtered_data['ScheduledDate'].min(), end=filtered_data['ScheduledDate'].max())

    # Aggregate the data by counting the number of surgeries per day
    filtered_data_grouped = filtered_data.groupby('ScheduledDate').size().reindex(full_date_range, fill_value=0).reset_index(name='COUNT')
    filtered_data_grouped.rename(columns={'index': 'ScheduledDate'}, inplace=True)

    # Add Summary Table
    summary_table = filtered_data.groupby('ProcedureSpecialtyDescription').agg(
        count=('ProcedureSpecialtyDescription', 'size'),
        average_duration=('book_dur', 'mean')
    ).reset_index()

    st.dataframe(summary_table)

    # Visualization options
    st.write("### Surgeries over Time")

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(filtered_data_grouped['ScheduledDate'], filtered_data_grouped['COUNT'])
    ax.set_title('Surgeries Over Time')
    ax.set_xlabel('Date')
    ax.set_ylabel('Number of Surgeries')
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Calculate the average number of surgeries per day of the week
    surgeries_per_day = filtered_data['DayOfWeek'].value_counts().reindex(
        ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    ).fillna(0)
    weeks_count = filtered_data['ScheduledDate'].nunique() / 7
    average_per_day_of_week = surgeries_per_day / weeks_count

    # Visualization of the average number of surgeries per day of the week
    st.write("### Average Number of Surgeries per Day of the Week")

    fig, ax = plt.subplots(figsize=(10, 6))
    average_per_day_of_week.plot(kind='bar', ax=ax)
    ax.set_title('Average Number of Surgeries per Day of the Week')
    ax.set_xlabel('Day of the Week')
    ax.set_ylabel('Average Number of Surgeries')
    plt.xticks(rotation=45)
    ax.grid(True)
    st.pyplot(fig)

    # Calculate the total duration of surgeries per day of the week
    total_duration_per_day = filtered_data.groupby('DayOfWeek')['book_dur'].sum().reindex(
        ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    ).fillna(0)

    # Visualization of the total duration of surgeries per day of the week
    st.write("### Total Duration of Surgeries per Day of the Week")

    fig, ax = plt.subplots(figsize=(10, 6))
    total_duration_per_day.plot(kind='bar', ax=ax)
    ax.set_title('Total Duration of Surgeries per Day of the Week')
    ax.set_xlabel('Day of the Week')
    ax.set_ylabel('Total Duration (minutes)')
    plt.xticks(rotation=45)
    ax.grid(True)
    st.pyplot(fig)

    # Calculate the count of surgeries per room
    count_per_room = filtered_data['Roomdescription'].value_counts()

    # Visualization of the count of surgeries per room
    st.write("### Count of Surgeries per Room")

    fig, ax = plt.subplots(figsize=(10, 6))
    count_per_room.plot(kind='bar', ax=ax)
    ax.set_title('Count of Surgeries per Room')
    ax.set_xlabel('Room')
    ax.set_ylabel('Count')
    plt.xticks(rotation=45)
    ax.grid(True)
    st.pyplot(fig)

    # Calculate the total booked duration of surgeries per room
    duration_per_room = filtered_data.groupby('Roomdescription')['book_dur'].sum()

    # Visualization of the total booked duration of surgeries per room
    st.write("### Total Booked Duration of Surgeries per Room")

    fig, ax = plt.subplots(figsize=(10, 6))
    duration_per_room.plot(kind='bar', ax=ax)
    ax.set_title('Total Booked Duration of Surgeries per Room')
    ax.set_xlabel('Room')
    ax.set_ylabel('Duration (minutes)')
    plt.xticks(rotation=45)
    ax.grid(True)
    st.pyplot(fig)