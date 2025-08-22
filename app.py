import streamlit as st
import pandas as pd
import os

# Entry/landing page shown AFTER login.
# Decides whether to send users to onboarding or the dashboard.

st.set_page_config(page_title="🌿 Digital Detox Companion", page_icon="🌿", layout="wide")

# --- Nature-inspired styling (soft gradient + glass overlay) ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    .main { background: linear-gradient(135deg, #E8F5E8 0%, #F0F8F0 40%, #E0F2F1 100%); font-family: 'Inter', sans-serif; }
    .block-container { background: rgba(255,255,255,0.9); backdrop-filter: blur(12px); border-radius: 22px; padding: 3rem; box-shadow: 0 12px 36px rgba(44,110,73,0.15); }
    h1, h2, h3, h4, h5, h6 { color: #2C6E49; font-weight: 600; }
    .stButton>button { background: linear-gradient(45deg, #A8D5BA, #81C784); color: #2C6E49; border: 0; border-radius: 14px; padding: 0.8rem 1.6rem; box-shadow: 0 6px 18px rgba(129,199,132,0.35); font-weight: 600; }
    .stButton>button:hover { transform: translateY(-1px); box-shadow: 0 10px 24px rgba(129,199,132,0.45); }
    .sub { color: #2C6E49; opacity: 0.85; }
    </style>
    """,
    unsafe_allow_html=True,
)

PROFILES_FILE = "user_profiles.csv"

def ensure_profiles_csv():
    """Create profiles CSV if missing (for first run on new machines)."""
    if not os.path.exists(PROFILES_FILE):
        pd.DataFrame(
            columns=[
                "user_id",
                "username",
                "sleep_hours",
                "eating_habits",
                "main_goal",
                "mood_after_screen",
                "daily_offline_time",
                "onboarding_complete",
            ]
        ).to_csv(PROFILES_FILE, index=False)

def get_profile(user_id: int):
    if not os.path.exists(PROFILES_FILE):
        return None
    df = pd.read_csv(PROFILES_FILE)
    row = df[df["user_id"] == user_id]
    return None if row.empty else row.iloc[0].to_dict()

# --- Auth guard ---
if "user_id" not in st.session_state or not st.session_state.user_id:
    # Not logged in → send to landing/login page
    st.switch_page("landing_page.py")

ensure_profiles_csv()
profile = get_profile(st.session_state.user_id)

# --- Landing content ---
st.markdown("# Your Personal Digital Detox Companion")
st.markdown(
    "<h4 class='sub'>A simple way to balance your digital life and improve your well-being.</h4>",
    unsafe_allow_html=True,
)

st.markdown("""
<div style='height: 12px'></div>
""", unsafe_allow_html=True)

colA, colB = st.columns([2,1])
with colA:
    st.markdown(
        """
        • Track your daily screen time with ease  
        • Learn how screens affect sleep, stress, and focus  
        • Build momentum with tiny, realistic micro-challenges  
        • 100% private and offline — your data stays with you
        """
    )
with colB:
    st.image(
        "assets/nature_scene.svg",
        caption="Nature time > screen time",
        use_column_width=True,
    )

st.markdown("""
<div style='height: 16px'></div>
""", unsafe_allow_html=True)

cta = st.button("🌱 Start My Journey", use_container_width=True)

if cta:
    # If no profile or onboarding not complete → go to onboarding
    if not profile or not bool(profile.get("onboarding_complete")):
        st.switch_page("profile_setup.py")
    else:
        st.switch_page("digital_detox.py")

# Helpful tip for returning users
if profile and profile.get("onboarding_complete"):
    st.info("Welcome back! Click 'Start My Journey' to go to your dashboard.")
