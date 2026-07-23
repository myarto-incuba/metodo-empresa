from __future__ import annotations

import streamlit as st

from components.audit_ui import render_audit_header
from core.audit_facade import get_audit
from core.interview_repository import load_interview
from core.scoring_engine import calculate_results
from core.ux_repository import load_action_plan, save_action_plan


audit_id = st.session_state.get("active_audit_id")
audit = get_audit(audit_id) if audit_id else None
if audit is None:
    st.warning("Selecciona una auditoría desde Auditorías.")
    st.stop()

render_audit_header(audit)
st.title("Plan de acción")
st.caption("Convierte el diagnóstico en responsables, plazos y prioridades.")

interview = load_interview(audit_id)
results = calculate_results(interview)
plan = load_action_plan(audit_id)

if not plan:
    plan = [
        {
            "action": recommendation,
            "priority": "Alta" if index < 2 else "Media",
            "owner": "",
            "deadline": "30 días" if index < 2 else "60 días",
            "status": "Pendiente",
        }
        for index, recommendation in enumerate(results["recommendations"])
    ]

if not plan:
    st.info("Primero responde la entrevista para generar prioridades.")
    st.stop()

edited = []
for index, row in enumerate(plan):
    with st.container(border=True):
        action = st.text_input(
            "Acción",
            value=row.get("action", ""),
            key=f"plan-action-{audit_id}-{index}",
        )
        col_1, col_2, col_3, col_4 = st.columns(4)
        priority = col_1.selectbox(
            "Prioridad",
            ["Alta", "Media", "Baja"],
            index=["Alta", "Media", "Baja"].index(row.get("priority", "Media")),
            key=f"plan-priority-{audit_id}-{index}",
        )
        owner = col_2.text_input(
            "Responsable",
            value=row.get("owner", ""),
            placeholder="Por definir",
            key=f"plan-owner-{audit_id}-{index}",
        )
        deadline = col_3.text_input(
            "Plazo",
            value=row.get("deadline", ""),
            placeholder="30 días",
            key=f"plan-deadline-{audit_id}-{index}",
        )
        statuses = ["Pendiente", "En proceso", "Completada"]
        status = col_4.selectbox(
            "Estado",
            statuses,
            index=statuses.index(row.get("status", "Pendiente")),
            key=f"plan-status-{audit_id}-{index}",
        )
        edited.append(
            {
                "action": action,
                "priority": priority,
                "owner": owner,
                "deadline": deadline,
                "status": status,
            }
        )

button_1, button_2 = st.columns([3, 1])
if button_1.button("Guardar plan de acción", type="primary", use_container_width=True):
    save_action_plan(audit_id, edited)
    st.success("Plan guardado.")
    st.rerun()

if button_2.button("＋ Agregar acción", use_container_width=True):
    edited.append(
        {
            "action": "Nueva acción",
            "priority": "Media",
            "owner": "",
            "deadline": "",
            "status": "Pendiente",
        }
    )
    save_action_plan(audit_id, edited)
    st.rerun()
