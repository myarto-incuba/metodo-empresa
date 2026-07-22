import pandas as pd
import streamlit as st

from config import ACTION_HORIZONS
from core.database import init_db, list_findings, create_action, list_actions
from core.selectors import audit_selector
from utils.styles import apply_styles

st.set_page_config(page_title="Roadmap", page_icon="✅", layout="wide")
apply_styles()
init_db()

st.title("Ruta de transformación")
audit_id = audit_selector()

findings = list_findings(audit_id)
finding_options = {"Acción independiente": None}
finding_options.update({f["title"]: f["id"] for f in findings})

with st.form("action_form"):
    finding_label = st.selectbox("Hallazgo relacionado", list(finding_options.keys()))
    action = st.text_area("Acción concreta *")
    c1, c2, c3 = st.columns(3)
    owner = c1.text_input("Responsable")
    horizon = c2.selectbox("Horizonte", ACTION_HORIZONS)
    due_date = c3.date_input("Fecha objetivo")
    c4, c5 = st.columns(2)
    estimated_cost = c4.number_input("Costo estimado", min_value=0.0)
    estimated_saving = c5.number_input("Ahorro o impacto estimado", min_value=0.0)
    success_metric = st.text_input("Indicador de éxito")
    save = st.form_submit_button("Agregar acción")

    if save:
        if not action.strip():
            st.error("La acción es obligatoria.")
        else:
            create_action({
                "audit_id": audit_id,
                "finding_id": finding_options[finding_label],
                "action": action.strip(),
                "owner": owner.strip(),
                "horizon": horizon,
                "estimated_cost": estimated_cost,
                "estimated_saving": estimated_saving,
                "success_metric": success_metric.strip(),
                "due_date": str(due_date),
            })
            st.success("Acción agregada.")
            st.rerun()

actions = list_actions(audit_id)
st.subheader("Plan de acción")
if actions:
    st.dataframe(pd.DataFrame(actions), use_container_width=True, hide_index=True)
else:
    st.info("No hay acciones.")
