from __future__ import annotations

import streamlit as st
from components.audit_ui import render_audit_header
from components.page_header import render_page_header
from core.audit_facade import get_audit
from core.ux_repository import load_evidence, save_evidence


audit_id = st.session_state.get("active_audit_id")
audit = get_audit(audit_id) if audit_id else None
if audit is None:
    st.warning("Selecciona una auditoría desde Auditorías.")
    st.stop()

render_page_header(
    title="Evidencias",
    eyebrow="Aprende",
    description="Controla qué documentos están disponibles y qué información sigue pendiente.",
)
render_audit_header(audit)

rows = load_evidence(audit_id)
statuses = ["Pendiente", "Solicitada", "Disponible", "No aplica"]
complete = sum(row.get("status") in {"Disponible", "No aplica"} for row in rows)
progress = complete / len(rows) if rows else 0

summary, action = st.columns([4, 1.2], vertical_alignment="center")
summary.subheader("Repositorio de evidencia")
summary.caption(f"{complete} de {len(rows)} evidencias resueltas")
action.metric("Avance", f"{progress:.0%}")
st.progress(progress)
st.divider()

edited = []
for area in dict.fromkeys(row["area"] for row in rows):
    st.subheader(area)
    st.caption("DOCUMENTO / ESTADO / NOTAS")
    for index, row in enumerate(rows):
        if row["area"] != area:
            continue
        name_col, status_col = st.columns([2.5, 1], vertical_alignment="center")
        name_col.markdown(f"**{row['name']}**")
        current = row.get("status", "Pendiente")
        status = status_col.selectbox(
            "Estado",
            statuses,
            index=statuses.index(current) if current in statuses else 0,
            key=f"evidence-status-{audit_id}-{index}",
            label_visibility="collapsed",
        )
        notes = st.text_input(
            "Notas",
            value=row.get("notes", ""),
            placeholder="Ubicación, responsable o validación pendiente.",
            key=f"evidence-notes-{audit_id}-{index}",
            label_visibility="collapsed",
        )
        edited.append({"area": row["area"], "name": row["name"], "status": status, "notes": notes})
        st.divider()

save_col, _ = st.columns([1.5, 3])
if save_col.button("Guardar evidencias", type="primary", use_container_width=True):
    save_evidence(audit_id, edited)
    st.success("Evidencias actualizadas.")
    st.rerun()
