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

from PAC_U import app as pacu_app
from PAC_U_overview import app as pacu_overview_app
from PAC_U_count import app as pacu_count_app

# Load the dataset
file_path = 'CMH-2019-04-01-2024-04-01.csv'
file_path_2 = 'PACU_DATA.csv'

@st.cache_data
def get_data(path) -> pd.DataFrame:
    try:
        # Attempt to read the file from deployment path
        data = pd.read_csv(path)
    except Exception as e:
        # Fallback to GitHub local path
        data = pd.read_csv(r'C:\Users\agish\Documents\GitHub\CMH-DataSharing\CMH-2019-04-01-2024-04-01.csv')
    return data

@st.cache_data
def get_pacu_data(path) -> pd.DataFrame:
    try:
        # Attempt to read the PACU file from deployment path
        data_pacu = pd.read_csv(path)
    except Exception as e:
        # Fallback to GitHub local path for the PACU file
        data_pacu = pd.read_csv(r'C:\Users\agish\Documents\GitHub\CMH Dashboard\EDAs\PACU_DATA.csv')
    return data_pacu

@st.cache_data
def preprocess_data(data: pd.DataFrame) -> pd.DataFrame:
    # Convert relevant columns to datetime
    datetime_columns_main = [
        'ScheduledDate', 'SurgeryDate', 'ScheduledDateTime', 
        'RoomEnterDateTime', 'RoomExitDateTime'
    ]
    
    for col in datetime_columns_main:
        data[col] = pd.to_datetime(data[col], errors='coerce')

    # Extract date parts for 'SurgeryDate'
    data['Surgery Year'] = data['SurgeryDate'].dt.year
    data['Surgery Month'] = data['SurgeryDate'].dt.month
    data['Surgery Day of The Month'] = data['SurgeryDate'].dt.day
    data['Surgery Day of The Week'] = data['SurgeryDate'].dt.day_name()
    data['DayOfWeek'] = data['ScheduledDate'].dt.day_name()
    
    return data

@st.cache_data
def preprocess_pacu_data(data_pacu: pd.DataFrame) -> pd.DataFrame:
    datetime_columns_pacu = [
        'RoomEnterDateTime', 'RoomExitDateTime', 'SurgeryDate', 
        'PacuStartdatetime', 'PacuEnddatetime', 'PacuReadyDischargeDateTime', 
        'DecisiontoTreatDatetime'
    ]
    
    for col in datetime_columns_pacu:
        data_pacu[col] = pd.to_datetime(data_pacu[col], errors='coerce')
    
    return data_pacu

data = preprocess_data(get_data(file_path))
data_pacu = preprocess_pacu_data(get_pacu_data(file_path_2))

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
    "Post Anasthesia Unit Overview": pacu_overview_app,
    "Post Anasthesia Unit": pacu_app,
    "PAC U Utlization":pacu_count_app,
    
}

st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))

page = PAGES[selection]

if selection in ['Post Anasthesia Unit',"Post Anasthesia Unit Overview","PAC U Utlization"]:
    page(data_pacu)
else:
    page(data)

