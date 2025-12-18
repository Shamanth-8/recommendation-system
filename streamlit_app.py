import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os
import random

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
        background-color: #ffffff;  /* White background */
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
        color: #ffffff;
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
    .stRadio label {
        padding: 1rem 1.25rem;
        border-radius: 8px;
        background: #f8fafc;
        border: 2px solid #e2e8f0;
        transition: all 0.2s ease;
        margin: 0.25rem 0;
        cursor: pointer;
    }
    
    /* Radio button text */
    .stRadio label p {
        color: #1a202c !important;  /* Very dark gray for best contrast */
        font-weight: 500;
        font-size: 1.05rem;
    }
    
    /* Hover state */
    .stRadio label:hover {
        background: #edf2f7;
        border-color: #cbd5e0;
    }

    /* Selected state styling wrapper provided by Streamlit */
    div[role="radiogroup"] > label[data-baseweb="radio"] {
        background-color: #eff6ff !important;
        border-color: #4e73df !important;
    }

    /* The actual radio circle */
    div[role="radiogroup"] > label[data-baseweb="radio"] div:first-child {
        background-color: #ffffff !important;
        border-color: #4e73df !important;
    }

    /* The inner filled circle when selected */
    div[role="radiogroup"] > label[data-baseweb="radio"] div:first-child > div {
        background-color: #4e73df !important;
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
        background: #f1f1f1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #c1c1c1;
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
            "type": "selectbox",
            "options": [
                "Frontend Development", "Backend Development", "Data Science", "DevOps", "UI/UX Design", "Full Stack",
                "Banking & Finance", "Healthcare", "Hospitality", "Insurance", "Manufacturing", "Oil & Gas", "Retail", "Telecommunications"
            ]
        },
        {
            "id": "q2",
            "question": "Which skills or tools are you proficient in?",
            "type": "multiselect",
            "options": [
                "Python", "JavaScript", "Java", "C++", "Go", "Rust", "TypeScript",
                "Banking", "Finance", "Healthcare", "Nursing", "Customer Service", "Sales", "Management", "Leadership",
                "Insurance", "Claims", "Manufacturing", "Operations", "Retail", "Telecommunications", "Network"
            ]
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
        },
        {
            "id": "q5",
            "question": "What position level are you targeting?",
            "type": "selectbox",
            "options": ["Entry", "Mid", "Senior", "Executive"]
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
    
    # Load Catalog
    catalog_path = os.path.join(os.path.dirname(__file__), 'data', 'catalog.json')
    catalog = []
    
    try:
        if os.path.exists(catalog_path):
            with open(catalog_path, 'r') as f:
                catalog = json.load(f)
        else:
            st.warning("Catalog file not found. Showing sample recommendations.")
    except Exception as e:
        st.error(f"Error loading catalog: {e}")
        
    # User's selected category from Q1
    user_category = st.session_state.answers.get("q1", "")
    user_skills = st.session_state.answers.get("q2", [])
    user_position_level = st.session_state.answers.get("q5", "Entry")
    
    # Filter and Score Recommendations
    recommendations = []
    
    if catalog:
        for item in catalog:
            score = 0
            # Strong match for category
            if item.get("category") == user_category:
                score += 50
            
            # Match for position level
            if item.get("position_level") == user_position_level:
                score += 25
            
            # Match for skills/tags
            tags = item.get("tags", [])
            for skill in user_skills:
                if skill in tags:
                    score += 15
            
            # Add some randomness for variation in generic scores
            score += random.randint(0, 10)
            
            # Only include if there is some relevance or if it's high scoring
            if score > 0:
                match_percentage = min(99, 50 + score) if item.get("category") == user_category else min(80, 20 + score)
                
                item_copy = item.copy()
                item_copy["match"] = f"{match_percentage}%"
                item_copy["type"] = "Assessment" # Default type
                recommendations.append(item_copy)
        
        # Sort by match score (simulated by checking the integer value of the percentage string)
        recommendations.sort(key=lambda x: int(x["match"].strip('%')), reverse=True)
        
        # Take top 3
        recommendations = recommendations[:3]
    
    # Fallback if no catalog or no matches found (shouldn't happen with proper catalog)
    if not recommendations:
         recommendations = [
            {
                "title": "General Software Engineering",
                "type": "Course",
                "provider": "SHL Academy",
                "match": "80%",
                "description": "A comprehensive guide to software development principles."
            }
        ]
    
    for rec in recommendations:
        with st.expander(f"🎯 {rec['title']} - {rec['match']} Match"):
            st.markdown(f"""
            **Type:** {rec.get('type', 'Assessment')}  
            **Provider:** {rec.get('provider', 'SHL')}  
            **Category:** {rec.get('category', 'General')}  
            **Position Level:** {rec.get('position_level', 'N/A')}  
            **Match Score:** {rec.get('match', 'N/A')}  
            **Remote Support:** {rec.get('remote_support', 'N/A')}  
            **Adaptive:** {rec.get('adaptive_reasoning', 'N/A')}  
            **Description:** {rec.get('description', '')}  
            """)

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
            <p>© 2025 Career Path Finder</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
