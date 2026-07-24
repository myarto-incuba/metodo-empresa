from __future__ import annotations

import streamlit as st
from components.page_header import render_page_header
from core.audit_facade import delete_company_audits, list_audits

render_page_header(
    title="Empresas",
    eyebrow="Gestión de clientes",
    description="Organizaciones registradas y actividad asociada.",
)

audits = list_audits() or []
companies: dict[str, dict[str, object]] = {}
for audit in audits:
    name = str(getattr(audit, "company_name", "Empresa") or "Empresa").strip()
    row = companies.setdefault(
        name,
        {"sector": getattr(audit, "sector", "") or "Sin sector", "audits": 0, "latest": ""},
    )
    row["audits"] = int(row["audits"]) + 1
    row["latest"] = max(str(row["latest"]), str(getattr(audit, "audit_date", "") or ""))

summary, _ = st.columns([1, 3])
summary.metric("Empresas activas", len(companies))
st.divider()

if not companies:
    st.info("Una empresa aparecerá aquí cuando se cree su primera auditoría.")
else:
    header = st.columns([3, 1, 1.5, 1])
    for col, label in zip(header, ["Empresa", "Auditorías", "Última actividad", ""]):
        col.caption(label.upper())
    st.divider()

    for name, row in sorted(companies.items()):
        info, count, latest, actions = st.columns([3, 1, 1.5, 1], vertical_alignment="center")
        info.markdown(f"**{name}**")
        info.caption(str(row["sector"]))
        count.write(row["audits"])
        latest.caption(str(row["latest"] or "Sin fecha"))
        if actions.button("Eliminar", key=f"delete-request-{name}", use_container_width=True):
            st.session_state.company_pending_deletion = name
        st.divider()

        if st.session_state.get("company_pending_deletion") == name:
            st.warning(f"Se eliminarán {row['audits']} auditoría(s) de {name}.")
            confirmation = st.text_input(
                f'Escribe "{name}" para confirmar', key=f"confirm-text-{name}"
            )
            c1, c2, _ = st.columns([1.5, 1, 2])
            if c1.button(
                "Eliminar definitivamente",
                type="primary",
                disabled=confirmation.strip() != name,
                key=f"confirm-{name}",
                use_container_width=True,
            ):
                try:
                    delete_company_audits(name)
                    st.session_state.company_pending_deletion = None
                    st.rerun()
                except Exception as exc:
                    st.error(str(exc))
            if c2.button("Cancelar", key=f"cancel-{name}", use_container_width=True):
                st.session_state.company_pending_deletion = None
                st.rerun()
