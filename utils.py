"""
Utility functions for the Digital Detox Companion app.

This module contains helper functions for:
- CSV data handling and management
- Chart generation and visualization
- Activity suggestions and recommendations
- Data validation and processing
"""

import pandas as pd
import matplotlib.pyplot as plt
import os
import random
from datetime import datetime, timedelta

# --- Data Management Functions ---

def ensure_csv_file(filename, columns):
    """
    Ensure a CSV file exists with the specified columns.
    Creates the file if it doesn't exist.
    
    Args:
        filename (str): The CSV filename
        columns (list): List of column names
    """
    if not os.path.exists(filename):
        df = pd.DataFrame(columns=columns)
        df.to_csv(filename, index=False)

def load_user_data(user_id, filename):
    """
    Load data for a specific user from a CSV file.
    
    Args:
        user_id (int): The user's ID
        filename (str): The CSV filename
        
    Returns:
        pandas.DataFrame: Filtered data for the user
    """
    if not os.path.exists(filename):
        return pd.DataFrame()
    
    df = pd.read_csv(filename)
    return df[df['user_id'] == user_id] if 'user_id' in df.columns else pd.DataFrame()

def save_user_data(data_dict, filename):
    """
    Save user data to a CSV file.
    
    Args:
        data_dict (dict): Dictionary containing the data to save
        filename (str): The CSV filename
    """
    if os.path.exists(filename):
        df = pd.read_csv(filename)
    else:
        df = pd.DataFrame()
    
    new_row = pd.DataFrame([data_dict])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(filename, index=False)

# --- Chart Generation Functions ---

def create_screen_time_chart(user_data, chart_type='line'):
    """
    Create a screen time visualization chart.
    
    Args:
        user_data (pandas.DataFrame): User's screen time data
        chart_type (str): Type of chart ('line', 'bar', 'area')
        
    Returns:
        matplotlib.figure.Figure: The generated chart
    """
    if user_data.empty:
        return None
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Set nature-inspired colors
    colors = ['#FF6B35', '#4CAF50', '#2196F3']
    
    if chart_type == 'line':
        ax.plot(user_data['date'], user_data['phone'], marker='o', label='📱 Phone', 
                linewidth=2, color=colors[0])
        ax.plot(user_data['date'], user_data['laptop'], marker='s', label='💻 Laptop', 
                linewidth=2, color=colors[1])
        ax.plot(user_data['date'], user_data['tablet'], marker='^', label='📟 Tablet', 
                linewidth=2, color=colors[2])
    
    elif chart_type == 'bar':
        width = 0.25
        x = range(len(user_data))
        ax.bar([i - width for i in x], user_data['phone'], width, label='📱 Phone', color=colors[0], alpha=0.8)
        ax.bar(x, user_data['laptop'], width, label='💻 Laptop', color=colors[1], alpha=0.8)
        ax.bar([i + width for i in x], user_data['tablet'], width, label='📟 Tablet', color=colors[2], alpha=0.8)
        ax.set_xticks(x)
        ax.set_xticklabels(user_data['date'])
    
    # Style the chart
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Hours', fontsize=12)
    ax.set_title('Screen Time Trends', fontsize=14, fontweight='bold', color='#2C6E49')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3, color='#A8D5BA')
    ax.set_facecolor('#F9FFF9')
    fig.set_facecolor('#F9FFF9')
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    return fig

def create_mood_chart(user_data):
    """
    Create a mood distribution pie chart.
    
    Args:
        user_data (pandas.DataFrame): User's mood data
        
    Returns:
        matplotlib.figure.Figure: The generated chart
    """
    if user_data.empty or 'mood' not in user_data.columns:
        return None
    
    mood_counts = user_data['mood'].value_counts()
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Nature-inspired colors for moods
    colors = ['#A8D5BA', '#81C784', '#4CAF50', '#66BB6A', '#8BC34A', '#CDDC39', '#FFC107', '#FF8A65']
    
    wedges, texts, autotexts = ax.pie(mood_counts.values, labels=mood_counts.index, 
                                     autopct='%1.1f%%', startangle=90, 
                                     colors=colors[:len(mood_counts)])
    
    ax.set_title('Mood Distribution', fontsize=14, fontweight='bold', color='#2C6E49')
    fig.set_facecolor('#F9FFF9')
    
    return fig

# --- Activity Suggestion Functions ---

def get_activity_suggestions():
    """
    Get a comprehensive list of mindful activities organized by category.
    
    Returns:
        dict: Activities organized by mood and goal categories
    """
    return {
        'stress_relief': [
            "Take 10 deep breaths and count each one",
            "Step outside for 5 minutes of fresh air",
            "Do gentle neck and shoulder stretches",
            "Listen to calming nature sounds",
            "Practice the 5-4-3-2-1 grounding technique",
            "Write down three things you're grateful for",
            "Make a warm cup of herbal tea mindfully"
        ],
        'energy_boost': [
            "Take a 10-minute walk around the block",
            "Do 20 jumping jacks or push-ups",
            "Drink a large glass of water",
            "Step into bright natural light",
            "Do energizing yoga poses",
            "Listen to upbeat music and dance",
            "Call a friend who makes you laugh"
        ],
        'focus_enhancement': [
            "Organize your workspace for 5 minutes",
            "Practice meditation for 5-10 minutes",
            "Do a brain dump: write all thoughts on paper",
            "Use the Pomodoro Technique for your next task",
            "Clear mental clutter with a quick brain dump",
            "Set three priorities for the rest of the day",
            "Practice mindful breathing for 3 minutes"
        ],
        'creativity_boost': [
            "Sketch or doodle for 10 minutes",
            "Write in a journal about your day",
            "Take photos of interesting things around you",
            "Try a new recipe or cooking technique",
            "Rearrange furniture or decorations",
            "Start a new creative project",
            "Brainstorm solutions to a current challenge"
        ],
        'social_connection': [
            "Send a thoughtful message to someone you care about",
            "Call a family member or old friend",
            "Write a handwritten note or letter",
            "Plan a future activity with someone",
            "Share a meal with others",
            "Join a local community group or class",
            "Volunteer for a cause you care about"
        ],
        'nature_connection': [
            "Water your plants or tend to a garden",
            "Sit outside and observe nature for 10 minutes",
            "Take a barefoot walk on grass",
            "Watch clouds or stars",
            "Collect interesting leaves, stones, or shells",
            "Feed birds or watch wildlife",
            "Plan a future outdoor adventure"
        ]
    }

def get_personalized_suggestion(profile, mood, screen_time_today=0):
    """
    Get a personalized activity suggestion based on user profile and current state.
    
    Args:
        profile (dict): User's profile information
        mood (str): Current mood
        screen_time_today (float): Hours of screen time today
        
    Returns:
        str: Personalized activity suggestion
    """
    activities = get_activity_suggestions()
    
    # Determine activity category based on mood and goals
    if 'Stressed' in mood or 'Down' in mood:
        category = 'stress_relief'
    elif 'Tired' in mood:
        category = 'energy_boost'
    elif 'Focused' in mood or 'Contemplative' in mood:
        category = 'focus_enhancement'
    elif 'Happy' in mood or 'Energetic' in mood:
        category = 'creativity_boost'
    else:
        category = 'nature_connection'  # Default
    
    # Adjust based on user's main goal
    if profile and 'main_goal' in profile:
        goal = profile['main_goal'].lower()
        if 'nature' in goal or 'outdoors' in goal:
            category = 'nature_connection'
        elif 'social' in goal or 'connection' in goal:
            category = 'social_connection'
        elif 'productivity' in goal or 'focus' in goal:
            category = 'focus_enhancement'
    
    # If high screen time, prioritize nature/physical activities
    if screen_time_today > 6:
        category = random.choice(['nature_connection', 'energy_boost'])
    
    return random.choice(activities[category])

# --- Data Validation Functions ---

def validate_screen_time_input(phone, laptop, tablet):
    """
    Validate screen time input values.
    
    Args:
        phone (float): Phone screen time in hours
        laptop (float): Laptop screen time in hours
        tablet (float): Tablet screen time in hours
        
    Returns:
        tuple: (is_valid, error_message)
    """
    try:
        phone = float(phone)
        laptop = float(laptop)
        tablet = float(tablet)
        
        if any(val < 0 for val in [phone, laptop, tablet]):
            return False, "Screen time cannot be negative"
        
        if any(val > 24 for val in [phone, laptop, tablet]):
            return False, "Screen time cannot exceed 24 hours per day"
        
        total = phone + laptop + tablet
        if total > 24:
            return False, "Total screen time cannot exceed 24 hours per day"
        
        return True, ""
    
    except (ValueError, TypeError):
        return False, "Please enter valid numbers for screen time"

def calculate_weekly_stats(user_data):
    """
    Calculate weekly statistics from user data.
    
    Args:
        user_data (pandas.DataFrame): User's screen time data
        
    Returns:
        dict: Weekly statistics
    """
    if user_data.empty:
        return {}
    
    recent_week = user_data.tail(7) if len(user_data) >= 7 else user_data
    
    stats = {
        'avg_daily_total': recent_week['total_screen'].mean(),
        'avg_phone': recent_week['phone'].mean(),
        'avg_laptop': recent_week['laptop'].mean(),
        'avg_tablet': recent_week['tablet'].mean(),
        'days_tracked': len(recent_week),
        'most_common_mood': recent_week['mood'].mode().iloc[0] if not recent_week['mood'].mode().empty else "Unknown"
    }
    
    # Calculate trend
    if len(user_data) >= 14:
        previous_week = user_data.iloc[-14:-7]['total_screen'].mean()
        current_week = recent_week['total_screen'].mean()
        stats['trend'] = current_week - previous_week
    else:
        stats['trend'] = 0
    
    return stats

# --- Insight Generation Functions ---

def generate_insight_messages(user_data, profile):
    """
    Generate personalized insight messages based on user data patterns.
    
    Args:
        user_data (pandas.DataFrame): User's tracking data
        profile (dict): User's profile information
        
    Returns:
        list: List of insight messages
    """
    insights = []
    
    if user_data.empty:
        return ["🌱 Welcome to your digital wellness journey! Start tracking to unlock personalized insights."]
    
    stats = calculate_weekly_stats(user_data)
    
    # Screen time insights
    if stats['avg_daily_total'] < 4:
        insights.append("🎉 Excellent! You're maintaining healthy screen time levels.")
    elif stats['avg_daily_total'] < 6:
        insights.append("👍 Good balance! Consider the 20-20-20 rule for eye health.")
    else:
        insights.append("⚠️ Consider setting screen time boundaries. Try shorter, focused sessions.")
    
    # Trend insights
    if 'trend' in stats and stats['trend'] < -0.5:
        insights.append(f"📉 Great progress! You've reduced screen time by {abs(stats['trend']):.1f} hours this week.")
    elif 'trend' in stats and stats['trend'] > 1:
        insights.append("📈 Screen time increased this week. What strategies might help you refocus?")
    
    # Mood insights
    if 'Peaceful' in stats['most_common_mood'] or 'Happy' in stats['most_common_mood']:
        insights.append("😊 Your positive mood patterns are wonderful to see!")
    elif 'Stressed' in stats['most_common_mood']:
        insights.append("🧘 Consider incorporating stress-relief activities between screen sessions.")
    
    # Device-specific insights
    if stats['avg_phone'] > stats['avg_laptop'] + stats['avg_tablet']:
        insights.append("📱 Phone is your primary device. Try phone-free zones during meals.")
    
    return insights if insights else ["Keep tracking to discover patterns in your digital wellness journey! 🌟"]

# --- Export Helper Functions ---

def prepare_export_data(user_id):
    """
    Prepare user data for export across all CSV files.
    
    Args:
        user_id (int): The user's ID
        
    Returns:
        dict: Dictionary containing all user data
    """
    export_data = {
        'profile': load_user_data(user_id, 'user_profiles.csv'),
        'screen_time': load_user_data(user_id, 'daily_screen_time.csv'),
        'achievements': load_user_data(user_id, 'user_achievements.csv') if os.path.exists('user_achievements.csv') else pd.DataFrame()
    }
    
    return export_data

# --- Challenge Generation Functions ---

def generate_weekly_challenges(profile):
    """
    Generate personalized 7-day challenges based on user profile.
    
    Args:
        profile (dict): User's profile information
        
    Returns:
        list: List of 7 daily challenges
    """
    base_challenges = [
        "📱 Day 1: Try phone-free meals today",
        "🚶 Day 2: Take a 15-minute walk without devices",
        "🌙 Day 3: No screens 1 hour before bedtime",
        "📝 Day 4: Write or journal offline for 10 minutes",
        "🧘 Day 5: Start the day with 5 minutes of mindfulness",
        "🌿 Day 6: Spend 20 minutes in nature device-free",
        "🎯 Day 7: Complete a creative hobby offline"
    ]
    
    # Customize based on user's main goal
    if profile and 'main_goal' in profile:
        goal = profile['main_goal'].lower()
        
        if 'sleep' in goal:
            base_challenges[2] = "🌙 Day 3: Create a calming bedtime routine (no screens 2 hours before bed)"
            base_challenges[4] = "🛏️ Day 5: Practice bedroom device boundaries"
        
        elif 'nature' in goal:
            base_challenges[1] = "🌲 Day 2: Explore a new outdoor space for 20 minutes"
            base_challenges[5] = "🌺 Day 6: Garden, observe plants, or collect natural objects"
        
        elif 'productivity' in goal:
            base_challenges[3] = "⚡ Day 4: Use time-blocking technique for focused work"
            base_challenges[6] = "🎯 Day 7: Complete deep work session without digital distractions"
        
        elif 'stress' in goal:
            base_challenges[0] = "🕯️ Day 1: Practice mindful eating without distractions"
            base_challenges[4] = "🧘 Day 5: Try a 10-minute stress-relief meditation"
    
    return base_challenges

if __name__ == "__main__":
    # Test functions
    print("Digital Detox Companion Utils loaded successfully! 🌿")
    print(f"Available activity categories: {list(get_activity_suggestions().keys())}")
