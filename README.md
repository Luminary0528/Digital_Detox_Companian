# 🌿 Digital Detox Companion

![Digital Detox Companion](https://img.shields.io/badge/Digital-Wellness-green?style=for-the-badge&logo=leaf) ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white) ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

**Your Mindful Digital Wellness Journey Starts Here** 🌱

A beautiful, privacy-first Streamlit web application designed to help you build a healthier relationship with technology. Track your screen time, discover mindful activities, and transform your digital habits with personalized insights and gentle guidance.

---

## ✨ Features

### 🎨 Beautiful Landing Page
- **Calming Nature Theme**: Soft greenery, animated gradients, and nature-inspired design
- **Glassmorphism UI**: Modern, clean interface with blur effects and smooth animations
- **Responsive Design**: Works perfectly on desktop and mobile browsers

### 🔐 Secure Authentication
- **Privacy-First**: All data stored locally on your device (CSV files)
- **Simple Login/Signup**: Clean tabs with beautiful forms
- **Password Protection**: SHA-256 hashed passwords for security

### 🧑‍💻 Personalized Onboarding
- **Step-by-Step Questions**: Tailored questionnaire to understand your goals
- **Wellness Profile Creation**: Sleep habits, eating patterns, and digital wellness goals
- **Customized Experience**: Personalized dashboard based on your responses

### 📊 Interactive Dashboard
- **Real-time Tracking**: Daily screen time input for phone, laptop, and tablet
- **Beautiful Visualizations**: 7-day trends, device usage breakdown, mood tracking
- **Personal Insights**: AI-generated suggestions based on your patterns
- **Progress Metrics**: Tracking streaks, averages, and improvements

### 🏆 Achievement System
- **Digital Badges**: Earn achievements for consistent tracking and healthy habits
- **Progress Tracking**: Visual progress bars and milestone celebrations
- **7-Day Challenges**: Personalized challenges based on your wellness goals

### 🎯 Mindful Activities
- **Mood-Based Suggestions**: Activities tailored to your current emotional state
- **Goal-Oriented**: Recommendations aligned with your wellness objectives
- **Offline Focus**: Encouraging real-world activities and digital breaks

### 📈 Data Export & Analysis
- **Multiple Formats**: Export data as CSV, JSON, or Excel workbooks
- **Comprehensive Reports**: Detailed summary of your digital wellness journey
- **Data Portability**: Take your data anywhere, maintain full control

---

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- Web browser (Chrome, Firefox, Safari, Edge)

### Installation

1. **Clone or Download** the repository:
   ```bash
   git clone https://github.com/yourusername/Digital_Detox_Companion.git
   cd Digital_Detox_Companion
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   streamlit run landing_page.py
   ```

4. **Open Your Browser**:
   - The app will automatically open at `http://localhost:8501`
   - If it doesn't open automatically, visit the URL shown in your terminal

### First Time Setup

1. **Create Account**: Use the "Sign Up" tab to create your account
2. **Complete Onboarding**: Answer the wellness questionnaire (takes 2-3 minutes)
3. **Start Tracking**: Log your first day's screen time and mood
4. **Explore Features**: Check out achievements, export data, and discover insights

---

## 📱 How to Use

### Daily Workflow
1. **Morning Check-in**: Set your intention for the day
2. **Track Throughout Day**: Note screen time for each device
3. **Evening Reflection**: Log your mood and any observations
4. **Review Insights**: Check personalized suggestions and progress

### Weekly Review
- **View Trends**: Analyze your 7-day screen time patterns
- **Complete Challenges**: Work through your personalized detox challenges
- **Earn Achievements**: Unlock badges for consistent healthy habits
- **Export Data**: Download reports to track long-term progress

---

## 🛠️ Technical Details

### Architecture
- **Frontend**: Streamlit (Python web framework)
- **Data Storage**: Local CSV files (no external database)
- **Visualization**: Matplotlib for charts and graphs
- **Styling**: Custom CSS with nature-inspired themes

### File Structure
```
Digital_Detox_Companion/
├── landing_page.py          # Beautiful landing page with auth
├── app.py                   # Main routing logic
├── profile_setup.py         # Onboarding questionnaire
├── digital_detox.py         # Main dashboard
├── achievements.py          # Badge system and progress tracking
├── data_export.py          # Data export functionality
├── assets/                  # Local images and resources
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── Data Files (auto-generated):
    ├── users.csv           # User accounts
    ├── user_profiles.csv   # Onboarding responses
    ├── daily_screen_time.csv  # Daily tracking data
    └── user_achievements.csv  # Earned badges
```

### Dependencies
- **streamlit**: Web application framework
- **pandas**: Data manipulation and CSV handling
- **matplotlib**: Chart generation and visualization
- **xlsxwriter**: Excel export functionality

---

## 🎨 Design Philosophy

### Nature-Inspired Wellness
- **Calming Colors**: Soft greens, blues, and earth tones
- **Organic Shapes**: Rounded corners, flowing gradients
- **Peaceful Interactions**: Smooth animations, gentle feedback

### Privacy by Design
- **Local Storage**: All data remains on your device
- **No Tracking**: No analytics, cookies, or external requests
- **Full Control**: Export, delete, or modify your data anytime

### Gentle Guidance
- **Non-Judgmental**: Positive encouragement, not guilt or shame
- **Realistic Goals**: Small, achievable steps toward better habits
- **Personal Agency**: You choose your goals and pace

---

## 🔒 Privacy & Security

### Data Protection
- **Local Only**: All data stored in CSV files on your computer
- **No Cloud Sync**: Nothing sent to external servers
- **Password Security**: SHA-256 hashed passwords
- **Complete Control**: Delete or export your data anytime

### What We Don't Collect
- ❌ No personal information beyond what you provide
- ❌ No browsing history or app usage data
- ❌ No location tracking
- ❌ No third-party analytics

---

## 📞 Support

Need help? Here are your options:

1. **Check the FAQ**: Common questions answered below
2. **Create an Issue**: Report bugs or request features on GitHub
3. **Read the Code**: Everything is open source and documented

---

## ❓ Frequently Asked Questions

### Q: Is my data safe?
**A**: Yes! All data is stored locally on your computer. Nothing is sent to external servers.

### Q: Can I use this offline?
**A**: The app requires an internet connection to load initially, but all your data is local.

### Q: How do I backup my data?
**A**: Use the "Export Data" feature to download all your information in multiple formats.

### Q: Can I delete my account?
**A**: Simply delete the CSV files or use the export feature to save your data first.

### Q: Does this work on mobile?
**A**: Yes! The web interface is responsive and works great on mobile browsers.

---

**Made with ❤️ for digital wellness** • Start your mindful technology journey today! 🌿✨
