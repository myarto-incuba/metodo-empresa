from __future__ import annotations

from datetime import date
import streamlit as st


def render_page_header(*, title: str, description: str = "", eyebrow: str = "Método Empresa") -> None:
    left, right = st.columns([4, 1], vertical_alignment="bottom")
    with left:
        st.caption(eyebrow.upper())
        st.title(title)
        if description:
            st.caption(description)
    with right:
        st.caption(date.today().strftime("%d %b %Y"))
    st.divider()
