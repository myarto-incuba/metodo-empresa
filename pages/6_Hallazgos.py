import pandas as pd
import streamlit as st

from config import AUDIT_MODULES, RISK_LEVELS, CONFIDENCE_LEVELS
from core.database import init_db, create_finding, list_findings
from core.selectors import audit_selector
from utils.styles import apply_styles

st.set_page_config(page_title="Hallazgos", page_icon="🔎", layout="wide")
apply_styles()
init_db()

st.title("Hallazgos accionables")
audit_id = audit_selector()
modules = {m["name"]: m["code"] for m in AUDIT_MODULES}

with st.form("finding_form"):
    module_name = st.selectbox("Módulo", list(modules.keys()))
    title = st.text_input("Título del hallazgo *")
    description = st.text_area("¿Qué encontramos?")
    evidence = st.text_area("Evidencia")
    root_cause = st.text_area("Causa raíz")
    consequence = st.text_area("Consecuencia")
    operational_impact = st.text_area("Impacto operativo")
    human_impact = st.text_area("Impacto humano")
    recommendation = st.text_area("Recomendación")
    c1, c2, c3 = st.columns(3)
    financial_impact = c1.number_input("Impacto financiero", min_value=0.0)
    risk_level = c2.selectbox("Riesgo", RISK_LEVELS)
    confidence = c3.selectbox("Confiabilidad", CONFIDENCE_LEVELS)
    save = st.form_submit_button("Guardar hallazgo")

    if save:
        if not title.strip():
            st.error("El título es obligatorio.")
        else:
            create_finding({
                "audit_id": audit_id,
                "module_code": modules[module_name],
                "title": title.strip(),
                "description": description.strip(),
                "evidence": evidence.strip(),
                "root_cause": root_cause.strip(),
                "consequence": consequence.strip(),
                "financial_impact": financial_impact,
                "operational_impact": operational_impact.strip(),
                "human_impact": human_impact.strip(),
                "risk_level": risk_level,
                "confidence": confidence,
                "recommendation": recommendation.strip(),
            })
            st.success("Hallazgo registrado.")
            st.rerun()

findings = list_findings(audit_id)
st.subheader("Hallazgos registrados")
if findings:
    st.dataframe(pd.DataFrame(findings), use_container_width=True, hide_index=True)
else:
    st.info("No hay hallazgos.")
