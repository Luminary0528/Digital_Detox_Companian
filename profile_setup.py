import streamlit as st
import pandas as pd
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="🌿 Onboarding - Digital Detox Companion",
    page_icon="🌿",
    layout="centered"
)

# --- Enhanced Styling with Nature Theme ---
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    
    /* Main Background with Nature Theme */
    .main {
        background: linear-gradient(135deg, #E8F5E8 0%, #F0F8F0 50%, #E0F2F1 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Semi-transparent white overlay for content */
    .block-container {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(44, 110, 73, 0.1);
    }
    
    /* Headers with nature colors */
    h1, h2, h3, h4, h5, h6 {
        color: #2C6E49;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
    }
    
    /* Enhanced buttons */
    .stButton>button {
        background: linear-gradient(45deg, #A8D5BA, #7FB069);
        color: #2C6E49;
        border-radius: 12px;
        border: none;
        padding: 0.7rem 2rem;
        font-weight: 500;
        font-family: 'Inter', sans-serif;
        box-shadow: 0 4px 15px rgba(127, 176, 105, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(127, 176, 105, 0.4);
    }
    
    /* Form elements styling */
    .stSelectbox>div>div>select,
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input {
        border-radius: 10px;
        border: 2px solid #A8D5BA;
        background: rgba(255, 255, 255, 0.9);
        font-family: 'Inter', sans-serif;
    }
    
    /* Info boxes */
    .stInfo {
        background: rgba(168, 213, 186, 0.2);
        border-left: 4px solid #A8D5BA;
        border-radius: 8px;
    }
    
    /* Nature emoji decorations */
    .nature-decoration {
        font-size: 1.5rem;
        opacity: 0.7;
        margin: 0 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- Constants ---
PROFILES_FILE = "user_profiles.csv"

# --- Helper Functions ---
def init_profiles_file():
    """Initialize user_profiles.csv if it doesn't exist"""
    if not os.path.exists(PROFILES_FILE):
        df = pd.DataFrame(columns=[
            "user_id", "username", "sleep_hours", "eating_habits", "main_goal", 
            "mood_after_screen", "daily_offline_time", "onboarding_complete"
        ])
        df.to_csv(PROFILES_FILE, index=False)

def get_user_profile(user_id):
    """Get user profile if exists"""
    if not os.path.exists(PROFILES_FILE):
        return None
    
    df = pd.read_csv(PROFILES_FILE)
    user_profile = df[df['user_id'] == user_id]
    
    if user_profile.empty:
        return None
    
    return user_profile.iloc[0].to_dict()

def save_user_profile(user_id, username, sleep_hours, eating_habits, main_goal, mood_after_screen, daily_offline_time):
    """Save or update user profile"""
    df = pd.read_csv(PROFILES_FILE)
    
    # Remove existing profile for this user
    df = df[df['user_id'] != user_id]
    
    # Add new profile
    new_profile = pd.DataFrame({
        "user_id": [user_id],
        "username": [username],
        "sleep_hours": [sleep_hours],
        "eating_habits": [eating_habits],
        "main_goal": [main_goal],
        "mood_after_screen": [mood_after_screen],
        "daily_offline_time": [daily_offline_time],
        "onboarding_complete": [True]
    })
    
    df = pd.concat([df, new_profile], ignore_index=True)
    df.to_csv(PROFILES_FILE, index=False)

# --- Check Authentication ---
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.error("🔒 Please login first to access your wellness journey")
    st.switch_page("login_page.py")

# --- Initialize Files ---
init_profiles_file()

# --- Check if Profile Already Exists ---
existing_profile = get_user_profile(st.session_state.user_id)

if existing_profile and existing_profile.get('onboarding_complete'):
    # Profile already complete, go to main app
    st.switch_page("digital_detox.py")

# --- Main Onboarding Questionnaire ---
st.markdown("# 🌿 Welcome to Your Digital Wellness Journey")
st.markdown(f"### Hello, {st.session_state.username}! <span class='nature-decoration'>🌱</span>", unsafe_allow_html=True)
st.markdown("*Let's personalize your experience with a quick questionnaire*")

st.markdown("---")

with st.form("onboarding_form"):
    # Sleep Section
    st.markdown("#### 😴 Sleep & Rest <span class='nature-decoration'>🌙</span>", unsafe_allow_html=True)
    sleep_hours = st.selectbox(
        "How many hours do you typically sleep per night?",
        ["Less than 6 hours", "6-7 hours", "7-8 hours", "8-9 hours", "More than 9 hours"],
        help="This helps us understand if screen time affects your sleep quality"
    )
    
    st.markdown("---")
    
    # Lifestyle Section
    st.markdown("#### 🥗 Lifestyle Habits <span class='nature-decoration'>🍃</span>", unsafe_allow_html=True)
    eating_habits = st.selectbox(
        "How would you describe your eating habits?",
        ["Healthy (balanced meals, regular schedule)", 
         "Average (mostly good, some processed food)", 
         "Poor (irregular meals, frequent fast food)"],
        help="We'll suggest activities that complement your lifestyle"
    )
    
    st.markdown("---")
    
    # Goals Section
    st.markdown("#### 🎯 Your Wellness Goal <span class='nature-decoration'>🌟</span>", unsafe_allow_html=True)
    main_goal = st.selectbox(
        "What's your main goal for digital wellness?",
        ["Better sleep quality",
         "More offline time & nature connection", 
         "Reduce stress and anxiety",
         "Boost productivity and focus"],
        help="This will shape your personalized challenge plans"
    )
    
    st.markdown("---")
    
    # Screen Time Impact Section
    st.markdown("#### 📱 Screen Time Impact <span class='nature-decoration'>🧠</span>", unsafe_allow_html=True)
    mood_after_screen = st.selectbox(
        "How do you typically feel after long screen use?",
        ["Tired and drained", 
         "Anxious or restless", 
         "Motivated and energized", 
         "Neutral (no strong feeling)"],
        help="Understanding this helps us suggest better alternatives"
    )
    
    st.markdown("---")
    
    # Time Availability Section
    st.markdown("#### ⏰ Offline Time Availability <span class='nature-decoration'>🕐</span>", unsafe_allow_html=True)
    daily_offline_time = st.selectbox(
        "How much time can you realistically dedicate daily to offline activities?",
        ["15-30 minutes", "30-60 minutes", "1-2 hours", "2+ hours"],
        help="We'll suggest activities that fit your schedule"
    )
    
    st.markdown("---")
    
    # Submit Button
    submitted = st.form_submit_button("🌱 Complete My Wellness Profile", use_container_width=True)
    
    if submitted:
        save_user_profile(
            st.session_state.user_id,
            st.session_state.username,
            sleep_hours,
            eating_habits,
            main_goal,
            mood_after_screen,
            daily_offline_time
        )
        
        st.success("🎉 Profile created successfully! Welcome to your digital wellness journey.")
        st.balloons()
        
        # Show a preview of what's coming
        st.markdown("### 🚀 What's Next?")
        st.info("""
        **Your personalized dashboard includes:**
        - 📊 Weekly screen time tracking & insights
        - 🎯 Custom offline activity suggestions
        - 💡 Daily motivational wellness tips
        - 🏆 7-day detox challenge tailored to your goals
        """)
        
        # Auto-redirect after 3 seconds
        import time
        time.sleep(2)
        st.switch_page("digital_detox.py")

# --- Help Section ---
st.markdown("---")
st.markdown("#### 🤔 Why These Questions? <span class='nature-decoration'>❓</span>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.info("""
    **🔒 Privacy First**
    - All data stays on your device
    - No cloud storage or tracking
    - Complete offline functionality
    """)

with col2:
    st.info("""
    **🎯 Personalization**
    - Tailored activity suggestions
    - Custom challenge difficulty
    - Smart insights for your goals
    """)

st.markdown("---")
st.markdown("<div style='text-align: center; color: #2C6E49; opacity: 0.7;'>🌿 Taking the first step towards digital wellness 🌿</div>", unsafe_allow_html=True)
