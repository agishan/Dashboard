import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path)
    data['RoomEnterDateTime'] = pd.to_datetime(data['RoomEnterDateTime'], errors='coerce')
    data['RoomExitDateTime'] = pd.to_datetime(data['RoomExitDateTime'], errors='coerce')
    data['PacuStartdatetime'] = pd.to_datetime(data['PacuStartdatetime'], errors='coerce')
    data['PacuEnddatetime'] = pd.to_datetime(data['PacuEnddatetime'], errors='coerce')
    return data

@st.cache_data
def filter_data(data, start_date, end_date):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    filtered_data = data[
        (data['PacuEnddatetime'] >= start_date) & 
        (data['PacuEnddatetime'] <= end_date)
    ]
    return filtered_data

@st.cache_data
def calculate_counts(procedure_data, _time_range):
    counts = []
    for time in _time_range:
        count = procedure_data[(procedure_data['PacuStartdatetime'] <= time) & (procedure_data['PacuEnddatetime'] >= time)].shape[0]
        counts.append(count)
    return pd.DataFrame({'Time': _time_range, 'Count': counts})

@st.cache_data
def calculate_max_counts_per_day(time_data):
    time_data['Date'] = time_data['Time'].dt.date
    max_counts_per_day = time_data.groupby('Date')['Count'].max().reset_index()
    return max_counts_per_day

@st.cache_data
def calculate_weekly_counts(time_data):
    time_data['Week'] = time_data['Time'].dt.to_period('W').apply(lambda r: r.start_time + pd.Timedelta(days=6))
    weekly_counts = time_data.groupby('Week')['Count'].max().reset_index()
    return weekly_counts

def app(data):
    st.title("Surgery Recovery Times")

    # Select Date Range
    date_range = st.sidebar.date_input("Select Date Range:", [data['PacuEnddatetime'].min(), data['PacuEnddatetime'].max()])

    # Filter data based on selected criteria
    filtered_data = filter_data(data, date_range[0], date_range[1])

    # Calculate recovery times
    filtered_data['RecoveryTime'] = pd.to_datetime(filtered_data['PacuEnddatetime'], errors='coerce') - pd.to_datetime(filtered_data['PacuStartdatetime'], errors='coerce')
    filtered_data['RecoveryTimeMinutes'] = filtered_data['RecoveryTime'].dt.total_seconds() / 60
    
    # Remove NaN values
    filtered_data = filtered_data.dropna(subset=['RecoveryTimeMinutes'])

    procedure_data = filtered_data[(filtered_data['RecoveryTimeMinutes'] < (60 * 24)) & (filtered_data['RecoveryTimeMinutes'] > 0)]

    # Create a time range and calculate the number of patients in PACU
    time_range = pd.date_range(start=date_range[0], end=date_range[1], freq='H')
    time_data = calculate_counts(procedure_data, time_range)

    # Plot the number of patients in PACU over time using Plotly
    fig = px.line(time_data, x='Time', y='Count', title='Number of Patients in PACU Over Time')
    st.plotly_chart(fig)

    # Calculate and plot the highest count of patients in PACU per day
    max_counts_per_day = calculate_max_counts_per_day(time_data)
    fig_max_counts = px.bar(max_counts_per_day, x='Date', y='Count', title='Highest Count of Patients in PACU Per Day')
    st.plotly_chart(fig_max_counts)

    # Calculate and plot the weekly counts of patients in PACU
    weekly_counts = calculate_weekly_counts(time_data)
    fig_weekly_counts = px.bar(weekly_counts, x='Week', y='Count', title='Weekly Highest Count of Patients in PACU')
    st.plotly_chart(fig_weekly_counts)

    # Single Day Selection
    selected_day = st.date_input("Select a Day to View:", value=date_range[0])
    lookahead = st.radio("Lookahead Duration:", options=["1 day", "7 days"])
    lookahead_days = 2 if lookahead == "1 day" else 7
    selected_start = pd.to_datetime(selected_day)
    selected_end = selected_start + pd.Timedelta(days=lookahead_days - 1)

    # Filter data for the selected week
    selected_week_data = filter_data(data, selected_start, selected_end)
    selected_time_range = pd.date_range(start=selected_start, end=selected_end, freq='H')
    selected_time_data = calculate_counts(selected_week_data, selected_time_range)

    # Plot the number of patients in PACU for the selected week
    fig_selected_week = px.line(selected_time_data, x='Time', y='Count', title=f'Number of Patients in PACU from {selected_start.date()} to {selected_end.date()}')
    st.plotly_chart(fig_selected_week)

    # Reorder columns
    cols_to_front = [
        'PacuStartdatetime', 'PacuEnddatetime', 'ProcedureSpecialtyDescription', 
        'SurgicalPriority', 'SurgicalPriorityDescription', 'ProcedureMnemonic'
    ]
    selected_week_data = selected_week_data[cols_to_front + [col for col in selected_week_data.columns if col not in cols_to_front]]

    # Display table of filtered data for the selected week
    st.write(f"Filtered Data from {selected_start.date()} to {selected_end.date()}")
    st.dataframe(selected_week_data)
