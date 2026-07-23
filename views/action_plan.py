from __future__ import annotations

import streamlit as st

from components.audit_ui import render_audit_header
from components.brand import render_footer, render_wordmark
from core.audit_facade import get_audit
from core.interview_repository import load_interview
from core.scoring_engine import calculate_results
from core.ux_repository import load_action_plan, save_action_plan


audit_id = st.session_state.get("active_audit_id")
audit = get_audit(audit_id) if audit_id else None
if audit is None:
    st.warning("Selecciona una auditoría desde Auditorías.")
    st.stop()

render_wordmark()
render_audit_header(audit)

st.markdown('<div class="inc-eyebrow">Plan de acción</div>', unsafe_allow_html=True)
st.title("Roadmap de 90 días")
st.caption("Convierte el diagnóstico en responsables, plazos, prioridades y seguimiento.")

interview = load_interview(audit_id)
results = calculate_results(interview)
plan = load_action_plan(audit_id)

if not plan:
    recommendations = results.get("recommendations", [])
    plan = [
        {
            "action": recommendation,
            "priority": "Alta" if index < 2 else "Media",
            "owner": "",
            "deadline": "30 días" if index < 2 else "60 días" if index < 4 else "90 días",
            "status": "Pendiente",
        }
        for index, recommendation in enumerate(recommendations)
    ]

if not plan:
    st.info("Primero responde la entrevista para generar prioridades.")
    st.stop()

completed = sum(1 for row in plan if row.get("status") == "Completada")
in_progress = sum(1 for row in plan if row.get("status") == "En proceso")
high_priority = sum(1 for row in plan if row.get("priority") == "Alta")

m1, m2, m3 = st.columns(3)
m1.metric("Acciones", len(plan))
m2.metric("Alta prioridad", high_priority)
m3.metric("Avance", f"{round(completed / len(plan) * 100) if plan else 0}%")

st.markdown('<div class="inc-section-title">Secuencia de implementación</div>', unsafe_allow_html=True)

edited = []
periods = [
    ("0–30 días", lambda row: "30" in str(row.get("deadline", ""))),
    ("31–60 días", lambda row: "60" in str(row.get("deadline", ""))),
    ("61–90 días", lambda row: "90" in str(row.get("deadline", ""))),
]
used_indexes = set()

for period_name, predicate in periods:
    st.markdown(f"### {period_name}")
    period_found = False
    for index, row in enumerate(plan):
        if index in used_indexes or not predicate(row):
            continue
        period_found = True
        used_indexes.add(index)
        with st.container(border=True):
            top_1, top_2 = st.columns([3, 1])
            action = top_1.text_input(
                "Acción",
                value=row.get("action", ""),
                key=f"plan-action-{audit_id}-{index}",
            )
            statuses = ["Pendiente", "En proceso", "Completada"]
            status = top_2.selectbox(
                "Estado",
                statuses,
                index=statuses.index(row.get("status", "Pendiente")),
                key=f"plan-status-{audit_id}-{index}",
            )
            col_1, col_2, col_3 = st.columns(3)
            priorities = ["Alta", "Media", "Baja"]
            priority = col_1.selectbox(
                "Prioridad",
                priorities,
                index=priorities.index(row.get("priority", "Media")),
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
                value=row.get("deadline", period_name),
                key=f"plan-deadline-{audit_id}-{index}",
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
    if not period_found:
        st.caption("Sin acciones asignadas a este periodo.")

# Keep unmatched actions visible
for index, row in enumerate(plan):
    if index in used_indexes:
        continue
    st.markdown("### Sin periodo definido")
    with st.container(border=True):
        action = st.text_input(
            "Acción",
            value=row.get("action", ""),
            key=f"plan-action-{audit_id}-{index}",
        )
        col_1, col_2, col_3, col_4 = st.columns(4)
        priorities = ["Alta", "Media", "Baja"]
        priority = col_1.selectbox(
            "Prioridad",
            priorities,
            index=priorities.index(row.get("priority", "Media")),
            key=f"plan-priority-{audit_id}-{index}",
        )
        owner = col_2.text_input(
            "Responsable",
            value=row.get("owner", ""),
            key=f"plan-owner-{audit_id}-{index}",
        )
        deadline = col_3.text_input(
            "Plazo",
            value=row.get("deadline", ""),
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

save_col, add_col = st.columns([3, 1])
if save_col.button("Guardar roadmap", type="primary", use_container_width=True):
    save_action_plan(audit_id, edited)
    st.success("Roadmap guardado.")
    st.rerun()

if add_col.button("＋ Agregar acción", use_container_width=True):
    edited.append(
        {
            "action": "Nueva acción",
            "priority": "Media",
            "owner": "",
            "deadline": "90 días",
            "status": "Pendiente",
        }
    )
    save_action_plan(audit_id, edited)
    st.rerun()

render_footer()
