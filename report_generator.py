import pandas as pd
import datetime

def generate_report_text(df, theme="neo_brutalist"):
    """
    Generates a structured weekly summary report comparing the last 7 days with the preceding 7 days.
    """
    if len(df) < 14:
        # Not enough data for a comparison, but we can generate a simple summary
        df_week = df.tail(7)
        if df_week.empty:
            return "No data logged yet. Please add entries in the 'Daily Entry' tab!"
            
        study_sum = df_week["study_hours"].sum()
        sleep_avg = df_week["sleep_hours"].mean()
        exercise_sum = df_week["exercise_minutes"].sum()
        screen_avg = df_week["screen_time"].mean()
        
        return f"""==================================================
✏️ WEEKLY REPORT (INITIAL PERIOD)
Generated: {datetime.date.today().strftime('%Y-%m-%d')}
==================================================

- TOTAL STUDY HOURS: {study_sum:.1f} hours
- AVERAGE SLEEP: {sleep_avg:.1f} hours/night
- TOTAL EXERCISE: {exercise_sum:.0f} minutes
- AVERAGE SCREEN TIME: {screen_avg:.1f} hours/day

Note: Please log at least 14 days of data to unlock full week-over-week comparative metrics!
=================================================="""

    # We have at least 14 days of data
    df_this_week = df.tail(7)
    df_last_week = df.iloc[-14:-7]
    
    # Calculate metrics for this week
    study_this = df_this_week["study_hours"].sum()
    sleep_this = df_this_week["sleep_hours"].mean()
    exercise_this = df_this_week["exercise_minutes"].sum()
    screen_this = df_this_week["screen_time"].mean()
    prod_this = df_this_week["productivity_score"].mean()
    
    # Calculate metrics for last week
    study_last = df_last_week["study_hours"].sum()
    sleep_last = df_last_week["sleep_hours"].mean()
    exercise_last = df_last_week["exercise_minutes"].sum()
    screen_last = df_last_week["screen_time"].mean()
    prod_last = df_last_week["productivity_score"].mean()
    
    # Calculate percentage changes
    screen_change = ((screen_this - screen_last) / screen_last * 100) if screen_last > 0 else 0
    prod_change = ((prod_this - prod_last) / prod_last * 100) if prod_last > 0 else 0
    
    # Textual comparison direction
    prod_direction = "improved" if prod_change >= 0 else "declined"
    screen_direction = "reduced" if screen_change <= 0 else "increased"
    
    report = f"""==================================================
✏️ WEEKLY PRODUCTIVITY REPORT
Generated: {datetime.date.today().strftime('%Y-%m-%d')}
==================================================

SUMMARY:
This week you studied {study_this:.1f} hours, slept an average of {sleep_this:.1f} hours, exercised for {exercise_this:.0f} minutes, and {screen_direction} screen time by {abs(screen_change):.1f}% compared to last week.

PRODUCTIVITY PERFORMANCE:
- THIS WEEK AVG SCORE: {prod_this:.1f}/100
- LAST WEEK AVG SCORE: {prod_last:.1f}/100
- STATUS: Productivity {prod_direction} by {abs(prod_change):.1f}%!

HABITS PERFORMANCE BREAKDOWN:
- STUDY: {study_this:.1f} hours vs {study_last:.1f} hours last week
- SLEEP: {sleep_this:.1f}h average vs {sleep_last:.1f}h average last week
- EXERCISE: {exercise_this:.0f} mins vs {exercise_last:.0f} mins last week
- SCREEN TIME: {screen_this:.1f}h average vs {screen_last:.1f}h average last week

==================================================
STATUS: ACTION REQUIRED. SEE RECOMMENDATIONS TAB.
=================================================="""
        
    return report
