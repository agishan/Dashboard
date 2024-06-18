import streamlit as st

def app(data):
    st.title("Surgery Scheduling Dashboard")
    st.markdown("""
### 1.1 Demand Overview
**Purpose:** This view provides an overview of the surgical demand, including the count of surgeries, duration, and distribution across various dimensions.
**Filters:**
- Specialty
- Priorities (1-5)
- Date Range
- Years
- Rooms
- Surgeon IDs
**Visualizations:**
- Count of surgeries over time
- Average number of surgeries per day of the week
- Total duration of surgeries per day of the week
- Count of surgeries per room
- Total booked duration of surgeries per room

### 1.2 Surgeon Overview
**Purpose:** Analyze the performance and workload of individual surgeons.
**Filters:**
- Specialty
- Priorities (1-5)
- Date Range
- Years
- Rooms
- Surgeon IDs
**Visualizations:**
- Surgeries by surgeon ID
- Average duration of surgeries per surgeon ID
- Surgeries per room for selected surgeon IDs
- Surgeries per day of the week for selected surgeon IDs

### 1.3 Surgeon Drill Down
**Purpose:** Dive deeper into the performance and workload of a specific surgeon.
**Filters:**
- Select single surgeon ID
- Select specialties
- Date range
- Rooms
**Tables:**
- Summary table for selected surgeon ID
- Specialties for selected surgeon ID
**Visualizations:**
- Surgeries per day of the week for selected surgeon ID
- Surgeries per room for selected surgeon ID

### 1.4 Room Usage
**Purpose:** Monitor the utilization of operating rooms and analyze the distribution of surgical priorities.
**Filters:**
- Select date range
- Select rooms
- Remove weekends
- Remove Ontario civic holidays
**Visualizations:**
- Room utilization percentage by specialty (based on 8 hours per day)
- Surgical priority utilization as a percentage of total minutes scheduled per room
**Table:**
- Total utilization percentage by room
- Specialty utilization as a percentage of total minutes scheduled per room

### 1.5 Room Drill Down
**Purpose:** Analyze the utilization and performance of a specific operating room.
**Filters:**
- Date range
- Select room
- Remove weekends
- Remove Ontario civic holidays
**Visualizations:**
- Count of surgeries by surgery types
- Histogram of surgery durations (in the room)
- Day of the week utilization (sum of minutes used)
- Counts per surgeon ID (in the room)
- Utilization by surgeon ID
                """)
