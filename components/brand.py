from __future__ import annotations

import streamlit as st


BRAND = {
    "ink": "#111214",
    "paper": "#F6F3EC",
    "lime": "#C7F43D",
    "violet": "#7357FF",
    "coral": "#FF6259",
    "muted": "#A7A3AE",
}


def apply_incubatour_brand() -> None:
    st.markdown(
        """
        <style>
        :root {
            --inc-ink: #111214;
            --inc-paper: #F6F3EC;
            --inc-lime: #C7F43D;
            --inc-violet: #7357FF;
            --inc-coral: #FF6259;
            --inc-muted: #A7A3AE;
            --inc-panel: #18191D;
            --inc-border: rgba(255,255,255,.10);
        }

        html, body, [class*="css"] {
            font-family: Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont,
                         "Segoe UI", sans-serif;
        }

        .stApp {
            background:
                radial-gradient(circle at 85% 0%, rgba(115,87,255,.15), transparent 28rem),
                radial-gradient(circle at 0% 100%, rgba(199,244,61,.08), transparent 28rem),
                var(--inc-ink);
            color: var(--inc-paper);
        }

        .block-container {
            max-width: 1380px;
            padding-top: 2rem;
            padding-bottom: 5rem;
        }

        [data-testid="stSidebar"] {
            background: #15161A;
            border-right: 1px solid var(--inc-border);
        }

        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
        [data-testid="stSidebar"] label {
            color: rgba(246,243,236,.82);
        }

        [data-testid="stSidebarNav"] span {
            font-weight: 620;
        }

        h1, h2, h3 {
            color: var(--inc-paper);
            letter-spacing: -.035em;
        }

        p, li, label, .stCaption {
            color: rgba(246,243,236,.74);
        }

        hr {
            border-color: var(--inc-border);
        }

        .inc-wordmark {
            display: flex;
            align-items: center;
            gap: .75rem;
            margin-bottom: 2.6rem;
        }

        .inc-mark {
            width: 42px;
            height: 42px;
            border-radius: 14px;
            background: var(--inc-lime);
            color: var(--inc-ink);
            display: grid;
            place-items: center;
            font-weight: 950;
            font-size: 1.3rem;
            transform: rotate(-5deg);
            box-shadow: 0 12px 32px rgba(199,244,61,.16);
        }

        .inc-brand-name {
            color: var(--inc-paper);
            font-size: .9rem;
            font-weight: 850;
            letter-spacing: .12em;
        }

        .inc-product-name {
            color: var(--inc-lime);
            font-size: .68rem;
            font-weight: 760;
            letter-spacing: .10em;
            margin-top: .12rem;
        }

        .inc-eyebrow {
            display: inline-flex;
            align-items: center;
            gap: .55rem;
            color: var(--inc-lime);
            font-size: .74rem;
            text-transform: uppercase;
            letter-spacing: .16em;
            font-weight: 760;
            margin-bottom: 1rem;
        }

        .inc-eyebrow:before {
            content: "";
            display: inline-block;
            width: 24px;
            height: 3px;
            border-radius: 4px;
            background: var(--inc-lime);
        }

        .inc-hero {
            position: relative;
            overflow: hidden;
            background: linear-gradient(135deg, #1A1B20 0%, #17171B 70%);
            border: 1px solid var(--inc-border);
            border-radius: 28px;
            padding: 3rem;
            margin-bottom: 1.8rem;
            min-height: 260px;
        }

        .inc-hero:after {
            content: "MÉTODO";
            position: absolute;
            right: -1rem;
            bottom: -3.5rem;
            font-size: 8rem;
            line-height: 1;
            font-weight: 950;
            color: rgba(199,244,61,.055);
            letter-spacing: -.08em;
            transform: rotate(-4deg);
        }

        .inc-hero h1 {
            max-width: 760px;
            font-size: clamp(2.8rem, 5vw, 5.4rem);
            line-height: .95;
            margin: 0 0 1.3rem;
            letter-spacing: -.065em;
        }

        .inc-hero h1 span {
            color: var(--inc-lime);
        }

        .inc-hero-copy {
            max-width: 620px;
            font-size: 1.06rem;
            line-height: 1.6;
            color: rgba(246,243,236,.70);
        }

        .inc-tagline {
            display: inline-flex;
            padding: .65rem .9rem;
            border: 1px solid rgba(199,244,61,.35);
            border-radius: 999px;
            color: var(--inc-lime);
            background: rgba(199,244,61,.06);
            font-size: .78rem;
            font-weight: 750;
            margin-top: 1.25rem;
        }

        .inc-card {
            background: var(--inc-panel);
            border: 1px solid var(--inc-border);
            border-radius: 22px;
            padding: 1.35rem 1.45rem;
            min-height: 100%;
            transition: transform .18s ease, border-color .18s ease;
        }

        .inc-card:hover {
            transform: translateY(-2px);
            border-color: rgba(199,244,61,.30);
        }

        .inc-card-kicker {
            color: var(--inc-muted);
            font-size: .7rem;
            letter-spacing: .13em;
            text-transform: uppercase;
            font-weight: 740;
        }

        .inc-card-value {
            color: var(--inc-paper);
            font-size: 2.55rem;
            line-height: 1;
            font-weight: 900;
            letter-spacing: -.06em;
            margin: .65rem 0 .45rem;
        }

        .inc-card-label {
            color: rgba(246,243,236,.68);
            font-size: .9rem;
        }

        .inc-card-accent {
            border-top: 4px solid var(--inc-lime);
        }

        .inc-audit-card {
            border: 1px solid var(--inc-border);
            border-radius: 22px;
            padding: 1.35rem;
            background: rgba(24,25,29,.95);
            margin-bottom: .9rem;
        }

        .inc-company {
            color: var(--inc-paper);
            font-size: 1.25rem;
            font-weight: 850;
            letter-spacing: -.025em;
        }

        .inc-meta {
            color: rgba(246,243,236,.55);
            font-size: .82rem;
            margin-top: .25rem;
        }

        .inc-badge {
            display: inline-flex;
            align-items: center;
            padding: .38rem .65rem;
            border-radius: 999px;
            background: rgba(115,87,255,.14);
            color: #BFB2FF;
            font-size: .72rem;
            font-weight: 750;
        }

        .inc-question-shell {
            max-width: 900px;
            margin: 1rem auto 0;
        }

        .inc-question-number {
            color: var(--inc-lime);
            font-size: .77rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: .14em;
        }

        .inc-question {
            color: var(--inc-paper);
            font-size: clamp(2rem, 4vw, 3.65rem);
            line-height: 1.08;
            font-weight: 860;
            letter-spacing: -.055em;
            margin: .9rem 0 2rem;
        }

        div[role="radiogroup"] {
            gap: .65rem;
        }

        div[role="radiogroup"] label {
            background: #1B1C21;
            border: 1px solid var(--inc-border);
            border-radius: 16px;
            padding: .75rem 1rem;
            transition: border-color .18s ease, transform .18s ease;
        }

        div[role="radiogroup"] label:hover {
            border-color: rgba(199,244,61,.45);
            transform: translateY(-1px);
        }

        div[data-testid="stMetric"] {
            background: var(--inc-panel);
            border: 1px solid var(--inc-border);
            border-radius: 20px;
            padding: 1.05rem 1.15rem;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-color: var(--inc-border);
            border-radius: 22px;
            background: rgba(24,25,29,.78);
        }

        div[data-baseweb="tab-list"] {
            gap: .35rem;
            border-bottom: 1px solid var(--inc-border);
        }

        button[data-baseweb="tab"] {
            border-radius: 12px 12px 0 0;
            font-weight: 700;
        }

        .stButton > button,
        .stFormSubmitButton > button {
            border-radius: 14px;
            min-height: 46px;
            font-weight: 800;
            border: 1px solid rgba(255,255,255,.14);
        }

        .stButton > button[kind="primary"],
        .stFormSubmitButton > button[kind="primary"] {
            background: var(--inc-lime);
            color: var(--inc-ink);
            border-color: var(--inc-lime);
        }

        .stButton > button[kind="primary"]:hover,
        .stFormSubmitButton > button[kind="primary"]:hover {
            background: #D6FF62;
            color: var(--inc-ink);
            border-color: #D6FF62;
        }

        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, var(--inc-lime), var(--inc-violet));
        }

        input, textarea, [data-baseweb="select"] > div {
            background: #191A1F !important;
            border-color: rgba(255,255,255,.12) !important;
            color: var(--inc-paper) !important;
            border-radius: 13px !important;
        }

        .inc-section-title {
            font-size: 1.55rem;
            font-weight: 850;
            color: var(--inc-paper);
            margin: 2.4rem 0 1rem;
            letter-spacing: -.035em;
        }

        .inc-footer-line {
            margin-top: 4rem;
            padding-top: 1rem;
            border-top: 1px solid var(--inc-border);
            color: rgba(246,243,236,.38);
            font-size: .72rem;
            letter-spacing: .08em;
            text-transform: uppercase;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_wordmark() -> None:
    st.markdown(
        """
        <div class="inc-wordmark">
            <div class="inc-mark">I</div>
            <div>
                <div class="inc-brand-name">INCUBATOUR</div>
                <div class="inc-product-name">MÉTODO EMPRESA</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_page_intro(eyebrow: str, title: str, description: str = "") -> None:
    st.markdown(f'<div class="inc-eyebrow">{eyebrow}</div>', unsafe_allow_html=True)
    st.markdown(f"# {title}")
    if description:
        st.caption(description)


def render_footer() -> None:
    st.markdown(
        '<div class="inc-footer-line">Incubatour · Le ponemos método a tu locura.</div>',
        unsafe_allow_html=True,
    )
