import streamlit as st
import pandas as pd
import plotly.express as px

def filter_data(data, speciality):
    return data[data['ProcedureSpecialtyDescription'] == speciality]

def app(data):
    st.title("Surgery Recovery Times")

    # Sidebar filters
    st.sidebar.title("Filters")
    
    # Select Speciality
    specialities = sorted(data['ProcedureSpecialtyDescription'].unique().tolist())
    selected_speciality = st.sidebar.selectbox("Select Speciality:", specialities)
    
    # Filter data based on selected specialty
    filtered_data = filter_data(data, selected_speciality)

    # Calculate recovery times
    filtered_data['RecoveryTime'] = pd.to_datetime(filtered_data['PacuReadyDischargeDateTime'], errors='coerce') - pd.to_datetime(filtered_data['RoomExitDateTime'], errors='coerce')
    filtered_data['RecoveryTimeMinutes'] = filtered_data['RecoveryTime'].dt.total_seconds() / 60
    
    # Remove NaN values
    filtered_data = filtered_data.dropna(subset=['RecoveryTimeMinutes'])

    # Plot recovery times
    fig = px.box(filtered_data, x='ProcedureDescription', y='RecoveryTimeMinutes', title=f'Recovery Times for {selected_speciality}')
    st.plotly_chart(fig)

    # Summary statistics table for each surgery
    summary_stats = filtered_data.groupby('ProcedureDescription')['RecoveryTimeMinutes'].describe().reset_index()
    summary_stats.columns = ['Procedure', 'Count', 'Mean', 'Std', 'Min', '25%', '50%', '75%', 'Max']
    st.write(f"Summary Statistics for Recovery Times in {selected_speciality}")
    st.dataframe(summary_stats)

    # Allow users to drill down into specific procedures
    selected_procedure = st.selectbox("Select Procedure:", filtered_data['ProcedureDescription'].unique())
    procedure_data = filtered_data[filtered_data['ProcedureDescription'] == selected_procedure]

    # Plot recovery times for the selected procedure
    fig = px.histogram(procedure_data, x='RecoveryTimeMinutes', nbins=50, title=f'Recovery Times for {selected_procedure}')
    st.plotly_chart(fig)

    # Display table of counts and average recovery times
    summary_table = procedure_data.groupby('ProcedureDescription').agg(
        count=('ProcedureDescription', 'size'),
        average_recovery_time=('RecoveryTimeMinutes', 'mean')
    ).reset_index()
    st.dataframe(summary_table)