from __future__ import annotations

import streamlit as st

from components.audit_ui import apply_product_style


st.set_page_config(
    page_title="Método Empresa",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_product_style()

general_pages = [
    st.Page("views/dashboard.py", title="Dashboard", icon=":material/home:", default=True),
    st.Page("views/companies.py", title="Empresas", icon=":material/domain:"),
    st.Page("views/audits.py", title="Auditorías", icon=":material/assignment:"),
]

audit_pages = [
    st.Page("views/interview.py", title="Entrevista", icon=":material/forum:"),
    st.Page("views/evidence.py", title="Evidencias", icon=":material/folder_open:"),
    st.Page("views/diagnosis.py", title="Diagnóstico", icon=":material/analytics:"),
    st.Page("views/action_plan.py", title="Plan de acción", icon=":material/task_alt:"),
]

navigation = {"General": general_pages}
if st.session_state.get("active_audit_id"):
    navigation["Auditoría activa"] = audit_pages

page = st.navigation(navigation)
page.run()
