import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def filter_data(data):
    # Parse date and time columns and handle errors
    data['ScheduledDateTime'] = pd.to_datetime(data['ScheduledDateTime'])
    data['RoomEnterDateTime'] = pd.to_datetime(data['RoomEnterDateTime'])
    data['RoomExitDateTime'] = pd.to_datetime(data['RoomExitDateTime'])

    # Filter out rows where date parsing failed
    data = data.dropna(subset=['ScheduledDateTime', 'RoomEnterDateTime', 'RoomExitDateTime'])

    # Calculate the difference between scheduled and actual entry times
    data['EntryTimeDifference'] = data['RoomEnterDateTime'] - data['ScheduledDateTime']

    # Calculate the actual duration spent in the room
    data['ActualDuration'] = data['RoomExitDateTime'] - data['RoomEnterDateTime']

    # Ensure book_dur is numeric and represents duration in minutes
    data['book_dur'] = pd.to_numeric(data['book_dur'], errors='coerce')

    # Calculate the actual duration in minutes
    data['ActualDurationMinutes'] = data['ActualDuration'].dt.total_seconds() / 60

    # Calculate the difference between scheduled and actual duration
    data['DurationDifference'] = data['ActualDurationMinutes'] - data['book_dur']

    st.sidebar.title("Filters")
    st.sidebar.markdown("Select the Procedure Speciality, Date options, and Rooms:")

    # Select Speciality
    specialities = sorted(data['ProcedureSpecialtyDescription'].unique().tolist())
    selected_speciality = st.sidebar.selectbox("Select Speciality:", specialities)

    # Filter data based on selected specialty
    filtered_data = data[data['ProcedureSpecialtyDescription'] == selected_speciality]

    # Select Date Range
    date_range = st.sidebar.date_input("Select Date Range:", [filtered_data['ScheduledDateTime'].min(), filtered_data['ScheduledDateTime'].max()])

    # Select Surgical Priority
    surgical_priorities = sorted(filtered_data['SurgicalPriority'].unique().tolist())
    all_priorities = st.sidebar.checkbox("Select all priorities", value=True)
    if all_priorities:
        selected_priorities = st.sidebar.multiselect("Select Surgical Priorities:", surgical_priorities, default=surgical_priorities)
    else:
        selected_priorities = st.sidebar.multiselect("Select Surgical Priorities:", surgical_priorities)

    # Select Rooms
    rooms = sorted(filtered_data['Roomdescription'].unique().tolist())
    all_rooms = st.sidebar.checkbox("Select all rooms", value=True)
    if all_rooms:
        selected_rooms = st.sidebar.multiselect("Select Rooms:", rooms, default=rooms)
    else:
        selected_rooms = st.sidebar.multiselect("Select Rooms:", rooms)

    # Select Surgeon IDs
    surgeons = sorted(filtered_data['surgeonID'].unique().tolist())
    all_surgeons = st.sidebar.checkbox("Select all surgeons", value=True)
    if all_surgeons:
        selected_surgeons = st.sidebar.multiselect("Select Surgeons:", surgeons, default=surgeons)
    else:
        selected_surgeons = st.sidebar.multiselect("Select Surgeons:", surgeons)

    # Select Surgery Types
    surgeries = sorted(filtered_data['ProcedureDescription'].unique().tolist())
    all_surgeries = st.sidebar.checkbox("Select all surgeries", value=True)
    if all_surgeries:
        selected_surgeries = st.sidebar.multiselect("Select Surgeries:", surgeries, default=surgeries)
    else:
        selected_surgeries = st.sidebar.multiselect("Select Surgeries:", surgeries)

    # Filter data based on selected criteria
    filtered_data = filtered_data[
        (filtered_data['ScheduledDateTime'] >= pd.to_datetime(date_range[0])) &
        (filtered_data['ScheduledDateTime'] <= pd.to_datetime(date_range[1])) &
        (filtered_data['Roomdescription'].isin(selected_rooms if selected_rooms else rooms)) &
        (filtered_data['SurgicalPriority'].isin(selected_priorities if selected_priorities else surgical_priorities)) &
        (filtered_data['surgeonID'].isin(selected_surgeons if selected_surgeons else surgeons)) &
        (filtered_data['ProcedureDescription'].isin(selected_surgeries if selected_surgeries else surgeries))
    ]

    return filtered_data

def app(data):
    st.title("Surgical Specialty Delay Analysis")
    st.subheader('Delay is calculated as Real Time - Booked Time, Booked time includes 15 minutes extra')
    filtered_data = filter_data(data)

    # Add Summary Table
    summary_table = filtered_data.groupby('ProcedureDescription').agg(
        count=('ProcedureDescription', 'size'),
        average_booked_duration=('book_dur', 'mean'),
        average_real_duration=('ActualDurationMinutes', 'mean'),
        average_delay=('DurationDifference', 'mean')
    ).reset_index()

    st.dataframe(summary_table)

    # Visualization options
    st.write("### Delay Analysis")

    # Delay by Room
    delay_by_room = filtered_data.groupby('Roomdescription').agg(
        count=('Roomdescription', 'size'),
        average_delay=('DurationDifference', 'mean')
    )

    st.write("#### Delay by Room")
    fig, ax = plt.subplots(figsize=(10, 6))
    delay_by_room['average_delay'].plot(kind='bar', ax=ax)
    ax.set_title('Average Delay by Room')
    ax.set_xlabel('Room')
    ax.set_ylabel('Average Delay (minutes)')
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Summary Table for Delay by Room
    st.dataframe(delay_by_room.reset_index())

    # Delay by Surgery
    delay_by_surgery = filtered_data.groupby('ProcedureDescription').agg(
        count=('ProcedureDescription', 'size'),
        average_delay=('DurationDifference', 'mean')
    )

    st.write("#### Delay by Surgery")
    fig, ax = plt.subplots(figsize=(10, 6))
    delay_by_surgery['average_delay'].plot(kind='bar', ax=ax)
    ax.set_title('Average Delay by Surgery')
    ax.set_xlabel('Surgery')
    ax.set_ylabel('Average Delay (minutes)')
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Summary Table for Delay by Surgery
    st.dataframe(delay_by_surgery.reset_index())

    # Delay by Day of the Week
    delay_by_day = filtered_data.groupby(filtered_data['ScheduledDateTime'].dt.day_name()).agg(
        count=('ScheduledDateTime', 'size'),
        average_delay=('DurationDifference', 'mean')
    ).reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

    st.write("#### Delay by Day of the Week")
    fig, ax = plt.subplots(figsize=(10, 6))
    delay_by_day['average_delay'].plot(kind='bar', ax=ax)
    ax.set_title('Average Delay by Day of the Week')
    ax.set_xlabel('Day of the Week')
    ax.set_ylabel('Average Delay (minutes)')
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Summary Table for Delay by Day of the Week
    st.dataframe(delay_by_day.reset_index())

    # Delay by Surgeon
    delay_by_surgeon = filtered_data.groupby('surgeonID').agg(
        count=('surgeonID', 'size'),
        average_delay=('DurationDifference', 'mean')
    )

    st.write("#### Delay by Surgeon")
    fig, ax = plt.subplots(figsize=(10, 6))
    delay_by_surgeon['average_delay'].plot(kind='bar', ax=ax)
    ax.set_title('Average Delay by Surgeon')
    ax.set_xlabel('Surgeon ID')
    ax.set_ylabel('Average Delay (minutes)')
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Summary Table for Delay by Surgeon
    st.dataframe(delay_by_surgeon.reset_index())