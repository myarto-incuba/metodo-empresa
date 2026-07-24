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
            --paper:#f7f3ec;
            --muted:#9b9da8;

            /* Poker de As · identidad Incubatour */
            --analiza:#8CBF3F;
            --aprende:#E7C54A;
            --adapta:#E6A34A;
            --actua:#C13A79;
            --actua-dark:#9E2F6E;

            --border:rgba(255,255,255,.10);
        }

        .stApp{
            background:
              linear-gradient(rgba(255,255,255,.018) 1px, transparent 1px),
              linear-gradient(90deg, rgba(255,255,255,.018) 1px, transparent 1px),
              radial-gradient(circle at 86% 0%, rgba(193,58,121,.20), transparent 27rem),
              radial-gradient(circle at 0% 100%, rgba(140,191,63,.09), transparent 28rem),
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
            content:"DECISION LAB · MÉTODO EMPRESA";
            display:block;
            color:var(--actua);
            font-size:.60rem;
            letter-spacing:.12em;
            font-weight:850;
            padding:0 1rem 1rem;
        }

        [data-testid="stSidebarNav"] a{
            border-radius:12px;
            margin:.15rem .55rem;
        }

        [data-testid="stSidebarNav"] a[aria-current="page"]{
            background:linear-gradient(90deg,rgba(193,58,121,.17),rgba(230,163,74,.08));
            border:1px solid rgba(193,58,121,.24);
        }

        h1,h2,h3,h4{
            color:var(--paper);
            letter-spacing:-.045em;
        }

        p,label,li,.stCaption{color:rgba(247,243,236,.72)}

        .inc-topbar{
            display:flex;
            justify-content:space-between;
            align-items:center;
            margin-bottom:1.25rem;
        }

        .inc-logo{display:flex;align-items:center;gap:.9rem}

        .inc-logo-symbols{
            display:flex;
            align-items:flex-end;
            gap:2px;
            min-width:52px;
            height:48px;
        }
        .inc-logo-symbols span{display:block;line-height:1;transform:rotate(45deg)}
        .inc-logo-symbols .a1{color:var(--analiza);font-size:13px;margin-bottom:2px}
        .inc-logo-symbols .a2{color:var(--aprende);font-size:17px;margin-bottom:8px}
        .inc-logo-symbols .a3{color:var(--adapta);font-size:21px;margin-bottom:15px}
        .inc-logo-symbols .a4{color:var(--actua);font-size:27px;margin-bottom:23px}

        .inc-logo-title{font-size:.82rem;letter-spacing:.16em;font-weight:950}
        .inc-logo-sub{color:var(--actua);font-size:.64rem;letter-spacing:.13em;font-weight:850;margin-top:.15rem}

        .inc-status{
            border:1px solid var(--border);
            border-radius:999px;
            padding:.45rem .7rem;
            color:rgba(247,243,236,.65);
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
            padding:3.15rem 3.5rem 2.8rem;
            min-height:350px;
            background:linear-gradient(140deg,rgba(23,24,30,.99),rgba(12,13,16,.98));
            box-shadow:0 24px 80px rgba(0,0,0,.28);
        }

        .inc-hero:before{
            content:"";
            position:absolute;
            width:470px;height:470px;border-radius:50%;
            right:-130px;top:-180px;
            background:radial-gradient(circle,rgba(193,58,121,.42),rgba(230,163,74,.10) 40%,transparent 66%);
        }

        .inc-hero:after{
            content:"DECISION LAB";
            position:absolute;
            right:-1.2rem;
            bottom:-3.4rem;
            font-size:7.4rem;
            font-weight:950;
            letter-spacing:-.09em;
            color:rgba(255,255,255,.032);
            transform:rotate(-4deg);
            white-space:nowrap;
        }

        .inc-eyebrow{
            display:flex;align-items:center;gap:.6rem;
            color:var(--actua);
            font-size:.72rem;
            font-weight:900;
            letter-spacing:.18em;
            text-transform:uppercase;
            margin-bottom:1rem;
        }
        .inc-eyebrow:before{content:"";width:30px;height:3px;border-radius:999px;background:var(--actua)}

        .inc-hero h1{
            position:relative;z-index:2;
            max-width:860px;
            font-size:clamp(3.2rem,5.8vw,6rem);
            line-height:.92;
            margin:0;
            letter-spacing:-.075em;
        }
        .inc-hero .accent{color:var(--actua)}

        .inc-hero-copy{
            position:relative;z-index:2;
            max-width:720px;
            font-size:1.12rem;
            line-height:1.65;
            margin-top:1.5rem;
            color:rgba(247,243,236,.68);
        }

        .inc-pill{
            position:relative;z-index:2;
            display:inline-flex;
            margin-top:1.25rem;
            border:1px solid rgba(193,58,121,.42);
            border-radius:999px;
            padding:.62rem .9rem;
            color:#f3aacb;
            background:rgba(193,58,121,.08);
            font-size:.75rem;
            font-weight:850;
        }

        .inc-method-grid{
            display:grid;
            grid-template-columns:repeat(4,1fr);
            gap:.8rem;
            margin:1rem 0 1.8rem;
        }
        .inc-method-card{
            position:relative;
            overflow:hidden;
            border:1px solid var(--border);
            border-radius:18px;
            padding:1rem 1.05rem;
            background:rgba(20,22,27,.92);
            min-height:105px;
        }
        .inc-method-card:after{
            content:"◆";
            position:absolute;
            right:.8rem;
            bottom:-.5rem;
            font-size:3.1rem;
            opacity:.12;
        }
        .inc-method-card.analiza{border-top:3px solid var(--analiza)}
        .inc-method-card.aprende{border-top:3px solid var(--aprende)}
        .inc-method-card.adapta{border-top:3px solid var(--adapta)}
        .inc-method-card.actua{border-top:3px solid var(--actua)}
        .inc-method-card.analiza:after{color:var(--analiza)}
        .inc-method-card.aprende:after{color:var(--aprende)}
        .inc-method-card.adapta:after{color:var(--adapta)}
        .inc-method-card.actua:after{color:var(--actua)}
        .inc-method-name{font-size:.92rem;font-weight:900;letter-spacing:.02em}
        .inc-method-copy{font-size:.72rem;line-height:1.4;color:rgba(247,243,236,.48);margin-top:.35rem;max-width:170px}

        .inc-metric-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin:1rem 0 1.8rem}
        .inc-metric-card{
            position:relative;overflow:hidden;min-height:165px;
            border:1px solid var(--border);border-radius:24px;
            padding:1.35rem 1.45rem;background:rgba(20,22,27,.96);
            transition:transform .18s ease,border-color .18s ease;
        }
        .inc-metric-card:hover{transform:translateY(-2px);border-color:rgba(193,58,121,.28)}
        .inc-metric-card.green{border-top:4px solid var(--analiza)}
        .inc-metric-card.orange{border-top:4px solid var(--adapta)}
        .inc-metric-card.magenta{border-top:4px solid var(--actua)}
        .inc-metric-kicker{color:var(--muted);font-size:.68rem;letter-spacing:.14em;font-weight:850;text-transform:uppercase}
        .inc-metric-value{font-size:3.3rem;line-height:1;margin:.7rem 0 .45rem;font-weight:950;letter-spacing:-.07em}
        .inc-metric-label{color:rgba(247,243,236,.58);font-size:.9rem}

        .inc-section-title{font-size:1.7rem;font-weight:950;letter-spacing:-.05em}

        .inc-workspace{
            border:1px solid var(--border);border-radius:28px;padding:1.7rem 1.8rem;margin-bottom:1.2rem;
            background:linear-gradient(130deg,rgba(28,30,37,.98),rgba(15,16,20,.98));
        }
        .inc-workspace-company{font-size:2.2rem;font-weight:950;letter-spacing:-.06em}
        .inc-workspace-meta{color:rgba(247,243,236,.50);font-size:.82rem;margin-top:.25rem}
        .inc-progress-track{height:10px;border-radius:999px;overflow:hidden;background:rgba(255,255,255,.07);margin:.95rem 0 .6rem}
        .inc-progress-fill{height:100%;border-radius:999px;background:linear-gradient(90deg,var(--analiza),var(--aprende),var(--adapta),var(--actua))}

        .inc-question-shell{border:1px solid var(--border);border-radius:28px;padding:2rem;background:linear-gradient(150deg,rgba(22,24,30,.98),rgba(13,14,17,.98));box-shadow:0 24px 70px rgba(0,0,0,.20)}
        .inc-question-number{color:var(--actua);font-size:.72rem;font-weight:900;letter-spacing:.15em;text-transform:uppercase}
        .inc-conversation-title{color:rgba(247,243,236,.48);font-size:.9rem;margin-top:1.05rem}
        .inc-question{font-size:clamp(2.15rem,4vw,3.9rem);line-height:1.04;font-weight:950;letter-spacing:-.065em;margin:.45rem 0 1.8rem}

        .inc-diagnosis-grid{display:grid;grid-template-columns:1.05fr 1fr 1fr;gap:1rem;margin:1rem 0 1.5rem}
        .inc-diagnosis-card{border:1px solid var(--border);border-radius:24px;padding:1.45rem;background:rgba(20,22,27,.96)}
        .inc-diagnosis-card.primary{background:linear-gradient(145deg,rgba(193,58,121,.17),rgba(20,22,27,.98))}
        .inc-score{font-size:5.5rem;line-height:.9;font-weight:950;color:var(--actua);letter-spacing:-.09em;margin:.7rem 0}
        .inc-area-row{display:grid;grid-template-columns:145px 1fr 58px;align-items:center;gap:.85rem;margin:.95rem 0}
        .inc-area-track{height:12px;border-radius:999px;background:rgba(255,255,255,.07);overflow:hidden}
        .inc-area-fill{height:100%;border-radius:999px;background:linear-gradient(90deg,var(--analiza),var(--adapta),var(--actua))}

        div[role="radiogroup"]{display:grid !important;grid-template-columns:repeat(4,1fr);gap:.65rem}
        div[role="radiogroup"] label{border:1px solid var(--border);background:var(--panel2);border-radius:16px;padding:.8rem .95rem;min-height:58px}
        div[role="radiogroup"] label:hover{border-color:rgba(193,58,121,.45);transform:translateY(-1px)}

        div[data-testid="stMetric"],div[data-testid="stVerticalBlockBorderWrapper"]{
            background:rgba(20,22,27,.92);border:1px solid var(--border);border-radius:22px;
        }

        .stButton>button,.stFormSubmitButton>button{min-height:48px;border-radius:14px;font-weight:850}
        .stButton>button[kind="primary"],.stFormSubmitButton>button[kind="primary"]{
            background:var(--actua);color:#fff;border-color:var(--actua);
            box-shadow:0 10px 28px rgba(193,58,121,.22);
        }
        .stButton>button[kind="primary"]:hover,.stFormSubmitButton>button[kind="primary"]:hover{
            background:var(--actua-dark);border-color:var(--actua-dark);color:#fff;
        }

        input,textarea,[data-baseweb="select"]>div{
            background:#17191f !important;color:var(--paper) !important;
            border-color:rgba(255,255,255,.12) !important;border-radius:14px !important;
        }
        .stProgress>div>div>div>div{background:linear-gradient(90deg,var(--analiza),var(--aprende),var(--adapta),var(--actua))}

        @media(max-width:950px){
            .inc-metric-grid,.inc-diagnosis-grid,.inc-method-grid{grid-template-columns:1fr 1fr}
            div[role="radiogroup"]{grid-template-columns:1fr 1fr}
            .inc-hero{padding:2rem}
        }
        @media(max-width:620px){.inc-method-grid,.inc-metric-grid{grid-template-columns:1fr}}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_wordmark() -> None:
    st.markdown(
        """
        <div class="inc-topbar">
          <div class="inc-logo">
            <div class="inc-logo-symbols" aria-hidden="true">
              <span class="a1">◆</span><span class="a2">◆</span><span class="a3">◆</span><span class="a4">◆</span>
            </div>
            <div>
              <div class="inc-logo-title">INCUBATOUR</div>
              <div class="inc-logo-sub">DECISION LAB · MÉTODO EMPRESA</div>
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
        'font-size:.68rem;letter-spacing:.10em;text-transform:uppercase;color:rgba(247,243,236,.30)">'
        'Incubatour · Decision Lab · Le ponemos método a tu locura.</div>',
        unsafe_allow_html=True,
    )
