import streamlit as st

# Custom SVG Icons and Graphics
SVG_GRAPHICS = {
    "neo_star": """
    <svg width="60" height="60" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg" style="display: block; margin: auto;">
        <path d="M50 0L63.5 36.5L100 50L63.5 63.5L50 100L36.5 63.5L0 50L36.5 36.5L50 0Z" fill="#F39C12" stroke="#000000" stroke-width="4"/>
    </svg>
    """,
    "neo_flower": """
    <svg width="60" height="60" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" style="display: block; margin: auto;">
        <circle cx="50" cy="50" r="18" fill="#FF6B6B" stroke="#000000" stroke-width="4"/>
        <circle cx="50" cy="20" r="16" fill="#4D96FF" stroke="#000000" stroke-width="4"/>
        <circle cx="50" cy="80" r="16" fill="#4D96FF" stroke="#000000" stroke-width="4"/>
        <circle cx="20" cy="50" r="16" fill="#4D96FF" stroke="#000000" stroke-width="4"/>
        <circle cx="80" cy="50" r="16" fill="#4D96FF" stroke="#000000" stroke-width="4"/>
        <circle cx="50" cy="50" r="8" fill="#FEE440"/>
    </svg>
    """
}

# Neo Brutalism CSS stylesheet
NEO_BRUTALIST_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Lexend+Mega:wght@400;700;900&family=Outfit:wght@400;700;900&display=swap');

/* Global Style Overrides */
*, *:before, *:after {
    box-sizing: border-box !important;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: #FDFBF7 !important;
    font-family: 'Outfit', sans-serif !important;
    color: #000000 !important;
}

h1, h2, h3 {
    font-family: 'Lexend Mega', sans-serif !important;
    font-weight: 900 !important;
    color: #000000 !important;
    text-transform: uppercase;
    letter-spacing: -1px;
}

/* Sidebar Custom Styling */
[data-testid="stSidebar"] {
    background-color: #A8E6CF !important;
    border-right: 4px solid #000000 !important;
}

[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2 {
    color: #000000 !important;
    font-family: 'Lexend Mega', sans-serif !important;
}

/* Base button styling */
.stButton > button {
    background-color: #FFB7B2 !important;
    color: #000000 !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 900 !important;
    font-size: 1.1rem !important;
    border: 3px solid #000000 !important;
    border-radius: 8px !important;
    box-shadow: 4px 4px 0px 0px #000000 !important;
    transition: all 0.1s ease-in-out !important;
    text-transform: uppercase !important;
    padding: 0.6rem 1.5rem !important;
}

.stButton > button:hover {
    transform: translate(-2px, -2px) !important;
    box-shadow: 6px 6px 0px 0px #000000 !important;
    background-color: #FF9B94 !important;
}

.stButton > button:active {
    transform: translate(2px, 2px) !important;
    box-shadow: 2px 2px 0px 0px #000000 !important;
}

/* Inputs, Textareas, Selects */
div[data-baseweb="input"], select, div[data-baseweb="select"] {
    border: 3px solid #000000 !important;
    border-radius: 6px !important;
    background-color: #FFFFFF !important;
    color: #000000 !important;
    box-shadow: 3px 3px 0px 0px #000000 !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
}

/* Ensure all widget labels, slider text, and inputs have high contrast black text */
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"],
label,
.stSlider label,
.stNumberInput label,
.stDateInput label {
    color: #000000 !important;
    font-weight: 900 !important;
    font-family: 'Outfit', sans-serif !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}

[data-testid="stSlider"] *,
[data-testid="stNumberInput"] *,
[data-testid="stDateInput"] *,
[data-baseweb="input"] * {
    color: #000000 !important;
    font-family: 'Outfit', sans-serif !important;
}

/* Metric Card - Uniform Squares */
.neo-card {
    background-color: #FFF275; /* Pastel yellow */
    border: 4px solid #000000;
    border-radius: 12px;
    padding: 1.25rem;
    margin: 0 auto 1.25rem auto;
    box-shadow: 6px 6px 0px 0px #000000;
    transition: transform 0.2s ease;
    width: 100%;
    max-width: 220px;
    aspect-ratio: 1 / 1;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-sizing: border-box !important;
}

.neo-card:hover {
    transform: scale(1.04);
}

.neo-card-pink {
    background-color: #FFB7B2; /* Pastel pink */
}

.neo-card-blue {
    background-color: #D4C4FB; /* Pastel purple */
}

.neo-card-green {
    background-color: #BFFF80; /* Pastel green */
}

.neo-card-title {
    font-family: 'Lexend Mega', sans-serif;
    font-weight: 900;
    font-size: 0.9rem;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
    color: #000000;
    border-bottom: 2px solid #000000;
    padding-bottom: 0.25rem;
}

.neo-card-value {
    font-family: 'Lexend Mega', sans-serif;
    font-weight: 900;
    font-size: clamp(1.2rem, 5vw, 2rem) !important;
    color: #000000;
    margin: 0.25rem 0;
}

.neo-card-trend {
    font-size: 0.85rem;
    font-weight: 900;
    color: #000000;
    background-color: #FFFFFF;
    border: 2px solid #000000;
    border-radius: 4px;
    padding: 0.15rem 0.5rem;
    display: inline-block;
}

/* Brutalist Header graphic box */
.brutalist-header-box {
    background: #E8F0FE;
    border: 4px solid #000000;
    border-radius: 8px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 8px 8px 0px 0px #000000;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.brutalist-badge {
    background: #FEE440;
    border: 3px solid #000000;
    font-family: 'Lexend Mega', sans-serif;
    font-weight: 900;
    font-size: 0.8rem;
    padding: 0.25rem 0.75rem;
    border-radius: 4px;
    text-transform: uppercase;
    box-shadow: 2px 2px 0px 0px #000000;
}

/* Sidebar Radio Navigation Override - Pure Neo Brutalism */
/* Sidebar Radio Navigation Override - Pure Neo Brutalism */
[data-testid="stSidebar"] div[role="radiogroup"] {
    display: flex !important;
    flex-direction: column !important;
    gap: 0.6rem !important;
}

/* Reset parent option containers to prevent double borders */
[data-testid="stSidebar"] div[role="radiogroup"] > div {
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin: 0 !important;
}

[data-testid="stSidebar"] div[role="radiogroup"] label,
[data-testid="stSidebar"] div[role="radiogroup"] [role="radio"] {
    background-color: #FFFFFF !important;
    color: #000000 !important;
    border: 4px solid #000000 !important;
    border-radius: 0px !important; /* Sharp brutalist blocks */
    padding: 0.8rem 1.2rem !important;
    margin-bottom: 0.3rem !important;
    box-shadow: 4px 4px 0px 0px #000000 !important;
    font-weight: 900 !important;
    cursor: pointer !important;
    display: flex !important;
    align-items: center !important;
    width: 100% !important;
    transition: all 0.1s ease-in-out !important;
}

[data-testid="stSidebar"] div[role="radiogroup"] label:hover,
[data-testid="stSidebar"] div[role="radiogroup"] [role="radio"]:hover {
    transform: translate(-2px, -2px) !important;
    box-shadow: 6px 6px 0px 0px #000000 !important;
    background-color: #FFB7B2 !important; /* Pastel pink hover */
}

[data-testid="stSidebar"] div[role="radiogroup"] label:has(input[type="radio"]:checked),
[data-testid="stSidebar"] div[role="radiogroup"] [role="radio"]:has(input[type="radio"]:checked),
[data-testid="stSidebar"] div[role="radiogroup"] [aria-checked="true"] {
    background-color: #FFF275 !important; /* Pastel yellow checked */
    border: 4px solid #000000 !important;
    box-shadow: 4px 4px 0px 0px #000000 !important;
}

/* Hide default circle inputs */
[data-testid="stSidebar"] div[role="radiogroup"] label div[role="presentation"],
[data-testid="stSidebar"] div[role="radiogroup"] label input,
[data-testid="stSidebar"] div[role="radiogroup"] [role="radio"] div[role="presentation"],
[data-testid="stSidebar"] div[role="radiogroup"] [role="radio"] input {
    display: none !important;
}

/* Style all text inside the navigation items to follow Neo Brutalism and force black color */
[data-testid="stSidebar"] div[role="radiogroup"] label *,
[data-testid="stSidebar"] div[role="radiogroup"] [role="radio"] * {
    font-size: 1.05rem !important;
    font-weight: 900 !important;
    text-transform: uppercase !important;
    font-family: 'Outfit', sans-serif !important;
    color: #000000 !important;
    letter-spacing: 0.5px !important;
}

/* Ensure emoji and text align nicely on a single row */
[data-testid="stSidebar"] div[role="radiogroup"] label div[data-testid="stMarkdownContainer"] {
    display: flex !important;
    align-items: center !important;
    gap: 0.6rem !important;
    width: 100% !important;
}

[data-testid="stSidebar"] div[role="radiogroup"] label div[data-testid="stMarkdownContainer"] p {
    display: flex !important;
    align-items: center !important;
    gap: 0.6rem !important;
    margin: 0 !important;
    padding: 0 !important;
    width: 100% !important;
}

/* --- HIGH-CONTRAST AND WIDGET VISIBILITY FIXES --- */

/* st.metric container styling */
div[data-testid="stMetric"] {
    background-color: #FFFFFF !important;
    border: 3px solid #000000 !important;
    border-radius: 8px !important;
    padding: 0.75rem 0.6rem !important;
    box-shadow: 4px 4px 0px 0px #000000 !important;
    text-align: center !important;
    min-height: 100px !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: space-between !important;
}

/* st.metric label styling */
div[data-testid="stMetricLabel"] *, 
div[data-testid="stMetricLabel"] {
    color: #000000 !important;
    font-weight: 800 !important;
    font-family: 'Outfit', sans-serif !important;
    text-transform: uppercase !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.2px !important;
    white-space: normal !important;
    line-height: 1.2 !important;
}

/* st.metric value styling */
div[data-testid="stMetricValue"] *, 
div[data-testid="stMetricValue"] {
    color: #000000 !important;
    font-weight: 900 !important;
    font-family: 'Lexend Mega', sans-serif !important;
    font-size: 1.15rem !important;
    white-space: nowrap !important;
}

/* st.text_area container / textarea widget styling */
textarea {
    background-color: #FFFFFF !important;
    color: #000000 !important;
    border: 3px solid #000000 !important;
    border-radius: 8px !important;
    box-shadow: 4px 4px 0px 0px #000000 !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
    padding: 1rem !important;
    font-size: 1rem !important;
}

/* Streamlit container form card custom styling */
div.element-container:has(div.stSlider), 
div.element-container:has(div.stNumberInput) {
    color: #000000 !important;
}

/* Wide card layout overrides for highlights */
.neo-card-wide {
    aspect-ratio: auto !important;
    max-width: none !important;
    height: auto !important;
    min-height: 120px !important;
}

/* Container styling for forms to replace broken raw HTML divs */
.st-key-daily_entry_form, .st-key-settings_form {
    border: 4px solid #000000 !important;
    background-color: #FFFFFF !important;
    padding: 2rem !important;
    box-shadow: 8px 8px 0px 0px #000000 !important;
    border-radius: 8px !important;
    margin-bottom: 2rem !important;
}
"""

def inject_theme_styles():
    """Injects custom Neo-Brutalist CSS into the Streamlit session."""
    st.markdown(f"<style>{NEO_BRUTALIST_CSS}</style>", unsafe_allow_html=True)

def draw_card(title, value, trend_text="", trend_arrow="→", card_style="default", wide=False):
    """
    Renders a Neo-Brutalist HTML card component.
    card_style can be: 'default', 'pink', 'blue', 'green' (or 'primary', 'secondary', 'gold')
    """
    style_cls = "neo-card"
    if card_style in ["pink", "primary"]:
        style_cls += " neo-card-pink"
    elif card_style in ["blue", "secondary"]:
        style_cls += " neo-card-blue"
    elif card_style in ["green", "gold"]:
        style_cls += " neo-card-green"
        
    if wide:
        style_cls += " neo-card-wide"
        
    trend_html = ""
    if trend_text:
        trend_html = f'<div class="neo-card-trend">{trend_arrow} {trend_text}</div>'
        
    card_html = f"""
    <div class="{style_cls}">
        <div class="neo-card-title">{title}</div>
        <div class="neo-card-value">{value}</div>
        {trend_html}
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

def render_svg(graphic_key):
    """Safely renders one of our custom SVG drawings inside Streamlit."""
    if graphic_key in SVG_GRAPHICS:
        st.markdown(SVG_GRAPHICS[graphic_key], unsafe_allow_html=True)
