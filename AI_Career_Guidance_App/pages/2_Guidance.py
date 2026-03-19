import streamlit as st
import requests
import json
import os
from streamlit_oauth import OAuth2Component
from dotenv import load_dotenv
import ollama  # Local AI library

load_dotenv()

# ----------------- PAGE CONFIG -------------------
st.set_page_config(page_title="🎯 AI Career Guidance", layout="centered")

def _oauth_redirect_uri() -> str:
    port = st.get_option("server.port") or 8501
    return f"http://localhost:{port}/component/streamlit_oauth.authorize_button"

def logout():
    st.session_state.logged_in = False
    st.session_state.token = None
    if "user_name" in st.session_state:
        del st.session_state["user_name"]
    if "user_email" in st.session_state:
        del st.session_state["user_email"]
    st.rerun()

# ----------------- GOOGLE OAUTH SETUP -------------------
oauth2 = OAuth2Component(
    client_id=os.environ.get("GOOGLE_CLIENT_ID", ""),
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET", ""),
    authorize_endpoint="https://accounts.google.com/o/oauth2/auth",
    token_endpoint="https://oauth2.googleapis.com/token"
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "token" not in st.session_state:
    st.session_state.token = None
    
# ----------------- CSS STYLING -------------------
st.markdown("""
    <style>
        body { background-color: #0e1117; color: #ffffff; }
        .stTextArea textarea { background-color: #1e2130; color: #ffffff; }
        .title-style { font-size: 42px; font-weight: bold; text-align: center; color: #f9fafc; }
        .desc-style { font-size: 18px; text-align: center; color: #cfcfcf; }
        .box-style { padding: 1.5rem; border-radius: 12px; background-color: #1a1d2e; box-shadow: 0 0 20px rgba(0, 255, 255, 0.1); }
        .footer { margin-top: 3rem; text-align: center; font-size: 12px; color: #555; }
        .stButton button[kind="secondary"] { background-color: #D32F2F; color: white; border-radius: 6px; font-weight: bold; border: none; }
    </style>
""", unsafe_allow_html=True)

# ----------------- LOGIN LOGIC -------------------
if not st.session_state.logged_in:
    if not os.environ.get("GOOGLE_CLIENT_ID") or not os.environ.get("GOOGLE_CLIENT_SECRET"):
        st.error("⚠️ Google OAuth credentials missing in .env")
        st.stop()
    
    st.markdown("<h2 style='text-align:center; color:white;'>🔐 Please log in to use the app</h2>", unsafe_allow_html=True)
    
    result = oauth2.authorize_button(
        name="Login with Google",
        redirect_uri=_oauth_redirect_uri(),
        scope="https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile",
        pkce="S256",
    )

    if result and "token" in result:
        st.session_state.token = result["token"]
        st.session_state.logged_in = True
        st.rerun()
    st.stop()

# ----------------- FETCH USER INFO -------------------
user_name = "User"
user_email = "Unknown"

if st.session_state.token:
    access_token = st.session_state.token.get("access_token")
    try:
        user_info = requests.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        ).json()
        user_name = user_info.get("name", "User")
        user_email = user_info.get("email", "Unknown")
    except Exception:
        logout()
        st.stop()

# ----------------- HEADER -------------------
col_logo, col_title, col_logout = st.columns([1, 3, 1])
with col_title:
    st.markdown('<p class="title-style" style="text-align:left; font-size:30px; margin-top:5px;">🎯 AI Career Guidance</p>', unsafe_allow_html=True)
with col_logout:
    st.button("Log Out", on_click=logout, type="secondary", key="logout_btn")

st.markdown(f'<p class="desc-style">Welcome, {user_name} ({user_email})</p>', unsafe_allow_html=True)

# ----------------- MAIN APP CHAT INTERFACE (OLLAMA) -------------------
with st.container():
    st.markdown('<div class="box-style">', unsafe_allow_html=True)

    with st.form(key="career_form", clear_on_submit=False):
        user_input = st.text_area("🧠 Tell me about your interests, skills, or goals:")
        submit = st.form_submit_button("🚀 Get Career Suggestions")

    if submit:
        if not user_input.strip():
            st.warning("⚠️ Please enter something first!")
        else:
            # Check for creator info
            keywords = ["who made", "who built", "who created", "owner", "creator", "developed by"]
            if any(kw in user_input.lower() for kw in keywords):
                st.success("🤖 This chatbot was built by **Suraj**.")
            else:
                # OLLAMA LOGIC REPLACING OPENROUTER
                with st.spinner("🤖 Ollama is thinking locally..."):
                    try:
                        # You can change 'llama3.2' to 'gemma2' or any model you pulled
                        response = ollama.chat(model='llama3.2:3b',
                            messages=[
                                {"role": "system", "content": "You are a helpful career counselor AI. Your response must be formatted using Markdown (bullet points, bolding, and headers)."},
                                {"role": "user", "content": f"My skills and interests: {user_input}. Provide a structured response with suggestions, required skills, and a potential next step."}
                            ]
                        )
                        
                        # Extract the message content
                        answer = response['message']['content']
                        st.success("💡 Here are some career suggestions for you:")
                        st.markdown(answer)

                    except Exception as e:
                        st.error(f"❌ Could not connect to Ollama: {e}")
                        st.info("Check if Ollama is running on your machine and you have pulled the model using: `ollama pull llama3.2`")

    st.markdown('</div>', unsafe_allow_html=True)

# ----------------- FOOTER -------------------
st.markdown('<p class="footer">Built with ❤️ using Streamlit and Local Ollama</p>', unsafe_allow_html=True)