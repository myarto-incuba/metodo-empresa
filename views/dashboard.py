from __future__ import annotations

import streamlit as st

from components.audit_ui import audit_progress
from components.brand import render_footer, render_wordmark
from core.audit_facade import list_audits


render_wordmark()

st.markdown(
    """
    <section class="inc-hero">
      <div class="inc-eyebrow">Centro de operaciones</div>
      <h1>Le ponemos <span class="accent">método</span><br>a tu empresa.</h1>
      <div class="inc-hero-copy">
        Una metodología digital para conducir conversaciones estratégicas,
        detectar patrones y convertirlos en decisiones, prioridades y acción.
      </div>
      <div class="inc-pill">Le ponemos método a tu locura.</div>
    </section>
    """,
    unsafe_allow_html=True,
)

audits = list_audits()
in_progress = sum(1 for audit in audits if getattr(audit, "status", "") != "Completada")
completed = sum(1 for audit in audits if getattr(audit, "status", "") == "Completada")

st.markdown(
    f"""
    <div class="inc-metric-grid">
      <div class="inc-metric-card lime">
        <div class="inc-metric-kicker">Portafolio</div>
        <div class="inc-metric-value">{len(audits)}</div>
        <div class="inc-metric-label">Auditorías registradas</div>
      </div>
      <div class="inc-metric-card purple">
        <div class="inc-metric-kicker">En movimiento</div>
        <div class="inc-metric-value">{in_progress}</div>
        <div class="inc-metric-label">Procesos activos</div>
      </div>
      <div class="inc-metric-card coral">
        <div class="inc-metric-kicker">Resultados</div>
        <div class="inc-metric-value">{completed}</div>
        <div class="inc-metric-label">Auditorías completadas</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

left, right = st.columns([4, 1])
with left:
    st.markdown('<div class="inc-section-title">Expedientes activos</div>', unsafe_allow_html=True)
with right:
    if st.button("＋ Nueva auditoría", type="primary", use_container_width=True):
        st.switch_page("views/audits.py")

if not audits:
    st.info("Todavía no hay auditorías. Crea la primera para comenzar.")
else:
    for audit in reversed(audits):
        audit_id = getattr(audit, "audit_id", "")
        progress = audit_progress(audit_id)
        with st.container(border=True):
            col1, col2, col3 = st.columns([3,2,1])
            col1.markdown(f"### {getattr(audit,'company_name','Empresa')}")
            col1.caption(getattr(audit,'sector','') or "Sector no indicado")
            col2.write(f"**Avance integral · {round(progress['overall']*100)}%**")
            col2.progress(progress["overall"])
            if col3.button("Abrir →", key=f"open-{audit_id}", use_container_width=True):
                st.session_state.active_audit_id = audit_id
                st.switch_page("views/interview.py")

render_footer()
