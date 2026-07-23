from __future__ import annotations

import streamlit as st

from core.audit_repository import get_audit, list_audits
from core.interview_repository import load_interview
from core.scoring_engine import calculate_results


st.set_page_config(
    page_title="Resultados | Método Empresa",
    page_icon="📊",
    layout="wide",
)

st.title("Panel de diagnóstico")
st.caption("Resultados preliminares para orientar la conversación y la visita presencial.")

audits = list_audits()
if not audits:
    st.warning("No hay auditorías registradas.")
    st.stop()

audit_options = {
    f"{audit.company_name} · {audit.audit_id}": audit.audit_id
    for audit in audits
}

default_id = st.session_state.get("active_audit_id")
default_index = 0
if default_id:
    for index, audit_id in enumerate(audit_options.values()):
        if audit_id == default_id:
            default_index = index
            break

selected_label = st.selectbox(
    "Auditoría",
    list(audit_options),
    index=default_index,
)
audit_id = audit_options[selected_label]
audit = get_audit(audit_id)
interview = load_interview(audit_id)
results = calculate_results(interview)

if audit is None:
    st.error("No fue posible cargar la auditoría.")
    st.stop()

st.markdown(f"## {audit.company_name}")
st.caption(
    f"{audit.sector or 'Sector no indicado'} · "
    f"Fecha: {audit.audit_date} · Auditor: {audit.auditor_name}"
)

if results["answered"] == 0:
    st.info("Todavía no existen respuestas para esta auditoría.")
    st.stop()

metric_1, metric_2, metric_3, metric_4 = st.columns(4)
metric_1.metric("Madurez general", f'{results["overall_score"]}%')
metric_2.metric("Nivel", results["maturity"])
metric_3.metric("Avance", f'{results["progress"]:.0%}')
metric_4.metric("Respondidas", f'{results["answered"]}/{results["total"]}')

st.progress(results["overall_score"] / 100)

if results["progress"] < 1:
    st.warning(
        "Diagnóstico preliminar: la entrevista todavía no está completa. "
        "Los resultados cambiarán al guardar más respuestas."
    )

st.divider()
st.subheader("Resultados por área")

area_columns = st.columns(5)
ordered_areas = ["Dirección", "Finanzas", "Comercial", "Operaciones", "Personas"]
for column, area in zip(area_columns, ordered_areas):
    score = results["area_scores"].get(area)
    if score is None:
        column.metric(area, "Pendiente")
    else:
        column.metric(area, f"{score}%")
        column.progress(score / 100)

st.divider()
left, right = st.columns([3, 2])

with left:
    st.subheader("Hipótesis detectadas")
    if not results["hypotheses"]:
        st.success("No se detectan debilidades con las respuestas disponibles.")
    else:
        for index, hypothesis in enumerate(results["hypotheses"], start=1):
            with st.container(border=True):
                st.markdown(f"**{index}. {hypothesis['name']}**")
                st.progress(hypothesis["confidence"] / 100)
                st.caption(
                    f"Intensidad observada: {hypothesis['confidence']}%"
                )

with right:
    st.subheader("Prioridades sugeridas")
    if not results["recommendations"]:
        st.info("Se generarán cuando existan debilidades identificadas.")
    else:
        for index, recommendation in enumerate(
            results["recommendations"],
            start=1,
        ):
            st.markdown(f"**{index}.** {recommendation}")

st.divider()
st.subheader("Lectura ejecutiva")

weakest_areas = sorted(
    results["area_scores"].items(),
    key=lambda item: item[1],
)[:2]

if weakest_areas:
    area_text = " y ".join(
        f"{area} ({score}%)"
        for area, score in weakest_areas
    )
else:
    area_text = "las áreas aún no evaluadas"

primary_hypothesis = (
    results["hypotheses"][0]["name"]
    if results["hypotheses"]
    else "sin una hipótesis crítica confirmada"
)

st.write(
    f"Con la información capturada, Synoni presenta un nivel de madurez "
    f"**{results['maturity'].lower()} ({results['overall_score']}%)**. "
    f"Las áreas que requieren mayor atención preliminar son {area_text}. "
    f"El patrón principal observado es **{primary_hypothesis}**. "
    "Estos resultados deben validarse con evidencia documental y observación "
    "durante la visita presencial."
)
