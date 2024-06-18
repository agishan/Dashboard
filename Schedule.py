import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def filter_data(data):
    # Parse date and time columns and handle errors
    data['ScheduledDateTime'] = pd.to_datetime(data['ScheduledDateTime'], errors='coerce')
    data['RoomEnterDateTime'] = pd.to_datetime(data['RoomEnterDateTime'], errors='coerce')
    data['RoomExitDateTime'] = pd.to_datetime(data['RoomExitDateTime'], errors='coerce')
    return data

def app(data):
    st.title("Surgical Rooms Gantt Chart")

    # Filtered data for Gantt chart
    filtered_data = filter_data(data)

    # Select a single day
    unique_dates = filtered_data['ScheduledDateTime'].dt.date.unique()
    selected_date = st.sidebar.date_input("Select Date", min_value=min(unique_dates), max_value=max(unique_dates))

    # Filter data for the selected date
    daily_data = filtered_data[filtered_data['ScheduledDateTime'].dt.date == pd.to_datetime(selected_date).date()]

    if daily_data.empty:
        st.write("No data available for the selected date.")
        return

    # Convert times to hours for the Gantt chart
    daily_data['StartHour'] = daily_data['RoomEnterDateTime'].dt.hour + daily_data['RoomEnterDateTime'].dt.minute / 60
    daily_data['EndHour'] = daily_data['RoomExitDateTime'].dt.hour + daily_data['RoomExitDateTime'].dt.minute / 60
    daily_data['Duration'] = (daily_data['RoomExitDateTime'] - daily_data['RoomEnterDateTime']).dt.total_seconds() / 3600  # Duration in hours

    # Prepare data for Gantt chart
    gantt_data = daily_data[['EncounterID', 'ProcedureSpecialtyDescription', 'Roomdescription', 'StartHour', 'EndHour', 'surgeonID']]
    gantt_data = gantt_data.rename(columns={'ProcedureSpecialtyDescription': 'Task', 'Roomdescription': 'Resource', 'StartHour': 'Start', 'EndHour': 'Finish'})

    # Create Gantt chart using Plotly
    fig = go.Figure()

    unique_tasks = gantt_data['Task'].unique()
    colors = px.colors.qualitative.Plotly[:len(unique_tasks)]

    task_color_map = {task: colors[i] for i, task in enumerate(unique_tasks)}

    for i, row in gantt_data.iterrows():
        fig.add_trace(go.Bar(
            x=[row['Finish'] - row['Start']],
            y=[row['Resource']],
            base=row['Start'],
            orientation='h',
            name=row['Task'],
            hoverinfo='text',
            hovertext=f"Task: {row['Task']}<br>Surgeon ID: {row['surgeonID']}<br>Encounter ID: {row['EncounterID']}<br>Start: {row['Start']}<br>Finish: {row['Finish']}",
            marker=dict(color=task_color_map[row['Task']])
        ))

    fig.update_layout(
        title='Gantt Chart of Surgical Rooms',
        xaxis=dict(
            title='Time (Hours)',
            tickmode='linear',
            tick0=0,
            dtick=1,
            range=[0, 24]
        ),
        yaxis=dict(
            title='Rooms',
            type='category'
        ),
        barmode='stack',
        showlegend=True
    )

    st.plotly_chart(fig)

    # Display separate schedule tables for each room
    rooms = daily_data['Roomdescription'].unique()
    for room in rooms:
        st.write(f"### Schedule for Room: {room}")
        room_data = daily_data[daily_data['Roomdescription'] == room]
        # Reorder columns to ensure the first three columns are RoomEnterDateTime, RoomExitDateTime, and ProcedureSpecialtyDescription
        column_order = ['RoomEnterDateTime', 'RoomExitDateTime', 'ProcedureSpecialtyDescription'] + [col for col in room_data.columns if col not in ['RoomEnterDateTime', 'RoomExitDateTime', 'ProcedureSpecialtyDescription']]
        room_data = room_data[column_order]
        st.dataframe(room_data)

    # Summary table showing count, sum, and average duration of surgeries in each room
    summary = daily_data.groupby('Roomdescription').agg(
        SurgeryCount=('EncounterID', 'count'),
        TotalDuration=('Duration', 'sum'),
        AverageDuration=('Duration', 'mean')
    ).reset_index()

    st.write("### Summary of Surgeries in Each Room")
    st.dataframe(summary)
