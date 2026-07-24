from __future__ import annotations

from datetime import date
from typing import Any
import streamlit as st

WIZARD_STATE_KEY = "new_audit_wizard_step"


def open_session_wizard() -> None:
    st.session_state[WIZARD_STATE_KEY] = "welcome"


def close_session_wizard() -> None:
    st.session_state[WIZARD_STATE_KEY] = None
    for key in ("wizard_company_name", "wizard_sector", "wizard_auditor_name", "wizard_audit_date"):
        st.session_state.pop(key, None)


def get_session_wizard_step() -> str | None:
    return st.session_state.get(WIZARD_STATE_KEY)


def render_welcome_step() -> None:
    st.caption("NUEVA SESIÓN ESTRATÉGICA")
    st.header("Convierte una conversación en un plan de acción")
    st.caption("En 35–45 minutos obtendrás una lectura ejecutiva, riesgos y prioridades para los próximos 90 días.")
    st.write("")
    cols = st.columns(4)
    items = [
        ("01", "Madurez", "Una lectura clara del nivel actual."),
        ("02", "Hallazgos", "Patrones, fortalezas y obstáculos."),
        ("03", "Riesgos", "Factores que limitan el desempeño."),
        ("04", "Plan", "Acciones ordenadas por prioridad."),
    ]
    for col, (number, title, text) in zip(cols, items):
        col.caption(number)
        col.markdown(f"**{title}**")
        col.caption(text)
    st.divider()
    c1, c2, _ = st.columns([1.2, 1, 3])
    if c1.button("Comenzar", type="primary", use_container_width=True):
        st.session_state[WIZARD_STATE_KEY] = "profile"
        st.rerun()
    if c2.button("Cancelar", use_container_width=True):
        close_session_wizard()
        st.rerun()


def render_profile_step() -> dict[str, Any] | None:
    st.caption("PASO 2 DE 2")
    st.header("Datos de la sesión")
    st.caption("Esta información identificará el expediente en todo el proceso.")
    with st.form("new_audit_form"):
        company_name = st.text_input("Empresa", key="wizard_company_name")
        sector = st.text_input("Sector", key="wizard_sector")
        auditor_name = st.text_input("Consultor", key="wizard_auditor_name")
        audit_date = st.date_input("Fecha", value=date.today(), key="wizard_audit_date")
        c1, c2, _ = st.columns([1.4, 1, 2])
        submitted = c1.form_submit_button("Crear sesión", type="primary", use_container_width=True)
        cancelled = c2.form_submit_button("Cancelar", use_container_width=True)
    if cancelled:
        close_session_wizard()
        st.rerun()
    if submitted:
        if not company_name.strip() or not auditor_name.strip():
            st.error("Empresa y consultor son obligatorios.")
            return None
        return {
            "company_name": company_name.strip(),
            "sector": sector.strip(),
            "auditor_name": auditor_name.strip(),
            "audit_date": audit_date.isoformat(),
        }
    return None


def render_session_wizard() -> dict[str, Any] | None:
    step = get_session_wizard_step()
    if step == "welcome":
        render_welcome_step()
    elif step == "profile":
        return render_profile_step()
    return None
