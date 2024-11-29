import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from database import (
    get_all_enrollments, 
    delete_enrollment, 
    delete_all_enrollments_for_course,
    update_course_capacity,
    get_course_capacity
)

def main():
    st.title("HOD Course Enrollment Dashboard")

    # Predefined list of all courses
    all_courses = [
        'CSE228', 'CSE3114', 'CSE3005', 'CSE3115', 'CSE3014', 
        'CSE3112', 'CSE243', 'CSE3111', 'CSE6002', 'BCA217',
        'CSA3020', 'CSE3113', 'CSE3134', 'CSE3001', 'CSE3036',
        'CSE5006', 'CSE3106', 'CSE2037', 'CSE2039', 'MAT1002',
        'CSE3152', 'CSE2060', 'CSE2015', 'CSE3087'
    ]

    # Fetch enrollments
    enrollments = get_all_enrollments()

    # Enrollment Visualization
    st.subheader("Course Enrollment Visualization")
    fig, ax = plt.subplots(figsize=(15, 7))
    
    # Ensure all courses are represented, even with zero enrollments
    course_data = enrollments['course_code'].value_counts().reindex(all_courses, fill_value=0)
    
    sns.barplot(x=course_data.index, y=course_data.values, ax=ax)
    ax.set_xlabel("Course Code")
    ax.set_ylabel("Number of Enrolled Students")
    ax.set_title("Course Enrollment")
    plt.xticks(rotation=90, ha='right')
    st.pyplot(fig)

    # Enrollment Percentage Visualization
    st.subheader("Course Enrollment Percentage")
    course_data = pd.DataFrame({
        'course_code': all_courses,
        'enrolled': [course_data.get(course, 0) for course in all_courses],
        'capacity': [get_course_capacity(course) for course in all_courses]
    })
    
    course_data['enrollment_percentage'] = course_data['enrolled'] / course_data['capacity'] * 100
    fig, ax = plt.subplots(figsize=(15, 7))
    sns.barplot(x='course_code', y='enrollment_percentage', data=course_data, ax=ax)
    ax.set_xlabel("Course Code")
    ax.set_ylabel("Enrollment Percentage")
    ax.set_title("Course Enrollment Percentage")
    plt.xticks(rotation=90, ha='right')
    ax.set_ylim(0, 100)
    for i, v in enumerate(course_data['enrollment_percentage']):
        ax.text(i, v + 1, f'{v:.1f}%', ha='center', va='bottom', rotation=90)
    st.pyplot(fig)

    # Course Management Section
    st.subheader("Course Management")
    for course in all_courses:
        st.write(f"\nCourse: {course}")
        
        # Seat Management
        current_capacity = get_course_capacity(course)
        col1, col2 = st.columns([2, 1])
        
        with col1:
            new_capacity = st.number_input(
                f"Modify seat allocation for {course} (Current: {current_capacity})",
                min_value=1,
                value=current_capacity,
                key=f"capacity_{course}"
            )
        
        with col2:
            if st.button(f"Update Seats for {course}"):
                update_course_capacity(course, new_capacity)
                st.success(f"Updated seat capacity for {course} to {new_capacity}")
                st.rerun()
        
        # Enrollment Management
        course_enrollments = enrollments[enrollments['course_code'] == course]
        search_term = st.text_input(f"Search Roll Number in {course}", key=f"search_{course}")

        if search_term:
            course_enrollments = course_enrollments[
                course_enrollments['student_id'].str.contains(search_term, case=False)
            ]

        if not course_enrollments.empty:
            for _, enrollment in course_enrollments.iterrows():
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.write(f"Student: {enrollment['student_id']}")
                with col2:
                    st.write(f"Enrolled on: {enrollment['enrollment_date']}")
                with col3:
                    if st.button(f"Delete", key=f"{course}_{enrollment['student_id']}"):
                        delete_enrollment(enrollment['student_id'], course)
                        st.success(f"Deleted enrollment of {enrollment['student_id']}")
                        st.rerun()
            
            if st.button(f"Delete All Enrollments for {course}"):
                delete_all_enrollments_for_course(course)
                st.success(f"All enrollments for {course} deleted")
                st.rerun()
        else:
            st.write(f"No enrollments found for {course}")

        if st.button(f"Download CSV for {course}"):
            csv = course_enrollments.to_csv(index=False)
            st.download_button(
                label=f"Download {course} enrollments",
                data=csv,
                file_name=f"{course}_enrollments.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main()