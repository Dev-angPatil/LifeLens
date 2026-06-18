def generate_recommendations(df):
    """
    Analyzes historical data (last 7 entries) and outputs 3-5 action-oriented recommendations.
    Tone: Bold, direct, punchy, action-oriented (Neo-Brutalist).
    """
    if df.empty:
        return [
            "📝 NO DATA FOUND: Enter your first daily habit log under 'Daily Entry' to start analyzing your patterns.",
            "⚡ TRACK EVERYTHING: Make data logging a habit. Consistent data builds accurate 2D trend peaks.",
            "🔋 START TODAY: Productivity tracking leads directly to optimization. Don't wait."
        ]

    # Get averages of last 7 entries
    df_week = df.tail(7)
    avg_study = df_week["study_hours"].mean()
    avg_sleep = df_week["sleep_hours"].mean()
    avg_exercise = df_week["exercise_minutes"].mean()
    avg_screen = df_week["screen_time"].mean()
    avg_water = df_week["water_intake"].mean()
    avg_mood = df_week["mood"].mean()
    
    recs = []
    
    # Rule 1: Screen Time
    if avg_screen > 6.0:
        recs.append("🚨 SCREEN TIME OVERLOAD: Average screen time is over 6 hours. Turn off your screens 1-2 hours before bed. Your eyes need rest.")
            
    # Rule 2: Sleep Hours
    if avg_sleep < 7.0:
        recs.append("🔋 SLEEP DEFIENCY: Averaging less than 7 hours of sleep. Prioritize a consistent bedtime. Sleep is the foundation of cognitive power.")
    elif avg_sleep > 9.5:
        recs.append("💤 OVERSLEEPING DETECTED: Averaging over 9.5 hours of sleep. Try setting a standard morning alarm to avoid feeling lethargic.")
            
    # Rule 3: Exercise
    if avg_exercise < 20.0:
        recs.append("🏃 MOVE YOUR BODY: You are exercising less than 20 minutes a day on average. Block a 20-minute brisk walk or light workout. No excuses.")
            
    # Rule 4: Study/Productive Work
    if avg_study < 3.0:
        recs.append("📚 FOCUS DEFICIT: Average study time is under 3 hours. Time-block deep focus sessions of 50 minutes. Put your phone in another room.")
            
    # Rule 5: Water Intake
    if avg_water < 2.0:
        recs.append("💧 DEHYDRATION ALERT: Drinking less than 2.0 liters of water. Drink 2.0L+ to improve your metabolism, kidney function, and focus.")
            
    # Rule 6: Mood and Balance
    if avg_mood < 6.0:
        recs.append("🧠 STRESS MANAGEMENT: Average mood score is below 6/10. Reduce workloads, increase sleep, and take structured 10-minute recovery breaks.")

    # If the user is doing amazing in all habits
    if not recs:
        recs = [
            "🏆 CRUSHING IT: All weekly metrics are in optimal zones. Maintain your current habit discipline.",
            "🔥 STREAK PRESERVATION: Your streak is active. Keep logs up to date and continue pushing limits.",
            "⚡ OPTIMAL ENERGY: Keep your hydration, sleep, and study sessions balanced."
        ]
            
    # Limit recommendations to 3-5
    return recs[:5]
