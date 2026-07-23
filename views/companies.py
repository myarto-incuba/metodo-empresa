from __future__ import annotations

import streamlit as st

from core.audit_facade import list_audits


st.title("Empresas")
st.caption("Vista consolidada de empresas auditadas.")

audits = list_audits()
companies = {}

for audit in audits:
    name = getattr(audit, "company_name", "Empresa")
    companies.setdefault(
        name,
        {
            "sector": getattr(audit, "sector", "") or "No indicado",
            "audits": 0,
            "latest": "",
        },
    )
    companies[name]["audits"] += 1
    companies[name]["latest"] = max(
        companies[name]["latest"],
        str(getattr(audit, "audit_date", "") or ""),
    )

if not companies:
    st.info("Las empresas aparecerán aquí al crear auditorías.")
else:
    for name, row in sorted(companies.items()):
        with st.container(border=True):
            col_1, col_2, col_3 = st.columns([3, 2, 1])
            col_1.markdown(f"### {name}")
            col_1.caption(row["sector"])
            col_2.metric("Auditorías", row["audits"])
            col_3.caption(f"Última: {row['latest'] or 'Sin fecha'}")
