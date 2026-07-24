from __future__ import annotations

import streamlit as st


def render_incubatour_signature(*, compact: bool = False) -> None:
    if compact:
        st.caption("◆ ◆ ◆ ◆  INCUBATOUR® · MÉTODO EMPRESA®")
        return
    st.caption("◆ ◆ ◆ ◆  INCUBATOUR®")
    st.subheader("Método Empresa®")
    st.caption("Diagnóstico estratégico para convertir conversaciones en decisiones y acciones.")


def render_methodology_path(*, active_phase: str | None = None) -> None:
    phases = ["Analiza", "Aprende", "Adapta", "Actúa"]
    cols = st.columns(4)
    for col, phase in zip(cols, phases):
        active = bool(active_phase and phase.lower() == active_phase.lower())
        col.caption("FASE ACTUAL" if active else "FASE")
        col.markdown(f"**{'● ' if active else ''}{phase}**")
    st.divider()


def render_method_value_card() -> None:
    st.subheader("De la conversación a la acción")
    st.caption("Analiza la empresa, identifica patrones, adapta prioridades y construye un plan de 90 días.")


def render_incubatour_footer() -> None:
    st.divider()
    st.caption("Incubatour® · Método Empresa®")
