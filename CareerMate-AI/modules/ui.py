import textwrap

import streamlit as st


def load_css():

    st.markdown(
        textwrap.dedent(
            """
        <style>

        /* ============================================
           DESIGN TOKENS
        ============================================ */

        :root {
            --bg-primary: #0f172a;
            --bg-secondary: #111827;
            --bg-tertiary: #1e293b;
            --surface: #16213a;
            --surface-hover: #1c2b4a;
            --border-color: rgba(148, 163, 184, 0.15);
            --text-primary: #f1f5f9;
            --text-secondary: #94a3b8;
            --accent-blue: #2563eb;
            --accent-purple: #7c3aed;
            --accent-gradient: linear-gradient(135deg, #2563eb, #7c3aed);
            --success: #22c55e;
            --warning: #f59e0b;
            --danger: #ef4444;
        }

        /* ============================================
           APP BACKGROUND
        ============================================ */

        .stApp {
            background: linear-gradient(
                135deg,
                #0f172a,
                #111827,
                #1e293b
            );
            color: var(--text-primary);
        }

        /* Force readable text everywhere on the dark background */
        .stApp, .stApp p, .stApp span, .stApp label,
        .stApp li, .stMarkdown, .stMarkdown p {
            color: var(--text-primary);
        }

        h1, h2, h3, h4, h5, h6 {
            color: var(--text-primary) !important;
            font-weight: 700 !important;
        }

        .stCaption, [data-testid="stCaptionContainer"] {
            color: var(--text-secondary) !important;
        }

        /* ============================================
           SIDEBAR
        ============================================ */

        [data-testid="stSidebar"] {
            background: #0b1120;
            border-right: 1px solid var(--border-color);
        }

        [data-testid="stSidebar"] * {
            color: var(--text-primary) !important;
        }

        [data-testid="stSidebar"] .stRadio label {
            padding: 6px 4px;
            border-radius: 8px;
            transition: background 0.15s ease;
        }

        [data-testid="stSidebar"] .stRadio label:hover {
            background: var(--surface-hover);
        }

        /* ============================================
           METRICS
        ============================================ */

        [data-testid="stMetric"] {
            padding: 20px;
            border-radius: 15px;
            background: var(--surface);
            border: 1px solid var(--border-color);
        }

        [data-testid="stMetricLabel"] {
            color: var(--text-secondary) !important;
        }

        [data-testid="stMetricValue"] {
            color: var(--text-primary) !important;
        }

        /* ============================================
           BUTTONS
        ============================================ */

        .stButton > button {
            width: 100%;
            border-radius: 10px;
            font-weight: 600;
            background: var(--accent-gradient);
            color: #ffffff;
            border: none;
            padding: 0.6em 1em;
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }

        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 18px rgba(124, 58, 237, 0.35);
            color: #ffffff;
        }

        .stButton > button:active {
            transform: translateY(0);
        }

        /* ============================================
           CARDS
        ============================================ */

        .career-card {
            padding: 25px;
            border-radius: 18px;
            margin-bottom: 15px;
            background: var(--surface);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
        }

        .career-card h3 {
            margin-top: 0;
            color: var(--text-primary) !important;
        }

        .career-card p {
            color: var(--text-secondary) !important;
            margin-bottom: 0;
        }

        /* ============================================
           HERO
        ============================================ */

        .hero {
            padding: 45px;
            border-radius: 25px;
            background: var(--accent-gradient);
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(37, 99, 235, 0.25);
        }

        .hero h1 {
            color: white !important;
            font-size: 48px;
            margin-bottom: 10px;
        }

        .hero p {
            color: rgba(255, 255, 255, 0.9) !important;
            font-size: 18px;
            margin-bottom: 0;
        }

        /* ============================================
           INPUTS (text input, textarea, selectbox)
        ============================================ */

        .stTextInput input,
        .stTextArea textarea,
        .stNumberInput input {
            background: var(--bg-tertiary) !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 8px !important;
        }

        .stTextInput input:focus,
        .stTextArea textarea:focus {
            border-color: var(--accent-purple) !important;
            box-shadow: 0 0 0 1px var(--accent-purple) !important;
        }

        [data-baseweb="select"] > div {
            background: var(--bg-tertiary) !important;
            border-color: var(--border-color) !important;
            color: var(--text-primary) !important;
        }

        /* Selected pills in multiselect */
        [data-baseweb="tag"] {
            background: var(--accent-purple) !important;
        }

        /* ============================================
           ALERTS (info / success / warning / error)
        ============================================ */

        [data-testid="stAlert"] {
            border-radius: 12px;
            border: 1px solid var(--border-color);
        }

        /* ============================================
           EXPANDERS
        ============================================ */

        [data-testid="stExpander"] {
            background: var(--surface);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            overflow: hidden;
        }

        [data-testid="stExpander"] summary {
            color: var(--text-primary) !important;
            font-weight: 600;
        }

        /* ============================================
           CHAT
        ============================================ */

        [data-testid="stChatMessage"] {
            background: var(--surface);
            border: 1px solid var(--border-color);
            border-radius: 14px;
            padding: 4px 8px;
        }

        /* ============================================
           PROGRESS BAR
        ============================================ */

        .stProgress > div > div {
            background: var(--accent-gradient) !important;
        }

        /* ============================================
           DIVIDERS
        ============================================ */

        hr {
            border-color: var(--border-color) !important;
        }

        /* ============================================
           DATAFRAMES / TABLES
        ============================================ */

        [data-testid="stDataFrame"] {
            border-radius: 10px;
            overflow: hidden;
            border: 1px solid var(--border-color);
        }

        </style>
            """
        ),
        unsafe_allow_html=True
    )


def hero_section():

    st.markdown(
        '<div class="hero"><h1>🚀 CareerMate AI</h1>'
        '<p>Your intelligent career companion for discovering '
        'opportunities, analyzing skills, and building your future.</p>'
        '</div>',
        unsafe_allow_html=True
    )


def info_card(title, description):

    st.markdown(
        f'<div class="career-card"><h3>{title}</h3>'
        f'<p>{description}</p></div>',
        unsafe_allow_html=True
    )