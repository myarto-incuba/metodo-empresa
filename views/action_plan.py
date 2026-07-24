from __future__ import annotations

import streamlit as st
from components.audit_ui import render_audit_header
from components.brand import render_footer
from components.page_header import render_page_header
from core.audit_facade import get_audit
from core.interview_repository import load_interview
from core.narrative_engine import build_strategic_reading
from core.ux_repository import load_action_plan, save_action_plan


audit_id = st.session_state.get("active_audit_id")
audit = get_audit(audit_id) if audit_id else None
if audit is None:
    st.warning("Selecciona una auditoría desde Auditorías.")
    st.stop()

reading = build_strategic_reading(
    load_interview(audit_id), company_name=getattr(audit, "company_name", "La empresa")
)
plan = load_action_plan(audit_id) or reading["roadmap"]
render_page_header(
    title="Plan de acción",
    eyebrow="Actúa",
    description="Prioridades, responsables y estado de las acciones de los próximos 90 días.",
)
render_audit_header(audit)

if not plan:
    st.info("Todavía no hay patrones suficientes para construir un roadmap.")
    st.stop()

completed = sum(row.get("status") == "Completada" for row in plan)
progress = completed / len(plan)
summary, done, overall = st.columns([3, 1, 1])
summary.subheader("Roadmap de 90 días")
summary.caption("Actualiza responsables, prioridad y estado de cada acción.")
done.metric("Completadas", f"{completed}/{len(plan)}")
overall.metric("Avance", f"{progress:.0%}")
st.progress(progress)
st.divider()

edited = []
for period in ("0–30 días", "31–60 días", "61–90 días"):
    st.subheader(period)
    period_rows = [row for row in plan if row.get("period", row.get("deadline")) == period]
    if not period_rows:
        st.caption("Sin acciones asignadas.")
    for index, row in enumerate(period_rows):
        source, priority_label = st.columns([4, 1])
        source.caption(row.get("source_pattern", "Lectura estratégica").upper())
        priority_label.caption(f"PRIORIDAD {row.get('priority', 'Media').upper()}")
        action = st.text_input(
            "Acción", value=row.get("action", ""), key=f"action-{period}-{index}"
        )
        owner_col, priority_col, status_col = st.columns([2, 1, 1])
        owner = owner_col.text_input(
            "Responsable",
            value=row.get("owner", ""),
            placeholder="Por definir",
            key=f"owner-{period}-{index}",
        )
        priorities = ["Alta", "Media", "Baja"]
        current_priority = row.get("priority", "Media")
        priority = priority_col.selectbox(
            "Prioridad",
            priorities,
            index=priorities.index(current_priority) if current_priority in priorities else 1,
            key=f"priority-{period}-{index}",
        )
        statuses = ["Pendiente", "En proceso", "Completada"]
        current_status = row.get("status", "Pendiente")
        status = status_col.selectbox(
            "Estado",
            statuses,
            index=statuses.index(current_status) if current_status in statuses else 0,
            key=f"status-{period}-{index}",
        )
        if row.get("reason"):
            st.caption(row["reason"])
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
        st.divider()

save_col, _ = st.columns([1.5, 3])
if save_col.button("Guardar plan", type="primary", use_container_width=True):
    save_action_plan(audit_id, edited)
    st.success("Plan guardado.")
    st.rerun()

render_footer()
