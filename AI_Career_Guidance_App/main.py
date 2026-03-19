import streamlit as st
from streamlit_oauth import OAuth2Component
import requests
from dotenv import load_dotenv
import os
import ollama

load_dotenv()

# ----------------- PAGE CONFIG -------------------
st.set_page_config(page_title="AI Career Portal", layout="wide", initial_sidebar_state="expanded")

# --- Custom CSS (Deep Blue Theme) ---
st.markdown("""
    <style>
        .stApp { background-color: #152238; color: #ffffff; }
        .welcome-title {
            font-size: 3.5rem; font-weight: 800; color: #4CAF50;
            text-align: center; margin-bottom: 0.5rem; text-transform: uppercase;
        }
        .welcome-subtitle {
            color: #ccc; font-size: 1.5rem; text-align: center; margin-top: 0;
        }
        .status-box {
            padding: 10px; border-radius: 10px; text-align: center; margin: 10px 0;
        }
    </style>
""", unsafe_allow_html=True)

# ----------------- OAUTH SETUP -------------------
def _oauth_redirect_uri() -> str:
    port = st.get_option("server.port") or 8501
    return f"http://localhost:{port}/component/streamlit_oauth.authorize_button"

oauth2 = OAuth2Component(
    client_id=os.environ.get("GOOGLE_CLIENT_ID", ""),
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET", ""),
    authorize_endpoint="https://accounts.google.com/o/oauth2/auth",
    token_endpoint="https://oauth2.googleapis.com/token"
)

# Initialize Session State
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "token" not in st.session_state:
    st.session_state.token = None

# ----------------- LOGIN LOGIC -------------------
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>🔐 Career Portal Login</h1>", unsafe_allow_html=True)
    
    # Check if Ollama is running before letting them in
    try:
        ollama.list()
        st.success("✅ Local AI Engine (Ollama) is Online")
    except Exception:
        st.error("⚠️ Local AI Engine is Offline. Please open the Ollama Desktop App.")

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

# ----------------- POST-LOGIN CONTENT -------------------
if st.session_state.logged_in:
    # Fetch user details once
    if "user_name" not in st.session_state:
        try:
            user_info = requests.get(
                "https://www.googleapis.com/oauth2/v3/userinfo",
                headers={"Authorization": f"Bearer {st.session_state.token.get('access_token')}"}
            ).json()
            st.session_state.user_name = user_info.get("name", "User")
        except:
            st.session_state.logged_in = False
            st.rerun()

    user_name = st.session_state.get("user_name", "User")
    
    st.markdown(f'<div class="welcome-title">WELCOME TO SURAJ CHATBOT</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="welcome-subtitle">Securely Signed in as {user_name}!</div>', unsafe_allow_html=True)
    
    st.info("👋 Access the **📊 Roadmap** page from the sidebar to start your career analysis.")
    
    # Quick Status Dashboard
    col1, col2 = st.columns(2)
    with col1:
        st.write("### 🤖 AI Engine Status")
        st.write("Model: `llama3.2` (Local)")
        st.write("Rate Limits: **Unlimited**")
    with col2:
        st.write("### 👤 Account")
        st.write(f"User: {user_name}")
        if st.button("Log Out"):
            st.session_state.clear()
            st.rerun()