from __future__ import annotations

import streamlit as st


def apply_incubatour_brand() -> None:
    st.markdown(
        """
        <style>
        :root{
            --bg:#08090c;
            --panel:#12141a;
            --panel-2:#171a21;
            --paper:#f7f3ec;
            --muted:#9ea1aa;
            --analiza:#8CBF3F;
            --aprende:#E7C54A;
            --adapta:#E6A34A;
            --actua:#C13A79;
            --actua-dark:#9E2F6E;
            --border:rgba(255,255,255,.10);
            --border-strong:rgba(255,255,255,.16);
        }

        html, body, [data-testid="stAppViewContainer"], .stApp{
            background:
              linear-gradient(rgba(255,255,255,.018) 1px, transparent 1px),
              linear-gradient(90deg, rgba(255,255,255,.018) 1px, transparent 1px),
              radial-gradient(circle at 82% 4%, rgba(193,58,121,.22), transparent 27rem),
              radial-gradient(circle at 8% 88%, rgba(230,163,74,.10), transparent 24rem),
              var(--bg);
            background-size:32px 32px,32px 32px,auto,auto,auto;
            color:var(--paper);
        }

        [data-testid="stMainBlockContainer"], .block-container{
            max-width:1420px;
            padding-top:1.4rem;
            padding-bottom:5rem;
        }

        [data-testid="stSidebar"]{
            background:rgba(12,13,17,.985);
            border-right:1px solid var(--border);
        }
        [data-testid="stSidebarNav"]::before{
            content:"INCUBATOUR";
            display:block;
            color:var(--paper);
            font-size:.72rem;
            letter-spacing:.19em;
            font-weight:950;
            padding:.75rem 1rem .15rem;
        }
        [data-testid="stSidebarNav"]::after{
            content:"DECISION LAB · MÉTODO EMPRESA";
            display:block;
            color:var(--actua);
            font-size:.59rem;
            letter-spacing:.12em;
            font-weight:850;
            padding:0 1rem 1.05rem;
        }
        [data-testid="stSidebarNav"] a{
            border-radius:12px;
            margin:.15rem .55rem;
            min-height:42px;
            transition:all .16s ease;
        }
        [data-testid="stSidebarNav"] a:hover{
            background:rgba(255,255,255,.045);
        }
        [data-testid="stSidebarNav"] a[aria-current="page"]{
            background:linear-gradient(90deg,rgba(193,58,121,.19),rgba(230,163,74,.07));
            border:1px solid rgba(193,58,121,.28);
            box-shadow:inset 3px 0 0 var(--actua);
        }

        h1,h2,h3,h4{color:var(--paper);letter-spacing:-.045em}
        p,label,li,.stCaption{color:rgba(247,243,236,.72)}
        hr{border-color:var(--border)!important}

        .inc-topbar{
            display:flex;justify-content:space-between;align-items:center;
            margin-bottom:1.25rem;
        }
        .inc-logo{display:flex;align-items:center;gap:.9rem}
        .inc-logo-symbols{display:flex;align-items:flex-end;gap:2px;min-width:52px;height:48px}
        .inc-logo-symbols span{display:block;line-height:1;transform:rotate(45deg)}
        .inc-logo-symbols .a1{color:var(--analiza);font-size:13px;margin-bottom:2px}
        .inc-logo-symbols .a2{color:var(--aprende);font-size:17px;margin-bottom:8px}
        .inc-logo-symbols .a3{color:var(--adapta);font-size:21px;margin-bottom:15px}
        .inc-logo-symbols .a4{color:var(--actua);font-size:27px;margin-bottom:23px}
        .inc-logo-title{font-size:.82rem;letter-spacing:.16em;font-weight:950}
        .inc-logo-sub{color:var(--actua);font-size:.64rem;letter-spacing:.13em;font-weight:850;margin-top:.15rem}
        .inc-status{
            border:1px solid var(--border);border-radius:999px;padding:.45rem .72rem;
            color:rgba(247,243,236,.62);font-size:.67rem;font-weight:850;
            letter-spacing:.08em;text-transform:uppercase;background:rgba(255,255,255,.025)
        }

        .inc-hero{
            position:relative;overflow:hidden;border:1px solid var(--border-strong);
            border-radius:32px;padding:3.35rem 3.6rem 3rem;min-height:420px;
            background:
              linear-gradient(145deg,rgba(28,29,36,.99),rgba(11,12,15,.99)),
              var(--panel);
            box-shadow:0 34px 95px rgba(0,0,0,.38),inset 0 1px 0 rgba(255,255,255,.045);
        }
        .inc-hero:before{
            content:"";position:absolute;width:560px;height:560px;border-radius:50%;
            right:-160px;top:-225px;
            background:radial-gradient(circle,rgba(193,58,121,.50),rgba(230,163,74,.13) 39%,transparent 68%);
            filter:blur(2px);
        }
        .inc-hero:after{
            content:"DECISION LAB";position:absolute;right:-1.4rem;bottom:-3.8rem;
            font-size:8.5rem;font-weight:950;letter-spacing:-.09em;
            color:rgba(255,255,255,.035);transform:rotate(-4deg);white-space:nowrap;
        }
        .inc-hero-grid{position:relative;z-index:2;display:grid;grid-template-columns:minmax(0,1.55fr) minmax(280px,.75fr);gap:3rem;align-items:end}
        .inc-eyebrow{display:flex;align-items:center;gap:.65rem;color:var(--actua);font-size:.72rem;font-weight:900;letter-spacing:.18em;text-transform:uppercase;margin-bottom:1.05rem}
        .inc-eyebrow:before{content:"";width:32px;height:3px;border-radius:999px;background:linear-gradient(90deg,var(--adapta),var(--actua))}
        .inc-hero h1{max-width:850px;font-size:clamp(3.4rem,5.8vw,6.25rem);line-height:.91;margin:0;letter-spacing:-.078em}
        .inc-hero .accent{color:var(--actua);text-shadow:0 0 34px rgba(193,58,121,.22)}
        .inc-hero-copy{max-width:710px;font-size:1.08rem;line-height:1.65;margin-top:1.5rem;color:rgba(247,243,236,.67)}
        .inc-pill{display:inline-flex;margin-top:1.3rem;border:1px solid rgba(193,58,121,.43);border-radius:999px;padding:.65rem .95rem;color:#f3aacb;background:rgba(193,58,121,.09);font-size:.74rem;font-weight:850}

        .inc-poker{border-left:1px solid rgba(255,255,255,.11);padding-left:1.6rem;margin-bottom:.1rem}
        .inc-poker-title{font-size:.65rem;letter-spacing:.17em;text-transform:uppercase;color:rgba(247,243,236,.44);font-weight:900;margin-bottom:.9rem}
        .inc-poker-row{display:grid;grid-template-columns:24px 86px 1fr;gap:.55rem;align-items:center;padding:.62rem 0;border-bottom:1px solid rgba(255,255,255,.065)}
        .inc-poker-row:last-child{border-bottom:0}
        .inc-poker-symbol{font-size:.95rem;transform:rotate(45deg);display:inline-block}
        .inc-poker-name{font-size:.82rem;font-weight:900;color:var(--paper)}
        .inc-poker-copy{font-size:.68rem;color:rgba(247,243,236,.43);line-height:1.35}
        .inc-poker-row.analiza .inc-poker-symbol{color:var(--analiza)}
        .inc-poker-row.aprende .inc-poker-symbol{color:var(--aprende)}
        .inc-poker-row.adapta .inc-poker-symbol{color:var(--adapta)}
        .inc-poker-row.actua .inc-poker-symbol{color:var(--actua)}

        .inc-metric-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin:1.15rem 0 1.9rem}
        .inc-metric-card{
            position:relative;overflow:hidden;min-height:176px;border:1px solid var(--border);
            border-radius:25px;padding:1.45rem 1.55rem;background:linear-gradient(150deg,rgba(24,26,33,.96),rgba(17,19,24,.96));
            box-shadow:0 18px 45px rgba(0,0,0,.18);transition:transform .18s ease,border-color .18s ease,box-shadow .18s ease;
        }
        .inc-metric-card:after{content:"";position:absolute;right:-40px;bottom:-55px;width:145px;height:145px;border-radius:50%;opacity:.13}
        .inc-metric-card:hover{transform:translateY(-3px);border-color:rgba(255,255,255,.18);box-shadow:0 24px 58px rgba(0,0,0,.26)}
        .inc-metric-card.green{border-top:4px solid var(--analiza)}
        .inc-metric-card.green:after{background:var(--analiza)}
        .inc-metric-card.orange{border-top:4px solid var(--adapta)}
        .inc-metric-card.orange:after{background:var(--adapta)}
        .inc-metric-card.magenta{border-top:4px solid var(--actua)}
        .inc-metric-card.magenta:after{background:var(--actua)}
        .inc-metric-kicker{color:var(--muted);font-size:.67rem;letter-spacing:.15em;font-weight:900;text-transform:uppercase}
        .inc-metric-value{font-size:3.55rem;line-height:1;margin:.72rem 0 .48rem;font-weight:950;letter-spacing:-.075em}
        .inc-metric-label{color:rgba(247,243,236,.57);font-size:.9rem}
        .inc-section-title{font-size:1.75rem;font-weight:950;letter-spacing:-.05em}

        [data-testid="stVerticalBlockBorderWrapper"]{
            border:1px solid var(--border)!important;border-radius:24px!important;
            background:linear-gradient(145deg,rgba(24,26,32,.95),rgba(15,17,21,.96))!important;
            box-shadow:0 18px 45px rgba(0,0,0,.18);
            transition:transform .18s ease,border-color .18s ease;
        }
        [data-testid="stVerticalBlockBorderWrapper"]:hover{transform:translateY(-2px);border-color:rgba(193,58,121,.27)!important}

        .inc-workspace{border:1px solid var(--border);border-radius:28px;padding:1.7rem 1.8rem;margin-bottom:1.2rem;background:linear-gradient(130deg,rgba(28,30,37,.98),rgba(15,16,20,.98))}
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

        div[role="radiogroup"]{display:grid!important;grid-template-columns:repeat(4,1fr);gap:.65rem}
        div[role="radiogroup"] label{border:1px solid var(--border);background:var(--panel-2);border-radius:16px;padding:.8rem .95rem;min-height:58px;transition:all .15s ease}
        div[role="radiogroup"] label:hover{border-color:rgba(193,58,121,.45);transform:translateY(-1px)}
        div[data-testid="stMetric"]{background:rgba(20,22,27,.92);border:1px solid var(--border);border-radius:22px}
        .stButton>button,.stFormSubmitButton>button{min-height:48px;border-radius:14px;font-weight:850;border-color:var(--border-strong);transition:all .16s ease}
        .stButton>button:hover,.stFormSubmitButton>button:hover{transform:translateY(-1px);border-color:rgba(193,58,121,.42)}
        .stButton>button[kind="primary"],.stFormSubmitButton>button[kind="primary"]{background:var(--actua);color:#fff;border-color:var(--actua);box-shadow:0 10px 28px rgba(193,58,121,.22)}
        .stButton>button[kind="primary"]:hover,.stFormSubmitButton>button[kind="primary"]:hover{background:var(--actua-dark);border-color:var(--actua-dark);color:#fff}
        input,textarea,[data-baseweb="select"]>div{background:#17191f!important;color:var(--paper)!important;border-color:rgba(255,255,255,.12)!important;border-radius:14px!important}
        [data-testid="stProgressBar"]>div{background:rgba(255,255,255,.075)!important}
        [data-testid="stProgressBar"]>div>div{background:linear-gradient(90deg,var(--analiza),var(--aprende),var(--adapta),var(--actua))!important}
        /* Oculta por completo la barra superior nativa de Streamlit */
        header[data-testid="stHeader"]{
            display:none!important;
            height:0!important;
            min-height:0!important;
        }
        [data-testid="stToolbar"],
        [data-testid="stDecoration"],
        [data-testid="stStatusWidget"]{
            display:none!important;
        }
        [data-testid="stAppViewContainer"] > .main{
            padding-top:0!important;
        }
        [data-testid="stMainBlockContainer"],
        .block-container{
            padding-top:1.15rem!important;
        }
        #MainMenu,footer{visibility:hidden}

        @media(max-width:1050px){.inc-hero-grid{grid-template-columns:1fr}.inc-poker{border-left:0;border-top:1px solid rgba(255,255,255,.10);padding:1.4rem 0 0}.inc-hero{min-height:auto}.inc-metric-grid,.inc-diagnosis-grid{grid-template-columns:1fr 1fr}}
        @media(max-width:720px){.inc-hero{padding:2.1rem 1.7rem}.inc-hero h1{font-size:3.35rem}.inc-metric-grid{grid-template-columns:1fr}.inc-topbar{align-items:flex-start}.inc-status{display:none}div[role="radiogroup"]{grid-template-columns:1fr 1fr}}
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
        'Incubatour · Decision Lab · Le ponemos método a tu empresa.</div>',
        unsafe_allow_html=True,
    )
