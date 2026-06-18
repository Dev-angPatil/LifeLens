import streamlit as st
from database import calculate_productivity_score

def get_productivity_status(score):
    """
    Returns status category and a color/emoji based on productivity score.
    - Excellent: 80 - 100
    - Good: 60 - 79
    - Average: 40 - 59
    - Needs Improvement: < 40
    """
    if score >= 80:
        return "Excellent", "🏆", "#2ecc71"  # Mint Green
    elif score >= 60:
        return "Good", "⭐", "#3498db"       # Soft Blue
    elif score >= 40:
        return "Average", "😐", "#f1c40f"    # Yellow
    else:
        return "Needs Improvement", "⚠️", "#e74c3c" # Red/Coral

def get_trend_indicator(today_val, avg_val, higher_is_better=True):
    """
    Returns the arrow and trend status based on comparison:
    ↑ Improving
    ↓ Declining
    → Stable
    
    For screen time, lower is better, so the logic is inverted.
    """
    if today_val is None or avg_val is None or avg_val == 0:
        return "→ Stable", "→"
        
    diff_percent = (today_val - avg_val) / avg_val
    
    # If difference is within 5%, it's stable
    if abs(diff_percent) < 0.05:
        return "→ Stable", "→"
        
    if today_val > avg_val:
        if higher_is_better:
            return "↑ Improving", "↑"
        else:
            return "↓ Declining", "↓" # screen time is higher, which is bad
    else:
        if higher_is_better:
            return "↓ Declining", "↓"
        else:
            return "↑ Improving", "↑" # screen time is lower, which is good

# (End of file)
