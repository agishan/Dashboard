import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

def filter_data(data, specialities, start_date, end_date, selected_rooms):
    # Convert dates to datetime if they are not already
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    filtered_data = data[data['ProcedureSpecialtyDescription'].isin(specialities)]
    filtered_data = filtered_data[
        (filtered_data['PacuEnddatetime'] >= start_date) & 
        (filtered_data['PacuEnddatetime'] <= end_date) &
        (filtered_data['Roomdescription'].isin(selected_rooms))
    ]
    return filtered_data

def app(data):
    st.title("Surgery Recovery Times")

    # Sidebar filters
    st.sidebar.title("Filters")
    
    # Select Speciality
    specialities = sorted(data['ProcedureSpecialtyDescription'].unique().tolist())
    select_all = st.sidebar.checkbox("Select All Specialties")
    
    if select_all:
        selected_specialities = specialities
    else:
        selected_specialities = st.sidebar.multiselect("Select Specialities:", specialities, default=specialities)

    # Select Date Range
    date_range = st.sidebar.date_input("Select Date Range:", [data['PacuEnddatetime'].min(), data['PacuEnddatetime'].max()])
    
    # Select Rooms
    rooms = sorted(data['Roomdescription'].unique().tolist())
    selected_rooms = st.sidebar.multiselect("Select Rooms:", rooms, default=rooms)
    
    # Filter data based on selected criteria
    filtered_data = filter_data(data, selected_specialities, date_range[0], date_range[1], selected_rooms)

    # Calculate recovery times
    filtered_data['RecoveryTime'] = pd.to_datetime(filtered_data['PacuEnddatetime'], errors='coerce') - pd.to_datetime(filtered_data['PacuStartdatetime'], errors='coerce')
    filtered_data['RecoveryTimeMinutes'] = filtered_data['RecoveryTime'].dt.total_seconds() / 60
    
    # Remove NaN values
    filtered_data = filtered_data.dropna(subset=['RecoveryTimeMinutes'])

    procedure_data = filtered_data[(filtered_data['RecoveryTimeMinutes'] < (60 * 24)) & (filtered_data['RecoveryTimeMinutes'] > 0)]

    # Plot recovery times for the selected procedure
    fig = px.histogram(procedure_data, x='RecoveryTimeMinutes', nbins=5000, title='Recovery Times')
    st.plotly_chart(fig)

    # Display table of counts and average recovery times
    summary_table = procedure_data.groupby(['ProcedureDescription', 'Roomdescription']).agg(
        count=('ProcedureDescription', 'size'),
        average_recovery_time=('RecoveryTimeMinutes', 'mean')
    ).reset_index()
    st.dataframe(summary_table)

    # Extract month and year for aggregation
    procedure_data['Month_Year'] = procedure_data['PacuEnddatetime'].dt.to_period('M')

    # Group by Month_Year and calculate mean PACU_Duration
    monthly_avg_duration = procedure_data.groupby('Month_Year')['RecoveryTimeMinutes'].mean().reset_index()
    monthly_avg_duration = monthly_avg_duration.sort_values('Month_Year')
    monthly_avg_duration['Month_Year'] = monthly_avg_duration['Month_Year'].dt.to_timestamp()

    # st.dataframe(monthly_avg_duration)

    # Plot using Matplotlib
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(monthly_avg_duration['Month_Year'], monthly_avg_duration['RecoveryTimeMinutes'], marker='o')
    
    ax.set_title('Average PACU Duration by Month')
    ax.set_xlabel('Month-Year')
    ax.set_ylabel('Average Duration (minutes)')
    ax.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(rotation=45, ha='right')
    
    st.pyplot(fig)

    # Average PACU Duration by Room
    room_averages = procedure_data.groupby('Roomdescription')['RecoveryTimeMinutes'].mean().sort_values(ascending=False)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=room_averages.index, y=room_averages.values, ax=ax)
    
    ax.set_title('Average PACU Duration by Room', fontsize=16)
    ax.set_xlabel('Room Description', fontsize=12)
    ax.set_ylabel('Average Duration (minutes)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    
    # Add value labels on top of each bar
    for i, v in enumerate(room_averages.values):
        ax.text(i, v, f'{v:.2f}', ha='center', va='bottom')
    
    st.pyplot(fig)

