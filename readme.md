# Dashboard Documentation
This documentation provides a comprehensive guide to understanding and using the Dashboard. It explains the data filtering options, metrics calculations, and visualizations available in each dashboard.

## Accessing the Dashboard
To access the Surgical Unit Dashboard, follow these steps:
- Clone the repository from the GitHub link provided.
- Ensure you have the required dependencies installed (Streamlit, Python, Pandas, Matplotlib, Plotly).
- Open the `app.py` file and update the `file_path` variable to point to the correct location of the CSV data file on your local machine.
- via the terminal 'streamlit run `filepath/app.py`' to launch the dashboard locally.
- Dashboard should open automatically otherwise open a web browser and navigate to the specified local URL 

## Table of Contents

- [Dashboard Documentation](#dashboard-documentation)
  - [Accessing the Dashboard](#accessing-the-dashboard)
  - [Table of Contents](#table-of-contents)
  - [Demand Overview Dashboard](#demand-overview-dashboard)
    - [Filtering Options](#filtering-options)
    - [Metrics Calculations](#metrics-calculations)
    - [Visualizations](#visualizations)
  - [Surgeon Overview Dashboard](#surgeon-overview-dashboard)
    - [Filtering Options](#filtering-options-1)
    - [Metrics Calculations](#metrics-calculations-1)
    - [Visualizations](#visualizations-1)
  - [Surgeon Drill Down Dashboard](#surgeon-drill-down-dashboard)
    - [Filtering Options](#filtering-options-2)
    - [Metrics Calculations](#metrics-calculations-2)
    - [Visualizations](#visualizations-2)
  - [Room Utilization Dashboard](#room-utilization-dashboard)
    - [Filtering Options](#filtering-options-3)
    - [Metrics Calculations](#metrics-calculations-3)
    - [Visualizations](#visualizations-3)
  - [Room Drill Down Dashboard](#room-drill-down-dashboard)
    - [Filtering Options](#filtering-options-4)
    - [Metrics Calculations](#metrics-calculations-4)
    - [Visualizations](#visualizations-4)
  - [Duration Analysis](#duration-analysis)
    - [Filtering Options](#filtering-options-5)
    - [Metrics Calculations](#metrics-calculations-5)
    - [Visualizations](#visualizations-5)
  - [Duration Drill Down Dashboard](#duration-drill-down-dashboard)
    - [Filtering Options](#filtering-options-6)
    - [Metrics Calculations](#metrics-calculations-6)
    - [Visualizations](#visualizations-6)
  - [Schedule Page Dashboard](#schedule-page-dashboard)
    - [Filtering Options](#filtering-options-7)
    - [Metrics Calculations](#metrics-calculations-7)
    - [Visualizations](#visualizations-7)


## Demand Overview Dashboard

### Filtering Options


The sidebar provides various filtering options to customize the data view:

1. **Procedure Speciality**: Select the specific procedure specialties to include in the analysis.
2. **Surgical Priority**: Choose the surgical priorities to filter the data.
3. **Date Range**: Specify the date range for the surgeries.
4. **Years**: Select the years to include in the analysis.
5. **Rooms**: Choose the rooms where surgeries were performed.
6. **Surgeon IDs**: Select the surgeon IDs to filter the data.

These filters allow you to narrow down the data to specific subsets, making it easier to focus on particular aspects of the surgical demand.

### Metrics Calculations

1. **Surgeries Over Time**
   - **Grouping**: The data is grouped by the `ScheduledDate`.
   - **Missing Dates**: Any missing dates within the specified range are filled with zero surgeries to ensure continuity in the time series.

2. **Summary Table**
   - **Procedure Specialties**: A summary table is generated showing the count of surgeries and the average duration of surgeries for each procedure specialty.
   - **Count**: The total number of surgeries performed for each specialty.
   - **Average Duration**: The mean duration of surgeries for each specialty.

3. **Average Number of Surgeries per Day of the Week**
   - **Calculation**: The total number of surgeries performed on each day of the week is divided by the number of weeks in the selected date range.
   - **Normalization**: This provides an average number of surgeries per day of the week, accounting for the variation in the number of weeks.

4. **Total Duration of Surgeries per Day of the Week**
   - **Summation**: The total duration of all surgeries performed on each day of the week is calculated.
   - **Comparison**: This helps to understand which days have the highest surgical load in terms of time.

5. **Count of Surgeries per Room**
   - **Room-wise Distribution**: The number of surgeries performed in each room is counted.
   - **Insights**: This metric helps identify the utilization of different rooms.

6. **Total Booked Duration of Surgeries per Room**
   - **Summation**: The total duration of surgeries booked in each room is summed up.
   - **Utilization**: Provides insights into which rooms are being used the most and their respective load.

### Visualizations

1. **Surgeries Over Time**
   - A line plot displays the number of surgeries performed over the selected date range, allowing users to identify trends and patterns in surgical demand over time.

2. **Average Number of Surgeries per Day of the Week**
   - A bar chart shows the average number of surgeries performed on each day of the week, highlighting the days with the highest and lowest surgical activity.

3. **Total Duration of Surgeries per Day of the Week**
   - A bar chart presents the total duration of surgeries for each day of the week, providing insights into the daily surgical load.

4. **Count of Surgeries per Room**
   - A bar chart illustrates the distribution of surgeries across different rooms, helping to understand room utilization.

5. **Total Booked Duration of Surgeries per Room**
   - A bar chart shows the total booked duration of surgeries for each room, indicating which rooms are used most intensively.

## Surgeon Overview Dashboard

### Filtering Options

The sidebar provides various filtering options to customize the data view:

1. **Procedure Speciality**: Select the specific procedure specialties to include in the analysis.
2. **Surgeon IDs**: Select the surgeon IDs to filter the data.
3. **Surgical Priority**: Choose the surgical priorities to filter the data.
4. **Date Range**: Specify the date range for the surgeries.
5. **Years**: Select the years to include in the analysis.
6. **Rooms**: Choose the rooms where surgeries were performed.

These filters allow you to narrow down the data to specific subsets, making it easier to focus on particular aspects of the surgeon's performance and surgical demand.

### Metrics Calculations

1. **Employment Days**
   - **Calculation**: The number of days between the first and last surgery performed by each surgeon.
   - **Purpose**: This metric helps to understand the active period of each surgeon within the selected date range.

2. **Average Minutes of Surgery per Day of Employment**
   - **Calculation**: The total duration of surgeries performed by each surgeon divided by the number of employment days.
   - **Purpose**: Provides insight into the average workload of each surgeon per day.

3. **Summary Table for Selected Surgeon IDs**
   - **Total Duration**: The total minutes of all surgeries performed by each surgeon.
   - **Total Surgeries**: The total count of surgeries performed by each surgeon.
   - **Average Duration**: The average duration of surgeries performed by each surgeon.
   - **Employment Days**: The total number of days between the first and last surgery for each surgeon.
   - **Average Minutes per Day**: The average number of minutes spent on surgeries per day of employment for each surgeon.

4. **Surgeries by Surgeon ID**
   - **Calculation**: The number of surgeries performed by each surgeon.
   - **Purpose**: Helps to understand the distribution of surgical workload among surgeons.

5. **Average Duration of Surgeries per Surgeon ID**
   - **Calculation**: The mean duration of surgeries performed by each surgeon.
   - **Purpose**: Provides insight into the average time spent on each surgery by each surgeon.

6. **Surgeries per Room for Selected Surgeon IDs**
   - **Calculation**: The count of surgeries performed by each surgeon in each room.
   - **Purpose**: Helps to identify room utilization for each surgeon.

7. **Surgeries per Day of the Week for Selected Surgeon IDs**
   - **Calculation**: The count of surgeries performed by each surgeon on each day of the week.
   - **Purpose**: Provides insight into the distribution of surgeries across different days of the week for each surgeon.

### Visualizations

1. **Surgeries by Surgeon ID**
   - A bar chart displays the number of surgeries performed by each surgeon, allowing users to see the distribution of surgical workload among surgeons.

2. **Average Duration of Surgeries per Surgeon ID**
   - A bar chart shows the average duration of surgeries for each surgeon, providing insights into the average time spent on each surgery by different surgeons.

3. **Surgeries per Room for Selected Surgeon IDs**
   - A stacked bar chart illustrates the number of surgeries performed in each room by different surgeons. This helps to understand the utilization of different rooms by each surgeon.

4. **Surgeries per Day of the Week for Selected Surgeon IDs**
   - A stacked bar chart displays the number of surgeries performed on each day of the week for each surgeon, highlighting the distribution of surgeries across the week.

## Surgeon Drill Down Dashboard

### Filtering Options

The sidebar provides various filtering options to customize the data view:

1. **Surgeon IDs**: Select the surgeon IDs to filter the data.
2. **Procedure Speciality**: Select the specific procedure specialties to include in the analysis.
3. **Surgical Priority**: Choose the surgical priorities to filter the data.
4. **Date Range**: Specify the date range for the surgeries.
5. **Years**: Select the years to include in the analysis.
6. **Rooms**: Choose the rooms where surgeries were performed.

These filters allow you to narrow down the data to specific subsets, focusing on detailed performance metrics and surgical demand for individual surgeons.

### Metrics Calculations

1. **Employment Days**
   - **Calculation**: The number of days between the first and last surgery performed by the selected surgeon.
   - **Purpose**: This metric helps to understand the active period of the surgeon within the selected date range.

2. **Average Minutes of Surgery per Day of Employment**
   - **Calculation**: The total duration of surgeries performed by the selected surgeon divided by the number of employment days.
   - **Purpose**: Provides insight into the average workload of the surgeon per day.

3. **Summary Table for Selected Surgeon ID**
   - **Total Duration**: The total minutes of all surgeries performed by the selected surgeon.
   - **Total Surgeries**: The total count of surgeries performed by the selected surgeon.
   - **Average Duration**: The average duration of surgeries performed by the selected surgeon.
   - **Employment Days**: The total number of days between the first and last surgery for the selected surgeon.
   - **Average Minutes per Day**: The average number of minutes spent on surgeries per day of employment for the selected surgeon.

4. **Specialties for Selected Surgeon ID**
   - **Calculation**: The count of surgeries performed by the selected surgeon in each specialty.
   - **Purpose**: Helps to identify the distribution of surgeries across different specialties for the selected surgeon.

### Visualizations

1. **Surgeries per Day of the Week for Selected Surgeon ID**
   - A bar chart displays the number of surgeries performed on each day of the week for the selected surgeon, providing insights into weekly surgical patterns.

2. **Surgeries per Room for Selected Surgeon ID**
   - A bar chart shows the number of surgeries performed in each room by the selected surgeon, highlighting room utilization for the selected surgeon.



## Room Utilization Dashboard

### Filtering Options

The sidebar provides various filtering options to customize the data view:

1. **Date Range**: Specify the date range for the surgeries.
2. **Rooms**: Choose the rooms where surgeries were performed.

Additionally, there are options to remove weekends and Ontario civic holidays from the analysis.

### Metrics Calculations

1. **Total Days**
   - **Calculation**: The total number of days between the selected start and end dates.
   - **Adjustments**: Days are adjusted by subtracting weekends and civic holidays if those options are selected.

2. **Room Utilization Percentage**
   - **Total Available Minutes**: Calculated as the total days (taken from date range) multiplied by 8 hours per day and 60 minutes per hour.
   - **Utilization Percentage**: The total booked duration of surgeries in each room, divided by the total available minutes, and multiplied by 100 to get a percentage.

3. **Speciality Utilization Percentage**
   - **Calculation**: The booked duration for each specialty within each room as a percentage of the total booked duration for that room.

4. **Surgical Priority Utilization Percentage**
   - **Calculation**: The booked duration for each surgical priority within each room as a percentage of the total booked duration for that room.

### Visualizations

1. **Room Utilization Percentage by Speciality**
   - A stacked bar chart showing the percentage of room utilization by each specialty.

2. **Total Utilization Percentage by Room**
   - A display of the total utilization percentage for each room.

3. **Speciality Utilization as Percentage of Total Minutes Scheduled per Room**
   - A table showing the percentage of total minutes scheduled for each specialty in each room.

4. **Room Utilization Percentage by Surgical Priority**
   - A stacked bar chart showing the percentage of room utilization by each surgical priority.

5. **Surgical Priority Utilization as Percentage of Total Minutes Scheduled per Room**
   - A table showing the percentage of total minutes scheduled for each surgical priority in each room.


## Room Drill Down Dashboard

### Filtering Options

The sidebar provides various filtering options to customize the data view:

1. **Date Range**: Specify the date range for the surgeries.
2. **Room**: Select the specific room to analyze.

Additionally, there are options to remove weekends and Ontario civic holidays from the analysis.

### Metrics Calculations

1. **Distribution of Surgery Types**
   - **Calculation**: The count of each surgery type performed in the selected room.

2. **Distribution of Surgery Durations**
   - **Calculation**: The frequency distribution of surgery durations in the selected room.

3. **Utilization by Day of the Week**
   - **Calculation**: The total duration of surgeries performed on each day of the week in the selected room.

4. **Distribution of Surgeries by Surgeon ID**
   - **Calculation**: The count of surgeries performed by each surgeon in the selected room.

5. **Utilization by Surgeon ID**
   - **Calculation**: The total duration of surgeries performed by each surgeon in the selected room.

### Visualizations

1. **Distribution of Surgery Types**
   - A bar chart showing the count of each surgery type performed in the selected room.

2. **Distribution of Surgery Durations**
   - A histogram showing the frequency distribution of surgery durations in the selected room.

3. **Utilization by Day of the Week**
   - A bar chart showing the total duration of surgeries performed on each day of the week in the selected room.

4. **Distribution of Surgeries by Surgeon ID**
   - A bar chart showing the count of surgeries performed by each surgeon in the selected room.

5. **Utilization by Surgeon ID**
   - A bar chart showing the total duration of surgeries performed by each surgeon in the selected room.

## Duration Analysis

### Filtering Options

The sidebar provides various filtering options to customize the data view:

1. **Procedure Speciality**: Select the specific procedure specialties to include in the analysis.
2. **Surgical Priority**: Choose the surgical priorities to filter the data.
3. **Date Range**: Specify the date range for the surgeries.
4. **Years**: Select the years to include in the analysis.
5. **Rooms**: Choose the rooms where surgeries were performed.
6. **Surgeon IDs**: Select the surgeon IDs to filter the data.

### Metrics Calculations

1. **Entry Time Difference**
   - **Calculation**: The difference between the actual room entry time and the scheduled time.

2. **Actual Duration**
   - **Calculation**: The difference between the room exit time and the room entry time, converted to minutes.

3. **Duration Difference**
   - **Calculation**: The difference between the actual duration and the booked duration of the surgery.

4. **Summary Table**
   - **Metrics**: Count of surgeries, average booked duration, average real duration, and average delay for each procedure specialty.

### Visualizations

1. **Duration Difference by Room**
   - A bar chart showing the average duration difference for each room.

2. **Duration Difference by Surgical Specialty**
   - A bar chart showing the average duration difference for each surgical specialty.

3. **Duration Difference by Day of the Week**
   - A bar chart showing the average duration difference for each day of the week.

## Duration Drill Down Dashboard

### Filtering Options

The sidebar provides various filtering options to customize the data view:

1. **Procedure Speciality**: Select the specific procedure specialty to include in the analysis.
2. **Date Range**: Specify the date range for the surgeries.
3. **Surgical Priority**: Choose the surgical priorities to filter the data.
4. **Rooms**: Select the rooms where surgeries were performed.
5. **Surgeon IDs**: Select the surgeons to filter the data.
6. **Surgery Types**: Select the specific surgery types to include in the analysis.

### Metrics Calculations

1. **Entry Time Difference**
   - **Calculation**: The difference between the actual room entry time and the scheduled time.

2. **Actual Duration**
   - **Calculation**: The difference between the room exit time and the room entry time, converted to minutes.

3. **Duration Difference**
   - **Calculation**: The difference between the actual duration and the booked duration of the surgery.

4. **Summary Table**
   - **Metrics**: Count of surgeries, average booked duration, average real duration, and average delay for each procedure description.

### Visualizations

1. **Delay by Room**
   - A bar chart showing the average delay for each room.

2. **Delay by Surgery**
   - A bar chart showing the average delay for each surgery.

3. **Delay by Day of the Week**
   - A bar chart showing the average delay for each day of the week.

4. **Delay by Surgeon**
   - A bar chart showing the average delay for each surgeon.

## Schedule Page Dashboard

### Filtering Options

The sidebar provides various filtering options to customize the data view:

1. **Select Date**: Choose a specific date to view the surgical schedule.
2. **Rooms**: Display separate schedule tables for each room.

### Metrics Calculations

1. **Gantt Chart Data Preparation**
   - **Start Hour**: Convert room entry times to hours.
   - **End Hour**: Convert room exit times to hours.
   - **Duration**: Calculate the duration of each surgery in hours.

2. **Summary Table**
   - **Surgery Count**: The number of surgeries in each room.
   - **Total Duration**: The total duration of surgeries in each room.
   - **Average Duration**: The average duration of surgeries in each room.

### Visualizations

1. **Gantt Chart of Surgical Rooms**
   - A Gantt chart displaying the schedule of surgeries in different rooms for the selected date.

2. **Separate Schedule Tables for Each Room**
   - Tables displaying the schedule for each room, including columns for room entry time, room exit time, and procedure specialty description.

3. **Summary of Surgeries in Each Room**
   - A summary table showing the count, total duration, and average duration of surgeries in each room.

By following this documentation, users can effectively navigate and utilize the Schedule Page dashboard to gain valuable insights into the daily schedule of surgical rooms, visualize the timing and duration of surgeries, and analyze the distribution of surgical activities across different rooms.