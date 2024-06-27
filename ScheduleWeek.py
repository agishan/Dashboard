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
    st.title("Surgical Rooms Weekly Gantt Chart")

    # Filtered data for Gantt chart
    filtered_data = filter_data(data)

    # Select a week
    unique_dates = filtered_data['ScheduledDateTime'].dt.date.unique()
    selected_date = st.sidebar.date_input("Select Start Date of the Week", min_value=min(unique_dates), max_value=max(unique_dates))

    # Get the start and end dates of the selected week
    start_date = pd.to_datetime(selected_date)
    end_date = start_date + pd.Timedelta(days=13)

    # Filter data for the selected week
    weekly_data = filtered_data[(filtered_data['ScheduledDateTime'].dt.date >= start_date.date()) & (filtered_data['ScheduledDateTime'].dt.date <= end_date.date())]

    if weekly_data.empty:
        st.write("No data available for the selected week.")
        return

    # Convert times to hours for the Gantt chart
    weekly_data['StartHour'] = weekly_data['RoomEnterDateTime'].dt.hour + weekly_data['RoomEnterDateTime'].dt.minute / 60
    weekly_data['EndHour'] = weekly_data['RoomExitDateTime'].dt.hour + weekly_data['RoomExitDateTime'].dt.minute / 60
    weekly_data['Duration'] = (weekly_data['RoomExitDateTime'] - weekly_data['RoomEnterDateTime']).dt.total_seconds() / 3600  # Duration in hours

    # Prepare data for Gantt chart
    weekly_data['DayOfWeek'] = weekly_data['ScheduledDateTime'].dt.day_name()
    weekly_data['DateOnly'] = weekly_data['ScheduledDateTime'].dt.date

    # Ensure rooms are sorted
    rooms = sorted(weekly_data['Roomdescription'].unique(), key=lambda x: (int(x.split()[1]) if x.split()[1].isdigit() else float('inf')))

    for room in rooms:
        st.write(f"### Schedule for Room: {room}")
        room_data = weekly_data[weekly_data['Roomdescription'] == room]
        room_data = room_data.sort_values(by='DateOnly')  # Sort days from earliest to latest
        gantt_data = room_data[['EncounterID', 'ProcedureSpecialtyDescription', 'DayOfWeek', 'DateOnly', 'StartHour', 'EndHour', 'surgeonID']]
        gantt_data = gantt_data.rename(columns={'ProcedureSpecialtyDescription': 'Task', 'DayOfWeek': 'Resource', 'StartHour': 'Start', 'EndHour': 'Finish'})

        # Create Gantt chart using Plotly
        fig = go.Figure()

        unique_tasks = gantt_data['Task'].unique()
        colors = px.colors.qualitative.Plotly[:len(unique_tasks)]

        task_color_map = {task: colors[i] for i, task in enumerate(unique_tasks)}

        for i, row in gantt_data.iterrows():
            fig.add_trace(go.Bar(
                x=[row['Finish'] - row['Start']],
                y=[row['DateOnly']],
                base=row['Start'],
                orientation='h',
                name=row['Task'],
                hoverinfo='text',
                hovertext=f"Task: {row['Task']}<br>Surgeon ID: {row['surgeonID']}<br>Encounter ID: {row['EncounterID']}<br>Start: {row['Start']}<br>Finish: {row['Finish']}",
                marker=dict(color=task_color_map[row['Task']])
            ))

        fig.update_layout(
            title=f'Gantt Chart for Room {room} from {start_date.date()} to {end_date.date()}',
            xaxis=dict(
                title='Time (Hours)',
                tickmode='linear',
                tick0=0,
                dtick=1,
                range=[0, 24]
            ),
            yaxis=dict(
                title='Date',
                type='category'
            ),
            barmode='stack',
            showlegend=True
        )

        st.plotly_chart(fig)

        # Display the schedule table for the room
        st.write(f"### Schedule Table for Room: {room}")
        schedule_table = room_data[['ScheduledDateTime', 'RoomEnterDateTime', 'RoomExitDateTime', 'ProcedureSpecialtyDescription', 'surgeonID', 'EncounterID']]
        st.dataframe(schedule_table)

    # Summary table showing count, sum, and average duration of surgeries in each room
    summary = weekly_data.groupby('Roomdescription').agg(
        SurgeryCount=('EncounterID', 'count'),
        TotalDuration=('Duration', 'sum'),
        AverageDuration=('Duration', 'mean')
    ).reset_index()

    st.write("### Summary of Surgeries in Each Room")
    st.dataframe(summary)
