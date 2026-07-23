from __future__ import annotations

import streamlit as st

from components.audit_ui import audit_progress
from core.audit_facade import list_audits


st.markdown('<div class="me-kicker">Método Empresa</div>', unsafe_allow_html=True)
st.title("Dashboard")
st.caption("Administra auditorías y continúa exactamente donde te quedaste.")

audits = list_audits()

top_1, top_2, top_3 = st.columns(3)
top_1.metric("Auditorías", len(audits))
top_2.metric(
    "En proceso",
    sum(1 for audit in audits if getattr(audit, "status", "") != "Completada"),
)
top_3.metric(
    "Completadas",
    sum(1 for audit in audits if getattr(audit, "status", "") == "Completada"),
)

st.divider()
st.subheader("Auditorías activas")

if not audits:
    st.info("Todavía no hay auditorías. Ve a Auditorías para crear la primera.")
else:
    for audit in reversed(audits):
        audit_id = getattr(audit, "audit_id", "")
        progress = audit_progress(audit_id)
        with st.container(border=True):
            left, middle, right = st.columns([3, 2, 1])
            with left:
                st.markdown(f"### {getattr(audit, 'company_name', 'Empresa')}")
                st.caption(
                    f"{getattr(audit, 'sector', '') or 'Sector no indicado'} · "
                    f"{getattr(audit, 'status', '') or 'En proceso'}"
                )
            with middle:
                st.write(f"**Avance integral: {round(progress['overall'] * 100)}%**")
                st.progress(progress["overall"])
            with right:
                if st.button("Abrir", key=f"open-{audit_id}", use_container_width=True):
                    st.session_state.active_audit_id = audit_id
                    st.switch_page("views/interview.py")
