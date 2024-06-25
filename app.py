import streamlit as st
import pandas as pd

from Home import app as home_app
from DemandOverview import app as demand_overview_app
from SurgeonOverview import app as surgeon_overview_app
from SurgeonDrillDown import app as surgeon_drill_down_app
from RoomUtilzation import app as room_utlization_app
from RoomDrillDown import app as room_drill_down_app
from Duration import app as duration_app
from DurationDrillDown import app as duration_drilldown_app
from Schedule import app as schedule_app
from ScheduleWeek import app as schedule__week_app


# Load the dataset
file_path = 'CMH-2019-04-01-2024-04-01.csv'

@st.cache_data
def get_data(path) -> pd.DataFrame:
    try:
    # Deployment path
        data = pd.read_csv(file_path)
    except Exception as e:
    # GitHub Local
        data = pd.read_csv(r'C:\Users\agish\Documents\GitHub\CMH-DataSharing\CMH-2019-04-01-2024-04-01.csv')
    return data
    

data = get_data(file_path)

#Need to cache and store these conversions to increase speed
data['ScheduledDate'] = pd.to_datetime(data['ScheduledDate'])
data['SurgeryDate'] = pd.to_datetime(data['SurgeryDate'])
data['Surgery Year'] = data['SurgeryDate'].dt.year
data['Surgery Month'] = data['SurgeryDate'].dt.month
data['Surgery Day of The Month'] = data['SurgeryDate'].dt.day
data['Surgery Day of The Week'] = data['SurgeryDate'].dt.day_name()
data['ScheduledDateTime'] = pd.to_datetime(data['ScheduledDateTime'], errors='coerce')
data['RoomEnterDateTime'] = pd.to_datetime(data['RoomEnterDateTime'], errors='coerce')
data['RoomExitDateTime'] = pd.to_datetime(data['RoomExitDateTime'], errors='coerce')
data['DayOfWeek'] = data['ScheduledDate'].dt.day_name()

PAGES = {
    "Home": home_app,
    "Demand Overview": demand_overview_app,
    "Surgeon Overview": surgeon_overview_app,
    "Surgeon Drill Down": surgeon_drill_down_app,
    "Room Usage": room_utlization_app,
    "Room Drill Down": room_drill_down_app,
    'Duration Analysis': duration_app,
    "Duration Drill Down": duration_drilldown_app,
    "Schedule": schedule_app,
    "Weekly Schedule": schedule__week_app,
    
}

st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))

page = PAGES[selection]
page(data)

