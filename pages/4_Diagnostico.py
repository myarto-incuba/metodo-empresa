import streamlit as st

from config import AUDIT_MODULES, STATUS_OPTIONS
from core.database import init_db, get_module_reviews, update_module_review
from core.selectors import audit_selector
from utils.styles import apply_styles

st.set_page_config(page_title="Diagnóstico", page_icon="📊", layout="wide")
apply_styles()
init_db()

st.title("Diagnóstico por módulos")
audit_id = audit_selector()
reviews = {r["module_code"]: r for r in get_module_reviews(audit_id)}

tabs = st.tabs([m["name"] for m in AUDIT_MODULES])
for tab, module in zip(tabs, AUDIT_MODULES):
    with tab:
        current = reviews[module["code"]]
        st.markdown(f"### {module['name']}")
        st.write(module["description"])
        st.caption(f"Peso metodológico: {module['weight']}%")
        with st.form(f"review_{module['code']}"):
            score = st.slider("Puntuación", 0, 100, int(current["score"]))
            status = st.selectbox(
                "Estado",
                STATUS_OPTIONS,
                index=STATUS_OPTIONS.index(current["status"]),
            )
            notes = st.text_area(
                "Notas, evidencias y contradicciones",
                value=current["notes"] or "",
                height=220,
            )
            save = st.form_submit_button("Guardar evaluación")
            if save:
                update_module_review(audit_id, module["code"], score, status, notes)
                st.success("Módulo actualizado.")
