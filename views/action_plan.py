from __future__ import annotations

import streamlit as st

from components.audit_ui import render_audit_header
from components.brand import render_footer, render_wordmark
from core.audit_facade import get_audit
from core.interview_repository import load_interview
from core.narrative_engine import build_strategic_reading
from core.ux_repository import load_action_plan, save_action_plan


audit_id = st.session_state.get("active_audit_id")
audit = get_audit(audit_id) if audit_id else None
if audit is None:
    st.warning("Selecciona una auditoría desde Auditorías.")
    st.stop()

render_wordmark()
render_audit_header(audit)

reading = build_strategic_reading(
    load_interview(audit_id),
    company_name=getattr(audit, "company_name", "La empresa"),
)
plan = load_action_plan(audit_id) or reading["roadmap"]

st.markdown('<div class="inc-eyebrow">Implementación</div>', unsafe_allow_html=True)
st.title("Roadmap inteligente de 90 días")
st.caption("Cada acción conserva la conexión con el patrón que la originó.")

if not plan:
    st.info("Todavía no hay patrones suficientes para construir un roadmap.")
    st.stop()

edited = []
for period in ("0–30 días", "31–60 días", "61–90 días"):
    st.markdown(f"## {period}")
    period_rows = [
        row for row in plan
        if row.get("period", row.get("deadline")) == period
    ]
    for index, row in enumerate(period_rows):
        source = row.get("source_pattern", "Lectura estratégica")
        with st.container(border=True):
            st.caption(source.upper())
            action = st.text_input(
                "Acción",
                value=row.get("action", ""),
                key=f"action-{period}-{index}",
            )
            c1, c2, c3 = st.columns(3)
            owner = c1.text_input(
                "Responsable",
                value=row.get("owner", ""),
                placeholder="Por definir",
                key=f"owner-{period}-{index}",
            )
            priority_options = ["Alta", "Media", "Baja"]
            priority_value = row.get("priority", "Media")
            priority = c2.selectbox(
                "Prioridad",
                priority_options,
                index=priority_options.index(priority_value)
                if priority_value in priority_options else 1,
                key=f"priority-{period}-{index}",
            )
            status_options = ["Pendiente", "En proceso", "Completada"]
            status_value = row.get("status", "Pendiente")
            status = c3.selectbox(
                "Estado",
                status_options,
                index=status_options.index(status_value)
                if status_value in status_options else 0,
                key=f"status-{period}-{index}",
            )
            st.caption(row.get("reason", ""))
            edited.append(
                {
                    **row,
                    "period": period,
                    "deadline": period,
                    "action": action,
                    "owner": owner,
                    "priority": priority,
                    "status": status,
                }
            )

if st.button("Guardar plan de acción", type="primary", use_container_width=True):
    save_action_plan(audit_id, edited)
    st.success("Plan guardado.")
    st.rerun()

render_footer()
