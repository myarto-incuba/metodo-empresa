import pandas as pd
import streamlit as st

from core.database import init_db, list_companies, create_audit, list_audits
from utils.styles import apply_styles

st.set_page_config(page_title="Auditorías", page_icon="🧭", layout="wide")
apply_styles()
init_db()

st.title("Auditorías")

companies = list_companies()
if not companies:
    st.warning("Primero registra una empresa.")
    st.stop()

company_options = {c["name"]: c["id"] for c in companies}

with st.form("audit_form"):
    st.subheader("Crear auditoría")
    company_name = st.selectbox("Empresa", list(company_options.keys()))
    title = st.text_input("Nombre", value="Diagnóstico integral")
    objective = st.text_area(
        "Objetivo",
        value="Detectar fugas, riesgos, ineficiencias y oportunidades de crecimiento.",
    )
    c1, c2 = st.columns(2)
    start = c1.date_input("Inicio del periodo analizado")
    end = c2.date_input("Fin del periodo analizado")
    save = st.form_submit_button("Crear auditoría")
    if save:
        create_audit(company_options[company_name], title.strip(), objective.strip(), start, end)
        st.success("Auditoría creada con sus nueve módulos.")
        st.rerun()

audits = list_audits()
st.subheader("Auditorías registradas")
if audits:
    st.dataframe(pd.DataFrame(audits), use_container_width=True, hide_index=True)
