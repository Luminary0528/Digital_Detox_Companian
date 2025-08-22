import streamlit as st
import pandas as pd
import hashlib
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="🌿 Digital Detox Companion", 
    page_icon="🌿", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Beautiful Landing Page Styling ---
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Hide Streamlit elements for clean landing page */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
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
    
    /* Container for the landing content */
    .landing-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 30px;
        padding: 3rem 2rem;
        margin: 2rem auto;
        max-width: 1000px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.2);
        text-align: center;
    }
    
    /* Hero title styling - using solid color for maximum visibility */
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        color: #1B4332 !important;
        margin-bottom: 1rem;
        font-family: 'Poppins', sans-serif;
        line-height: 1.2;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Subtitle styling */
    .hero-subtitle {
        font-size: 1.4rem;
        color: #2D3748 !important;
        margin-bottom: 2rem;
        font-weight: 400;
        line-height: 1.6;
    }
    
    /* Feature cards */
    .feature-card {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem;
        border-left: 5px solid #4CAF50;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        height: 100%;
    }
    
    .feature-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #1B4332 !important;
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        color: #2D3748 !important;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    
    /* Action buttons styling */
    .action-button {
        background: linear-gradient(45deg, #4CAF50, #2E7D32);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 1rem 3rem;
        font-size: 1.1rem;
        font-weight: 600;
        margin: 0.5rem 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 8px 25px rgba(76, 175, 80, 0.3);
        text-decoration: none;
        display: inline-block;
    }
    
    .action-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(76, 175, 80, 0.4);
        color: white;
        text-decoration: none;
    }
    
    .action-button.secondary {
        background: linear-gradient(45deg, #607D8B, #455A64);
        box-shadow: 0 8px 25px rgba(96, 125, 139, 0.3);
    }
    
    .action-button.secondary:hover {
        box-shadow: 0 12px 35px rgba(96, 125, 139, 0.4);
    }
    
    /* Nature illustration styling */
    .nature-illustration {
        margin: 2rem 0;
        font-size: 4rem;
        line-height: 1;
        opacity: 0.8;
    }
    
    /* Stats section */
    .stats-section {
        background: linear-gradient(135deg, #E8F5E8, #F0F8F0);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
    }
    
    .stat-item {
        text-align: center;
        padding: 1rem;
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2C6E49;
        display: block;
    }
    
    .stat-label {
        color: #666;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    /* Form containers */
    .auth-container {
        background: rgba(255, 255, 255, 0.98);
        border-radius: 25px;
        padding: 2.5rem;
        margin: 2rem auto;
        max-width: 450px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .auth-title {
        font-size: 2rem;
        font-weight: 600;
        color: #2C6E49;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 15px;
        border: 2px solid #A8D5BA;
        padding: 0.8rem;
        font-size: 1rem;
        background: rgba(255, 255, 255, 0.9);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #4CAF50;
        box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
    }
    
    /* Button in forms */
    .stButton > button {
        background: linear-gradient(45deg, #4CAF50, #2E7D32);
        color: white;
        border-radius: 20px;
        border: none;
        padding: 0.8rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(76, 175, 80, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(76, 175, 80, 0.4);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        border-radius: 15px;
        padding: 0.8rem 1.5rem;
        border: 2px solid transparent;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(45deg, #4CAF50, #2E7D32);
        color: white;
        border-color: #4CAF50;
    }
    
    /* Animation classes */
    .fade-in {
        animation: fadeIn 1s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .bounce {
        animation: bounce 2s infinite;
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-10px); }
        60% { transform: translateY(-5px); }
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }
        
        .hero-subtitle {
            font-size: 1.1rem;
        }
        
        .landing-container {
            margin: 1rem;
            padding: 2rem 1.5rem;
        }
        
        .feature-card {
            margin: 0.5rem 0;
        }
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

# --- Landing Page Content ---
def show_landing_page():
    """Display the beautiful landing page"""
    
    st.markdown("""
    <div class="landing-container fade-in">
        <div class="hero-title">
            📵 Digital Detox Companion
        </div>
        <div class="hero-subtitle">
            Your Mindful Digital Wellness Journey Starts Here
        </div>
        
        <div class="nature-illustration bounce">
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
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Smart Tracking</div>
            <div class="feature-desc">
                Monitor your screen time across devices with beautiful visualizations 
                and personalized insights to understand your digital patterns.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🧘</div>
            <div class="feature-title">Mindful Activities</div>
            <div class="feature-desc">
                Receive personalized activity suggestions based on your mood, goals, 
                and current screen time to promote digital wellness.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🏆</div>
            <div class="feature-title">Achievement System</div>
            <div class="feature-desc">
                Earn badges and track your progress through 7-day challenges 
                designed to build healthier digital habits gradually.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Stats section
    st.markdown("""
    <div class="stats-section fade-in">
        <h3 style="text-align: center; color: #2C6E49; margin-bottom: 2rem;">Join the Digital Wellness Movement</h3>
        <div style="display: flex; justify-content: space-around; flex-wrap: wrap;">
            <div class="stat-item">
                <span class="stat-number">4.5</span>
                <div class="stat-label">Hours saved daily on average</div>
            </div>
            <div class="stat-item">
                <span class="stat-number">89%</span>
                <div class="stat-label">Report improved focus</div>
            </div>
            <div class="stat-item">
                <span class="stat-number">7</span>
                <div class="stat-label">Days to build new habits</div>
            </div>
            <div class="stat-item">
                <span class="stat-number">100%</span>
                <div class="stat-label">Privacy protected locally</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_auth_forms():
    """Show login and signup forms in a beautiful design"""
    
    st.markdown('<div class="auth-container fade-in">', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Sign Up"])
    
    with tab1:
        st.markdown('<div class="auth-title">Welcome Back! 🌿</div>', unsafe_allow_html=True)
        
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
                        st.success("🎉 Welcome back! Redirecting to your dashboard...")
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password")
                else:
                    st.warning("⚠️ Please fill in all fields")
    
    with tab2:
        st.markdown('<div class="auth-title">Join the Community! 🌱</div>', unsafe_allow_html=True)
        
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
                                st.success("🎊 Account created successfully! Welcome to Digital Detox Companion!")
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
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- Main App Logic ---

# Initialize session state
if 'user_id' not in st.session_state:
    st.session_state.user_id = None

# Check if user is logged in
if st.session_state.user_id:
    # User is logged in, show the main app content
    # Check if user has completed profile setup
    if not os.path.exists("user_profiles.csv"):
        # Create profiles file
        pd.DataFrame(columns=['user_id', 'username', 'sleep_hours', 'eating_habits', 'main_goal', 
                             'mood_after_screen', 'daily_offline_time', 'onboarding_complete']).to_csv("user_profiles.csv", index=False)
    
    profiles_df = pd.read_csv("user_profiles.csv")
    user_profile = profiles_df[profiles_df['user_id'] == st.session_state.user_id]
    
    if user_profile.empty or not user_profile.iloc[0].get('onboarding_complete', False):
        # Show onboarding
        st.markdown("### 🌿 Welcome! Let's set up your wellness profile")
        st.info("Redirecting to onboarding...")
        if st.button("Continue to Profile Setup"):
            # Switch to profile setup mode
            st.session_state.show_onboarding = True
            st.rerun()
    else:
        # Show dashboard
        st.markdown("### 🌿 Welcome back to your wellness dashboard!")
        st.success("Redirecting to your personalized dashboard...")
        if st.button("Continue to Dashboard"):
            # Switch to dashboard mode
            st.session_state.show_dashboard = True
            st.rerun()
else:
    # Show landing page and authentication
    show_landing_page()
    show_auth_forms()
    
    # Footer
    st.markdown("""
    <div style="text-align: center; margin-top: 3rem; padding: 2rem; color: #666;">
        <p style="font-size: 0.9rem;">
            🔒 <strong>Your Privacy Matters:</strong> All data is stored locally on your device.<br>
            No personal information is sent to external servers.
        </p>
        <p style="font-size: 0.8rem; margin-top: 1rem;">
            Made with ❤️ for digital wellness • © 2025 Digital Detox Companion
        </p>
    </div>
    """, unsafe_allow_html=True)
