import sqlite3
import pandas as pd
import datetime
import random

DB_NAME = "life_dashboard.db"

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def calculate_productivity_score(study_hours, sleep_hours, exercise_minutes, screen_time, water_intake):
    """
    Calculates and normalizes the productivity score (0-100).
    Formula:
    +4 points per study hour
    +2 points per exercise session (exercise_minutes > 0)
    +2 points if sleep is between 7 and 9 hours
    +1 point if water intake >= 2.0 liters
    -3 points if screen time > 6 hours
    Max Raw Score = (16 * 4) + 2 + 2 + 1 = 69 (since study_hours max is 16)
    """
    raw_score = 0
    raw_score += study_hours * 4
    if exercise_minutes > 0:
        raw_score += 2
    if 7.0 <= sleep_hours <= 9.0:
        raw_score += 2
    if water_intake >= 2.0:
        raw_score += 1
    if screen_time > 6:
        raw_score -= 3
        
    # Max raw score possible is 16*4 + 2 + 2 + 1 = 69.
    # Min raw score possible is -3.
    # Normalizing raw score to 0-100 range:
    max_raw = 69.0
    normalized = (raw_score / max_raw) * 100.0
    return round(min(100.0, max(0.0, normalized)), 1)

def init_db():
    """Initializes the database and inserts 14 days of mock data if empty."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create the habits table (storing water_intake as REAL to support float liters)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_habits (
            date TEXT PRIMARY KEY,
            study_hours REAL,
            sleep_hours REAL,
            exercise_minutes REAL,
            screen_time REAL,
            mood INTEGER,
            water_intake REAL,
            productivity_score REAL
        )
    """)
    conn.commit()
    
    # Check if empty
    cursor.execute("SELECT COUNT(*) FROM daily_habits")
    count = cursor.fetchone()[0]
    
    if count == 0:
        # Prepopulate with 14 days of realistic mock data
        today = datetime.date.today()
        
        # High quality seeds to make metrics look realistic and interesting
        # e.g., weekly cycles (higher study on weekdays, more exercise/sleep on weekends)
        for i in range(14, 0, -1):
            target_date = today - datetime.timedelta(days=i)
            date_str = target_date.strftime("%Y-%m-%d")
            
            # Determine day of week to generate realistic patterns
            day_of_week = target_date.weekday() # 0 = Monday, 6 = Sunday
            
            if day_of_week >= 5: # Weekend
                study = round(random.uniform(1.0, 3.5), 1)
                sleep = round(random.uniform(7.5, 9.5), 1)
                exercise = random.choice([0, 30, 45, 60, 90])
                screen = round(random.uniform(4.0, 8.5), 1)
                mood = random.choice([7, 8, 9, 10])
                water = round(random.uniform(1.5, 3.2), 1) # in liters
            else: # Weekday
                study = round(random.uniform(4.0, 9.0), 1)
                sleep = round(random.uniform(6.0, 8.0), 1)
                exercise = random.choice([0, 15, 30, 45, 60])
                screen = round(random.uniform(3.0, 6.0), 1)
                mood = random.choice([6, 7, 8, 9])
                water = round(random.uniform(2.0, 3.8), 1) # in liters
                
            score = calculate_productivity_score(study, sleep, exercise, screen, water)
            
            cursor.execute("""
                INSERT OR REPLACE INTO daily_habits 
                (date, study_hours, sleep_hours, exercise_minutes, screen_time, mood, water_intake, productivity_score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (date_str, study, sleep, exercise, screen, mood, water, score))
            
        conn.commit()
        
    conn.close()

def insert_entry(date_str, study, sleep, exercise, screen, mood, water):
    """Inserts or updates a daily entry in the database."""
    score = calculate_productivity_score(study, sleep, exercise, screen, water)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO daily_habits 
        (date, study_hours, sleep_hours, exercise_minutes, screen_time, mood, water_intake, productivity_score)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (date_str, study, sleep, exercise, screen, mood, water, score))
    conn.commit()
    conn.close()
    return score

def get_all_entries():
    """Retrieves all entries sorted by date ascending as a Pandas DataFrame."""
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM daily_habits ORDER BY date ASC", conn)
    conn.close()
    return df

def get_entry_by_date(date_str):
    """Retrieves a single entry by date. Returns a dictionary or None."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM daily_habits WHERE date = ?", (date_str,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def delete_entry(date_str):
    """Deletes an entry by date."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM daily_habits WHERE date = ?", (date_str,))
    conn.commit()
    conn.close()
