import streamlit as st
import json
import ollama  # <--- Use the local library instead of requests
import os

# 🔐 Block access if not logged in
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("🔒 Please login to access this page.")
    st.stop()

# 🎨 Page setup
st.set_page_config(page_title="📊 Career Suggestions & Roadmap", layout="wide")

# ✅ CSS Styling (Kept as is)
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
        font-family: 'Segoe UI', sans-serif;
    }
    .block-container {
        background-color: rgba(20, 20, 30, 0.95);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0px 0px 20px rgba(0, 200, 255, 0.2);
    }
    h1, h2, h3, h4, h5, h6, p, li {
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# 👋 Title
st.title("📊 Career Suggestions & Roadmap Generator")
st.markdown("**Get AI-powered career suggestions and personalized roadmaps based on your profile**")
st.divider()

# 📋 Section 1: User Profile Input
st.header("📋 Step 1: Tell Us About Yourself")

with st.form(key="profile_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        skills = st.text_area(
            "🧠 Your Skills (comma-separated)",
            placeholder="e.g., Python, Machine Learning, Data Analysis, Leadership",
            height=100
        )
        education = st.selectbox(
            "🎓 Education Level",
            ["High School", "Bachelor's Degree", "Master's Degree", "PhD", "Self-Taught"]
        )
    
    with col2:
        interests = st.text_area(
            "❤️ Your Interests (comma-separated)",
            placeholder="e.g., AI, Web Development, Cybersecurity, Business",
            height=100
        )
        experience = st.selectbox(
            "💼 Work Experience",
            ["0-1 years", "1-3 years", "3-5 years", "5-10 years", "10+ years"]
        )
    
    goals = st.text_area(
        "🎯 Your Career Goals",
        placeholder="What do you want to achieve in your career?",
        height=80
    )
    
    submit_button = st.form_submit_button("🚀 Generate Suggestions & Roadmap", use_container_width=True)

# 🎯 Process and Generate Suggestions
if submit_button:
    if not skills.strip() or not interests.strip() or not goals.strip():
        st.warning("⚠️ Please fill in all fields to get suggestions!")
    else:
        with st.spinner("🤖 Ollama is analyzing your profile locally... (No API limits)"):
            try:
                # 1. Prepare the prompt
                prompt = f"""
                As an expert career counselor, analyze the following profile and provide detailed career guidance:
                
                **Profile:**
                - Skills: {skills}
                - Interests: {interests}
                - Education: {education}
                - Experience: {experience}
                - Goals: {goals}
                
                Please provide your response in the following structured format:
                
                ## 🎯 Top 3 Recommended Career Paths
                For each career, include: Job Title, Why it's a good fit, Salary, and Responsibilities.
                
                ## 📚 Skills to Develop
                (List 5-7 essential skills needed)
                
                ## 🗓️ 6-Month Roadmap
                - Month 1-2: specific actions
                - Month 3-4: specific actions
                - Month 5-6: specific actions
                
                ## 🔗 Resources & Learning Paths
                ## 💡 Additional Tips
                """

                # 2. Call Ollama (Make sure you pulled llama3.2 or your preferred model)
                response = ollama.chat(
                    model='llama3.2:3b', 
                    messages=[
                        {"role": "system", "content": "You are an expert career counselor. Use Markdown for formatting."},
                        {"role": "user", "content": prompt}
                    ]
                )

                # 3. Display Result
                answer = response['message']['content']
                st.success("✅ Career suggestions generated successfully!")
                st.divider()
                st.markdown(answer)
                
                # Download Button
                st.download_button(
                    label="📥 Download Roadmap as Text",
                    data=answer,
                    file_name="career_roadmap.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"❌ Connection to Ollama failed: {e}")
                st.info("💡 Ensure the Ollama app is open and you have run 'ollama pull llama3.2' in your terminal.")

# 📌 Helpful Tips Section (Footer kept as is)
st.divider()
st.header("💡 Tips for Career Development")
# ... (Rest of your Tips columns)