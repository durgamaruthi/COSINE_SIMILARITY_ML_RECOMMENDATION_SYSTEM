# Elective Course Recommendation System - Presidency University

## Overview
An ML recommendation system designed to assist Presidency University students in selecting elective courses based on their academic performance, preferences, and real-time seat availability. The system features dynamic interfaces for students, HODs, and faculty members, providing a streamlined experience for course recommendations and management.

## Objectives
- Provide personalized course recommendations using collaborative filtering
- Manage real-time seat allocation and enrollment
- Offer distinct interfaces for students, HODs, and faculty
- Enable data-driven decision making for course selection
- Maintain system scalability and concurrent user access

## Key Features
- Real-time dynamic recommendation engine
- Multi-user role-based access
- Automated seat management
- Interactive data visualizations
- Export functionality for enrollment data

## Technology Stack
- Python 3.8+
- Streamlit for web interface
- SQLite3 for database management
- Scikit-learn for recommendation engine
- Plotly for data visualization

## Dataset Information
The system uses a structured dataset (`main.xlsx`) containing:
- Approximately 10,600 student records
- 24 unique course codes
- Features: RollNumber, Course Code, Marks (200), Grade, Grade Points

Available Course Codes:
CSE228, CSE3114, CSE3005, CSE3115, CSE3014, CSE3112, CSE243, CSE3111, CSE6002, BCA217, CSA3020, CSE3113, CSE3134, CSE3001, CSE3036, CSE5006, CSE3106, CSE2037, CSE2039, MAT1002, CSE3152, CSE2060, CSE2015, CSE3087

## Project Structure
elective_system/ │ ├── .streamlit/ │ └── config.toml # Streamlit configuration │ ├── database.py # Database operations ├── recsys.py # Recommendation engine ├── student.py # Student interface ├── hod.py # HOD interface ├── faculty.py # Faculty interface ├── main.xlsx # Dataset └── requirements.txt # Dependencies

## Setup Instructions

1. Create and activate virtual environment:
```bash
python -m venv elective_venv
source elective_venv/bin/activate  # Unix/MacOS
elective_venv\Scripts\activate     # Windows
```

2.Install required packages:
```bash
pip install streamlit pandas numpy scikit-learn plotly openpyxl
```

3.Configure Streamlit theme: Create .streamlit/config.toml:
[theme]
primaryColor="#FF4081"
backgroundColor="#E8F5E9"
secondaryBackgroundColor="#B9F6CA"
textColor="#000000"

## Running the Application
1.Start Student Portal:
```
streamlit run student.py
```
2.Start HOD Portal:
```
streamlit run hod.py
```
3.Start Faculty Portal:
```
streamlit run faculty.py
```

## Module Descriptions

## database.py
Manages SQLite database operations
Handles course and enrollment data
Controls seat allocation
Provides data consistency
## recsys.py
Implements collaborative filtering
Processes student performance data
Generates course recommendations
Ensures dynamic computation

## student.py
Displays personalized recommendations
Manages course enrollment
Shows real-time seat availability
Maintains session state

## hod.py
Controls course capacity
Monitors enrollment statistics
Provides data visualization
Enables administrative actions

## faculty.py
Tracks student enrollments
Generates course reports
Exports enrollment data
Visualizes course statistics

## User Workflows

## Student Flow
Enter roll number
View personalized recommendations
Check seat availability
Enroll in courses
Receive confirmation

## HOD Flow
Monitor course enrollments
Adjust seat capacity
View enrollment statistics
Manage course data
Export reports

## Faculty Flow
Select courses to monitor
View enrolled students
Search specific enrollments
Download course reports
Track seat availability

## Technical Considerations

## Performance
Real-time recommendation computation
Optimized database queries
Efficient session management
Concurrent user handling

## Security
Hashed student identifiers
Thread-safe database operations
Role-based access control
Session state management

## Scalability
Modular code structure
Independent interfaces
Extensible database schema
Configurable parameters

## Constraints and Limitations
Real-time updates may have slight delay
Recommendations based on available historical data
System requires active internet connection

## License

This project is licensed under the MIT License - see the LICENSE file for details.
