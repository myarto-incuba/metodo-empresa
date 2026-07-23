from __future__ import annotations

import streamlit as st

from components.audit_ui import audit_progress
from components.brand import render_footer, render_wordmark, safe
from core.audit_facade import list_audits


render_wordmark()

st.markdown(
    """
    <section class="inc-hero">
        <div class="inc-eyebrow">Copiloto de consultoría</div>
        <h1>Le ponemos <span>método</span><br>a tu empresa.</h1>
        <div class="inc-hero-copy">
            Una metodología digital para conducir conversaciones estratégicas,
            detectar patrones y convertirlos en decisiones, prioridades y acción.
        </div>
        <div class="inc-tagline">Le ponemos método a tu locura.</div>
    </section>
    """,
    unsafe_allow_html=True,
)

audits = list_audits()
in_progress = sum(1 for audit in audits if getattr(audit, "status", "") != "Completada")
completed = sum(1 for audit in audits if getattr(audit, "status", "") == "Completada")

cols = st.columns(3)
cards = [
    ("PORTAFOLIO", len(audits), "Auditorías registradas"),
    ("EN MOVIMIENTO", in_progress, "Procesos activos"),
    ("RESULTADOS", completed, "Auditorías completadas"),
]
for col, (kicker, value, label) in zip(cols, cards):
    with col:
        st.markdown(
            f"""
            <div class="inc-card inc-card-accent">
                <div class="inc-card-kicker">{kicker}</div>
                <div class="inc-card-value">{value}</div>
                <div class="inc-card-label">{label}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

head, action = st.columns([4, 1])
with head:
    st.markdown('<div class="inc-section-title">Expedientes activos</div>', unsafe_allow_html=True)
with action:
    st.write("")
    st.write("")
    if st.button("＋ Nueva auditoría", type="primary", use_container_width=True):
        st.switch_page("views/audits.py")

if not audits:
    st.info("Todavía no hay auditorías. Crea la primera para comenzar.")
else:
    for audit in reversed(audits):
        audit_id = getattr(audit, "audit_id", "")
        progress = audit_progress(audit_id)
        company = safe(getattr(audit, "company_name", "Empresa"))
        sector = safe(getattr(audit, "sector", "") or "Sector no indicado")
        status = safe(getattr(audit, "status", "") or "En proceso")

        with st.container(border=True):
            left, middle, right = st.columns([3.2, 2, 1.1])
            with left:
                st.markdown(f'<div class="inc-badge">{status.upper()}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="inc-company" style="margin-top:.75rem">{company}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="inc-meta">{sector}</div>', unsafe_allow_html=True)
            with middle:
                st.write("")
                st.markdown(f"**Avance integral · {round(progress['overall'] * 100)}%**")
                st.progress(progress["overall"])
            with right:
                st.write("")
                if st.button("Abrir expediente →", key=f"open-{audit_id}", use_container_width=True):
                    st.session_state.active_audit_id = audit_id
                    st.switch_page("views/interview.py")

render_footer()
