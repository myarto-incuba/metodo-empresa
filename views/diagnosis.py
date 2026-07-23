from __future__ import annotations

import streamlit as st

from components.audit_ui import render_audit_header
from core.audit_facade import get_audit
from core.interview_repository import load_interview
from core.scoring_engine import calculate_results
from core.ux_repository import load_action_plan
from knowledge.interview_questions import QUESTIONS_BY_CODE


audit_id = st.session_state.get("active_audit_id")
audit = get_audit(audit_id) if audit_id else None
if audit is None:
    st.warning("Selecciona una auditoría desde Auditorías.")
    st.stop()

render_audit_header(audit)
st.title("Diagnóstico")
st.caption("Resultados, hallazgos, hipótesis y prioridades en una sola experiencia.")

interview = load_interview(audit_id)
answers = interview.get("answers", {})
results = calculate_results(interview)

if not answers:
    st.info("Completa algunas preguntas de la entrevista para generar el diagnóstico.")
    st.stop()

summary_tab, findings_tab, hypotheses_tab, plan_tab = st.tabs(
    ["Resumen", "Hallazgos", "Hipótesis", "Plan de acción"]
)

with summary_tab:
    metric_1, metric_2, metric_3 = st.columns(3)
    metric_1.metric("Madurez general", f"{results['overall_score']}%")
    metric_2.metric("Nivel", results["maturity"])
    metric_3.metric("Entrevista", f"{results['progress']:.0%}")

    st.subheader("Áreas")
    columns = st.columns(5)
    for column, area in zip(
        columns,
        ["Dirección", "Finanzas", "Comercial", "Operaciones", "Personas"],
    ):
        score = results["area_scores"].get(area)
        column.metric(area, f"{score}%" if score is not None else "Pendiente")
        if score is not None:
            column.progress(score / 100)

    weakest = sorted(results["area_scores"].items(), key=lambda item: item[1])[:2]
    if weakest:
        st.info(
            "Áreas prioritarias preliminares: "
            + " y ".join(f"{area} ({score}%)" for area, score in weakest)
            + "."
        )

with findings_tab:
    findings = []
    strengths = []
    for code, answer in answers.items():
        question = QUESTIONS_BY_CODE.get(code)
        if question is None:
            continue
        response = answer.get("answer")
        row = {
            "area": question.area,
            "text": question.text,
            "comment": answer.get("comment", ""),
            "evidence": answer.get("evidence_notes", ""),
        }
        if response in {"No", "Parcialmente"}:
            findings.append(row)
        elif response == "Sí":
            strengths.append(row)

    left, right = st.columns(2)
    with left:
        st.subheader("Hallazgos")
        if not findings:
            st.caption("No hay hallazgos críticos con las respuestas disponibles.")
        for finding in findings:
            with st.container(border=True):
                st.caption(finding["area"])
                st.write(f"**{finding['text']}**")
                if finding["comment"]:
                    st.write(finding["comment"])
                if finding["evidence"]:
                    st.caption(f"Evidencia: {finding['evidence']}")

    with right:
        st.subheader("Fortalezas")
        if not strengths:
            st.caption("Aparecerán al registrar respuestas afirmativas.")
        for strength in strengths[:8]:
            with st.container(border=True):
                st.caption(strength["area"])
                st.write(f"**{strength['text']}**")
                if strength["comment"]:
                    st.write(strength["comment"])

with hypotheses_tab:
    if not results["hypotheses"]:
        st.info("Todavía no hay hipótesis suficientes.")
    for index, hypothesis in enumerate(results["hypotheses"], start=1):
        with st.container(border=True):
            col_1, col_2 = st.columns([3, 1])
            col_1.markdown(f"### {index}. {hypothesis['name']}")
            col_2.metric("Intensidad", f"{hypothesis['confidence']}%")
            st.progress(hypothesis["confidence"] / 100)

with plan_tab:
    plan = load_action_plan(audit_id)
    if not plan:
        st.info("El plan todavía no ha sido formalizado.")
        st.write("Prioridades preliminares:")
        for index, recommendation in enumerate(results["recommendations"], start=1):
            st.write(f"**{index}.** {recommendation}")
        if st.button("Construir plan de acción", type="primary"):
            st.switch_page("views/action_plan.py")
    else:
        for row in plan:
            with st.container(border=True):
                st.markdown(f"### {row.get('action', 'Acción')}")
                st.caption(
                    f"{row.get('priority', 'Media')} · "
                    f"Responsable: {row.get('owner', 'Por definir')} · "
                    f"Plazo: {row.get('deadline', 'Por definir')}"
                )
                st.write(row.get("status", "Pendiente"))
