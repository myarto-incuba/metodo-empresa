from __future__ import annotations

import html
import streamlit as st


def apply_incubatour_brand() -> None:
    st.markdown(
        """
        <style>
        :root {
            --inc-ink: #101114;
            --inc-panel: #17181d;
            --inc-panel-2: #1d1f25;
            --inc-paper: #f7f3e9;
            --inc-lime: #c9f43f;
            --inc-violet: #775cff;
            --inc-coral: #ff675f;
            --inc-muted: #a7a5ae;
            --inc-border: rgba(255,255,255,.10);
        }

        html, body, [class*="css"] {
            font-family: Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont,
                         "Segoe UI", sans-serif;
        }

        .stApp {
            background:
                radial-gradient(circle at 92% 4%, rgba(119,92,255,.13), transparent 25rem),
                radial-gradient(circle at 2% 92%, rgba(201,244,63,.07), transparent 28rem),
                var(--inc-ink);
            color: var(--inc-paper);
        }

        .block-container {
            max-width: 1380px;
            padding-top: 1.8rem;
            padding-bottom: 5rem;
        }

        [data-testid="stSidebar"] {
            background: #15161a;
            border-right: 1px solid var(--inc-border);
        }

        [data-testid="stSidebarNav"] span {
            font-weight: 650;
        }

        h1, h2, h3, h4 {
            color: var(--inc-paper);
            letter-spacing: -.035em;
        }

        p, li, label, .stCaption {
            color: rgba(247,243,233,.72);
        }

        hr { border-color: var(--inc-border); }

        .inc-wordmark {
            display:flex; align-items:center; gap:.75rem; margin-bottom:1.8rem;
        }
        .inc-mark {
            width:42px; height:42px; border-radius:14px;
            background:var(--inc-lime); color:var(--inc-ink);
            display:grid; place-items:center; font-weight:950; font-size:1.25rem;
            transform:rotate(-5deg);
        }
        .inc-brand-name {
            color:var(--inc-paper); font-size:.9rem; font-weight:900; letter-spacing:.12em;
        }
        .inc-product-name {
            color:var(--inc-lime); font-size:.68rem; font-weight:800; letter-spacing:.10em;
        }

        .inc-eyebrow {
            display:inline-flex; align-items:center; gap:.55rem;
            color:var(--inc-lime); font-size:.72rem; text-transform:uppercase;
            letter-spacing:.16em; font-weight:800; margin-bottom:.85rem;
        }
        .inc-eyebrow:before {
            content:""; width:22px; height:3px; border-radius:9px; background:var(--inc-lime);
        }

        .inc-hero {
            position:relative; overflow:hidden;
            border:1px solid var(--inc-border); border-radius:28px;
            padding:3rem; margin-bottom:1.4rem;
            background:linear-gradient(135deg,#1b1c22 0%,#15161a 72%);
        }
        .inc-hero:after {
            content:"MÉTODO"; position:absolute; right:-1rem; bottom:-3.2rem;
            font-size:8rem; font-weight:950; letter-spacing:-.08em;
            color:rgba(201,244,63,.05); transform:rotate(-4deg);
        }
        .inc-hero h1 {
            max-width:790px; font-size:clamp(2.8rem,5vw,5.3rem);
            line-height:.96; margin:0 0 1.15rem; letter-spacing:-.065em;
        }
        .inc-hero h1 span { color:var(--inc-lime); }
        .inc-hero-copy {
            max-width:650px; font-size:1.05rem; line-height:1.6;
            color:rgba(247,243,233,.68);
        }
        .inc-tagline {
            display:inline-flex; padding:.62rem .88rem; margin-top:1.2rem;
            border:1px solid rgba(201,244,63,.32); border-radius:999px;
            color:var(--inc-lime); background:rgba(201,244,63,.06);
            font-size:.76rem; font-weight:800;
        }

        .inc-card, .inc-audit-card, .inc-panel {
            background:rgba(24,25,30,.96);
            border:1px solid var(--inc-border);
            border-radius:22px;
        }
        .inc-card { padding:1.3rem 1.4rem; min-height:100%; }
        .inc-card-accent { border-top:4px solid var(--inc-lime); }
        .inc-card-kicker {
            color:var(--inc-muted); font-size:.68rem; letter-spacing:.13em;
            text-transform:uppercase; font-weight:800;
        }
        .inc-card-value {
            color:var(--inc-paper); font-size:2.65rem; line-height:1;
            font-weight:950; letter-spacing:-.06em; margin:.65rem 0 .45rem;
        }
        .inc-card-label { color:rgba(247,243,233,.63); font-size:.88rem; }

        .inc-audit-card { padding:1.35rem; margin-bottom:.8rem; }
        .inc-company { color:var(--inc-paper); font-size:1.3rem; font-weight:900; }
        .inc-meta { color:rgba(247,243,233,.52); font-size:.82rem; margin-top:.25rem; }
        .inc-badge {
            display:inline-flex; padding:.35rem .62rem; border-radius:999px;
            background:rgba(119,92,255,.15); color:#c4baff;
            font-size:.68rem; font-weight:850; letter-spacing:.05em;
        }

        .inc-workspace {
            border:1px solid var(--inc-border); border-radius:26px;
            background:linear-gradient(135deg,rgba(29,31,37,.98),rgba(20,21,25,.98));
            padding:1.55rem 1.7rem; margin-bottom:1.2rem;
        }
        .inc-workspace-company {
            color:var(--inc-paper); font-size:2rem; font-weight:950; letter-spacing:-.05em;
        }
        .inc-workspace-meta {
            color:rgba(247,243,233,.53); font-size:.82rem; margin-top:.25rem;
        }
        .inc-progress-track {
            height:8px; background:rgba(255,255,255,.08); border-radius:999px;
            overflow:hidden; margin:.95rem 0 .6rem;
        }
        .inc-progress-fill {
            height:100%; border-radius:999px;
            background:linear-gradient(90deg,var(--inc-lime),var(--inc-violet));
        }
        .inc-steps {
            display:grid; grid-template-columns:repeat(5,1fr); gap:.55rem; margin-top:1rem;
        }
        .inc-step {
            padding:.75rem .8rem; border:1px solid var(--inc-border);
            border-radius:14px; background:rgba(255,255,255,.025);
        }
        .inc-step-name {
            color:rgba(247,243,233,.48); font-size:.64rem; letter-spacing:.08em;
            text-transform:uppercase; font-weight:800;
        }
        .inc-step-value {
            color:var(--inc-paper); font-size:.95rem; font-weight:900; margin-top:.15rem;
        }

        .inc-question-shell { max-width:900px; margin:1rem auto 0; }
        .inc-question-number {
            color:var(--inc-lime); font-size:.74rem; font-weight:850;
            text-transform:uppercase; letter-spacing:.14em;
        }
        .inc-conversation-title {
            color:rgba(247,243,233,.52); font-size:.92rem; font-weight:700;
            margin:.9rem 0 .2rem;
        }
        .inc-question {
            color:var(--inc-paper); font-size:clamp(2rem,4vw,3.55rem);
            line-height:1.08; font-weight:900; letter-spacing:-.055em;
            margin:.55rem 0 1.8rem;
        }

        .inc-diagnosis-hero {
            display:grid; grid-template-columns:1.05fr 2fr; gap:1rem; margin-bottom:1rem;
        }
        .inc-score {
            padding:1.8rem; border-radius:24px; border:1px solid var(--inc-border);
            background:linear-gradient(145deg,rgba(201,244,63,.12),rgba(24,25,30,.98));
        }
        .inc-score-number {
            color:var(--inc-lime); font-size:5rem; line-height:.9;
            font-weight:950; letter-spacing:-.08em;
        }
        .inc-score-label { color:rgba(247,243,233,.55); margin-top:.7rem; }
        .inc-priority {
            padding:1.45rem; border-radius:24px; border:1px solid var(--inc-border);
            background:rgba(24,25,30,.96);
        }

        .inc-area-row {
            display:grid; grid-template-columns:145px 1fr 56px; gap:.8rem;
            align-items:center; margin:.85rem 0;
        }
        .inc-area-name { color:rgba(247,243,233,.72); font-size:.85rem; font-weight:700; }
        .inc-area-track {
            height:10px; border-radius:999px; overflow:hidden; background:rgba(255,255,255,.08);
        }
        .inc-area-fill {
            height:100%; border-radius:999px;
            background:linear-gradient(90deg,var(--inc-lime),var(--inc-violet));
        }
        .inc-area-value { color:var(--inc-paper); font-size:.82rem; font-weight:850; text-align:right; }

        .inc-section-title {
            font-size:1.55rem; font-weight:900; color:var(--inc-paper);
            margin:2.2rem 0 1rem; letter-spacing:-.035em;
        }
        .inc-footer-line {
            margin-top:4rem; padding-top:1rem; border-top:1px solid var(--inc-border);
            color:rgba(247,243,233,.33); font-size:.68rem; letter-spacing:.09em;
            text-transform:uppercase;
        }

        div[role="radiogroup"] { gap:.55rem; }
        div[role="radiogroup"] label {
            background:#1b1c21; border:1px solid var(--inc-border);
            border-radius:16px; padding:.72rem .95rem;
        }
        div[role="radiogroup"] label:hover { border-color:rgba(201,244,63,.42); }

        div[data-testid="stMetric"] {
            background:var(--inc-panel); border:1px solid var(--inc-border);
            border-radius:20px; padding:1rem 1.1rem;
        }
        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-color:var(--inc-border); border-radius:22px;
            background:rgba(24,25,30,.78);
        }

        .stButton > button, .stFormSubmitButton > button {
            border-radius:14px; min-height:46px; font-weight:850;
            border:1px solid rgba(255,255,255,.14);
        }
        .stButton > button[kind="primary"],
        .stFormSubmitButton > button[kind="primary"] {
            background:var(--inc-lime); color:var(--inc-ink); border-color:var(--inc-lime);
        }
        .stButton > button[kind="primary"]:hover,
        .stFormSubmitButton > button[kind="primary"]:hover {
            background:#d8ff67; color:var(--inc-ink); border-color:#d8ff67;
        }

        .stProgress > div > div > div > div {
            background:linear-gradient(90deg,var(--inc-lime),var(--inc-violet));
        }
        input, textarea, [data-baseweb="select"] > div {
            background:#191a1f !important; border-color:rgba(255,255,255,.12) !important;
            color:var(--inc-paper) !important; border-radius:13px !important;
        }

        @media (max-width: 900px) {
            .inc-steps { grid-template-columns:1fr 1fr; }
            .inc-diagnosis-hero { grid-template-columns:1fr; }
            .inc-hero { padding:2rem; }
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


def render_footer() -> None:
    st.markdown(
        '<div class="inc-footer-line">Incubatour · Le ponemos método a tu locura.</div>',
        unsafe_allow_html=True,
    )


def safe(value: object) -> str:
    return html.escape(str(value or ""))
