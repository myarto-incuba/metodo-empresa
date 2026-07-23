from __future__ import annotations

from datetime import date

import streamlit as st

from components.audit_ui import audit_progress
from core.audit_facade import create_audit_compatible, list_audits


st.title("Auditorías")
st.caption("Crea una auditoría o abre una existente.")

with st.expander("＋ Nueva auditoría", expanded=not bool(list_audits())):
    with st.form("new-audit"):
        company_name = st.text_input("Empresa", placeholder="Synoni")
        sector = st.text_input(
            "Sector",
            placeholder="Capacitación y eventos para la industria de bodas",
        )
        auditor_name = st.text_input("Auditor", value="Mariana")
        audit_date = st.date_input("Fecha", value=date.today())
        submitted = st.form_submit_button(
            "Crear auditoría",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        if not company_name.strip():
            st.warning("Escribe el nombre de la empresa.")
        else:
            try:
                audit = create_audit_compatible(
                    company_name.strip(),
                    sector.strip(),
                    auditor_name.strip(),
                    audit_date.isoformat(),
                )
            except Exception as exc:
                st.error(f"No fue posible crear la auditoría: {exc}")
            else:
                st.session_state.active_audit_id = getattr(audit, "audit_id", None)
                st.success("Auditoría creada.")
                st.rerun()

st.subheader("Historial")

audits = list_audits()
if not audits:
    st.info("No hay auditorías registradas.")
else:
    for audit in reversed(audits):
        audit_id = getattr(audit, "audit_id", "")
        progress = audit_progress(audit_id)
        with st.container(border=True):
            col_1, col_2, col_3 = st.columns([3, 2, 1])
            with col_1:
                st.markdown(f"### {getattr(audit, 'company_name', 'Empresa')}")
                st.caption(
                    f"{getattr(audit, 'sector', '') or 'Sector no indicado'} · "
                    f"{getattr(audit, 'status', '') or 'En proceso'}"
                )
            with col_2:
                st.write(f"**{round(progress['overall'] * 100)}% completado**")
                st.progress(progress["overall"])
            with col_3:
                if st.button("Continuar", key=f"continue-{audit_id}", use_container_width=True):
                    st.session_state.active_audit_id = audit_id
                    st.switch_page("views/interview.py")
