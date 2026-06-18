import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import datetime

def get_weekly_summary(df):
    """Calculates weekly metrics from the dataframe (last 7 entries)."""
    if df.empty:
        return {}
        
    # Get last 7 days of entries
    df_week = df.tail(7).copy()
    
    summary = {
        "avg_study": round(df_week["study_hours"].mean(), 1),
        "avg_sleep": round(df_week["sleep_hours"].mean(), 1),
        "avg_screen": round(df_week["screen_time"].mean(), 1),
        "avg_mood": round(df_week["mood"].mean(), 1),
        "avg_exercise": round(df_week["exercise_minutes"].mean(), 0),
        "avg_score": round(df_week["productivity_score"].mean(), 1)
    }
    
    # Identify key days
    best_row = df_week.loc[df_week["productivity_score"].idxmax()]
    worst_row = df_week.loc[df_week["productivity_score"].idxmin()]
    most_studious_row = df_week.loc[df_week["study_hours"].idxmax()]
    
    # Format date to weekday name
    def get_weekday_name(date_str):
        dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("%A")
        
    summary["best_day"] = f"{get_weekday_name(best_row['date'])} ({best_row['productivity_score']}/100)"
    summary["worst_day"] = f"{get_weekday_name(worst_row['date'])} ({worst_row['productivity_score']}/100)"
    summary["most_productive_day"] = f"{get_weekday_name(best_row['date'])}"
    summary["max_study_day"] = f"{get_weekday_name(most_studious_row['date'])} ({most_studious_row['study_hours']}h)"
    
    return summary

def get_theme_colors():
    """Returns color configurations based on active theme (Neo-Brutalist strictly)."""
    return {
        "bg": "#FDFBF7",
        "grid": "#E0DCD3",
        "text": "#000000",
        "border": "#000000",
        "colors": ["#FFF275", "#FFB7B2", "#D4C4FB", "#BFFF80", "#A8E6CF"],
        "line_width": 3,
        "font": "Outfit"
    }

def create_3d_productivity_mountain(df):
    """
    Renders 2D Productivity peaks with Mood correlation overlay.
    X = Day
    Y = Productivity Score & Mood (scaled to 100)
    """
    df_week = df.tail(7).copy()
    cfg = get_theme_colors()
    
    # Format dates as nice weekday abbreviations
    df_week["weekday"] = df_week["date"].apply(
        lambda x: datetime.datetime.strptime(x, "%Y-%m-%d").strftime("%a")
    )
    
    fig = go.Figure()
    
    # Area chart for Productivity Score
    fig.add_trace(go.Scatter(
        x=df_week["weekday"],
        y=df_week["productivity_score"],
        mode="lines+markers",
        name="Productivity Score",
        line=dict(
            color=cfg["colors"][0],
            width=cfg["line_width"] * 1.5
        ),
        fill="tozeroy",
        fillcolor="rgba(255, 242, 117, 0.4)",
        marker=dict(
            size=10,
            color=cfg["colors"][0],
            line=dict(color=cfg["text"], width=2)
        )
    ))
    
    # Scaled line for Mood
    fig.add_trace(go.Scatter(
        x=df_week["weekday"],
        y=df_week["mood"] * 10, # Scale 1-10 to 10-100
        mode="lines+markers",
        name="Mood (x10)",
        line=dict(
            color=cfg["colors"][2],
            width=cfg["line_width"],
            dash="dash"
        ),
        marker=dict(
            size=8,
            color=cfg["colors"][2],
            line=dict(color=cfg["text"], width=1.5)
        )
    ))
    
    fig.update_layout(
        title=dict(
            text="🏔️ Productivity Peaks & Mood",
            font=dict(family=cfg["font"], size=16, color=cfg["text"])
        ),
        xaxis=dict(
            title=dict(
                text="Day of Week",
                font=dict(family=cfg["font"], color=cfg["text"])
            ),
            tickfont=dict(family=cfg["font"], color=cfg["text"]),
            gridcolor=cfg["grid"]
        ),
        yaxis=dict(
            title=dict(
                text="Index (0 - 100)",
                font=dict(family=cfg["font"], color=cfg["text"])
            ),
            tickfont=dict(family=cfg["font"], color=cfg["text"]),
            gridcolor=cfg["grid"],
            range=[0, 105]
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(
            font=dict(family=cfg["font"], color=cfg["text"]),
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=40, r=40, b=40, t=60)
    )
    
    return fig

def create_3d_habit_radar(df):
    """
    Renders 2D Habit Radar Chart.
    Plots the 5 habits in a spider/radar shape.
    Normalized values from 0 to 10
    """
    df_week = df.tail(7)
    cfg = get_theme_colors()
    
    # Calculate Averages (Normalizing water against 4.0 liters)
    avg_study = min(10.0, (df_week["study_hours"].mean() / 16.0) * 10) if not df_week.empty else 5.0
    avg_sleep = min(10.0, (df_week["sleep_hours"].mean() / 12.0) * 10) if not df_week.empty else 5.0
    avg_exercise = min(10.0, (df_week["exercise_minutes"].mean() / 180.0) * 10) if not df_week.empty else 5.0
    avg_mood = df_week["mood"].mean() if not df_week.empty else 5.0
    avg_water = min(10.0, (df_week["water_intake"].mean() / 4.0) * 10) if not df_week.empty else 5.0
    
    values = [avg_study, avg_sleep, avg_exercise, avg_mood, avg_water]
    labels = ["Study Hours", "Sleep Hours", "Exercise Min", "Mood Score", "Water Intake"]
    
    # Close the radar loop
    values.append(values[0])
    labels.append(labels[0])
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=labels,
        fill="toself",
        fillcolor="rgba(212, 196, 251, 0.4)",
        line=dict(
            color=cfg["colors"][2],
            width=cfg["line_width"] * 1.5
        ),
        marker=dict(
            size=8,
            color=cfg["colors"][0],
            line=dict(color=cfg["text"], width=1.5)
        ),
        name="Habit Strengths"
    ))
    
    fig.update_layout(
        title=dict(
            text="🕸️ Habit Strength Radar",
            font=dict(family=cfg["font"], size=16, color=cfg["text"])
        ),
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10],
                gridcolor=cfg["grid"],
                tickfont=dict(family=cfg["font"], color=cfg["text"])
            ),
            angularaxis=dict(
                gridcolor=cfg["grid"],
                tickfont=dict(family=cfg["font"], color=cfg["text"])
            ),
            bgcolor="rgba(0,0,0,0)"
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=40, r=40, b=40, t=60),
        showlegend=False
    )
    
    return fig

def create_weekly_trend_surface(df):
    """
    Renders Weekly Habit Heatmap.
    X = Days of the week
    Y = Metrics (Study, Sleep, Screen, Water, Mood)
    Z = Values over the week
    """
    df_week = df.tail(7).copy()
    cfg = get_theme_colors()
    
    # Days
    weekdays = df_week["date"].apply(
        lambda x: datetime.datetime.strptime(x, "%Y-%m-%d").strftime("%a")
    ).values
    
    # Metrics
    metrics = ["Study Hours", "Sleep Hours", "Screen Time", "Water Intake", "Mood Score"]
    
    # Grid of raw values
    z_raw = np.zeros((len(metrics), len(weekdays)))
    z_raw[0] = df_week["study_hours"].values
    z_raw[1] = df_week["sleep_hours"].values
    z_raw[2] = df_week["screen_time"].values
    z_raw[3] = df_week["water_intake"].values
    z_raw[4] = df_week["mood"].values
    
    # Normalized grid (0-10) for color scaling
    z_norm = np.zeros((len(metrics), len(weekdays)))
    z_norm[0] = df_week["study_hours"].values * (10.0 / 16.0)     # Study: max 16
    z_norm[1] = df_week["sleep_hours"].values * (10.0 / 12.0)     # Sleep: max 12
    z_norm[2] = df_week["screen_time"].values * (10.0 / 16.0)     # Screen: max 16
    z_norm[3] = df_week["water_intake"].values * (10.0 / 4.0)     # Water: max 4L
    z_norm[4] = df_week["mood"].values                            # Mood: max 10
    
    # Colorscales
    colorscale = [[0.0, "#FDFBF7"], [0.5, "#FFF275"], [1.0, "#BFFF80"]]
        
    fig = go.Figure(data=go.Heatmap(
        z=z_norm,
        x=list(weekdays),
        y=metrics,
        colorscale=colorscale,
        showscale=False,
        hoverinfo="text",
        text=[
            [f"{z_raw[m, d]:.1f}" if m != 4 else f"{int(z_raw[m, d])}" 
             for d in range(len(weekdays))]
            for m in range(len(metrics))
        ]
    ))
    
    # Add annotations inside each cell
    annotations = []
    for m in range(len(metrics)):
        for d in range(len(weekdays)):
            val = z_raw[m, d]
            unit = ""
            if m == 0 or m == 1 or m == 2:
                unit = "h"
                text_val = f"{val:.1f}{unit}"
            elif m == 3:
                unit = "L"
                text_val = f"{val:.1f}{unit}"
            else:
                text_val = f"{int(val)}/10"
                
            annotations.append(dict(
                x=weekdays[d],
                y=metrics[m],
                text=text_val,
                font=dict(family=cfg["font"], size=12, color=cfg["text"], weight="bold"),
                showarrow=False
            ))
            
    fig.update_layout(
        title=dict(
            text="📉 Weekly Habit Heatmap",
            font=dict(family=cfg["font"], size=16, color=cfg["text"])
        ),
        xaxis=dict(
            title=dict(
                text="Day",
                font=dict(family=cfg["font"], color=cfg["text"])
            ),
            tickfont=dict(family=cfg["font"], color=cfg["text"]),
            gridcolor="rgba(0,0,0,0)"
        ),
        yaxis=dict(
            tickfont=dict(family=cfg["font"], color=cfg["text"]),
            gridcolor="rgba(0,0,0,0)"
        ),
        annotations=annotations,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=40, r=40, b=40, t=60)
    )
    
    return fig

def create_productivity_timeline(df):
    """
    Renders an animated timeline graph of the daily Productivity Score.
    Uses Plotly trace animations to draw the timeline chronologically.
    """
    df_week = df.tail(7).copy()
    cfg = get_theme_colors()
    
    df_week["weekday"] = df_week["date"].apply(
        lambda x: datetime.datetime.strptime(x, "%Y-%m-%d").strftime("%A")
    )
    
    # Let's build a timeline frame dataset
    frames = []
    for i in range(1, len(df_week) + 1):
        df_frame = df_week.iloc[:i]
        frames.append(go.Frame(
            data=[go.Scatter(
                x=df_frame["weekday"],
                y=df_frame["productivity_score"],
                mode="lines+markers"
            )],
            name=f"frame_{i}"
        ))
        
    fig = go.Figure(
        data=[go.Scatter(
            x=[df_week["weekday"].iloc[0]],
            y=[df_week["productivity_score"].iloc[0]],
            mode="lines+markers",
            line=dict(
                color=cfg["colors"][0],
                width=cfg["line_width"] * 1.5
            ),
            marker=dict(
                size=12,
                color=cfg["colors"][2],
                line=dict(color=cfg["text"], width=2)
            ),
            name="Score"
        )],
        layout=go.Layout(
            title=dict(
                text="📈 Animated Productivity Timeline",
                font=dict(family=cfg["font"], size=16, color=cfg["text"])
            ),
            xaxis=dict(
                title=dict(
                    text="Day of Week",
                    font=dict(family=cfg["font"], color=cfg["text"])
                ),
                tickfont=dict(family=cfg["font"], color=cfg["text"]),
                gridcolor=cfg["grid"]
            ),
            yaxis=dict(
                title=dict(
                    text="Productivity Score",
                    font=dict(family=cfg["font"], color=cfg["text"])
                ),
                tickfont=dict(family=cfg["font"], color=cfg["text"]),
                gridcolor=cfg["grid"],
                range=[0, 105]
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            updatemenus=[dict(
                type="buttons",
                showactive=False,
                x=0.0,
                y=1.15,
                xanchor="left",
                yanchor="top",
                buttons=[
                    dict(
                        label="▶ Play Animation",
                        method="animate",
                        args=[None, dict(
                            frame=dict(duration=400, redraw=False),
                            fromcurrent=True,
                            transition=dict(duration=200, easing="quadratic-in-out")
                        )]
                    )
                ]
            )],
            margin=dict(l=40, r=40, b=40, t=60)
        ),
        frames=frames
    )
    
    return fig
