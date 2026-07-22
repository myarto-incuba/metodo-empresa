import streamlit as st

def apply_styles():
    st.markdown(
        """
        <style>
        .block-container {padding-top: 1.4rem; padding-bottom: 3rem;}
        [data-testid="stMetric"] {
            border: 1px solid rgba(128,128,128,.2);
            padding: 14px;
            border-radius: 14px;
        }
        .method-card {
            border: 1px solid rgba(128,128,128,.22);
            border-radius: 16px;
            padding: 18px;
            margin-bottom: 12px;
        }
        .method-kicker {
            font-size: .78rem;
            text-transform: uppercase;
            letter-spacing: .08em;
            opacity: .65;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
