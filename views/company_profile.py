from __future__ import annotations

import streamlit as st


st.title("Expediente de la empresa")

st.write(
    """
    Antes de comenzar la sesión estratégica, necesitamos conocer el contexto
    básico de la organización y el resultado que espera alcanzar.
    """
)

existing_profile = st.session_state.get("company_profile", {})

with st.form("company_profile_form"):
    st.subheader("Información general")

    col1, col2 = st.columns(2)

    with col1:
        company_name = st.text_input(
            "Nombre de la empresa *",
            value=existing_profile.get("company_name", ""),
        )
        sector = st.text_input(
            "Sector *",
            value=existing_profile.get("sector", ""),
        )
        city = st.text_input(
            "Ciudad",
            value=existing_profile.get("city", ""),
        )

    with col2:
        country = st.text_input(
            "País *",
            value=existing_profile.get("country", ""),
        )
        website = st.text_input(
            "Sitio web",
            value=existing_profile.get("website", ""),
            placeholder="https://",
        )
        years_operating = st.number_input(
            "Años de operación",
            min_value=0,
            max_value=200,
            value=int(existing_profile.get("years_operating", 0)),
        )

    st.subheader("Organización")

    col1, col2 = st.columns(2)

    with col1:
        employee_count = st.number_input(
            "Número de colaboradores",
            min_value=0,
            max_value=100_000,
            value=int(existing_profile.get("employee_count", 0)),
        )

    with col2:
        annual_revenue = st.text_input(
            "Facturación anual",
            value=existing_profile.get("annual_revenue", ""),
            placeholder="Opcional",
        )

    st.subheader("Persona entrevistada")

    col1, col2 = st.columns(2)

    with col1:
        interviewee_name = st.text_input(
            "Nombre *",
            value=existing_profile.get("interviewee_name", ""),
        )
        interviewee_role = st.text_input(
            "Cargo *",
            value=existing_profile.get("interviewee_role", ""),
        )

    with col2:
        interviewee_email = st.text_input(
            "Correo",
            value=existing_profile.get("interviewee_email", ""),
        )
        interviewee_phone = st.text_input(
            "Teléfono",
            value=existing_profile.get("interviewee_phone", ""),
        )

    st.subheader("Objetivo estratégico")

    strategic_goal = st.text_area(
        "Si esta consultoría fuera un éxito, ¿qué tendría que haber cambiado "
        "dentro de tu empresa durante los próximos 12 meses? *",
        value=existing_profile.get("strategic_goal", ""),
        height=180,
        placeholder=(
            "Describe el resultado que la organización necesita alcanzar, "
            "el problema que quiere resolver o el cambio que espera conseguir."
        ),
    )

    submitted = st.form_submit_button(
        "Comenzar diagnóstico",
        type="primary",
        use_container_width=True,
    )

if submitted:
    required_fields = {
        "Nombre de la empresa": company_name,
        "Sector": sector,
        "País": country,
        "Nombre del entrevistado": interviewee_name,
        "Cargo": interviewee_role,
        "Objetivo estratégico": strategic_goal,
    }

    missing_fields = [
        label
        for label, value in required_fields.items()
        if not str(value).strip()
    ]

    if missing_fields:
        st.error(
            "Completa los campos obligatorios: "
            + ", ".join(missing_fields)
            + "."
        )
    else:
        st.session_state.company_profile = {
            "company_name": company_name.strip(),
            "sector": sector.strip(),
            "city": city.strip(),
            "country": country.strip(),
            "website": website.strip(),
            "years_operating": years_operating,
            "employee_count": employee_count,
            "annual_revenue": annual_revenue.strip(),
            "interviewee_name": interviewee_name.strip(),
            "interviewee_role": interviewee_role.strip(),
            "interviewee_email": interviewee_email.strip(),
            "interviewee_phone": interviewee_phone.strip(),
            "strategic_goal": strategic_goal.strip(),
        }

        st.session_state.onboarding_stage = "main"
        st.success("Expediente creado correctamente.")
        st.rerun()

