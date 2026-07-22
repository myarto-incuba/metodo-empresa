import pandas as pd
import streamlit as st

from core.database import init_db, insert_financial_rows, list_financial_rows, get_audit
from core.financial_engine import normalize_financial_dataframe, financial_summary, financial_alerts
from core.selectors import audit_selector
from utils.styles import apply_styles

st.set_page_config(page_title="Finanzas", page_icon="💰", layout="wide")
apply_styles()
init_db()

st.title("Finanzas y rentabilidad")
audit_id = audit_selector()
audit = get_audit(audit_id)

st.markdown(
    """
    Carga un archivo con estas columnas:
    `period`, `category`, `subcategory`, `description`, `amount`.

    También se aceptan encabezados en español como periodo, categoría, subcategoría, concepto y monto.
    """
)

uploaded = st.file_uploader("Archivo financiero", type=["xlsx", "csv"])
if uploaded:
    try:
        raw = pd.read_excel(uploaded) if uploaded.name.endswith("xlsx") else pd.read_csv(uploaded)
        normalized = normalize_financial_dataframe(raw)
        st.dataframe(normalized.head(30), use_container_width=True)
        if st.button("Importar datos"):
            insert_financial_rows(audit_id, normalized.to_dict("records"))
            st.success("Datos importados.")
            st.rerun()
    except Exception as exc:
        st.error(str(exc))

rows = list_financial_rows(audit_id)
if not rows:
    st.info("Aún no hay datos financieros importados.")
    st.stop()

df = pd.DataFrame(rows)
summary = financial_summary(df)

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Ingresos", f"{summary['income']:,.0f} {audit['currency']}")
c2.metric("Costos", f"{summary['costs']:,.0f}")
c3.metric("Gastos", f"{summary['expenses']:,.0f}")
c4.metric("Nómina", f"{summary['payroll']:,.0f}")
c5.metric("Resultado", f"{summary['profit']:,.0f}", f"{summary['margin']:.1f}%")

st.subheader("Alertas iniciales")
for alert in financial_alerts(summary):
    if alert["level"] in ["Crítico", "Alto"]:
        st.error(f"**{alert['title']}** — {alert['message']}")
    else:
        st.info(f"**{alert['title']}** — {alert['message']}")

st.subheader("Detalle")
st.dataframe(
    df[["period", "category", "subcategory", "description", "amount"]],
    use_container_width=True,
    hide_index=True,
)
