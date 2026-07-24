from __future__ import annotations

import streamlit as st
from components.audit_ui import audit_progress
from components.page_header import render_page_header
from components.session_wizard import (
    close_session_wizard,
    get_session_wizard_step,
    open_session_wizard,
    render_session_wizard,
)
from core.audit_facade import create_audit_compatible, list_audits


def overall(audit_id: str) -> float:
    try:
        values = audit_progress(audit_id)
        return sum(values.values()) / len(values) if values else 0.0
    except Exception:
        return 0.0


render_page_header(
    title="Auditorías",
    eyebrow="Método Empresa",
    description="Inicia una nueva sesión estratégica o continúa un expediente existente.",
)

if get_session_wizard_step() is None:
    intro, action = st.columns([4, 1.2], vertical_alignment="center")
    intro.subheader("Sesiones estratégicas")
    intro.caption("Cada expediente reúne conversación, evidencias, diagnóstico y plan de acción.")
    if action.button("＋ Nueva sesión", type="primary", use_container_width=True):
        open_session_wizard()
        st.rerun()
else:
    result = render_session_wizard()
    if result:
        try:
            audit = create_audit_compatible(
                result["company_name"], result["sector"], result["auditor_name"], result["audit_date"]
            )
            st.session_state.active_audit_id = getattr(audit, "audit_id")
            st.session_state.active_company = result["company_name"]
            close_session_wizard()
            st.switch_page("views/interview.py")
        except Exception as exc:
            st.error(f"No fue posible crear la sesión: {exc}")

st.divider()
audits = list_audits() or []
if not audits:
    st.info("Todavía no hay sesiones registradas.")
else:
    header = st.columns([3, 1.5, 2, 1])
    for col, label in zip(header, ["Empresa", "Avance", "Fecha / sector", ""]):
        col.caption(label.upper())
    st.divider()

    for audit in audits:
        audit_id = str(getattr(audit, "audit_id", ""))
        value = overall(audit_id)
        company = getattr(audit, "company_name", "Empresa")
        info, progress_col, meta, action = st.columns([3, 1.5, 2, 1], vertical_alignment="center")
        info.markdown(f"**{company}**")
        info.caption(getattr(audit, "auditor_name", "") or "Sin consultor")
        progress_col.progress(value)
        progress_col.caption(f"{value:.0%}")
        meta.caption(
            f"{getattr(audit, 'audit_date', 'Sin fecha')} · {getattr(audit, 'sector', '') or 'Sin sector'}"
        )
        if action.button("Abrir", key=f"continue-{audit_id}", use_container_width=True):
            st.session_state.active_audit_id = audit_id
            st.session_state.active_company = company
            st.switch_page("views/interview.py")
        st.divider()
