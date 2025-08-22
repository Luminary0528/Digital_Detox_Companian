import streamlit as st
import pandas as pd
import hashlib
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="📵 Digital Detox Companion - Login",
    page_icon="📵",
    layout="centered"
)

# --- Custom Styling ---
st.markdown("""
    <style>
    body {background-color: #F5F9F6;}
    .main {background-color: #F5F9F6;}
    h1, h2, h3, h4, h5, h6 {color: #2C6E49;}
    .stButton>button {
        background-color: #A8D5BA; 
        color: #2C6E49; 
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    .stTextInput>div>div>input {
        border-radius: 8px;
        border: 1px solid #A8D5BA;
    }
    .login-container {
        background-color: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# --- Constants ---
USERS_FILE = "users.csv"

# --- Helper Functions ---
def init_users_file():
    """Initialize users.csv if it doesn't exist"""
    if not os.path.exists(USERS_FILE):
        df = pd.DataFrame(columns=["user_id", "username", "password_hash"])
        df.to_csv(USERS_FILE, index=False)

def hash_password(password):
    """Hash password using SHA256 (simple but secure for demo)"""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def verify_password(password, hashed):
    """Verify password against hash"""
    return hashlib.sha256(password.encode('utf-8')).hexdigest() == hashed

def create_user(username, password):
    """Create new user account"""
    df = pd.read_csv(USERS_FILE)
    
    # Check if username already exists
    if username in df['username'].values:
        return False, "Username already exists"
    
    # Create new user
    user_id = len(df) + 1
    password_hash = hash_password(password)
    new_user = pd.DataFrame({
        "user_id": [user_id],
        "username": [username],
        "password_hash": [password_hash]
    })
    
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv(USERS_FILE, index=False)
    return True, user_id

def authenticate_user(username, password):
    """Authenticate user login"""
    if not os.path.exists(USERS_FILE):
        return False, None
    
    df = pd.read_csv(USERS_FILE)
    user_row = df[df['username'] == username]
    
    if user_row.empty:
        return False, None
    
    stored_hash = user_row.iloc[0]['password_hash']
    if verify_password(password, stored_hash):
        return True, user_row.iloc[0]['user_id']
    
    return False, None

# --- Initialize Session State ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'username' not in st.session_state:
    st.session_state.username = None

# --- Initialize Files ---
init_users_file()

# --- Main App Logic ---
if st.session_state.authenticated:
    # User is logged in → go to landing (app.py)
    st.switch_page("app.py")
else:
    # Show login/signup page
    st.markdown("# 📵 Digital Detox Companion")
    st.markdown("### Welcome to your mindful digital wellness journey")
    
    # Create tabs for Login and Signup
    tab1, tab2 = st.tabs(["🔐 Login", "✨ Create Account"])
    
    with tab1:
        st.markdown("#### Sign in to your account")
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_submitted = st.form_submit_button("Sign In", use_container_width=True)
            
            if login_submitted:
                if username and password:
                    success, user_id = authenticate_user(username, password)
                    if success:
                        st.session_state.authenticated = True
                        st.session_state.user_id = user_id
                        st.session_state.username = username
                        st.success("Welcome back! Redirecting...")
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
                else:
                    st.error("Please enter both username and password")
    
    with tab2:
        st.markdown("#### Create your digital wellness account")
        with st.form("signup_form"):
            new_username = st.text_input("Choose a Username")
            new_password = st.text_input("Choose a Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            signup_submitted = st.form_submit_button("Create Account", use_container_width=True)
            
            if signup_submitted:
                if new_username and new_password and confirm_password:
                    if new_password != confirm_password:
                        st.error("Passwords don't match")
                    elif len(new_password) < 4:
                        st.error("Password must be at least 4 characters")
                    else:
                        success, result = create_user(new_username, new_password)
                        if success:
                            st.success("Account created successfully! Please login.")
                        else:
                            st.error(result)
                else:
                    st.error("Please fill in all fields")
    
    # --- App Description ---
    st.markdown("---")
    st.markdown("#### 🌱 Why Choose Digital Detox Companion?")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Smart Insights**
        - Links screen time to sleep & mood
        - Discovers your personal patterns
        - Suggests micro-activities
        """)
    
    with col2:
        st.markdown("""
        **Privacy First**
        - All data stays on your device
        - Works completely offline
        - Secure local storage
        """)
    
    st.markdown("#### 🎯 Perfect for:")
    st.markdown("✅ Anyone wanting to reduce screen addiction  \n✅ People in rural areas (works offline)  \n✅ Privacy-conscious users  \n✅ Beginners to digital wellness")
