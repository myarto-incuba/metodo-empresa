from __future__ import annotations

import streamlit as st

from components.audit_ui import render_audit_header
from core.audit_facade import get_audit
from core.ux_repository import load_evidence, save_evidence


audit_id = st.session_state.get("active_audit_id")
audit = get_audit(audit_id) if audit_id else None
if audit is None:
    st.warning("Selecciona una auditoría desde Auditorías.")
    st.stop()

render_audit_header(audit)
st.title("Evidencias")
st.caption("Registra qué documentos están disponibles y qué debe validarse presencialmente.")

rows = load_evidence(audit_id)
areas = list(dict.fromkeys(row["area"] for row in rows))
edited_rows = []

for area in areas:
    st.subheader(area)
    for index, row in enumerate(rows):
        if row["area"] != area:
            continue
        with st.container(border=True):
            col_1, col_2 = st.columns([2, 1])
            col_1.markdown(f"**{row['name']}**")
            status = col_2.selectbox(
                "Estado",
                ["Pendiente", "Solicitada", "Disponible", "No aplica"],
                index=["Pendiente", "Solicitada", "Disponible", "No aplica"].index(row["status"]),
                key=f"evidence-status-{audit_id}-{index}",
                label_visibility="collapsed",
            )
            notes = st.text_input(
                "Notas",
                value=row.get("notes", ""),
                placeholder="Dónde está, quién la enviará o qué falta validar.",
                key=f"evidence-notes-{audit_id}-{index}",
            )
            edited_rows.append(
                {
                    "area": row["area"],
                    "name": row["name"],
                    "status": status,
                    "notes": notes,
                }
            )

if st.button("Guardar evidencias", type="primary", use_container_width=True):
    save_evidence(audit_id, edited_rows)
    st.success("Evidencias actualizadas.")
    st.rerun()
