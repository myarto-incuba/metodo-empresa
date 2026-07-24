from __future__ import annotations

import streamlit as st


st.markdown(
    """
    <div style="
        max-width: 900px;
        margin: 5rem auto 2rem auto;
        text-align: center;
    ">
        <p style="
            font-size: 0.85rem;
            font-weight: 700;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            opacity: 0.65;
            margin-bottom: 1rem;
        ">
            Incubatour
        </p>

        <h1 style="
            font-size: clamp(2.6rem, 6vw, 5rem);
            line-height: 1;
            margin-bottom: 1rem;
        ">
            Método Empresa®
        </h1>

        <h2 style="
            font-size: 1.45rem;
            font-weight: 400;
            opacity: 0.8;
            margin-bottom: 2rem;
        ">
            Sistema de Diagnóstico Estratégico Empresarial
        </h2>

        <p style="
            max-width: 720px;
            margin: 0 auto 3rem auto;
            font-size: 1.1rem;
            line-height: 1.7;
            opacity: 0.8;
        ">
            Una sesión guiada para evaluar el nivel de madurez de tu
            organización, identificar los factores que limitan su crecimiento
            y definir sus prioridades estratégicas.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("### Al finalizar obtendrás")

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown(
        """
        - Índice de madurez empresarial
        - Diagnóstico por áreas
        - Fortalezas competitivas
        """
    )

with col2:
    st.markdown(
        """
        - Riesgos y cuellos de botella
        - Prioridades estratégicas
        - Plan de acción recomendado
        """
    )

st.markdown("---")

info_col, button_col = st.columns([1, 1])

with info_col:
    st.markdown(
        """
        **Duración aproximada**

        35–45 minutos
        """
    )

with button_col:
    if st.button(
        "Iniciar sesión estratégica",
        type="primary",
        use_container_width=True,
    ):
        st.session_state.onboarding_stage = "profile"
        st.rerun()

st.caption("Método Empresa® · Versión 2.0 · Incubatour")

