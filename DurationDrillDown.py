import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def filter_data(data):
    # Data conversion
    data['ScheduledDateTime'] = pd.to_datetime(data['ScheduledDateTime'])
    data['RoomEnterDateTime'] = pd.to_datetime(data['RoomEnterDateTime'])
    data['RoomExitDateTime'] = pd.to_datetime(data['RoomExitDateTime'])
    data = data.dropna(subset=['ScheduledDateTime', 'RoomEnterDateTime', 'RoomExitDateTime'])

    # Metric Calculation
    data['ActualDuration'] = data['RoomExitDateTime'] - data['RoomEnterDateTime']
    data['book_dur'] = pd.to_numeric(data['book_dur'], errors='coerce')
    data['ActualDurationMinutes'] = data['ActualDuration'].dt.total_seconds() / 60

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
    st.title("Surgical Specialty Duration Analysis")
    st.subheader('Comparing Real Duration and Booked Duration')
    filtered_data = filter_data(data)

    summary_table = filtered_data.groupby('ProcedureDescription').agg(
        count=('ProcedureDescription', 'size'),
        average_booked_duration=('book_dur', 'mean'),
        average_real_duration=('ActualDurationMinutes', 'mean')
    ).reset_index()

    st.dataframe(summary_table)

    # Visualizations
    st.write("### Duration Analysis")

    # Duration by Room
    duration_by_room = filtered_data.groupby('Roomdescription').agg(
        count=('Roomdescription', 'size'),
        average_booked_duration=('book_dur', 'mean'),
        average_real_duration=('ActualDurationMinutes', 'mean')
    )

    st.write("#### Duration by Room")
    fig, ax = plt.subplots(figsize=(10, 6))
    duration_by_room[['average_booked_duration', 'average_real_duration']].plot(kind='bar', ax=ax)
    ax.set_title('Average Duration by Room')
    ax.set_xlabel('Room')
    ax.set_ylabel('Average Duration (minutes)')
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Summary Table for Duration by Room
    st.dataframe(duration_by_room.reset_index())

    # Duration by Surgery
    duration_by_surgery = filtered_data.groupby('ProcedureDescription').agg(
        count=('ProcedureDescription', 'size'),
        average_booked_duration=('book_dur', 'mean'),
        average_real_duration=('ActualDurationMinutes', 'mean')
    )

    st.write("#### Duration by Surgery")
    fig, ax = plt.subplots(figsize=(10, 6))
    duration_by_surgery[['average_booked_duration', 'average_real_duration']].plot(kind='bar', ax=ax)
    ax.set_title('Average Duration by Surgery')
    ax.set_xlabel('Surgery')
    ax.set_ylabel('Average Duration (minutes)')
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Summary Table for Duration by Surgery
    st.dataframe(duration_by_surgery.reset_index())

    # Duration by Day of the Week
    duration_by_day = filtered_data.groupby(filtered_data['ScheduledDateTime'].dt.day_name()).agg(
        count=('ScheduledDateTime', 'size'),
        average_booked_duration=('book_dur', 'mean'),
        average_real_duration=('ActualDurationMinutes', 'mean')
    ).reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

    st.write("#### Duration by Day of the Week")
    fig, ax = plt.subplots(figsize=(10, 6))
    duration_by_day[['average_booked_duration', 'average_real_duration']].plot(kind='bar', ax=ax)
    ax.set_title('Average Duration by Day of the Week')
    ax.set_xlabel('Day of the Week')
    ax.set_ylabel('Average Duration (minutes)')
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Summary Table for Duration by Day of the Week
    st.dataframe(duration_by_day.reset_index())

    # Duration by Surgeon
    duration_by_surgeon = filtered_data.groupby('surgeonID').agg(
        count=('surgeonID', 'size'),
        average_booked_duration=('book_dur', 'mean'),
        average_real_duration=('ActualDurationMinutes', 'mean')
    )

    st.write("#### Duration by Surgeon")
    fig, ax = plt.subplots(figsize=(10, 6))
    duration_by_surgeon[['average_booked_duration', 'average_real_duration']].plot(kind='bar', ax=ax)
    ax.set_title('Average Duration by Surgeon')
    ax.set_xlabel('Surgeon ID')
    ax.set_ylabel('Average Duration (minutes)')
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Summary Table for Duration by Surgeon
    st.dataframe(duration_by_surgeon.reset_index())

