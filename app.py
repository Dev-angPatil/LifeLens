import streamlit as st
import pandas as pd
import datetime
import database as db
import utils
import styles
import analytics
import recommendations
import report_generator

# Page configurations
st.set_page_config(
    page_title="LifeLens - Habit Dashboard",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
db.init_db()

# Inject custom stylesheet overrides
styles.inject_theme_styles()

# Sidebar Layout
with st.sidebar:
    st.markdown('<div class="brutalist-badge" style="text-align:center; font-size:1.4rem; padding:0.5rem; margin-bottom:1rem;">🧬 LIFE LENS OS</div>', unsafe_allow_html=True)
    styles.render_svg("neo_flower")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Navigation
    st.subheader("NAVIGATE")
    page = st.radio(
        label="Select Page",
        options=["🏠 Dashboard", "📝 Daily Entry", "📊 Analytics", "📈 Weekly Report", "💡 Recommendations", "⚙️ Settings"],
        label_visibility="collapsed"
    )
    
    st.markdown("<br><hr><br>", unsafe_allow_html=True)
    
    # Quick quote or system state
    st.markdown('<div style="font-size:0.8rem; font-weight:900; border:2px solid #000; background:#FFF; padding:0.5rem; box-shadow:2px 2px 0px #000; color:#000000;">SYSTEM: RUNNING OPTIMAL.<br>DATA CACHE: ACTIVE.</div>', unsafe_allow_html=True)

# Helper function to compute streak
def get_streak_count(df):
    if df.empty:
        return 0
    dates = sorted(list(pd.to_datetime(df["date"]).dt.date))
    today = datetime.date.today()
    latest = dates[-1]
    
    # If the latest entry is older than yesterday, streak is broken
    if (today - latest).days > 1:
        return 0
        
    streak = 1
    current = latest
    for prev in reversed(dates[:-1]):
        diff = (current - prev).days
        if diff == 1:
            streak += 1
            current = prev
        elif diff == 0:
            continue
        else:
            break
    return streak

# Load DataFrame
df = db.get_all_entries()

# ----------------- PAGE ROUTING -----------------

if page == "🏠 Dashboard":
    # Header Banner
    st.markdown("""
    <div class="brutalist-header-box">
        <div>
            <h1>⚡ HABIT OPTIMIZATION DASHBOARD</h1>
            <p style="margin:0; font-weight:700;">TRACK HABITS. ANALYZE PATTERNS. OPTIMIZE PERFORMANCE.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Core Logic: Compare Latest Entry with 7-Day Averages
    if df.empty:
        st.warning("No data found. Please log some daily entries first or reset mock data in Settings!")
    else:
        # Get latest entry
        latest_entry = df.iloc[-1]
        latest_date = latest_entry["date"]
        
        # Calculate 7-day average excluding today's date if it's in the average
        df_prev_7 = df[df["date"] < latest_date].tail(7)
        if df_prev_7.empty:
            df_prev_7 = df.tail(7) # Fallback to all if not enough data
            
        avg_study = df_prev_7["study_hours"].mean()
        avg_sleep = df_prev_7["sleep_hours"].mean()
        avg_exercise = df_prev_7["exercise_minutes"].mean()
        avg_screen = df_prev_7["screen_time"].mean()
        avg_mood = df_prev_7["mood"].mean()
        avg_score = df_prev_7["productivity_score"].mean()
        
        # Streak
        streak = get_streak_count(df)
        
        # Status mappings for Productivity Score
        score_val = latest_entry["productivity_score"]
        status_txt, status_emoji, status_color = utils.get_productivity_status(score_val)
        
        # Trend arrows
        trend_score_txt, arrow_score = utils.get_trend_indicator(score_val, avg_score, True)
        trend_mood_txt, arrow_mood = utils.get_trend_indicator(latest_entry["mood"], avg_mood, True)
        trend_study_txt, arrow_study = utils.get_trend_indicator(latest_entry["study_hours"], avg_study, True)
        trend_sleep_txt, arrow_sleep = utils.get_trend_indicator(latest_entry["sleep_hours"], avg_sleep, True)
        trend_exercise_txt, arrow_exercise = utils.get_trend_indicator(latest_entry["exercise_minutes"], avg_exercise, True)
        trend_screen_txt, arrow_screen = utils.get_trend_indicator(latest_entry["screen_time"], avg_screen, False) # Lower screen time is better!
        
        # Info note about latest entry date
        st.info(f"Showing metrics for latest logged entry: **{latest_date}** (Compared with previous 7-day averages)")
        
        # Row 1 of Grid
        row1_col1, row1_col2, row1_col3, row1_col4 = st.columns(4)
        
        with row1_col1:
            styles.draw_card(
                title="Productivity Score",
                value=f"{score_val:.0f}/100",
                trend_text=f"{status_txt}",
                trend_arrow=status_emoji,
                card_style="primary"
            )
        with row1_col2:
            styles.draw_card(
                title="Current Mood",
                value=f"{latest_entry['mood']}/10",
                trend_text=trend_mood_txt,
                trend_arrow=arrow_mood,
                card_style="pink"
            )
        with row1_col3:
            styles.draw_card(
                title="Sleep Duration",
                value=f"{latest_entry['sleep_hours']:.1f} hrs",
                trend_text=trend_sleep_txt,
                trend_arrow=arrow_sleep,
                card_style="green"
            )
        with row1_col4:
            styles.draw_card(
                title="Weekly Streak",
                value=f"{streak} Days 🔥" if streak > 0 else "0 Days ❄️",
                trend_text="Stable" if streak > 0 else "Log Data!",
                trend_arrow="→",
                card_style="primary"
            )
            
        # Row 2 of Grid
        row2_col1, row2_col2, row2_col3, row2_col4 = st.columns(4)
        
        with row2_col1:
            styles.draw_card(
                title="Study Session",
                value=f"{latest_entry['study_hours']:.1f} hrs",
                trend_text=trend_study_txt,
                trend_arrow=arrow_study,
                card_style="blue"
            )
        with row2_col2:
            styles.draw_card(
                title="Screen Time",
                value=f"{latest_entry['screen_time']:.1f} hrs",
                trend_text=trend_screen_txt,
                trend_arrow=arrow_screen,
                card_style="gold"
            )
        with row2_col3:
            styles.draw_card(
                title="Fitness Workout",
                value=f"{latest_entry['exercise_minutes']:.0f} mins",
                trend_text=trend_exercise_txt,
                trend_arrow=arrow_exercise,
                card_style="secondary"
            )
        with row2_col4:
            styles.draw_card(
                title="Water Intake",
                value=f"{latest_entry['water_intake']:.1f} L",
                trend_text="Target: 2.0L" if latest_entry['water_intake'] < 2.0 else "Fully Hydrated!",
                trend_arrow="💧",
                card_style="green"
            )

elif page == "📝 Daily Entry":
    st.markdown("<h2>📝 LOG HABIT ENTRY</h2>", unsafe_allow_html=True)
    
    with st.container(key="daily_entry_form"):
        # Setup inputs
        entry_date = st.date_input("Date of Entry", datetime.date.today())
        date_str = entry_date.strftime("%Y-%m-%d")
        
        # Check if data already exists for this date
        existing_entry = db.get_entry_by_date(date_str)
        if existing_entry:
            st.warning(f"Note: An entry for **{date_str}** already exists. Submitting this form will overwrite it!")
            
        c1, c2 = st.columns(2)
        with c1:
            study_h = st.slider("Study Hours (focused work)", 0.0, 16.0, float(existing_entry["study_hours"]) if existing_entry else 4.0, step=0.5)
            sleep_h = st.slider("Sleep Hours (rest duration)", 0.0, 12.0, float(existing_entry["sleep_hours"]) if existing_entry else 7.5, step=0.5)
            exercise_m = st.slider("Exercise Minutes (movement)", 0.0, 180.0, float(existing_entry["exercise_minutes"]) if existing_entry else 30.0, step=5.0)
        with c2:
            screen_h = st.slider("Screen Time (entertainment/scroll)", 0.0, 16.0, float(existing_entry["screen_time"]) if existing_entry else 5.0, step=0.5)
            mood_s = st.slider("Mood Score (emotional state)", 1, 10, int(existing_entry["mood"]) if existing_entry else 7, step=1)
            water_i = st.slider("Water Intake (liters)", 0.0, 8.0, float(existing_entry["water_intake"]) if existing_entry else 2.5, step=0.1)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("Save Daily Entry"):
            score = db.insert_entry(date_str, study_h, sleep_h, exercise_m, screen_h, mood_s, water_i)
            
            # Display custom notification box
            st.markdown(f"""
            <div style="border:3px solid #000; background:#BFFF80; padding:1rem; box-shadow:4px 4px 0px #000; font-family:'Lexend Mega',sans-serif; font-weight:900; margin-top:1rem; color:#000000;">
                ✅ DAILY ENTRY SAVED SUCCESSFULLY FOR {date_str}!<br>
                📊 CALCULATED PRODUCTIVITY SCORE: {score:.1f}/100.
            </div>
            """, unsafe_allow_html=True)

elif page == "📊 Analytics":
    st.markdown("<h2>📊 INTERACTIVE ANALYTICS</h2>", unsafe_allow_html=True)
    
    if df.empty or len(df) < 3:
        st.warning("Not enough data to display charts. Please log more data or generate mock data in Settings!")
    else:
        # Create grid layout for charts
        c1, c2 = st.columns(2)
        
        with c1:
            fig1 = analytics.create_3d_productivity_mountain(df)
            st.plotly_chart(fig1, width="stretch")
            
            fig3 = analytics.create_weekly_trend_surface(df)
            st.plotly_chart(fig3, width="stretch")
            
        with c2:
            fig2 = analytics.create_3d_habit_radar(df)
            st.plotly_chart(fig2, width="stretch")
            
            fig4 = analytics.create_productivity_timeline(df)
            st.plotly_chart(fig4, width="stretch")

elif page == "📈 Weekly Report":
    st.markdown("<h2>📈 WEEKLY ANALYTICS & REPORTS</h2>", unsafe_allow_html=True)
    
    if df.empty:
        st.warning("No database data found to generate reports.")
    else:
        summary = analytics.get_weekly_summary(df)
        
        # Averages row
        col1, col2, col3, col4, col5 = st.columns(5)
        
        # Display theme-styled metrics
        with col1:
            st.metric("Avg Study Hours", f"{summary['avg_study']} hrs/day")
        with col2:
            st.metric("Avg Sleep Hours", f"{summary['avg_sleep']} hrs/night")
        with col3:
            st.metric("Avg Screen Time", f"{summary['avg_screen']} hrs/day")
        with col4:
            st.metric("Avg Mood Score", f"{summary['avg_mood']}/10")
        with col5:
            st.metric("Avg Exercise", f"{summary['avg_exercise']:.0f} mins/day")
            
        st.markdown("<br><hr><br>", unsafe_allow_html=True)
        
        # Highlights Cards
        h_col1, h_col2, h_col3 = st.columns(3)
        with h_col1:
            styles.draw_card(
                title="🏆 Best Day",
                value=summary["best_day"],
                trend_text="Peak Performance",
                card_style="green",
                wide=True
            )
        with h_col2:
            styles.draw_card(
                title="⚠️ Worst Day",
                value=summary["worst_day"],
                trend_text="Needs Improvement",
                card_style="pink",
                wide=True
            )
        with h_col3:
            styles.draw_card(
                title="💡 Most Productive Day",
                value=summary["most_productive_day"],
                trend_text="Top Output",
                card_style="blue",
                wide=True
            )
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Generate raw report text
        report_text = report_generator.generate_report_text(df)
        
        # Report Display Box
        st.subheader("Weekly Summary Report")
        st.text_area(
            label="Report Output",
            value=report_text,
            height=280,
            label_visibility="collapsed"
        )
        
        # Export button
        st.download_button(
            label="💾 DOWNLOAD REPORT (.txt)",
            data=report_text,
            file_name=f"weekly_report_{datetime.date.today().strftime('%Y-%m-%d')}.txt",
            mime="text/plain"
        )

elif page == "💡 Recommendations":
    st.markdown("<h2>💡 SMART RECOMMENDATIONS</h2>", unsafe_allow_html=True)
    
    recs = recommendations.generate_recommendations(df)
    
    # Display lists styled to match the theme
    st.markdown("<br>", unsafe_allow_html=True)
    for idx, rec in enumerate(recs):
        st.markdown(f"""
        <div style="border: 3px solid #000; background:#FFF; padding:1.2rem; margin-bottom:1rem; box-shadow:4px 4px 0px #000; font-family:'Outfit',sans-serif; font-weight:700; font-size:1.05rem; display:flex; align-items:center; gap:0.75rem;">
            <span style="font-size:1.5rem; background:#FFF275; border:2px solid #000; border-radius:4px; padding:0.15rem 0.5rem;">{idx+1}</span>
            <span>{rec}</span>
        </div>
        """, unsafe_allow_html=True)
            
    # Add an decorative graphic at the bottom
    st.markdown("<br><br>", unsafe_allow_html=True)
    styles.render_svg("neo_star")

elif page == "⚙️ Settings":
    st.markdown("<h2>⚙️ SYSTEM SETTINGS</h2>", unsafe_allow_html=True)
    
    with st.container(key="settings_form"):
        st.subheader("Database Management")
        st.write("Control the SQLite datastore cache.")
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🚨 CLEAR DATABASE"):
                db.get_db_connection().execute("DELETE FROM daily_habits")
                db.get_db_connection().commit()
                st.success("Database cleared successfully! The dashboard is now empty.")
                st.rerun()
                
        with c2:
            if st.button("🔥 RE-POPULATE MOCK DATA"):
                db.get_db_connection().execute("DELETE FROM daily_habits")
                db.get_db_connection().commit()
                db.init_db()
                st.success("Database populated with 14 days of mock data successfully!")
                st.rerun()
                
        st.markdown("<br><hr><br>", unsafe_allow_html=True)
        
        st.subheader("Raw Database Entries")
        st.dataframe(df, width="stretch")
