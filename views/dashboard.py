from __future__ import annotations

import streamlit as st

from components.audit_ui import audit_progress
from components.brand import render_footer, render_wordmark
from core.audit_facade import list_audits


render_wordmark()

st.markdown(
    """
    <section class="inc-hero">
        <div class="inc-eyebrow">Auditoría estratégica</div>
        <h1>Le ponemos <span>método</span><br>a tu empresa.</h1>
        <div class="inc-hero-copy">
            Diagnósticos integrales para convertir información dispersa
            en decisiones claras, prioridades y acciones concretas.
        </div>
        <div class="inc-tagline">Le ponemos método a tu locura.</div>
    </section>
    """,
    unsafe_allow_html=True,
)

audits = list_audits()
in_progress = sum(
    1 for audit in audits if getattr(audit, "status", "") != "Completada"
)
completed = sum(
    1 for audit in audits if getattr(audit, "status", "") == "Completada"
)

col_1, col_2, col_3 = st.columns(3)
cards = [
    (col_1, "PORTAFOLIO", len(audits), "Auditorías registradas"),
    (col_2, "EN MOVIMIENTO", in_progress, "Procesos activos"),
    (col_3, "RESULTADOS", completed, "Auditorías completadas"),
]

for column, kicker, value, label in cards:
    with column:
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

title_col, button_col = st.columns([4, 1])
with title_col:
    st.markdown(
        '<div class="inc-section-title">Auditorías activas</div>',
        unsafe_allow_html=True,
    )
with button_col:
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
        left, center, right = st.columns([3.2, 2, 1.2])
        with st.container():
            with left:
                st.markdown(
                    f"""
                    <div class="inc-audit-card">
                        <div class="inc-badge">EN PROCESO</div>
                        <div class="inc-company" style="margin-top:.8rem;">
                            {getattr(audit, 'company_name', 'Empresa')}
                        </div>
                        <div class="inc-meta">
                            {getattr(audit, 'sector', '') or 'Sector no indicado'}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with center:
                st.write("")
                st.markdown(f"**Avance integral · {round(progress['overall'] * 100)}%**")
                st.progress(progress["overall"])
            with right:
                st.write("")
                if st.button(
                    "Continuar →",
                    key=f"open-{audit_id}",
                    use_container_width=True,
                ):
                    st.session_state.active_audit_id = audit_id
                    st.switch_page("views/interview.py")

render_footer()
