import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def filter_data(data):
    # Parse date and time columns and handle errors
    data['ScheduledDateTime'] = pd.to_datetime(data['ScheduledDateTime'], errors='coerce')
    data['RoomEnterDateTime'] = pd.to_datetime(data['RoomEnterDateTime'], errors='coerce')
    data['RoomExitDateTime'] = pd.to_datetime(data['RoomExitDateTime'], errors='coerce')

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
    date_range = st.sidebar.date_input("Select Date Range:", [filtered_data['ScheduledDateTime'].min(), filtered_data['ScheduledDateTime'].max()])

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
        (filtered_data['ScheduledDateTime'] >= pd.to_datetime(date_range[0])) &
        (filtered_data['ScheduledDateTime'] <= pd.to_datetime(date_range[1])) &
        (filtered_data['Surgery Year'].isin(selected_years if selected_years else years)) &
        (filtered_data['Roomdescription'].isin(selected_rooms if selected_rooms else rooms))
    ]

    return filtered_data

def app(data):
    st.title("Surgery Schedule Analysis")
    st.subheader('Delay is calculated as Real Time - Booked Time, Booked time includes 15 minutes extra')
    filtered_data = filter_data(data)

    # Add Summary Table
    summary_table = filtered_data.groupby('ProcedureSpecialtyDescription').agg(
        count=('ProcedureSpecialtyDescription', 'size'),
        average_booked_duration=('book_dur', 'mean'),
        average_real_duration=('ActualDurationMinutes', 'mean'),
        average_delay=('DurationDifference', 'mean')
    ).reset_index()

    st.dataframe(summary_table)

    # Visualization options
    st.write("### Duration Difference Analysis")

    # DurationDifference by Room
    duration_diff_by_room = filtered_data.groupby('Roomdescription').agg(
        count=('Roomdescription', 'size'),
        average_duration_difference=('DurationDifference', 'mean')
    ).reset_index()

    st.write("#### Duration Difference by Room")
    fig, ax = plt.subplots(figsize=(10, 6))
    duration_diff_by_room.set_index('Roomdescription')['average_duration_difference'].plot(kind='bar', ax=ax)
    ax.set_title('Average Duration Difference by Room')
    ax.set_xlabel('Room')
    ax.set_ylabel('Average Duration Difference (minutes)')
    plt.xticks(rotation=45)
    st.pyplot(fig)
    st.dataframe(duration_diff_by_room)

    # DurationDifference by Surgical Specialty
    duration_diff_by_specialty = filtered_data.groupby('ProcedureSpecialtyDescription').agg(
        count=('ProcedureSpecialtyDescription', 'size'),
        average_duration_difference=('DurationDifference', 'mean')
    ).reset_index()

    st.write("#### Duration Difference by Surgical Specialty")
    fig, ax = plt.subplots(figsize=(10, 6))
    duration_diff_by_specialty.set_index('ProcedureSpecialtyDescription')['average_duration_difference'].plot(kind='bar', ax=ax)
    ax.set_title('Average Duration Difference by Surgical Specialty')
    ax.set_xlabel('Surgical Specialty')
    ax.set_ylabel('Average Duration Difference (minutes)')
    plt.xticks(rotation=45)
    st.pyplot(fig)
    st.dataframe(duration_diff_by_specialty)

    # DurationDifference by Day of the Week
    duration_diff_by_day = filtered_data.groupby(filtered_data['DayOfWeek']).agg(
        count=('DayOfWeek', 'size'),
        average_duration_difference=('DurationDifference', 'mean')
    ).reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']).reset_index()

    st.write("#### Duration Difference by Day of the Week")
    fig, ax = plt.subplots(figsize=(10, 6))
    duration_diff_by_day.set_index('DayOfWeek')['average_duration_difference'].plot(kind='bar', ax=ax)
    ax.set_title('Average Duration Difference by Day of the Week')
    ax.set_xlabel('Day of the Week')
    ax.set_ylabel('Average Duration Difference (minutes)')
    plt.xticks(rotation=45)
    st.pyplot(fig)
    st.dataframe(duration_diff_by_day)
