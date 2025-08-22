import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import hashlib
import os
import random
from datetime import datetime, timedelta

# --- Page Configuration ---
st.set_page_config(
    page_title="🌿 Digital Detox Companion", 
    page_icon="🌿", 
    layout="wide",
    initial_sidebar_state="auto"
)

# --- Beautiful Styling ---
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Beautiful gradient background with nature theme */
    .main {
        background: linear-gradient(135deg, 
            #667eea 0%, 
            #764ba2 25%, 
            #6a994e 50%, 
            #a7c957 75%, 
            #f2e8cf 100%
        );
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        min-height: 100vh;
        font-family: 'Poppins', sans-serif;
        color: #1B4332 !important;
    }
    
    /* Ensure all text is visible */
    * {
        color: #1B4332 !important;
    }
    
    /* Override for specific elements that need different colors */
    .stButton > button {
        color: white !important;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Container styling with better text contrast */
    .block-container {
        background: rgba(255, 255, 255, 0.98);
        backdrop-filter: blur(20px);
        border-radius: 25px;
        padding: 2rem;
        margin: 1rem auto;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: #1B4332;
    }
    
    /* Headers with nature theme - solid colors for better visibility */
    h1, h2, h3, h4, h5, h6 {
        color: #1B4332 !important;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
    }
    
    h1 {
        color: #1B4332 !important;
        font-size: 2.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #4CAF50, #2E7D32);
        color: white;
        border-radius: 20px;
        border: none;
        padding: 0.8rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(76, 175, 80, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(76, 175, 80, 0.4);
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 15px;
        border: 2px solid #A8D5BA;
        padding: 0.8rem;
        font-size: 1rem;
        background: rgba(255, 255, 255, 0.9);
    }
    
    /* Wellness tip card */
    .wellness-tip {
        background: linear-gradient(135deg, #E3F2FD, #F3E5F5);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 6px solid #FF6B35;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        color: #1B4332 !important;
    }
    
    .wellness-tip h4 {
        color: #1B4332 !important;
        margin-bottom: 0.5rem;
    }
    
    .wellness-tip p {
        color: #2D3748 !important;
        margin: 0;
    }
    
    /* Feature cards */
    .feature-card {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem;
        border-left: 5px solid #4CAF50;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
        height: 100%;
        color: #1B4332;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1B4332 !important;
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        color: #2D3748 !important;
        font-size: 0.9rem;
        line-height: 1.5;
    }
    </style>
""", unsafe_allow_html=True)

# --- Helper Functions ---
def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def init_users_file():
    """Initialize users CSV file if it doesn't exist"""
    if not os.path.exists("users.csv"):
        df = pd.DataFrame(columns=['user_id', 'username', 'password_hash'])
        df.to_csv("users.csv", index=False)

def authenticate_user(username, password):
    """Authenticate user credentials"""
    if not os.path.exists("users.csv"):
        return False, None
    
    users_df = pd.read_csv("users.csv")
    password_hash = hash_password(password)
    
    user = users_df[(users_df['username'] == username) & (users_df['password_hash'] == password_hash)]
    
    if not user.empty:
        return True, user.iloc[0]['user_id']
    return False, None

def create_user(username, password):
    """Create a new user account"""
    init_users_file()
    users_df = pd.read_csv("users.csv")
    
    # Check if username already exists
    if username in users_df['username'].values:
        return False, "Username already exists"
    
    # Generate new user ID
    new_user_id = len(users_df) + 1
    password_hash = hash_password(password)
    
    # Add new user
    new_user = pd.DataFrame([{
        'user_id': new_user_id,
        'username': username,
        'password_hash': password_hash
    }])
    
    users_df = pd.concat([users_df, new_user], ignore_index=True)
    users_df.to_csv("users.csv", index=False)
    
    return True, new_user_id

def get_user_profile(user_id):
    """Get user profile data"""
    if not os.path.exists("user_profiles.csv"):
        return None
    
    profiles_df = pd.read_csv("user_profiles.csv")
    user_profile = profiles_df[profiles_df['user_id'] == user_id]
    
    if user_profile.empty:
        return None
    
    return user_profile.iloc[0].to_dict()

def save_user_profile(user_id, username, sleep_hours, eating_habits, main_goal, mood_after_screen, daily_offline_time):
    """Save user profile data"""
    if not os.path.exists("user_profiles.csv"):
        df = pd.DataFrame(columns=['user_id', 'username', 'sleep_hours', 'eating_habits', 'main_goal', 
                                  'mood_after_screen', 'daily_offline_time', 'onboarding_complete', 'created_date'])
        df.to_csv("user_profiles.csv", index=False)
    
    profiles_df = pd.read_csv("user_profiles.csv")
    
    # Check if profile already exists
    existing_profile = profiles_df[profiles_df['user_id'] == user_id]
    
    profile_data = {
        'user_id': user_id,
        'username': username,
        'sleep_hours': sleep_hours,
        'eating_habits': eating_habits,
        'main_goal': main_goal,
        'mood_after_screen': mood_after_screen,
        'daily_offline_time': daily_offline_time,
        'onboarding_complete': True,
        'created_date': datetime.now().strftime("%Y-%m-%d")
    }
    
    if not existing_profile.empty:
        # Update existing profile
        profiles_df.loc[profiles_df['user_id'] == user_id, list(profile_data.keys())] = list(profile_data.values())
    else:
        # Add new profile
        new_profile = pd.DataFrame([profile_data])
        profiles_df = pd.concat([profiles_df, new_profile], ignore_index=True)
    
    profiles_df.to_csv("user_profiles.csv", index=False)

def init_screen_time_file():
    """Initialize the screen time CSV file if it doesn't exist"""
    file_path = "daily_screen_time.csv"
    if not os.path.exists(file_path):
        df = pd.DataFrame(columns=['user_id', 'date', 'phone', 'laptop', 'tablet', 'total_screen', 'mood', 'notes'])
        df.to_csv(file_path, index=False)

def save_daily_entry(user_id, phone, laptop, tablet, mood, notes=""):
    """Save a daily screen time entry"""
    init_screen_time_file()
    
    total_screen = phone + laptop + tablet
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Load existing data
    df = pd.read_csv("daily_screen_time.csv")
    
    # Check if entry for today already exists
    existing_entry = df[(df['user_id'] == user_id) & (df['date'] == today)]
    
    if not existing_entry.empty:
        # Update existing entry
        df.loc[(df['user_id'] == user_id) & (df['date'] == today), 
               ['phone', 'laptop', 'tablet', 'total_screen', 'mood', 'notes']] = [phone, laptop, tablet, total_screen, mood, notes]
    else:
        # Add new entry
        new_entry = pd.DataFrame([{
            'user_id': user_id,
            'date': today,
            'phone': phone,
            'laptop': laptop,
            'tablet': tablet,
            'total_screen': total_screen,
            'mood': mood,
            'notes': notes
        }])
        df = pd.concat([df, new_entry], ignore_index=True)
    
    df.to_csv("daily_screen_time.csv", index=False)

def get_user_screen_data(user_id):
    """Get all screen time data for a specific user"""
    init_screen_time_file()
    df = pd.read_csv("daily_screen_time.csv")
    user_data = df[df['user_id'] == user_id].sort_values('date')
    return user_data

# --- Constants ---
WELLNESS_QUOTES = [
    "The best time to plant a tree was 20 years ago. The second best time is now. 🌱",
    "In every walk with nature, one receives far more than they seek. 🌿",
    "Your mind is a garden. Your thoughts are the seeds. 🌸",
    "Take time to make your soul happy. 🦋",
    "Breathe in peace, breathe out stress. 🌊",
    "Digital wellness is self-care in the modern age. 📱💚",
    "Small steps daily lead to big changes yearly. 🌟"
]

MOODS = [
    "😌 Peaceful", "🎯 Focused", "😴 Tired", "😰 Stressed", 
    "😊 Happy", "🤔 Contemplative", "😔 Down", "⚡ Energetic"
]

# --- Initialize Session State ---
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'landing'
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'username' not in st.session_state:
    st.session_state.username = None

# --- Page Functions ---

def show_landing_page():
    """Display the beautiful landing page"""
    
    st.markdown("""
    <div style="text-align: center;">
        <h1>🌿 Digital Detox Companion</h1>
        <h3 style="color: #666; font-weight: 400;">Your Mindful Digital Wellness Journey Starts Here</h3>
        
        <div style="font-size: 3rem; margin: 2rem 0; opacity: 0.8;">
            🌿 🌸 🥒 🌊 ✨
        </div>
        
        <p style="font-size: 1.1rem; color: #666; margin: 2rem 0; line-height: 1.7;">
            Break free from digital overwhelm and cultivate a healthier relationship with technology. 
            Track your screen time, discover mindful activities, and transform your digital habits 
            with personalized insights and gentle guidance.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Features section
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Smart Tracking</div>
            <div class="feature-desc">
                Monitor your screen time across devices with beautiful visualizations 
                and personalized insights.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🧘</div>
            <div class="feature-title">Mindful Activities</div>
            <div class="feature-desc">
                Receive personalized activity suggestions based on your mood and goals.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🏆</div>
            <div class="feature-title">Achievement System</div>
            <div class="feature-desc">
                Earn badges through 7-day challenges designed to build healthier habits.
            </div>
        </div>
        """, unsafe_allow_html=True)

def show_auth_page():
    """Show login and signup forms"""
    
    st.markdown("## 🌿 Welcome to Digital Wellness")
    
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Sign Up"])
    
    with tab1:
        st.markdown("### Welcome Back! 🌿")
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            login_button = st.form_submit_button("🚀 Start My Wellness Journey")
            
            if login_button:
                if username and password:
                    success, user_id = authenticate_user(username, password)
                    if success:
                        st.session_state.user_id = user_id
                        st.session_state.username = username
                        st.session_state.current_page = 'check_profile'
                        st.success("🎉 Welcome back!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password")
                else:
                    st.warning("⚠️ Please fill in all fields")
    
    with tab2:
        st.markdown("### Join the Community! 🌱")
        
        with st.form("signup_form"):
            new_username = st.text_input("Choose Username", placeholder="Pick a unique username")
            new_password = st.text_input("Create Password", type="password", placeholder="Create a secure password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
            
            signup_button = st.form_submit_button("🌟 Create My Account")
            
            if signup_button:
                if new_username and new_password and confirm_password:
                    if new_password == confirm_password:
                        if len(new_password) >= 6:
                            success, result = create_user(new_username, new_password)
                            if success:
                                st.session_state.user_id = result
                                st.session_state.username = new_username
                                st.session_state.current_page = 'onboarding'
                                st.success("🎊 Account created successfully!")
                                st.balloons()
                                st.rerun()
                            else:
                                st.error(f"❌ {result}")
                        else:
                            st.warning("⚠️ Password must be at least 6 characters long")
                    else:
                        st.error("❌ Passwords don't match")
                else:
                    st.warning("⚠️ Please fill in all fields")

def show_onboarding_page():
    """Show the onboarding questionnaire"""
    
    st.markdown("# 🌱 Let's Set Up Your Wellness Profile")
    st.markdown("*Help us personalize your digital wellness journey*")
    
    with st.form("onboarding_form"):
        st.markdown("### 😴 Sleep & Lifestyle")
        sleep_hours = st.selectbox(
            "How many hours do you typically sleep?",
            ["Less than 6 hours", "6-7 hours", "7-8 hours", "8+ hours"],
            index=2
        )
        
        eating_habits = st.selectbox(
            "How would you describe your eating habits?",
            ["Very irregular", "Somewhat irregular", "Fairly regular", "Very regular"],
            index=2
        )
        
        st.markdown("### 🎯 Digital Wellness Goals")
        main_goal = st.selectbox(
            "What's your main wellness goal?",
            ["Better sleep quality", "Improved focus & productivity", "Stress reduction", 
             "More nature connection", "Better work-life balance"],
            index=0
        )
        
        mood_after_screen = st.selectbox(
            "How do you usually feel after long screen sessions?",
            ["Energized & focused", "Neutral", "Slightly tired", "Drained & unfocused", "Stressed or anxious"],
            index=2
        )
        
        daily_offline_time = st.selectbox(
            "How much offline time can you realistically commit daily?",
            ["15-30 minutes", "30-60 minutes", "1-2 hours", "2+ hours"],
            index=1
        )
        
        submit_button = st.form_submit_button("🌟 Complete My Profile", use_container_width=True)
        
        if submit_button:
            save_user_profile(
                st.session_state.user_id,
                st.session_state.username,
                sleep_hours,
                eating_habits,
                main_goal,
                mood_after_screen,
                daily_offline_time
            )
            st.success("🎉 Profile created! Welcome to your wellness journey!")
            st.session_state.current_page = 'dashboard'
            st.balloons()
            st.rerun()

def show_dashboard():
    """Show the main dashboard"""
    
    profile = get_user_profile(st.session_state.user_id)
    user_data = get_user_screen_data(st.session_state.user_id)
    
    # Sidebar for daily check-in
    with st.sidebar:
        st.markdown("### 🌿 Daily Wellness Check-in")
        st.markdown(f"*Hello, {st.session_state.username}!* 👋")
        
        with st.form("daily_check_in"):
            today = datetime.now().strftime("%Y-%m-%d")
            
            # Check if already logged today
            today_entry = user_data[user_data['date'] == today]
            has_logged_today = not today_entry.empty
            
            if has_logged_today:
                st.success("✅ Already checked in today!")
                existing = today_entry.iloc[0]
                phone_default = float(existing['phone'])
                laptop_default = float(existing['laptop'])
                tablet_default = float(existing['tablet'])
                mood_default = existing['mood']
            else:
                phone_default = 0.0
                laptop_default = 0.0
                tablet_default = 0.0
                mood_default = MOODS[1]
            
            st.markdown("#### ⏰ Screen Time Today")
            phone = st.number_input("📱 Phone (hours)", min_value=0.0, max_value=24.0, value=phone_default, step=0.5)
            laptop = st.number_input("💻 Laptop (hours)", min_value=0.0, max_value=24.0, value=laptop_default, step=0.5)
            tablet = st.number_input("📟 Tablet (hours)", min_value=0.0, max_value=24.0, value=tablet_default, step=0.5)
            
            total = phone + laptop + tablet
            st.markdown(f"**Total: {total:.1f} hours**")
            
            st.markdown("#### 🎭 Current Mood")
            mood = st.selectbox("How are you feeling?", MOODS, index=MOODS.index(mood_default) if mood_default in MOODS else 1)
            
            st.markdown("#### 📝 Optional Notes")
            notes = st.text_area("Any thoughts about today?", placeholder="How did screen time affect you?", height=80)
            
            submitted = st.form_submit_button("💾 Save Today's Check-in", use_container_width=True)
            
            if submitted:
                save_daily_entry(st.session_state.user_id, phone, laptop, tablet, mood, notes)
                st.success("🎉 Check-in saved!")
                st.rerun()
        
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    # Main dashboard content
    st.markdown("# 🌿 Your Digital Wellness Dashboard")
    greet_name = profile.get("username", "Friend") if profile else "Friend"
    goal_text = profile.get("main_goal", "Better balance") if profile else "Better balance"
    st.markdown(f"*Hi {greet_name}, focusing on: **{goal_text}***")
    
    # Daily wellness tip
    daily_quote = random.choice(WELLNESS_QUOTES)
    st.markdown(f"""
    <div class="wellness-tip">
        <h4>💡 Today's Wellness Wisdom</h4>
        <p><em>{daily_quote}</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress metrics
    if not user_data.empty:
        streak_days = len(user_data)
        st.markdown(f"### 🔥 Tracking Streak: {streak_days} days 🌱")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_total = user_data['total_screen'].mean()
            st.metric("📊 Average Screen Time", f"{avg_total:.1f} hrs/day")
        
        with col2:
            avg_phone = user_data['phone'].mean()
            st.metric("📱 Phone Usage", f"{avg_phone:.1f} hrs/day")
        
        with col3:
            most_common_mood = user_data['mood'].mode().iloc[0] if not user_data['mood'].mode().empty else "😌 Calm"
            mood_emoji = most_common_mood.split()[0] if most_common_mood else "😌"
            st.metric("🎭 Dominant Mood", mood_emoji)
        
        with col4:
            if len(user_data) >= 2:
                recent_avg = user_data.tail(3)['total_screen'].mean()
                older_avg = user_data.head(-3)['total_screen'].mean() if len(user_data) > 3 else recent_avg
                change = recent_avg - older_avg
                trend_emoji = "📉" if change < 0 else "📈"
                st.metric("📈 Recent Trend", f"{change:+.1f} hrs")
            else:
                st.metric("📈 Recent Trend", "Building data...")
    else:
        st.info("📈 **Start tracking today to see your progress metrics!** Use the sidebar to log your first day.")
    
    # Insights and suggestions
    if not user_data.empty:
        st.markdown("---")
        st.markdown("### 🔍 Your Personal Insights 🌟")
        
        recent_avg = user_data.tail(3)['total_screen'].mean()
        
        if recent_avg < 4:
            insight = "🎉 Excellent! You're maintaining healthy screen time levels."
        elif recent_avg < 6:
            insight = "👍 Good balance! Consider the 20-20-20 rule: every 20 minutes, look at something 20 feet away for 20 seconds."
        else:
            insight = "⚠️ High screen time detected. Try setting hourly reminders for breaks."
        
        st.info(insight)
        
        # Activity suggestion
        st.markdown("### 🎯 Your Mindful Activity Right Now 🌿")
        activities = {
            "Stressed": ["Take 10 deep breaths", "Go for a 5-minute walk", "Listen to calming music"],
            "Tired": ["Take a power nap", "Drink water and stretch", "Step outside for fresh air"],
            "Happy": ["Call a friend", "Write in a journal", "Take photos of nature"],
            "Focused": ["Tackle a creative project", "Read a book", "Learn something new"]
        }
        
        if len(user_data) > 0:
            recent_mood = user_data.iloc[-1]['mood']
            mood_key = next((key for key in activities.keys() if key in recent_mood), "Focused")
            suggestion = random.choice(activities[mood_key])
            st.success(f"💡 **Suggested activity:** {suggestion}")
        else:
            st.info("🌱 Log your mood in the sidebar to get personalized activity suggestions!")
    
    # Charts (if enough data)
    if len(user_data) >= 3:
        st.markdown("---")
        st.markdown("### 📈 Your Screen Time Journey 📊")
        
        if len(user_data) >= 7:
            recent_data = user_data.tail(7)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(recent_data['date'], recent_data['phone'], marker='o', label='📱 Phone', linewidth=2, color='#FF6B35')
            ax.plot(recent_data['date'], recent_data['laptop'], marker='s', label='💻 Laptop', linewidth=2, color='#4CAF50')
            ax.plot(recent_data['date'], recent_data['tablet'], marker='^', label='📟 Tablet', linewidth=2, color='#2196F3')
            
            ax.set_xlabel('Date', fontsize=12)
            ax.set_ylabel('Hours', fontsize=12)
            ax.set_title('7-Day Screen Time Breakdown', fontsize=14, fontweight='bold', color='#2C6E49')
            ax.legend(fontsize=10)
            ax.grid(True, alpha=0.3, color='#A8D5BA')
            ax.set_facecolor('#F9FFF9')
            fig.set_facecolor('#F9FFF9')
            
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.info(f"🔓 **Visual insights unlock after 7 days of tracking!** ({len(user_data)}/7 days complete)")
    
    # 7-Day Challenge
    st.markdown("---")
    st.markdown("### 🏆 Your 7-Day Wellness Challenge 🎯")
    
    challenges = [
        "📱 Day 1: Phone-free dinner - Enjoy a meal without any devices",
        "🚶 Day 2: Take a 20-minute walk without any devices",
        "🌙 Day 3: No screens 1 hour before bedtime",
        "📝 Day 4: Write in a journal for 10 minutes (offline)",
        "🧘 Day 5: Start the day with 5 minutes of meditation",
        "🌿 Day 6: Spend 30 minutes in nature without devices",
        "🎯 Day 7: Complete a creative hobby offline for 45 minutes"
    ]
    
    for i, challenge in enumerate(challenges, 1):
        is_completed = len(user_data) >= i
        status = "✅" if is_completed else "⏳"
        st.markdown(f"{status} {challenge}")
    
    if len(user_data) >= 7:
        st.success("🎉 Congratulations! You've completed your first week of digital wellness tracking!")
        st.balloons()

# --- Main App Logic ---

# Check user authentication and profile status
if st.session_state.user_id is None:
    if st.session_state.current_page == 'landing':
        show_landing_page()
        if st.button("🚀 Get Started", use_container_width=True, type="primary"):
            st.session_state.current_page = 'auth'
            st.rerun()
    elif st.session_state.current_page == 'auth':
        show_auth_page()
        if st.button("← Back to Home"):
            st.session_state.current_page = 'landing'
            st.rerun()
else:
    # User is logged in
    if st.session_state.current_page == 'check_profile':
        profile = get_user_profile(st.session_state.user_id)
        if not profile or not profile.get('onboarding_complete', False):
            st.session_state.current_page = 'onboarding'
        else:
            st.session_state.current_page = 'dashboard'
        st.rerun()
    elif st.session_state.current_page == 'onboarding':
        show_onboarding_page()
    elif st.session_state.current_page == 'dashboard':
        show_dashboard()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9em; margin-top: 2rem;">
    🌿 <strong>Digital Detox Companion</strong> - Your mindful journey to digital wellness<br>
    <em>All data is stored locally on your device for complete privacy</em> 🔒
</div>
""", unsafe_allow_html=True)
