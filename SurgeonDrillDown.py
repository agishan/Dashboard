import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def filter_data(data):
    st.sidebar.title("Filters")
    st.sidebar.markdown("Select the SERVICE_CATEGORY, SurgicalPriority, Date options, and Rooms:")

    # Select Surgeon ID
    surgeon_ids = sorted(data['surgeonID'].unique().tolist())
    selected_surgeons = st.sidebar.selectbox("Select Surgeon IDs:", surgeon_ids)
   
    # Filter data by selected Surgeon ID
    filtered_data = data[data['surgeonID'] == selected_surgeons]

    # Select Speciality
    specialities = sorted(filtered_data['ProcedureSpecialtyDescription'].unique().tolist())
    all_specialities = st.sidebar.checkbox("Select all specialities", value=True)
    if all_specialities:
        specialities_category = st.sidebar.multiselect("Select Speciality:", specialities, default=specialities)
    else:
        specialities_category = st.sidebar.multiselect("Select Speciality:", specialities)

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
        (filtered_data['SurgicalPriority'].isin(selected_priorities)) &
        (filtered_data['Surgery Year'].isin(selected_years)) &
        (filtered_data['Roomdescription'].isin(selected_rooms)) &
        (filtered_data['ProcedureSpecialtyDescription'].isin(specialities_category if not all_specialities else specialities))
    ]

    filtered_data = filtered_data[
        (filtered_data['ScheduledDate'] >= pd.to_datetime(date_range[0])) & 
        (filtered_data['ScheduledDate'] <= pd.to_datetime(date_range[1]))
    ]

    return filtered_data

def calculate_employment_days(filtered_data):
    first_surgery_date = filtered_data['ScheduledDate'].min()
    last_surgery_date = filtered_data['ScheduledDate'].max()
    employment_days = (last_surgery_date - first_surgery_date).days + 1  # Adding 1 to include both start and end dates
    return employment_days

def app(data):
    filtered_data_surgeon = filter_data(data)
    st.title("Surgeon Drill Down")

    # Calculate employment days
    employment_days = calculate_employment_days(filtered_data_surgeon)
    filtered_data_surgeon['EmploymentDays'] = employment_days

    # Calculate average minutes of surgery per day of employment
    total_duration = filtered_data_surgeon['book_dur'].sum()
    filtered_data_surgeon['AvgMinutesPerDay'] = total_duration / employment_days if employment_days > 0 else 0

    # Display summary table for selected Surgeon ID
    summary_table = filtered_data_surgeon.groupby('surgeonID').agg(
        total_surgeries=pd.NamedAgg(column='EncounterID', aggfunc='count'),
        total_duration=pd.NamedAgg(column='book_dur', aggfunc='sum'),
        average_duration=pd.NamedAgg(column='book_dur', aggfunc='mean'),
        employment_days=pd.NamedAgg(column='EmploymentDays', aggfunc='first'),
        avg_minutes_per_day=pd.NamedAgg(column='AvgMinutesPerDay', aggfunc='first')
    ).reset_index()
    st.write("### Summary Table for Selected Surgeon ID")
    st.dataframe(summary_table)

    # Display specialties for selected Surgeon ID
    specialties_table = filtered_data_surgeon['ProcedureSpecialtyDescription'].value_counts().reset_index()
    specialties_table.columns = ['Specialty', 'Count']
    st.write("### Specialties for Selected Surgeon ID")
    st.dataframe(specialties_table)

    # Visualization of surgeries by day of the week
    st.write("### Surgeries per Day of the Week for Selected Surgeon ID")

    surgeries_per_day = filtered_data_surgeon['DayOfWeek'].value_counts().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']).fillna(0)

    fig, ax = plt.subplots(figsize=(10, 6))
    surgeries_per_day.plot(kind='bar', ax=ax)
    ax.set_title('Surgeries per Day of the Week for Selected Surgeon ID')
    ax.set_xlabel('Day of the Week')
    ax.set_ylabel('Number of Surgeries')
    plt.xticks(rotation=45)
    ax.grid(True)
    st.pyplot(fig)

    # Visualization of surgeries by room for the selected surgeon
    st.write("### Surgeries per Room for Selected Surgeon ID")

    surgeries_per_room = filtered_data_surgeon['Roomdescription'].value_counts()

    fig, ax = plt.subplots(figsize=(10, 6))
    surgeries_per_room.plot(kind='bar', ax=ax)
    ax.set_title('Surgeries per Room for Selected Surgeon ID')
    ax.set_xlabel('Room')
    ax.set_ylabel('Number of Surgeries')
    plt.xticks(rotation=45)
    ax.grid(True)
    st.pyplot(fig)

