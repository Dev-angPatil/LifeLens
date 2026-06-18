# 🧬 LifeLens — Personal Habit Optimization Dashboard

> Track habits. Analyze patterns. Optimize performance.

LifeLens is a Python-powered personal analytics dashboard that transforms your daily habits into actionable insights through interactive visualizations, a rule-based recommendation engine, and a productivity scoring algorithm.

---

## ✨ Features

- **Productivity Score Engine** — A normalized 0–100 index calculated daily from your habits
- **Interactive Analytics** — Area charts, radar webs, animated timelines, and annotated heatmaps
- **Daily Log Form** — Uniform sliders for Study, Sleep, Exercise, Screen Time, Mood & Hydration (in liters)
- **Smart Recommendations** — Rule-based engine flagging dehydration, screen overload, sleep debt, and focus deficits
- **Weekly Reports** — Comparative week-over-week text summaries with download export

---

## 🛠️ Built With

- Python 3.12
- Streamlit
- Plotly
- Pandas
- NumPy
- SQLite3

---

## 🚀 Running Locally

```bash
# Clone the repository
git clone https://github.com/Dev-angPatil/LifeLens.git
cd LifeLens

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Launch the dashboard
streamlit run app.py
```

The app will auto-open at `http://localhost:8501`. On first launch, 14 days of realistic mock data is automatically seeded into the local SQLite database.

---

## 📁 Project Structure

```
LifeLens/
├── app.py              # Main Streamlit UI & page routing
├── database.py         # SQLite3 schema, CRUD, and mock data seeder
├── analytics.py        # Plotly 2D charts & weekly aggregations
├── recommendations.py  # Rule-based advisory engine
├── report_generator.py # Week-over-week text report formatter
├── styles.py           # Neo-Brutalist CSS injection & card components
├── utils.py            # Productivity score helpers & trend indicators
└── requirements.txt    # Python dependencies
```

---

## 📊 How the Productivity Score Works

```python
raw_score += study_hours * 4      # Focus is king
raw_score += 2  # if exercise > 0 # Movement bonus
raw_score += 2  # if sleep 7–9h   # Optimal sleep
raw_score += 1  # if water >= 2L  # Hydration bonus
raw_score -= 3  # if screen > 6h  # Screen penalty

score = (raw_score / 69.0) * 100  # Normalized 0–100
```

---

## 🎨 Design

Built with a **Light Neo-Brutalism** design language — thick black borders, offset box shadows, bold uppercase typography using [Lexend Mega](https://fonts.google.com/specimen/Lexend+Mega) and [Outfit](https://fonts.google.com/specimen/Outfit) from Google Fonts, and a pastel accent palette.
