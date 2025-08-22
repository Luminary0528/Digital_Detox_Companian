import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# --- Badge System Functions ---

def get_achievements():
    """Define all available achievements and their requirements"""
    return {
        "first_day": {
            "name": "🌱 Digital Seedling",
            "description": "Complete your first day of tracking",
            "requirement": 1,
            "type": "days_logged"
        },
        "week_warrior": {
            "name": "🗓️ Week Warrior", 
            "description": "Track for 7 consecutive days",
            "requirement": 7,
            "type": "days_logged"
        },
        "mindful_month": {
            "name": "🌙 Mindful Month",
            "description": "Track for 30 days",
            "requirement": 30,
            "type": "days_logged"
        },
        "screen_reducer": {
            "name": "📉 Screen Reducer",
            "description": "Reduce daily screen time by 2+ hours",
            "requirement": 2.0,
            "type": "screen_reduction"
        },
        "balance_master": {
            "name": "⚖️ Balance Master",
            "description": "Maintain under 4 hours daily for a week",
            "requirement": 4.0,
            "type": "weekly_average"
        },
        "mood_stabilizer": {
            "name": "😌 Mood Stabilizer",
            "description": "Log 'Peaceful' or 'Focused' mood 5 times",
            "requirement": 5,
            "type": "positive_moods"
        },
        "early_bird": {
            "name": "🌅 Early Bird",
            "description": "Log data before 9 AM three times",
            "requirement": 3,
            "type": "early_logging"
        },
        "consistent_tracker": {
            "name": "🎯 Consistent Tracker",
            "description": "No missed days in 2 weeks",
            "requirement": 14,
            "type": "consecutive_days"
        }
    }

def init_achievements_file():
    """Initialize achievements CSV file if it doesn't exist"""
    file_path = "user_achievements.csv"
    if not os.path.exists(file_path):
        df = pd.DataFrame(columns=['user_id', 'achievement_id', 'earned_date', 'achievement_name'])
        df.to_csv(file_path, index=False)

def check_achievements(user_id, user_data, profile):
    """Check which achievements user has earned"""
    init_achievements_file()
    achievements = get_achievements()
    earned_achievements = get_user_achievements(user_id)
    earned_ids = set(earned_achievements['achievement_id'].tolist())
    
    new_achievements = []
    
    for achievement_id, achievement in achievements.items():
        if achievement_id in earned_ids:
            continue  # Already earned
            
        earned = False
        
        if achievement['type'] == 'days_logged':
            earned = len(user_data) >= achievement['requirement']
            
        elif achievement['type'] == 'screen_reduction':
            if len(user_data) >= 2:
                first_day = user_data.iloc[0]['total_screen']
                recent_avg = user_data.tail(3)['total_screen'].mean()
                reduction = first_day - recent_avg
                earned = reduction >= achievement['requirement']
                
        elif achievement['type'] == 'weekly_average':
            if len(user_data) >= 7:
                week_avg = user_data.tail(7)['total_screen'].mean()
                earned = week_avg <= achievement['requirement']
                
        elif achievement['type'] == 'positive_moods':
            positive_moods = user_data[user_data['mood'].str.contains('Peaceful|Focused', na=False)]
            earned = len(positive_moods) >= achievement['requirement']
            
        elif achievement['type'] == 'early_logging':
            # This would need timestamp data - simplified for now
            earned = len(user_data) >= achievement['requirement']
            
        elif achievement['type'] == 'consecutive_days':
            if len(user_data) >= achievement['requirement']:
                # Check if dates are consecutive
                dates = pd.to_datetime(user_data['date']).sort_values()
                consecutive = all((dates.iloc[i] - dates.iloc[i-1]).days == 1 
                                for i in range(1, len(dates)))
                earned = consecutive
        
        if earned:
            award_achievement(user_id, achievement_id, achievement['name'])
            new_achievements.append(achievement)
    
    return new_achievements

def award_achievement(user_id, achievement_id, achievement_name):
    """Award an achievement to a user"""
    achievements_df = pd.read_csv("user_achievements.csv")
    new_achievement = pd.DataFrame([{
        'user_id': user_id,
        'achievement_id': achievement_id,
        'earned_date': datetime.now().strftime("%Y-%m-%d"),
        'achievement_name': achievement_name
    }])
    achievements_df = pd.concat([achievements_df, new_achievement], ignore_index=True)
    achievements_df.to_csv("user_achievements.csv", index=False)

def get_user_achievements(user_id):
    """Get all achievements for a specific user"""
    if not os.path.exists("user_achievements.csv"):
        return pd.DataFrame()
    achievements_df = pd.read_csv("user_achievements.csv")
    return achievements_df[achievements_df['user_id'] == user_id]

def display_achievements_page():
    """Display the achievements page"""
    st.markdown("# 🏆 Your Achievements")
    
    if 'user_id' not in st.session_state:
        st.error("Please log in first")
        st.switch_page("login_page.py")
        return
    
    # Custom CSS for achievement badges
    st.markdown("""
    <style>
    .achievement-badge {
        background: linear-gradient(135deg, #FFD700, #FFA500);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 5px solid #FF6B35;
    }
    .achievement-locked {
        background: linear-gradient(135deg, #E8E8E8, #D0D0D0);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 5px solid #999;
        opacity: 0.6;
    }
    .progress-bar {
        background-color: #E8E8E8;
        border-radius: 10px;
        height: 20px;
        overflow: hidden;
        margin: 10px 0;
    }
    .progress-fill {
        background: linear-gradient(90deg, #4CAF50, #2E7D32);
        height: 100%;
        transition: width 0.3s ease;
    }
    </style>
    """, unsafe_allow_html=True)
    
    user_id = st.session_state.user_id
    user_achievements = get_user_achievements(user_id)
    all_achievements = get_achievements()
    
    # Load user data for progress calculation
    if os.path.exists("daily_screen_time.csv"):
        screen_data = pd.read_csv("daily_screen_time.csv")
        user_data = screen_data[screen_data['user_id'] == user_id]
    else:
        user_data = pd.DataFrame()
    
    st.markdown("### 🌟 Earned Badges")
    
    if not user_achievements.empty:
        for _, achievement in user_achievements.iterrows():
            st.markdown(f"""
            <div class="achievement-badge">
                <h4>{achievement['achievement_name']}</h4>
                <p>Earned on: {achievement['earned_date']}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("🎯 No achievements earned yet! Start tracking to unlock your first badge.")
    
    st.markdown("### 🎯 Available Achievements")
    
    earned_ids = set(user_achievements['achievement_id'].tolist()) if not user_achievements.empty else set()
    
    for achievement_id, achievement in all_achievements.items():
        is_earned = achievement_id in earned_ids
        
        if not is_earned:
            # Calculate progress
            progress = 0
            if achievement['type'] == 'days_logged':
                progress = min(len(user_data) / achievement['requirement'], 1.0)
            elif achievement['type'] == 'screen_reduction' and len(user_data) >= 2:
                first_day = float(user_data.iloc[0]['total_screen'])
                recent_avg = float(user_data.tail(3)['total_screen'].mean())
                reduction = max(0, first_day - recent_avg)
                progress = min(reduction / achievement['requirement'], 1.0)
            elif achievement['type'] == 'positive_moods':
                positive_count = len(user_data[user_data['mood'].str.contains('Peaceful|Focused', na=False)])
                progress = min(positive_count / achievement['requirement'], 1.0)
            
            progress_percent = int(progress * 100)
            
            st.markdown(f"""
            <div class="achievement-locked">
                <h4>{achievement['name']}</h4>
                <p>{achievement['description']}</p>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {progress_percent}%"></div>
                </div>
                <small>Progress: {progress_percent}%</small>
            </div>
            """, unsafe_allow_html=True)

# --- Main App Logic ---
if __name__ == "__main__":
    display_achievements_page()
