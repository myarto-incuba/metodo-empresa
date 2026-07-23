from __future__ import annotations

from datetime import date

import streamlit as st

from core.audit_repository import create_audit, list_audits


st.set_page_config(
    page_title="Auditorías | Método Empresa",
    page_icon="🏢",
    layout="wide",
)

st.title("Método Empresa")
st.caption("MVP para crear y administrar auditorías empresariales.")

if "audit_created" not in st.session_state:
    st.session_state.audit_created = None


def _format_currency(value: float | None) -> str:
    if value is None:
        return "No indicada"
    return f"${value:,.2f}"


with st.sidebar:
    st.header("Nueva auditoría")

    with st.form("new_audit_form", clear_on_submit=True):
        company_name = st.text_input(
            "Nombre de la empresa *",
            placeholder="Ej. Empresa Piloto",
        )
        sector = st.text_input(
            "Sector",
            placeholder="Ej. Turismo, comercio, servicios",
        )

        employee_count_input = st.number_input(
            "Número de empleados",
            min_value=0,
            value=0,
            step=1,
        )

        annual_revenue_input = st.number_input(
            "Facturación anual",
            min_value=0.0,
            value=0.0,
            step=1000.0,
            help="Usa la moneda en la que se realizará la auditoría.",
        )

        audit_date = st.date_input(
            "Fecha de la auditoría",
            value=date.today(),
        )

        auditor_name = st.text_input(
            "Auditor responsable *",
            placeholder="Nombre completo",
        )

        submitted = st.form_submit_button(
            "Crear auditoría",
            type="primary",
            use_container_width=True,
        )

        if submitted:
            try:
                audit = create_audit(
                    company_name=company_name,
                    sector=sector,
                    employee_count=(
                        int(employee_count_input)
                        if employee_count_input > 0
                        else None
                    ),
                    annual_revenue=(
                        float(annual_revenue_input)
                        if annual_revenue_input > 0
                        else None
                    ),
                    audit_date=audit_date,
                    auditor_name=auditor_name,
                )
            except ValueError as exc:
                st.error(str(exc))
            else:
                st.session_state.audit_created = audit.audit_id
                st.success("Auditoría creada correctamente.")
                st.rerun()


audits = list_audits()

if st.session_state.audit_created:
    st.success(
        "Auditoría creada. Ya está lista para iniciar la entrevista."
    )
    st.session_state.audit_created = None

metric_1, metric_2, metric_3 = st.columns(3)
metric_1.metric("Auditorías", len(audits))
metric_2.metric(
    "Creadas",
    sum(audit.status == "Creada" for audit in audits),
)
metric_3.metric(
    "En proceso",
    sum(audit.status == "En proceso" for audit in audits),
)

st.divider()
st.subheader("Auditorías registradas")

if not audits:
    st.info(
        "Todavía no hay auditorías. Crea la primera desde el formulario lateral."
    )
else:
    for audit in audits:
        with st.container(border=True):
            title_column, status_column = st.columns([4, 1])

            with title_column:
                st.markdown(f"### {audit.company_name}")
                st.caption(
                    f"{audit.audit_id} · {audit.audit_date} · "
                    f"Auditor: {audit.auditor_name}"
                )

            with status_column:
                st.markdown(f"**{audit.status}**")

            detail_1, detail_2, detail_3 = st.columns(3)
            detail_1.write(f"**Sector:** {audit.sector or 'No indicado'}")
            detail_2.write(
                "**Empleados:** "
                f"{audit.employee_count if audit.employee_count is not None else 'No indicado'}"
            )
            detail_3.write(
                f"**Facturación:** {_format_currency(audit.annual_revenue)}"
            )

            if st.button(
                "Iniciar entrevista →",
                key=f"start-{audit.audit_id}",
                type="secondary",
            ):
                st.session_state.active_audit_id = audit.audit_id
                st.info(
                    "La auditoría quedó seleccionada. "
                    "La pantalla de entrevista se conectará en el siguiente paso."
                )
