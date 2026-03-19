import streamlit as st

# 🔐 Block access if not logged in
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("🔒 Please login to access this page.")
    st.stop()

# 🎨 Page setup
st.set_page_config(page_title="Home - AI Career Guidance", layout="centered")

# ✅ CSS: Local background + dark foreground
st.markdown("""
    <style>
    .stApp {
        background-image: url("../images/background.jpg");
        background-size: cover;
        background-position: center;
        font-family: 'Segoe UI', sans-serif;
    }
    .block-container {
        background-color: rgba(45, 0, 85, 0.85);  /* Dark purple foreground */
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.6);
        color: white;
    }
    h1, h2, h3, h4, h5, h6, p, li {
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# 👋 Home Content
st.title("👋 Welcome to AI Career Guidance!")

st.markdown("""
### 🤖 Your Personal AI Career Mentor

Let AI help you explore careers that match your **skills, interests, and goals**.

---

### 🌟 Features:

- 🧠 **Personalized Career Suggestions**
- 📈 **Future Roadmaps** based on your interests
- 💬 **AI Chatbot** trained to be your mentor
- 💼 Explore high-demand jobs in 2025

---

### 💡 Why This App?

- ✅ Powered by **OpenAI GPT Models**
- ✅ Easy to Use, Clean UI
- ✅ Perfect for students & job seekers

---

👉 Go to the **Main** tab to start chatting with the AI!
""")

st.image("https://cdn-icons-png.flaticon.com/512/4341/4341139.png", width=250)
