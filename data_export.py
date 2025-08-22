import streamlit as st
import pandas as pd
import os
from datetime import datetime
import zipfile
import io

def create_data_export():
    """Create a comprehensive data export for the user"""
    if 'user_id' not in st.session_state:
        st.error("Please log in first")
        return
    
    st.markdown("# 📊 Export Your Data")
    st.markdown("Download all your digital wellness tracking data in various formats.")
    
    user_id = st.session_state.user_id
    
    # Load all user data
    profile_data = get_user_profile_data(user_id)
    screen_data = get_user_screen_data(user_id)
    achievements_data = get_user_achievements_data(user_id)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📁 Available Data")
        st.markdown(f"- **Profile Information**: {len(profile_data)} record(s)")
        st.markdown(f"- **Screen Time Logs**: {len(screen_data)} day(s)")
        st.markdown(f"- **Achievements**: {len(achievements_data)} earned")
        
        st.markdown("### 📋 Export Options")
        export_format = st.selectbox("Choose format:", ["CSV Files (ZIP)", "JSON", "Excel Workbook"])
        include_summary = st.checkbox("Include summary report", value=True)
    
    with col2:
        st.markdown("### 📈 Data Preview")
        if not screen_data.empty:
            st.markdown("**Recent Screen Time:**")
            st.dataframe(screen_data.tail(5), use_container_width=True)
        else:
            st.info("No screen time data yet")
    
    if st.button("🔽 Download My Data", type="primary", use_container_width=True):
        if screen_data.empty and profile_data.empty:
            st.warning("No data to export yet. Start tracking to build your data!")
            return
        
        try:
            if export_format == "CSV Files (ZIP)":
                zip_buffer = create_csv_zip(user_id, profile_data, screen_data, achievements_data, include_summary)
                st.download_button(
                    label="📥 Download ZIP Archive",
                    data=zip_buffer.getvalue(),
                    file_name=f"digital_wellness_data_{user_id}_{datetime.now().strftime('%Y%m%d')}.zip",
                    mime="application/zip"
                )
            
            elif export_format == "JSON":
                json_data = create_json_export(user_id, profile_data, screen_data, achievements_data, include_summary)
                st.download_button(
                    label="📥 Download JSON",
                    data=json_data,
                    file_name=f"digital_wellness_data_{user_id}_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json"
                )
            
            elif export_format == "Excel Workbook":
                excel_buffer = create_excel_export(user_id, profile_data, screen_data, achievements_data, include_summary)
                st.download_button(
                    label="📥 Download Excel",
                    data=excel_buffer.getvalue(),
                    file_name=f"digital_wellness_data_{user_id}_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            
            st.success("✅ Data export ready for download!")
            
        except Exception as e:
            st.error(f"Export failed: {str(e)}")

def get_user_profile_data(user_id):
    """Get user profile data"""
    if os.path.exists("user_profiles.csv"):
        profiles = pd.read_csv("user_profiles.csv")
        return profiles[profiles['user_id'] == user_id]
    return pd.DataFrame()

def get_user_screen_data(user_id):
    """Get user screen time data"""
    if os.path.exists("daily_screen_time.csv"):
        screen_data = pd.read_csv("daily_screen_time.csv")
        return screen_data[screen_data['user_id'] == user_id]
    return pd.DataFrame()

def get_user_achievements_data(user_id):
    """Get user achievements data"""
    if os.path.exists("user_achievements.csv"):
        achievements = pd.read_csv("user_achievements.csv")
        return achievements[achievements['user_id'] == user_id]
    return pd.DataFrame()

def create_summary_report(user_id, profile_data, screen_data):
    """Create a summary report of user's digital wellness journey"""
    report = []
    report.append("DIGITAL WELLNESS SUMMARY REPORT")
    report.append("=" * 40)
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append(f"User ID: {user_id}")
    report.append("")
    
    if not profile_data.empty:
        profile = profile_data.iloc[0]
        report.append("PROFILE INFORMATION:")
        report.append(f"Username: {profile.get('username', 'N/A')}")
        report.append(f"Main Goal: {profile.get('main_goal', 'N/A')}")
        report.append(f"Sleep Schedule: {profile.get('sleep_schedule', 'N/A')}")
        report.append(f"Profile Created: {profile.get('created_date', 'N/A')}")
        report.append("")
    
    if not screen_data.empty:
        report.append("TRACKING STATISTICS:")
        report.append(f"Total Days Tracked: {len(screen_data)}")
        report.append(f"First Entry: {screen_data['date'].min()}")
        report.append(f"Latest Entry: {screen_data['date'].max()}")
        report.append("")
        
        report.append("AVERAGE USAGE:")
        report.append(f"Daily Screen Time: {screen_data['total_screen'].mean():.1f} hours")
        report.append(f"Phone Usage: {screen_data['phone'].mean():.1f} hours")
        report.append(f"Laptop Usage: {screen_data['laptop'].mean():.1f} hours")
        report.append(f"Tablet Usage: {screen_data['tablet'].mean():.1f} hours")
        report.append("")
        
        report.append("MOOD ANALYSIS:")
        mood_counts = screen_data['mood'].value_counts()
        for mood, count in mood_counts.head(3).items():
            report.append(f"{mood}: {count} days ({count/len(screen_data)*100:.1f}%)")
        report.append("")
        
        if len(screen_data) >= 7:
            recent_week = screen_data.tail(7)
            earlier_week = screen_data.head(7)
            recent_avg = recent_week['total_screen'].mean()
            earlier_avg = earlier_week['total_screen'].mean()
            change = recent_avg - earlier_avg
            
            report.append("PROGRESS ANALYSIS:")
            report.append(f"Recent Week Average: {recent_avg:.1f} hours/day")
            report.append(f"Early Week Average: {earlier_avg:.1f} hours/day")
            report.append(f"Change: {change:+.1f} hours/day")
            if change < 0:
                report.append("✅ Great job reducing screen time!")
            elif change > 0:
                report.append("📈 Screen time increased - consider new strategies")
            else:
                report.append("➖ Screen time remained stable")
    
    return "\n".join(report)

def create_csv_zip(user_id, profile_data, screen_data, achievements_data, include_summary):
    """Create a ZIP file with CSV exports"""
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Add CSV files
        if not profile_data.empty:
            profile_csv = profile_data.to_csv(index=False)
            zip_file.writestr("profile_data.csv", profile_csv)
        
        if not screen_data.empty:
            screen_csv = screen_data.to_csv(index=False)
            zip_file.writestr("screen_time_data.csv", screen_csv)
        
        if not achievements_data.empty:
            achievements_csv = achievements_data.to_csv(index=False)
            zip_file.writestr("achievements_data.csv", achievements_csv)
        
        # Add summary report
        if include_summary:
            summary = create_summary_report(user_id, profile_data, screen_data)
            zip_file.writestr("summary_report.txt", summary)
    
    zip_buffer.seek(0)
    return zip_buffer

def create_json_export(user_id, profile_data, screen_data, achievements_data, include_summary):
    """Create JSON export"""
    export_data = {
        "user_id": user_id,
        "export_date": datetime.now().isoformat(),
        "profile": profile_data.to_dict('records') if not profile_data.empty else [],
        "screen_time_logs": screen_data.to_dict('records') if not screen_data.empty else [],
        "achievements": achievements_data.to_dict('records') if not achievements_data.empty else []
    }
    
    if include_summary:
        export_data["summary_report"] = create_summary_report(user_id, profile_data, screen_data)
    
    return pd.Series([export_data]).to_json(orient='records', indent=2)

def create_excel_export(user_id, profile_data, screen_data, achievements_data, include_summary):
    """Create Excel workbook export"""
    excel_buffer = io.BytesIO()
    
    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        if not profile_data.empty:
            profile_data.to_excel(writer, sheet_name='Profile', index=False)
        
        if not screen_data.empty:
            screen_data.to_excel(writer, sheet_name='Screen Time', index=False)
        
        if not achievements_data.empty:
            achievements_data.to_excel(writer, sheet_name='Achievements', index=False)
        
        if include_summary:
            summary_df = pd.DataFrame([create_summary_report(user_id, profile_data, screen_data).split('\n')])
            summary_df.to_excel(writer, sheet_name='Summary Report', index=False, header=False)
    
    excel_buffer.seek(0)
    return excel_buffer

# --- Main App Logic ---
if __name__ == "__main__":
    create_data_export()
