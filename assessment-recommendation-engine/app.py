import streamlit as st
import pandas as pd
import plotly.express as px

# Initialize session state
if 'show_recommendations' not in st.session_state:
    st.session_state.show_recommendations = False
if 'answers' not in st.session_state:
    st.session_state.answers = {}

# Page configuration
st.set_page_config(
    page_title="Career Path Finder",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://example.com/help',
        'Report a bug': "https://example.com/bug",
        'About': "# Career Path Finder\nFind your ideal learning path based on your skills and interests!"
    }
)

# Custom CSS
st.markdown("""
<style>
    /* Base Styles */
    .main {
        padding: 2rem 1rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* Typography */
    h1 {
        color: #2c3e50;
        font-weight: 700;
        margin-bottom: 1.5rem;
        font-size: 2.5rem;
    }
    
    h2 {
        color: #34495e;
        font-weight: 600;
        margin: 1.5rem 0 1rem 0;
    }
    
    /* Cards */
    .question-card {
        padding: 1.75rem;
        margin: 1.25rem 0;
        border-radius: 12px;
        background-color: #000000;  /* Light gray background */
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    /* Ensure all text in question cards is dark */
    .question-card, .question-card * {
        color: #2d3748 !important;
    }
    
    .question-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
    }
    
    .recommendation-card {
        padding: 1.75rem;
        margin: 1.25rem 0;
        border-radius: 12px;
        background: linear-gradient(145deg, #f8f9ff 0%, #f0f4ff 100%);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border-left: 5px solid #4e73df;
        transition: all 0.3s ease;
    }
    
    .recommendation-card:hover {
        transform: translateX(5px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        background: linear-gradient(135deg, #4e73df 0%, #3a56c9 100%);
        color: #000000;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(78, 115, 223, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(78, 115, 223, 0.4);
    }
    
    .stButton>button:active {
        transform: translateY(0);
        box-shadow: 0 2px 4px rgba(78, 115, 223, 0.3);
    }
    
    /* Form Elements */
    .stRadio > div {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }
    
    /* Radio button container */
    .stRadio > div > label {
        padding: 1rem 1.25rem;
        border-radius: 8px;
        background: #000000;
        border: 2px solid #e2e8f0;
        transition: all 0.2s ease;
        margin: 0.25rem 0;
    }
    
    /* Radio button text */
    .stRadio > div > label > div:first-child {
        color: #1a202c !important;  /* Very dark gray for best contrast */
        font-weight: 500;
        font-size: 1.05rem;
    }
    
    /* Hover state */
    .stRadio > div > label:hover {
        background: #f7fafc;
        border-color: #4e73df;
        transform: translateX(3px);
    }
    
    /* Selected radio button */
    .stRadio > div > [data-baseweb="radio"] > div:first-child {
        background-color: #4e73df !important;
        border-color: #4e73df !important;
    }
    
    /* Make sure the radio button circle is visible */
    [data-baseweb="radio"] > div:first-child {
        background-color: #000000 !important;
        border-color: #4e73df !important;
    }
    
    /* Selected radio button inner circle */
    [data-baseweb="radio"] > div:first-child > div {
        background-color: #4e73df !important;
    }
    
    /* Fix for Streamlit's default styling */
    .stRadio label {
        color: #1a202c !important;
    }
    
    /* For the actual radio input (hidden but needs to be accessible) */
    .stRadio input[type="radio"] {
        opacity: 1 !important;
        position: relative !important;
        margin-right: 8px !important;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main {
            padding: 1rem 0.5rem;
        }
        
        h1 {
            font-size: 2rem;
            text-align: center;
        }
        
        .question-card, .recommendation-card {
            padding: 1.25rem;
            margin: 1rem 0;
        }
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease-out forwards;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #000000;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #000000;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #a8a8a8;
    }
</style>
""", unsafe_allow_html=True)

# Questions Page
def show_questions():
    st.markdown("## 📝 Assessment Questions")
    st.markdown("Answer these questions to get personalized recommendations for your career path.")
    st.markdown("---")
    
    questions = [
        {
            "id": "q1",
            "question": "What is your primary area of expertise?",
            "type": "radio",
            "options": ["Frontend Development", "Backend Development", "Data Science", "DevOps", "UI/UX Design"]
        },
        {
            "id": "q2",
            "question": "Which programming languages are you proficient in?",
            "type": "multiselect",
            "options": ["Python", "JavaScript", "Java", "C++", "Go", "Rust", "TypeScript"]
        },
        {
            "id": "q3",
            "question": "How many years of experience do you have?",
            "type": "slider",
            "min": 0,
            "max": 20,
            "value": 2
        },
        {
            "id": "q4",
            "question": "What type of role are you looking for?",
            "type": "selectbox",
            "options": ["Full-time", "Part-time", "Contract", "Internship"]
        }
    ]
    
    with st.form("assessment_form"):
        for q in questions:
            st.markdown(f'<div class="question-card">', unsafe_allow_html=True)
            st.subheader(q["question"])
            
            if q["type"] == "radio":
                answer = st.radio(
                    label=q["question"],
                    options=q["options"],
                    key=q["id"] + "_radio",
                    index=0,
                    label_visibility="collapsed"
                )
            elif q["type"] == "multiselect":
                answer = st.multiselect(
                    label=q["question"],
                    options=q["options"],
                    key=q["id"] + "_multiselect",
                    label_visibility="collapsed"
                )
            elif q["type"] == "slider":
                answer = st.slider(
                    label=q["question"],
                    min_value=q["min"],
                    max_value=q["max"],
                    value=q["value"],
                    key=q["id"] + "_slider",
                    label_visibility="collapsed"
                )
            elif q["type"] == "selectbox":
                answer = st.selectbox(
                    label=q["question"],
                    options=q["options"],
                    key=q["id"] + "_select",
                    index=0,
                    label_visibility="collapsed"
                )
            
            st.session_state.answers[q["id"]] = answer
            st.markdown('</div>', unsafe_allow_html=True)
        
        if st.form_submit_button("Submit Assessment", type="primary"):
            st.session_state.show_recommendations = True
            st.rerun()

# Recommendations Page
def show_recommendations():
    st.markdown("## 🎯 Your Personalized Recommendations")
    st.markdown("Based on your responses, here are some learning paths that match your profile:")
    st.markdown("---")
    
    # Sample recommendations based on answers
    recommendations = [
        {
            "title": "Advanced Python Programming",
            "type": "Course",
            "provider": "Coursera",
            "match": "92%",
            "description": "Master advanced Python concepts and design patterns"
        },
        {
            "title": "System Design Interview Prep",
            "type": "Interview Prep",
            "provider": "AlgoExpert",
            "match": "88%",
            "description": "Prepare for system design interviews with real-world scenarios"
        },
        {
            "title": "Data Structures & Algorithms",
            "type": "Learning Path",
            "provider": "LeetCode",
            "match": "85%",
            "description": "Master data structures and algorithms with 100+ practice problems"
        }
    ]
    
    for rec in recommendations:
        with st.expander(f"🎯 {rec['title']} - {rec['match']} Match"):
            st.markdown(f"""
            **Type:** {rec['type']}  
            **Provider:** {rec['provider']}  
            **Match Score:** {rec['match']}  
            **Description:** {rec['description']}  
            """)
            if st.button("View Details", key=f"view_{rec['title']}"):
                st.session_state.selected_recommendation = rec
                st.rerun()

# Main App
def main():
    # Add a nice header with gradient
    st.markdown(
        """
        <div style='background: linear-gradient(135deg, #4e73df 0%, #224abe 100%); 
                   padding: 2rem; 
                   border-radius: 12px; 
                   margin-bottom: 2rem; 
                   color: white; 
                   box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
            <h1 style='color: white; margin: 0;'>🎯 Career Path Finder</h1>
            <p style='margin: 0.5rem 0 0; opacity: 0.9; font-size: 1.1rem;'>
                Discover your ideal learning path based on your skills and interests
            </p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Add a progress indicator
    if not st.session_state.get('show_recommendations', False):
        progress_text = "Complete the assessment to see your recommendations"
        progress_bar = st.progress(0, text=progress_text)
        show_questions()
    else:
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("↩️ Take the assessment again", use_container_width=True):
                st.session_state.show_recommendations = False
                st.session_state.answers = {}
                st.rerun()
        st.markdown("---")
        show_recommendations()
    
    # Add a nice footer
    st.markdown(
        """
        <div style='margin-top: 4rem; padding: 1.5rem; text-align: center; color: #6c757d; font-size: 0.9rem;'>
            <p>© 2025 Career Path Finder | Built with ❤️ | <a href='#' style='color: #4e73df; text-decoration: none;'>Privacy Policy</a> • <a href='#' style='color: #4e73df; text-decoration: none;'>Terms of Service</a></p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
