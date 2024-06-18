# Surgical Unit Dashboard Documentation

## 1. Introduction
The Surgical Unit Dashboard is a visualization & drill-down tool designed to provide insights into various metrics and performance indicators for the surgical unit at Cambridge Memorial Hospital. This dashboard is intended for use by researchers at the University of Waterloo.

## 2. Accessing the Dashboard
To access the Surgical Unit Dashboard, follow these steps:
- Clone the repository from the GitHub link provided.
- Ensure you have the required dependencies installed (Streamlit, Python, Pandas, Matplotlib, Plotly).
- Open the `app.py` file and update the `file_path` variable to point to the correct location of the CSV data file(s) on your local machine.
- Streamlit run `filepath/app.py` file to launch the dashboard locally.
- Open a web browser and navigate to the specified local URL 

## 3. Dashboard Layout and Navigation
The Surgical Unit Dashboard is divided into five main views, each accessible through the navigation menu on the left side of the screen. Users can switch between views by clicking on the corresponding menu item.

## 4. View Descriptions
### 4.1 Demand Overview
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

### 4.2 Surgeon Overview
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

### 4.3 Surgeon Drill Down
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

### 4.4 Room Usage
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

### 4.5 Room Drill Down
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

## 5. Common Filters and Interactions
- **Date Range Filter:** All views include a date range filter, allowing users to specify the time period for which they want to analyze the data.
- **Export Data:** TO BE ADDED

## 6. Troubleshooting and FAQs
- **Error: Unable to locate CSV file:** Ensure that the `file_path` variable in the `app.py` file is correctly set to the location of your CSV data file(s).
- **Data not updating after changing filters:** Try refreshing the page or restarting the dashboard applications
- 