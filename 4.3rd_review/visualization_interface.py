import streamlit as st
import pandas as pd
import numpy as np
from sklearn.manifold import TSNE
import plotly.graph_objects as go
from database import get_all_enrollments
from recommendation_model import load_data, preprocess_data, compute_similarity, recommend_courses

def evaluate_recommendations(student_id, enrolled_courses, recommendations):
    hit_count = len(set(enrolled_courses) & set(recommendations))
    precision = hit_count / len(recommendations) if recommendations else 0
    recall = hit_count / len(enrolled_courses) if enrolled_courses else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    return precision, recall, f1_score

def create_tsne_visualization(grades_df, pivot_table, enrolled_students):
    enrolled_pivot = pivot_table[pivot_table.index.isin(enrolled_students)]
    X = enrolled_pivot.values
    
    tsne = TSNE(n_components=3, random_state=42)
    X_tsne = tsne.fit_transform(X)
    
    viz_df = pd.DataFrame({
        'x': X_tsne[:, 0],
        'y': X_tsne[:, 1],
        'z': X_tsne[:, 2],
        'Student_ID': enrolled_pivot.index,
        'Courses': [', '.join(grades_df[grades_df['RollNumber'] == sid]['Course Code'].tolist()) 
                   for sid in enrolled_pivot.index],
        'Average_Grade': [grades_df[grades_df['RollNumber'] == sid]['Grade Points'].mean() 
                         for sid in enrolled_pivot.index]
    })
    
    fig = go.Figure(data=[go.Scatter3d(
        x=viz_df['x'],
        y=viz_df['y'],
        z=viz_df['z'],
        mode='markers',
        marker=dict(
            size=8,
            color=viz_df['Average_Grade'],
            colorscale='Viridis',
            opacity=0.8,
            colorbar=dict(title="Average Grade Points")
        ),
        text=[f"Student: {sid}<br>Enrolled in: {courses}<br>Avg Grade: {grade:.2f}" 
              for sid, courses, grade in zip(viz_df['Student_ID'], 
                                          viz_df['Courses'], 
                                          viz_df['Average_Grade'])],
        hoverinfo='text'
    )])
    
    fig.update_layout(
        title=dict(
            text='Student Performance and Course Selection Analysis',
            y=0.95,
            x=0.5,
            xanchor='center',
            yanchor='top',
            font=dict(size=20)
        ),
        scene=dict(
            xaxis_title='Academic Performance Distribution',
            yaxis_title='Course Selection Similarity',
            zaxis_title='Grade Pattern Clustering',
            xaxis=dict(
                title_font=dict(size=12),
                tickfont=dict(size=10),
            ),
            yaxis=dict(
                title_font=dict(size=12),
                tickfont=dict(size=10),
            ),
            zaxis=dict(
                title_font=dict(size=12),
                tickfont=dict(size=10),
            ),
            camera=dict(
                up=dict(x=0, y=0, z=1),
                center=dict(x=0, y=0, z=0),
                eye=dict(x=1.5, y=1.5, z=1.5)
            )
        ),
        width=800,
        height=800,
        showlegend=False,
        annotations=[
            dict(
                text="X-axis: Distribution of academic performance across different courses",
                x=0, y=0, z=0,
                showarrow=False,
                font=dict(size=10),
                xshift=300,
                yshift=-300
            ),
            dict(
                text="Y-axis: Course selection patterns and student similarities",
                x=0, y=0, z=0,
                showarrow=False,
                font=dict(size=10),
                xshift=-300,
                yshift=-300
            ),
            dict(
                text="Z-axis: Grade patterns and course preference clusters",
                x=0, y=0, z=0,
                showarrow=False,
                font=dict(size=10),
                xshift=0,
                yshift=-300
            )
        ]
    )
    
    return fig

def main():
    st.title("Course Recommendation System Analytics")
    st.markdown("""
    This dashboard provides insights into the recommendation system's performance 
    and visualizes student enrollment patterns using t-SNE dimensionality reduction.
    """)

    grades_df, courses_df = load_data()
    pivot_table = preprocess_data(grades_df)
    similarity_matrix = compute_similarity(pivot_table)
    enrollments = get_all_enrollments()
    
    performance_data = []
    for student_id in enrollments['student_id'].unique():
        if student_id in pivot_table.index:
            enrolled_courses = enrollments[enrollments['student_id'] == student_id]['course_code'].tolist()
            recommendations = recommend_courses(student_id, pivot_table, similarity_matrix)
            precision, recall, f1_score = evaluate_recommendations(student_id, enrolled_courses, recommendations)
            performance_data.append({
                'student_id': student_id,
                'precision': precision,
                'recall': recall,
                'f1_score': f1_score
            })
    
    performance_df = pd.DataFrame(performance_data)
    
    if not performance_df.empty:
        st.subheader("Recommendation System Performance Metrics")
        col1, col2, col3 = st.columns(3)
        col1.metric("Average Precision", f"{performance_df['precision'].mean():.2f}")
        col2.metric("Average Recall", f"{performance_df['recall'].mean():.2f}")
        col3.metric("Average F1 Score", f"{performance_df['f1_score'].mean():.2f}")

        st.subheader("Interactive t-SNE Visualization")
        st.markdown("""
        This 3D visualization shows how students cluster based on their:
        - Academic performance
        - Course selection patterns
        - Grade distributions
        
        Hover over points to see detailed student information.
        """)
        enrolled_students = enrollments['student_id'].unique()
        fig_tsne = create_tsne_visualization(grades_df, pivot_table, enrolled_students)
        st.plotly_chart(fig_tsne)
        
        st.markdown("""
        **Visualization Guide:**
        - Points represent individual students
        - Color intensity indicates average grade points
        - Clustering shows similarities in academic patterns
        - Distance between points represents similarity in course choices
        """)
    else:
        st.info("Waiting for student enrollment data to generate visualizations.")

if __name__ == "__main__":
    main()
