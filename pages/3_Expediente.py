import streamlit as st

from core.database import init_db, get_profile, update_profile
from core.selectors import audit_selector
from utils.styles import apply_styles

st.set_page_config(page_title="Expediente", page_icon="📁", layout="wide")
apply_styles()
init_db()

st.title("Expediente general")
audit_id = audit_selector()
profile = get_profile(audit_id) or {}

with st.form("profile_form"):
    value_proposition = st.text_area("Propuesta de valor", value=profile.get("value_proposition") or "")
    products_services = st.text_area("Productos y servicios", value=profile.get("products_services") or "")
    customer_segments = st.text_area("Segmentos de clientes", value=profile.get("customer_segments") or "")
    revenue_streams = st.text_area("Fuentes de ingreso", value=profile.get("revenue_streams") or "")
    strategic_objectives = st.text_area("Objetivos estratégicos", value=profile.get("strategic_objectives") or "")
    decision_makers = st.text_area("Tomadores de decisión", value=profile.get("decision_makers") or "")
    perceived_bottlenecks = st.text_area("Cuellos de botella percibidos", value=profile.get("perceived_bottlenecks") or "")
    critical_dependencies = st.text_area("Dependencias críticas", value=profile.get("critical_dependencies") or "")
    notes = st.text_area("Notas generales", value=profile.get("notes") or "")
    save = st.form_submit_button("Guardar expediente")
    if save:
        update_profile(audit_id, {
            "value_proposition": value_proposition,
            "products_services": products_services,
            "customer_segments": customer_segments,
            "revenue_streams": revenue_streams,
            "strategic_objectives": strategic_objectives,
            "decision_makers": decision_makers,
            "perceived_bottlenecks": perceived_bottlenecks,
            "critical_dependencies": critical_dependencies,
            "notes": notes,
        })
        st.success("Expediente actualizado.")
