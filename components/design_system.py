from __future__ import annotations

import streamlit as st


def apply_design_system() -> None:
    st.markdown(
        """
        <style>
        :root {
            --bg: #0b0d12;
            --sidebar: #0e1117;
            --surface: #11151c;
            --surface-2: #151a22;
            --text: #f5f7fa;
            --muted: #939cab;
            --faint: #626c7a;
            --line: rgba(255,255,255,.075);
            --line-strong: rgba(255,255,255,.12);
            --accent: #c13a79;
            --accent-hover: #a92f69;
            --accent-soft: rgba(193,58,121,.12);
            --success: #8cbf3f;
            --warning: #e6a34a;
        }

        html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
            background: var(--bg);
            color: var(--text);
        }

        [data-testid="stMainBlockContainer"] {
            max-width: 1180px;
            padding: 2.25rem 3.25rem 5rem;
        }

        [data-testid="stSidebar"] {
            background: var(--sidebar);
            border-right: 1px solid var(--line);
        }

        [data-testid="stSidebar"] [data-testid="stSidebarContent"] {
            padding-top: 1.25rem;
        }

        [data-testid="stSidebarNav"] span,
        [data-testid="stSidebarNav"] p {
            font-size: .88rem;
        }

        [data-testid="stSidebarNav"] a {
            border-radius: 8px;
            margin: 2px 10px;
            min-height: 38px;
        }

        [data-testid="stSidebarNav"] a[aria-current="page"] {
            background: var(--accent-soft);
            color: #fff;
        }

        h1, h2, h3, h4 {
            color: var(--text);
            letter-spacing: -.035em;
        }
        h1 { font-size: 2.1rem !important; font-weight: 730 !important; }
        h2 { font-size: 1.45rem !important; font-weight: 680 !important; }
        h3 { font-size: 1.06rem !important; font-weight: 650 !important; }
        p, label, li { color: var(--text); }
        small, [data-testid="stCaptionContainer"] { color: var(--muted) !important; }

        hr { border-color: var(--line) !important; }

        .stButton > button,
        .stFormSubmitButton > button,
        .stDownloadButton > button {
            min-height: 2.45rem;
            border: 1px solid var(--line-strong);
            border-radius: 9px;
            background: var(--surface-2);
            color: var(--text);
            font-weight: 620;
            box-shadow: none;
            transition: all .15s ease;
        }
        .stButton > button:hover,
        .stFormSubmitButton > button:hover,
        .stDownloadButton > button:hover {
            border-color: rgba(193,58,121,.55);
            background: #1a202a;
            transform: translateY(-1px);
        }
        button[data-testid="baseButton-primary"],
        .stButton > button[kind="primary"],
        .stFormSubmitButton > button[kind="primary"] {
            background: var(--accent);
            border-color: var(--accent);
            color: white;
            box-shadow: 0 8px 24px rgba(193,58,121,.18);
        }
        button[data-testid="baseButton-primary"]:hover,
        .stButton > button[kind="primary"]:hover,
        .stFormSubmitButton > button[kind="primary"]:hover {
            background: var(--accent-hover);
            border-color: var(--accent-hover);
        }

        [data-testid="stMetric"] {
            padding: 0;
            background: transparent;
        }
        [data-testid="stMetricLabel"] { color: var(--muted); }
        [data-testid="stMetricValue"] {
            font-size: 1.8rem;
            font-weight: 720;
            letter-spacing: -.04em;
        }

        [data-testid="stVerticalBlockBorderWrapper"] {
            border-color: var(--line) !important;
            border-radius: 12px !important;
            background: rgba(255,255,255,.012);
        }

        [data-testid="stProgressBar"] > div > div {
            background: var(--accent) !important;
        }
        [data-testid="stProgressBar"] > div {
            background: rgba(255,255,255,.08) !important;
        }

        [data-baseweb="input"] > div,
        [data-baseweb="textarea"] > div,
        [data-baseweb="select"] > div {
            background: var(--surface) !important;
            border-color: var(--line-strong) !important;
            border-radius: 9px !important;
        }

        [role="radiogroup"] label {
            background: var(--surface);
            border: 1px solid var(--line);
            border-radius: 9px;
            padding: .6rem .8rem;
            margin-right: .25rem;
        }

        [data-baseweb="tab-list"] {
            gap: 1.25rem;
            border-bottom: 1px solid var(--line);
        }
        [data-baseweb="tab"] {
            background: transparent !important;
            padding-left: 0 !important;
            padding-right: 0 !important;
        }

        [data-testid="stAlert"] {
            border-radius: 10px;
            border-color: var(--line);
        }

        #MainMenu, footer { visibility: hidden; }
        </style>
        """,
        unsafe_allow_html=True,
    )
