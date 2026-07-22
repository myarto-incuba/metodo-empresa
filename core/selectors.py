import streamlit as st
from core.database import list_audits

def audit_selector(label="Auditoría"):
    audits = list_audits()
    if not audits:
        st.warning("Primero registra una empresa y crea una auditoría.")
        st.stop()

    options = {
        f"{a['company_name']} — {a['title']}": a["id"]
        for a in audits
    }
    selected = st.selectbox(label, list(options.keys()))
    return options[selected]
