import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import random
from datetime import datetime, timedelta

# Import achievements functions
try:
    from achievements import check_achievements, get_user_achievements
except ImportError:
    def check_achievements(user_id, user_data, profile):
        return []
    def get_user_achievements(user_id):
        return pd.DataFrame()

# --- Page Configuration ---
st.set_page_config(
    page_title="🌿 Digital Detox Dashboard", 
    page_icon="🌿", 
    layout="wide"
)

# --- Enhanced Nature-Inspired Styling ---
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    
    /* Main Background with Calming Nature Gradient */
    .main {
        background: linear-gradient(135deg, #E8F5E8 0%, #F0F8F0 30%, #E0F2F1 70%, #F1F8E9 100%);
        font-family: 'Inter', sans-serif;
        min-height: 100vh;
    }
    
    /* Semi-transparent overlay for content sections */
    .block-container {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(44, 110, 73, 0.15);
    }
    
    /* Headers with nature theme */
    h1, h2, h3, h4, h5, h6 {
        color: #2C6E49;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
    }
    
    h1 {
        background: linear-gradient(45deg, #2C6E49, #4CAF50);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
    }
    
    /* Custom widgets styling */
    .stSelectbox, .stNumberInput, .stTextArea {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 15px;
        border: 2px solid #A8D5BA;
    }
    
    /* Metrics styling */
    .metric-container {
        background: linear-gradient(135deg, #E8F5E8, #F0F8F0);
        border-radius: 15px;
        padding: 1rem;
        border-left: 5px solid #4CAF50;
        margin: 0.5rem 0;
    }
    
    /* Wellness tip card */
    .wellness-tip {
        background: linear-gradient(135deg, #E3F2FD, #F3E5F5);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 6px solid #FF6B35;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .wellness-tip h4 {
        color: #2C6E49;
        margin-bottom: 0.5rem;
    }
    
    /* Nature decorations */
    .nature-decoration {
        font-size: 1.2em;
        margin: 0 0.5rem;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #4CAF50, #2E7D32);
        color: white;
        border-radius: 25px;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(76, 175, 80, 0.4);
    }
    
    /* Form styling */
    .stForm {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 1.5rem;
        border: 2px solid #A8D5BA;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #E8F5E8, #F0F8F0);
    }
    </style>
""", unsafe_allow_html=True)

# --- Wellness Quotes ---
WELLNESS_QUOTES = [
    "The best time to plant a tree was 20 years ago. The second best time is now. 🌱",
    "In every walk with nature, one receives far more than they seek. 🌿",
    "Your mind is a garden. Your thoughts are the seeds. 🌸",
    "Take time to make your soul happy. 🦋",
    "Breathe in peace, breathe out stress. 🌊",
    "Digital wellness is self-care in the modern age. 📱💚",
    "Small steps daily lead to big changes yearly. 🌟",
    "Your attention is your most valuable resource. 💎",
    "Nature does not hurry, yet everything is accomplished. 🍃",
    "Balance is not something you find, it's something you create. ⚖️"
]

# --- Mood Options ---
MOODS = [
    "😌 Peaceful", "🎯 Focused", "😴 Tired", "😰 Stressed", 
    "😊 Happy", "🤔 Contemplative", "😔 Down", "⚡ Energetic"
]

# --- Helper Functions ---
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

def get_profile():
    """Get user profile data"""
    if not os.path.exists("user_profiles.csv"):
        return None
    
    profiles_df = pd.read_csv("user_profiles.csv")
    user_profile = profiles_df[profiles_df['user_id'] == st.session_state.user_id]
    
    if user_profile.empty:
        return None
    
    return user_profile.iloc[0].to_dict()

def generate_insights(user_data, profile):
    """Generate personalized insights based on user data"""
    if user_data.empty:
        return "🌱 Welcome to your digital wellness journey! Log your first day to start seeing insights."
    
    recent_avg = user_data.tail(3)['total_screen'].mean()
    
    insights = []
    
    # Screen time analysis
    if recent_avg < 4:
        insights.append("🎉 Excellent! You're maintaining healthy screen time levels.")
    elif recent_avg < 6:
        insights.append("👍 Good balance! Consider reducing screen time by 30 minutes daily.")
    else:
        insights.append("⚠️ High screen time detected. Try the 20-20-20 rule: every 20 minutes, look at something 20 feet away for 20 seconds.")
    
    # Mood analysis
    if len(user_data) >= 3:
        recent_moods = user_data.tail(3)['mood'].tolist()
        if any('Stressed' in mood for mood in recent_moods):
            insights.append("🧘 Stress detected. Try 5 minutes of deep breathing or a short walk.")
        elif any('Peaceful' in mood or 'Happy' in mood for mood in recent_moods):
            insights.append("😊 Great to see positive moods! Keep up the good balance.")
    
    # Progress tracking
    if len(user_data) >= 2:
        yesterday = user_data.iloc[-2]['total_screen']
        today = user_data.iloc[-1]['total_screen']
        change = today - yesterday
        
        if change < -0.5:
            insights.append(f"📉 Amazing! You reduced screen time by {abs(change):.1f} hours today!")
        elif change > 1:
            insights.append(f"📈 Screen time increased by {change:.1f} hours. Consider a digital break.")
    
    return " | ".join(insights) if insights else "Keep tracking to unlock personalized insights! 🌟"

def get_personalized_activity(profile, mood, user_data):
    """Generate personalized activity suggestions"""
    activities = {
        "Stressed": ["Take 10 deep breaths", "Go for a 5-minute walk", "Listen to calming music", "Do gentle stretches"],
        "Tired": ["Take a power nap", "Drink water and stretch", "Step outside for fresh air", "Do light yoga"],
        "Happy": ["Call a friend", "Write in a journal", "Take photos of nature", "Plan something fun"],
        "Focused": ["Tackle a creative project", "Read a book", "Learn something new", "Organize your space"]
    }
    
    mood_key = next((key for key in activities.keys() if key in mood), "Focused")
    return random.choice(activities[mood_key])

def get_challenge_plan(profile, user_data):
    """Generate a 7-day personalized challenge"""
    base_challenges = [
        "📱 Day 1: Phone-free dinner - Enjoy a meal without any devices",
        "🚶 Day 2: Take a 20-minute walk without any devices",
        "🌙 Day 3: No screens 1 hour before bedtime",
        "📝 Day 4: Write in a journal for 10 minutes (offline)",
        "🧘 Day 5: Start the day with 5 minutes of meditation",
        "🌿 Day 6: Spend 30 minutes in nature without devices",
        "🎯 Day 7: Complete a creative hobby offline for 45 minutes"
    ]
    
    # Customize based on profile
    if profile and 'main_goal' in profile:
        goal = profile['main_goal'].lower()
        if 'sleep' in goal:
            base_challenges[2] = "🌙 Day 3: No screens 2 hours before bedtime (for better sleep)"
        elif 'focus' in goal:
            base_challenges[4] = "🧘 Day 5: Start with 10 minutes of focused breathing"
        elif 'stress' in goal:
            base_challenges[1] = "🚶 Day 2: Take a stress-relief walk for 25 minutes"
    
    return base_challenges

# --- Main App Logic ---

# Check if user is logged in
if 'user_id' not in st.session_state:
    st.error("Please log in first")
    st.switch_page("login_page.py")

# Check if user has completed profile setup
profile = get_profile()
if not profile:
    st.error("🌿 Please complete your wellness profile first")
    st.switch_page("profile_setup.py")

# --- Initialize Files ---
init_screen_time_file()

# --- Load User Data ---
user_data = get_user_screen_data(st.session_state.user_id)

# --- Sidebar: Daily Check-in Form ---
with st.sidebar:
    st.markdown("### 🌿 Daily Wellness Check-in")
    username = profile.get('username', 'Friend') if profile else 'Friend'
    st.markdown(f"*Hello, {username}!* 👋")
    
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
            mood_default = MOODS[1]  # Default to "Focused"
        
        st.markdown("#### ⏰ Screen Time Today")
        phone = st.number_input("📱 Phone (hours)", min_value=0.0, max_value=24.0, value=phone_default, step=0.5)
        laptop = st.number_input("💻 Laptop (hours)", min_value=0.0, max_value=24.0, value=laptop_default, step=0.5)
        tablet = st.number_input("📟 Tablet (hours)", min_value=0.0, max_value=24.0, value=tablet_default, step=0.5)
        
        total = phone + laptop + tablet
        st.markdown(f"**Total: {total:.1f} hours**")
        
        st.markdown("#### 🎭 Current Mood")
        mood = st.selectbox("How are you feeling?", MOODS, index=MOODS.index(mood_default) if mood_default in MOODS else 1)
        
        st.markdown("#### 📝 Optional Notes")
        notes = st.text_area("Any thoughts about today?", placeholder="Optional: How did screen time affect you today?", height=80)
        
        submitted = st.form_submit_button("💾 Save Today's Check-in", use_container_width=True)
        
        if submitted:
            save_daily_entry(st.session_state.user_id, phone, laptop, tablet, mood, notes)
            
            # Check for new achievements
            new_achievements = check_achievements(st.session_state.user_id, user_data, profile)
            if new_achievements:
                for achievement in new_achievements:
                    st.balloons()
                    st.success(f"🏆 Achievement Unlocked: {achievement['name']}!")
            
            st.success("🎉 Check-in saved!")
            st.rerun()
    
    st.markdown("---")
    
    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏆 Achievements", use_container_width=True):
            st.switch_page("achievements.py")
    with col2:
        if st.button("📊 Export Data", use_container_width=True):
            st.switch_page("data_export.py")
    
    st.markdown("---")
    if st.button("🚪 Logout", use_container_width=True):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.switch_page("login_page.py")

# --- Main Dashboard ---
st.markdown("# 🌿 Your Digital Wellness Dashboard")
greet_name = profile.get("username", "Friend") if profile else "Friend"
goal_text = profile.get("main_goal", "Better balance") if profile else "Better balance"
st.markdown(f"*Hi {greet_name}, focusing on: **{goal_text}***")

# --- Daily Wellness Tip ---
daily_quote = random.choice(WELLNESS_QUOTES)
st.markdown(f"""
<div class="wellness-tip">
    <h4>💡 Today's Wellness Wisdom</h4>
    <p><em>{daily_quote}</em></p>
</div>
""", unsafe_allow_html=True)

# --- Progress Metrics ---
if not user_data.empty:
    streak_days = len(user_data)
    st.markdown(f"### 🔥 Tracking Streak: {streak_days} days <span class='nature-decoration'>🌱</span>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_total = user_data['total_screen'].mean()
        st.metric("📊 Average Screen Time", f"{avg_total:.1f} hrs/day", help="Your daily average across all devices")
    
    with col2:
        avg_phone = user_data['phone'].mean()
        st.metric("📱 Phone Usage", f"{avg_phone:.1f} hrs/day", help="Time spent on mobile device")
    
    with col3:
        most_common_mood = user_data['mood'].mode().iloc[0] if not user_data['mood'].mode().empty else "😌 Calm"
        mood_emoji = most_common_mood.split()[0] if most_common_mood else "😌"
        st.metric("🎭 Dominant Mood", mood_emoji, help="Your most frequent mood this week")
    
    with col4:
        # Show achievements count
        user_achievements = get_user_achievements(st.session_state.user_id)
        achievement_count = len(user_achievements)
        st.metric("🏆 Achievements", f"{achievement_count} earned", help="Click 'Achievements' in sidebar to see all badges")
    
    with col4:
        if len(user_data) >= 2:
            recent_avg = user_data.tail(3)['total_screen'].mean()
            older_avg = user_data.head(-3)['total_screen'].mean()
            change = recent_avg - older_avg
            trend_emoji = "📉" if change < 0 else "📈"
            st.metric("📈 Recent Trend", f"{change:+.1f} hrs", help="Change in recent screen time")
            if change < 0:
                st.success("🎉 Great job reducing screen time!")
else:
    st.info("📈 **Start tracking today to see your progress metrics!** Use the sidebar to log your first day.")

# --- Personalized Insights ---
st.markdown("---")
st.markdown("### 🔍 Your Personal Insights <span class='nature-decoration'>🌟</span>", unsafe_allow_html=True)

if not user_data.empty:
    insight = generate_insights(user_data, profile)
    st.info(insight)

# --- Personalized Activity Suggestion ---
st.markdown("---")
st.markdown("### 🎯 Your Mindful Activity Right Now <span class='nature-decoration'>🌿</span>", unsafe_allow_html=True)

if 'mood' in locals():  # If user just logged mood
    suggestion = get_personalized_activity(profile, mood, user_data)
    user_goal = profile.get('main_goal', 'better wellness') if profile else 'better wellness'
    st.success(f"Based on your {mood.split()[1].lower()} mood and '{user_goal}' goal: **{suggestion}**")
    st.caption("Tip: Take a 5-minute stretch break now to reset your mind.")
else:
    # Show general activity based on recent mood
    if not user_data.empty:
        recent_mood = user_data.iloc[-1]['mood'] if len(user_data) > 0 else "😌 Peaceful"
        suggestion = get_personalized_activity(profile, recent_mood, user_data)
        st.success(f"💡 **Suggested activity:** {suggestion}")
    else:
        st.info("🌱 Log your mood in the sidebar to get personalized activity suggestions!")

# --- Screen Time Visualization ---
if len(user_data) >= 3:
    st.markdown("---")
    st.markdown("### 📈 Your Screen Time Journey <span class='nature-decoration'>📊</span>", unsafe_allow_html=True)
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown("#### 📅 Weekly Trend")
        if len(user_data) >= 7:
            recent_data = user_data.tail(7)
            
            fig, ax = plt.subplots(figsize=(8, 5))
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
            
            # Format dates
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig)
        
        with chart_col2:
            st.markdown("#### 📊 Device Usage Summary")
            device_totals = {
                'Phone': user_data['phone'].sum(),
                'Laptop': user_data['laptop'].sum(),
                'Tablet': user_data['tablet'].sum()
            }
            
            fig2, ax2 = plt.subplots(figsize=(8, 5))
            bars = ax2.bar(device_totals.keys(), device_totals.values(), 
                          color=['#FF6B35', '#4CAF50', '#2196F3'], alpha=0.8)
            
            ax2.set_ylabel('Total Hours', fontsize=12)
            ax2.set_title('Total Usage by Device', fontsize=14, fontweight='bold', color='#2C6E49')
            ax2.set_facecolor('#F9FFF9')
            fig2.set_facecolor('#F9FFF9')
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                        f'{height:.1f}h', ha='center', va='bottom', fontweight='bold')
            
            plt.tight_layout()
            st.pyplot(fig2)
else:
    st.markdown("---")
    st.info(f"🔓 **Visual insights unlock after 3 days of tracking!** ({len(user_data)}/3 days complete) Keep going! 🌱")

# --- 7-Day Challenge Plan ---
st.markdown("---")
st.markdown("### 🏆 Your 7-Day Wellness Challenge <span class='nature-decoration'>🎯</span>", unsafe_allow_html=True)
challenge_goal = profile.get('main_goal', 'digital wellness') if profile else 'digital wellness'
st.markdown(f"*Tailored for your goal: **{challenge_goal}***")

challenge_plan = get_challenge_plan(profile, user_data)

for i, challenge in enumerate(challenge_plan, 1):
    # Mark completed days based on tracking history
    is_completed = len(user_data) >= i
    status = "✅" if is_completed else "⏳"
    st.markdown(f"{status} {challenge}")

if len(user_data) >= 7:
    st.success("🎉 Congratulations! You've completed your first week of digital wellness tracking!")
    st.balloons()
else:
    remaining_days = 7 - len(user_data)
    st.info(f"🌟 {remaining_days} more days to complete your first weekly challenge!")

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9em; margin-top: 2rem;'>
    🌿 <strong>Digital Detox Companion</strong> - Your mindful journey to digital wellness<br>
    <em>All data is stored locally on your device for complete privacy</em> 🔒
</div>
""", unsafe_allow_html=True)
