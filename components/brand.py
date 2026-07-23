from __future__ import annotations

import streamlit as st


def apply_incubatour_brand() -> None:
    st.markdown(
        """
        <style>
        :root{
            --bg:#0b0c0f;
            --panel:#14161b;
            --panel2:#1a1d24;
            --paper:#f6f2e8;
            --muted:#9b9da8;
            --lime:#c8ff3d;
            --purple:#7d63ff;
            --coral:#ff6b63;
            --cyan:#55d7ff;
            --border:rgba(255,255,255,.10);
        }

        .stApp{
            background:
              linear-gradient(rgba(255,255,255,.018) 1px, transparent 1px),
              linear-gradient(90deg, rgba(255,255,255,.018) 1px, transparent 1px),
              radial-gradient(circle at 85% 0%, rgba(125,99,255,.18), transparent 26rem),
              radial-gradient(circle at 0% 100%, rgba(200,255,61,.09), transparent 28rem),
              var(--bg);
            background-size:32px 32px,32px 32px,auto,auto,auto;
            color:var(--paper);
        }

        .block-container{
            max-width:1420px;
            padding-top:1.5rem;
            padding-bottom:5rem;
        }

        [data-testid="stSidebar"]{
            background:rgba(15,16,20,.98);
            border-right:1px solid var(--border);
        }

        [data-testid="stSidebarNav"]::before{
            content:"INCUBATOUR";
            display:block;
            color:var(--paper);
            font-size:.72rem;
            letter-spacing:.18em;
            font-weight:900;
            padding:.6rem 1rem .15rem;
        }

        [data-testid="stSidebarNav"]::after{
            content:"MÉTODO EMPRESA";
            display:block;
            color:var(--lime);
            font-size:.62rem;
            letter-spacing:.14em;
            font-weight:850;
            padding:0 1rem 1rem;
        }

        [data-testid="stSidebarNav"] a{
            border-radius:12px;
            margin:.15rem .55rem;
        }

        [data-testid="stSidebarNav"] a[aria-current="page"]{
            background:linear-gradient(90deg,rgba(200,255,61,.15),rgba(125,99,255,.10));
            border:1px solid rgba(200,255,61,.18);
        }

        h1,h2,h3,h4{
            color:var(--paper);
            letter-spacing:-.045em;
        }

        p,label,li,.stCaption{
            color:rgba(246,242,232,.72);
        }

        .inc-topbar{
            display:flex;
            justify-content:space-between;
            align-items:center;
            margin-bottom:1.25rem;
        }

        .inc-logo{
            display:flex;
            align-items:center;
            gap:.8rem;
        }

        .inc-logo-mark{
            width:46px;height:46px;border-radius:15px;
            background:var(--lime);
            color:#0a0b0d;
            display:grid;place-items:center;
            font-size:1.35rem;font-weight:950;
            box-shadow:0 12px 36px rgba(200,255,61,.16);
            transform:rotate(-4deg);
        }

        .inc-logo-title{
            font-size:.82rem;
            letter-spacing:.16em;
            font-weight:950;
        }

        .inc-logo-sub{
            color:var(--lime);
            font-size:.64rem;
            letter-spacing:.13em;
            font-weight:850;
            margin-top:.15rem;
        }

        .inc-status{
            border:1px solid var(--border);
            border-radius:999px;
            padding:.45rem .7rem;
            color:rgba(246,242,232,.65);
            font-size:.68rem;
            font-weight:800;
            letter-spacing:.08em;
            text-transform:uppercase;
        }

        .inc-hero{
            position:relative;
            overflow:hidden;
            border:1px solid var(--border);
            border-radius:30px;
            padding:3.3rem 3.5rem;
            min-height:330px;
            background:
              linear-gradient(140deg,rgba(22,24,30,.98),rgba(12,13,16,.98));
            box-shadow:0 24px 80px rgba(0,0,0,.28);
        }

        .inc-hero:before{
            content:"";
            position:absolute;
            width:420px;height:420px;border-radius:50%;
            right:-120px;top:-160px;
            background:radial-gradient(circle,rgba(125,99,255,.38),transparent 62%);
        }

        .inc-hero:after{
            content:"MÉTODO";
            position:absolute;
            right:-2rem;
            bottom:-4.8rem;
            font-size:9rem;
            font-weight:950;
            letter-spacing:-.09em;
            color:rgba(255,255,255,.035);
            transform:rotate(-5deg);
        }

        .inc-eyebrow{
            display:flex;align-items:center;gap:.6rem;
            color:var(--lime);
            font-size:.72rem;
            font-weight:900;
            letter-spacing:.18em;
            text-transform:uppercase;
            margin-bottom:1rem;
        }

        .inc-eyebrow:before{
            content:"";
            width:30px;height:3px;border-radius:999px;
            background:var(--lime);
        }

        .inc-hero h1{
            position:relative;
            z-index:2;
            max-width:820px;
            font-size:clamp(3.2rem,5.8vw,6rem);
            line-height:.92;
            margin:0;
            letter-spacing:-.075em;
        }

        .inc-hero .accent{color:var(--lime)}

        .inc-hero-copy{
            position:relative;
            z-index:2;
            max-width:690px;
            font-size:1.12rem;
            line-height:1.65;
            margin-top:1.55rem;
            color:rgba(246,242,232,.67);
        }

        .inc-pill{
            position:relative;
            z-index:2;
            display:inline-flex;
            margin-top:1.35rem;
            border:1px solid rgba(200,255,61,.35);
            border-radius:999px;
            padding:.62rem .9rem;
            color:var(--lime);
            background:rgba(200,255,61,.06);
            font-size:.75rem;
            font-weight:850;
        }

        .inc-metric-grid{
            display:grid;
            grid-template-columns:repeat(3,1fr);
            gap:1rem;
            margin:1rem 0 1.8rem;
        }

        .inc-metric-card{
            position:relative;
            overflow:hidden;
            min-height:165px;
            border:1px solid var(--border);
            border-radius:24px;
            padding:1.35rem 1.45rem;
            background:rgba(20,22,27,.96);
        }

        .inc-metric-card.lime{border-top:4px solid var(--lime)}
        .inc-metric-card.purple{border-top:4px solid var(--purple)}
        .inc-metric-card.coral{border-top:4px solid var(--coral)}

        .inc-metric-kicker{
            color:var(--muted);
            font-size:.68rem;
            letter-spacing:.14em;
            font-weight:850;
            text-transform:uppercase;
        }

        .inc-metric-value{
            font-size:3.3rem;
            line-height:1;
            margin:.7rem 0 .45rem;
            font-weight:950;
            letter-spacing:-.07em;
        }

        .inc-metric-label{
            color:rgba(246,242,232,.58);
            font-size:.9rem;
        }

        .inc-section-head{
            display:flex;
            justify-content:space-between;
            align-items:center;
            gap:1rem;
            margin:2.4rem 0 1rem;
        }

        .inc-section-title{
            font-size:1.7rem;
            font-weight:950;
            letter-spacing:-.05em;
        }

        .inc-workspace{
            border:1px solid var(--border);
            border-radius:28px;
            padding:1.7rem 1.8rem;
            margin-bottom:1.2rem;
            background:
              linear-gradient(130deg,rgba(28,30,37,.98),rgba(15,16,20,.98));
        }

        .inc-workspace-company{
            font-size:2.2rem;
            font-weight:950;
            letter-spacing:-.06em;
        }

        .inc-workspace-meta{
            color:rgba(246,242,232,.50);
            font-size:.82rem;
            margin-top:.25rem;
        }

        .inc-progress-track{
            height:10px;
            border-radius:999px;
            overflow:hidden;
            background:rgba(255,255,255,.07);
            margin:.95rem 0 .6rem;
        }

        .inc-progress-fill{
            height:100%;
            border-radius:999px;
            background:linear-gradient(90deg,var(--lime),var(--purple));
        }

        .inc-steps{
            display:grid;
            grid-template-columns:repeat(5,1fr);
            gap:.65rem;
            margin-top:1rem;
        }

        .inc-step{
            border:1px solid var(--border);
            border-radius:16px;
            padding:.78rem .85rem;
            background:rgba(255,255,255,.025);
        }

        .inc-step-name{
            color:rgba(246,242,232,.42);
            font-size:.62rem;
            font-weight:850;
            letter-spacing:.10em;
            text-transform:uppercase;
        }

        .inc-step-value{
            margin-top:.22rem;
            font-size:1rem;
            font-weight:950;
        }

        .inc-question-shell{
            border:1px solid var(--border);
            border-radius:28px;
            padding:2rem;
            background:linear-gradient(150deg,rgba(22,24,30,.98),rgba(13,14,17,.98));
            box-shadow:0 24px 70px rgba(0,0,0,.20);
        }

        .inc-question-number{
            color:var(--lime);
            font-size:.72rem;
            font-weight:900;
            letter-spacing:.15em;
            text-transform:uppercase;
        }

        .inc-conversation-title{
            color:rgba(246,242,232,.48);
            font-size:.9rem;
            margin-top:1.05rem;
        }

        .inc-question{
            font-size:clamp(2.15rem,4vw,3.9rem);
            line-height:1.04;
            font-weight:950;
            letter-spacing:-.065em;
            margin:.45rem 0 1.8rem;
        }

        .inc-diagnosis-grid{
            display:grid;
            grid-template-columns:1.05fr 1fr 1fr;
            gap:1rem;
            margin:1rem 0 1.5rem;
        }

        .inc-diagnosis-card{
            border:1px solid var(--border);
            border-radius:24px;
            padding:1.45rem;
            background:rgba(20,22,27,.96);
        }

        .inc-diagnosis-card.primary{
            background:linear-gradient(145deg,rgba(200,255,61,.16),rgba(20,22,27,.98));
        }

        .inc-score{
            font-size:5.5rem;
            line-height:.9;
            font-weight:950;
            color:var(--lime);
            letter-spacing:-.09em;
            margin:.7rem 0;
        }

        .inc-area-row{
            display:grid;
            grid-template-columns:145px 1fr 58px;
            align-items:center;
            gap:.85rem;
            margin:.95rem 0;
        }

        .inc-area-track{
            height:12px;
            border-radius:999px;
            background:rgba(255,255,255,.07);
            overflow:hidden;
        }

        .inc-area-fill{
            height:100%;
            border-radius:999px;
            background:linear-gradient(90deg,var(--lime),var(--purple));
        }

        div[role="radiogroup"]{
            display:grid !important;
            grid-template-columns:repeat(4,1fr);
            gap:.65rem;
        }

        div[role="radiogroup"] label{
            border:1px solid var(--border);
            background:var(--panel2);
            border-radius:16px;
            padding:.8rem .95rem;
            min-height:58px;
        }

        div[role="radiogroup"] label:hover{
            border-color:rgba(200,255,61,.45);
            transform:translateY(-1px);
        }

        div[data-testid="stMetric"],
        div[data-testid="stVerticalBlockBorderWrapper"]{
            background:rgba(20,22,27,.92);
            border:1px solid var(--border);
            border-radius:22px;
        }

        .stButton>button,.stFormSubmitButton>button{
            min-height:48px;
            border-radius:14px;
            font-weight:850;
        }

        .stButton>button[kind="primary"],
        .stFormSubmitButton>button[kind="primary"]{
            background:var(--lime);
            color:#0a0b0d;
            border-color:var(--lime);
        }

        input,textarea,[data-baseweb="select"]>div{
            background:#17191f !important;
            color:var(--paper) !important;
            border-color:rgba(255,255,255,.12) !important;
            border-radius:14px !important;
        }

        .stProgress>div>div>div>div{
            background:linear-gradient(90deg,var(--lime),var(--purple));
        }

        @media(max-width:950px){
            .inc-metric-grid,.inc-diagnosis-grid{grid-template-columns:1fr}
            .inc-steps{grid-template-columns:1fr 1fr}
            div[role="radiogroup"]{grid-template-columns:1fr 1fr}
            .inc-hero{padding:2rem}
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_wordmark() -> None:
    st.markdown(
        """
        <div class="inc-topbar">
          <div class="inc-logo">
            <div class="inc-logo-mark">I</div>
            <div>
              <div class="inc-logo-title">INCUBATOUR</div>
              <div class="inc-logo-sub">MÉTODO EMPRESA</div>
            </div>
          </div>
          <div class="inc-status">Copiloto de consultoría</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer() -> None:
    st.markdown(
        '<div style="margin-top:4rem;padding-top:1rem;border-top:1px solid rgba(255,255,255,.08);'
        'font-size:.68rem;letter-spacing:.10em;text-transform:uppercase;color:rgba(246,242,232,.30)">'
        'Incubatour · Le ponemos método a tu locura.</div>',
        unsafe_allow_html=True,
    )
