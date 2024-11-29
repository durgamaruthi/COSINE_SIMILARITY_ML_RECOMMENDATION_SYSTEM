import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def load_data():
    grades_df = pd.read_excel('/Users/maruthiwork/Desktop/IMPORTANT NOTES/4TH_YEAR_CAPSTONE_PROJECT/RECSYS FULL CODE/dataset for ml recommendation system for elective.xlsx')
    courses_df = pd.read_excel('/Users/maruthiwork/Desktop/IMPORTANT NOTES/4TH_YEAR_CAPSTONE_PROJECT/RECSYS FULL CODE/course details.xlsx')
    print("Data loaded successfully.")
    return grades_df, courses_df

def preprocess_data(df):
    pivot_table = df.pivot_table(
        values='Marks (200)', 
        index='RollNumber', 
        columns='Course Code', 
        fill_value=0
    )
    return pivot_table

def compute_similarity(pivot_table):
    similarity_matrix = cosine_similarity(pivot_table)
    return similarity_matrix

def get_course_explanation(student_id, recommended_course, grades_df, courses_df):
    student_grade = grades_df[
        (grades_df['RollNumber'] == student_id)
    ]['Grade'].iloc[0]
    
    higher_performing_courses = grades_df[
        grades_df['Grade'].isin(['A', 'A+'])
    ]['Course Code'].unique()[:3]
    
    explanation = f"Course {recommended_course} recommended because:\n"
    explanation += f"- Your grade in CSE228 is {student_grade}\n"
    explanation += f"- Students with A/A+ grades are usually recommended these courses: {list(higher_performing_courses)}"
    
    return explanation

def recommend_courses(student_id, pivot_table, similarity_matrix, previous_recommendations=None, n_recommendations=10):
    if student_id not in pivot_table.index:
        return []
    
    student_index = pivot_table.index.get_loc(student_id)
    student_similarities = similarity_matrix[student_index]
    similar_students = student_similarities.argsort()[::-1][1:11]
    
    recommendations = {}
    for course in pivot_table.columns:
        if pivot_table.iloc[student_index][course] == 0:
            if previous_recommendations and course in previous_recommendations:
                continue
            course_scores = pivot_table.iloc[similar_students][course]
            recommendations[course] = course_scores.mean()
            
    top_recommendations = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)[:n_recommendations]
    return [course for course, score in top_recommendations]

def store_recommendations(student_id, recommendations):
    print(f"Storing recommendations for student {student_id}: {recommendations}")

def clear_recommendations():
    print("Clearing all stored recommendations for the session.")
