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
    
    data = data[(data['ProcedureSpecialtyDescription'].isin(selected_specialities))]

    # Select Surgeon IDs
    surgeon_ids = sorted(data['surgeonID'].unique().tolist())
    all_surgeons = st.sidebar.checkbox("Select all surgeons", value=True)
    if all_surgeons:
        selected_surgeons = st.sidebar.multiselect("Select Surgeon IDs:", surgeon_ids, default=surgeon_ids)
    else:
        selected_surgeons = st.sidebar.multiselect("Select Surgeon IDs:", surgeon_ids)

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

def calculate_employment_days(filtered_data):
    employment_days = filtered_data.groupby('surgeonID')['ScheduledDate'].agg(lambda x: (x.max() - x.min()).days + 1)
    return employment_days

def app(data):
    st.title("Surgeon Overview")

    # Apply filters
    filtered_data_surgeons = filter_data(data)

    # Calculate employment days
    employment_days = calculate_employment_days(filtered_data_surgeons)
    filtered_data_surgeons = filtered_data_surgeons.merge(employment_days.rename('EmploymentDays'), on='surgeonID')

    # Calculate average minutes of surgery per day of employment
    filtered_data_surgeons['AvgMinutesPerDay'] = filtered_data_surgeons.groupby('surgeonID')['book_dur'].transform('sum') / filtered_data_surgeons['EmploymentDays']

    # Display summary table for selected Surgeon IDs
    summary_table = filtered_data_surgeons.groupby('surgeonID').agg(
        total_duration=pd.NamedAgg(column='book_dur', aggfunc='sum'),
        total_surgeries=pd.NamedAgg(column='EncounterID', aggfunc='count'),
        average_duration=pd.NamedAgg(column='book_dur', aggfunc='mean'),
        employment_days=pd.NamedAgg(column='EmploymentDays', aggfunc='first'),
        avg_minutes_per_day=pd.NamedAgg(column='AvgMinutesPerDay', aggfunc='first')
    ).reset_index()
    st.write("### Summary Table for Selected Surgeon IDs")
    st.dataframe(summary_table)
    
    # Visualization of surgeries by Surgeon ID
    st.write("### Surgeries by Surgeon ID")

    fig, ax = plt.subplots(figsize=(10, 6))
    filtered_data_surgeons['surgeonID'].value_counts().plot(kind='bar', ax=ax)
    ax.set_title('Surgeries by Surgeon ID')
    ax.set_xlabel('Surgeon ID')
    ax.set_ylabel('Number of Surgeries')
    plt.xticks(rotation=45)
    ax.grid(True)
    st.pyplot(fig)

    # Calculate the average duration of surgeries per Surgeon ID
    average_duration_per_surgeon = filtered_data_surgeons.groupby('surgeonID')['book_dur'].mean()

    # Visualization of the average duration of surgeries per Surgeon ID
    st.write("### Average Duration of Surgeries per Surgeon ID")

    fig, ax = plt.subplots(figsize=(10, 6))
    average_duration_per_surgeon.plot(kind='bar', ax=ax)
    ax.set_title('Average Duration of Surgeries per Surgeon ID')
    ax.set_xlabel('Surgeon ID')
    ax.set_ylabel('Average Duration (minutes)')
    plt.xticks(rotation=45)
    ax.grid(True)
    st.pyplot(fig)

    # Calculate the count of surgeries per room for each surgeon
    surgeries_per_room_per_surgeon = filtered_data_surgeons.groupby(['surgeonID', 'Roomdescription']).size().unstack(fill_value=0)

    # Visualization of the count of surgeries per room for each surgeon
    st.write("### Surgeries per Room for Selected Surgeon IDs")

    fig, ax = plt.subplots(figsize=(10, 6))
    surgeries_per_room_per_surgeon.plot(kind='bar', stacked=True, ax=ax)
    ax.set_title('Surgeries per Room for Selected Surgeon IDs')
    ax.set_xlabel('Surgeon ID')
    ax.set_ylabel('Number of Surgeries')
    plt.xticks(rotation=45)
    ax.grid(True)
    st.pyplot(fig)

    # Calculate the count of surgeries per day of the week for each surgeon
    surgeries_per_day_per_surgeon = filtered_data_surgeons.groupby(['surgeonID', 'DayOfWeek']).size().unstack(fill_value=0).reindex(columns=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

    # Visualization of the count of surgeries per day of the week for each surgeon
    st.write("### Surgeries per Day of the Week for Selected Surgeon IDs")

    fig, ax = plt.subplots(figsize=(10, 6))
    surgeries_per_day_per_surgeon.plot(kind='bar', stacked=True, ax=ax)
    ax.set_title('Surgeries per Day of the Week for Selected Surgeon IDs')
    ax.set_xlabel('Surgeon ID')
    ax.set_ylabel('Number of Surgeries')
    plt.xticks(rotation=45)
    ax.grid(True)
    st.pyplot(fig)
