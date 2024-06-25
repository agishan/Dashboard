import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def filter_data(data):
    # Parse date and time columns and handle errors
    data['ScheduledDateTime'] = pd.to_datetime(data['ScheduledDateTime'], errors='coerce')
    data['RoomEnterDateTime'] = pd.to_datetime(data['RoomEnterDateTime'], errors='coerce')
    data['RoomExitDateTime'] = pd.to_datetime(data['RoomExitDateTime'], errors='coerce')
    data = data.dropna(subset=['ScheduledDateTime', 'RoomEnterDateTime', 'RoomExitDateTime'])

    # Metric calculation
    data['EntryTimeDifference'] = data['RoomEnterDateTime'] - data['ScheduledDateTime']
    data['ActualDuration'] = data['RoomExitDateTime'] - data['RoomEnterDateTime']
    data['book_dur'] = pd.to_numeric(data['book_dur'], errors='coerce')
    data['ActualDurationMinutes'] = data['ActualDuration'].dt.total_seconds() / 60
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
    st.write("Duration Difference is Actual Duration - Booked Duration (schedule)")
    filtered_data = filter_data(data)

    summary_table = filtered_data.groupby('ProcedureSpecialtyDescription').agg(
        count=('ProcedureSpecialtyDescription', 'size'),
        average_booked_duration=('book_dur', 'mean'),
        average_real_duration=('ActualDurationMinutes', 'mean'),
        average_delay=('DurationDifference', 'mean')
    ).reset_index()

    st.dataframe(summary_table)

    duration_by_room = filtered_data.groupby('Roomdescription').agg(
        total_scheduled_duration=('book_dur', 'sum'),
        total_actual_duration=('ActualDurationMinutes', 'sum')
    ).reset_index()

     # Visualization: Duration Difference by Room
    st.write("### Duration Difference by Room")

    duration_diff_by_room = filtered_data.groupby('Roomdescription').agg(
        average_duration_difference=('DurationDifference', 'mean')
    ).reset_index()

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.bar(duration_diff_by_room['Roomdescription'], duration_diff_by_room['average_duration_difference'], color='skyblue')

    ax.set_xlabel('Room')
    ax.set_ylabel('Average Duration Difference (minutes)')
    ax.set_title('Average Duration Difference by Room')
    plt.xticks(rotation=45)

    st.pyplot(fig)

    # Visualization: Scheduled Duration vs Actual Duration
    st.write("### Scheduled vs Actual Duration")

    fig, ax = plt.subplots(figsize=(12, 8))
    bar_width = 0.4
    index = range(len(duration_by_room))

    bar1 = ax.bar(index, duration_by_room['total_scheduled_duration'], bar_width, label='Scheduled Duration')
    bar2 = ax.bar([i + bar_width for i in index], duration_by_room['total_actual_duration'], bar_width, label='Actual Duration')

    ax.set_xlabel('Room')
    ax.set_ylabel('Duration (minutes)')
    ax.set_title('Scheduled Duration vs Actual Duration by Room')
    ax.set_xticks([i + bar_width / 2 for i in index])
    ax.set_xticklabels(duration_by_room['Roomdescription'], rotation=45)
    ax.legend()

    st.pyplot(fig)

    # Visualization: Duration Difference by Surgical Specialty
    st.write("### Duration Difference by Surgical Specialty")

    duration_diff_by_specialty = filtered_data.groupby('ProcedureSpecialtyDescription').agg(
        average_duration_difference=('DurationDifference', 'mean')
    ).reset_index()

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.bar(duration_diff_by_specialty['ProcedureSpecialtyDescription'], duration_diff_by_specialty['average_duration_difference'], color='salmon')

    ax.set_xlabel('Surgical Specialty')
    ax.set_ylabel('Average Duration Difference (minutes)')
    ax.set_title('Average Duration Difference by Surgical Specialty')
    plt.xticks(rotation=45)

    st.pyplot(fig)

    # Scheduled vs Actual Duration by Surgical Specialty
    st.write("### Scheduled vs Actual Duration by Surgical Specialty")

    duration_by_specialty = filtered_data.groupby('ProcedureSpecialtyDescription').agg(
        total_scheduled_duration=('book_dur', 'sum'),
        total_actual_duration=('ActualDurationMinutes', 'sum')
    ).reset_index()

    fig, ax = plt.subplots(figsize=(12, 8))
    bar_width = 0.4
    index = range(len(duration_by_specialty))

    bar1 = ax.bar(index, duration_by_specialty['total_scheduled_duration'], bar_width, label='Scheduled Duration')
    bar2 = ax.bar([i + bar_width for i in index], duration_by_specialty['total_actual_duration'], bar_width, label='Actual Duration')

    ax.set_xlabel('Surgical Specialty')
    ax.set_ylabel('Duration (minutes)')
    ax.set_title('Scheduled vs Actual Duration by Surgical Specialty')
    ax.set_xticks([i + bar_width / 2 for i in index])
    ax.set_xticklabels(duration_by_specialty['ProcedureSpecialtyDescription'], rotation=45)
    ax.legend()

    st.pyplot(fig)

    # Visualization: Duration Difference by Day of the Week
    st.write("### Duration Difference by Day of the Week")

    duration_diff_by_day = filtered_data.groupby(filtered_data['ScheduledDateTime'].dt.day_name()).agg(
        average_duration_difference=('DurationDifference', 'mean')
    ).reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']).reset_index()

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.bar(duration_diff_by_day['ScheduledDateTime'], duration_diff_by_day['average_duration_difference'], color='lightgreen')

    ax.set_xlabel('Day of the Week')
    ax.set_ylabel('Average Duration Difference (minutes)')
    ax.set_title('Average Duration Difference by Day of the Week')
    plt.xticks(rotation=45)

    st.pyplot(fig)

    # Scheduled vs Actual Duration by Day of the Week
    st.write("### Scheduled vs Actual Duration by Day of the Week")

    duration_by_day = filtered_data.groupby(filtered_data['ScheduledDateTime'].dt.day_name()).agg(
        total_scheduled_duration=('book_dur', 'sum'),
        total_actual_duration=('ActualDurationMinutes', 'sum')
    ).reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']).reset_index()

    fig, ax = plt.subplots(figsize=(12, 8))
    bar_width = 0.4
    index = range(len(duration_by_day))

    bar1 = ax.bar(index, duration_by_day['total_scheduled_duration'], bar_width, label='Scheduled Duration')
    bar2 = ax.bar([i + bar_width for i in index], duration_by_day['total_actual_duration'], bar_width, label='Actual Duration')

    ax.set_xlabel('Day of the Week')
    ax.set_ylabel('Duration (minutes)')
    ax.set_title('Scheduled vs Actual Duration by Day of the Week')
    ax.set_xticks([i + bar_width / 2 for i in index])
    ax.set_xticklabels(duration_by_day['ScheduledDateTime'], rotation=45)
    ax.legend()

    st.pyplot(fig)
