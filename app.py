import pandas as pd
import plotly.express as px
import streamlit as st

from config import APP_NAME, APP_SUBTITLE
from core.database import init_db, list_audits, get_audit, get_module_reviews, list_findings, list_actions
from core.scoring import weighted_score, maturity_label
from utils.styles import apply_styles

st.set_page_config(page_title=APP_NAME, page_icon="🧭", layout="wide")
apply_styles()
init_db()

st.title(APP_NAME)
st.caption(APP_SUBTITLE)

audits = list_audits()
if not audits:
    st.info("Comienza registrando una empresa desde el menú lateral.")
    st.markdown(
        """
        ### Flujo de la beta
        **Empresa → Auditoría → Expediente → Diagnóstico → Hallazgos → Acciones → Dashboard**
        """
    )
    st.stop()

options = {f"{a['company_name']} — {a['title']}": a["id"] for a in audits}
selected = st.selectbox("Auditoría activa", list(options.keys()))
audit_id = options[selected]

audit = get_audit(audit_id)
reviews = get_module_reviews(audit_id)
findings = list_findings(audit_id)
actions = list_actions(audit_id)

score = weighted_score(reviews)
completed = sum(r["status"] == "Completado" for r in reviews)
critical = sum(f["risk_level"] == "Crítico" for f in findings)
saving = sum(float(a["estimated_saving"] or 0) for a in actions)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Salud empresarial", f"{score}/100", maturity_label(score))
c2.metric("Módulos completados", f"{completed}/{len(reviews)}")
c3.metric("Hallazgos críticos", critical)
c4.metric("Impacto potencial", f"{saving:,.0f} {audit['currency']}")

st.subheader("Radiografía 360")
df = pd.DataFrame(reviews)
if not df.empty:
    fig = px.line_polar(
        df,
        r="score",
        theta="module_name",
        line_close=True,
        range_r=[0, 100],
    )
    fig.update_traces(fill="toself")
    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)

with left:
    st.subheader("Prioridades")
    if findings:
        priority = {"Crítico": 1, "Alto": 2, "Medio": 3, "Bajo": 4}
        fdf = pd.DataFrame(findings)
        fdf["orden"] = fdf["risk_level"].map(priority)
        fdf = fdf.sort_values(["orden", "financial_impact"], ascending=[True, False])
        st.dataframe(
            fdf[["title", "module_code", "risk_level", "financial_impact"]],
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("Aún no hay hallazgos.")

with right:
    st.subheader("Ruta de transformación")
    if actions:
        adf = pd.DataFrame(actions)
        st.dataframe(
            adf[["action", "owner", "horizon", "status"]],
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("Aún no hay acciones.")
