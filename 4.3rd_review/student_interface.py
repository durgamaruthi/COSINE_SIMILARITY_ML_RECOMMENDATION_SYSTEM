import streamlit as st
import pandas as pd
from datetime import date
from recommendation_model import (
    load_data, 
    preprocess_data, 
    compute_similarity, 
    recommend_courses,
    get_course_explanation,
    store_recommendations,
    clear_recommendations
)
from database import (
    init_db, 
    get_course_enrollment, 
    get_course_capacity,
    enroll_student,
    is_student_enrolled,
    get_student_enrollments
)

def main():
    st.title("Elective Course Recommendation System")
    
    init_db()
    
    # Load data using the updated load_data function
    grades_df, courses_df = load_data()
    
    pivot_table = preprocess_data(grades_df)
    similarity_matrix = compute_similarity(pivot_table)
    
    student_id = st.text_input("Enter your Roll Number:")
    
    if student_id:
        # Check if already enrolled
        current_enrollments = get_student_enrollments(student_id)
        if current_enrollments:
            st.warning(f"You have already enrolled in course(s): {', '.join(current_enrollments)}")
            return
            
        if student_id in pivot_table.index:
            st.success(f"Welcome, Student {student_id}!")
            
            recommendations = recommend_courses(
                student_id, 
                pivot_table, 
                similarity_matrix,
                n_recommendations=10  # Changed to 10 recommendations
            )
            
            store_recommendations(student_id, recommendations)
            
            st.subheader("Recommended Courses:")
            for course in recommendations:
                course_info = courses_df[courses_df['course_code'] == course].iloc[0]
                current_enrolled = get_course_enrollment(course)
                current_capacity = get_course_capacity(course)
                
                if current_enrolled < current_capacity:  # Check if course is not full
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.write(f"\nCourse Code: {course}")
                        st.write(f"Course Name: {course_info['course_name']}")
                        st.write(f"Description: {course_info['description']}")
                        st.write(f"Objective: {course_info['objective']}")
                        st.write(f"Instructors: {course_info['instructors']}")
                        
                        explanation = get_course_explanation(student_id, course, grades_df, courses_df)
                        st.info(explanation)
                    
                    with col2:
                        st.write(f"Available Seats: {current_capacity - current_enrolled}")
                        st.write(f"Student Feedback: {course_info['feedback']}")
                        
                        if st.button(f"Enroll in {course}"):
                            success = enroll_student(student_id, course, str(date.today()))
                            if success:
                                st.success(f"Successfully enrolled in {course}")
                                clear_recommendations()
                                st.balloons()
                                st.rerun()
                            else:
                                st.error("You are already enrolled in this course")
                else:
                    st.warning(f"Course {course} is full and not available for enrollment.")
                
                st.write("-" * 50)
        else:
            st.error("Invalid Roll Number. Please try again.")

if __name__ == "__main__":
    main()