from __future__ import annotations

import html
import streamlit as st

from components.audit_ui import render_audit_header
from components.brand import render_footer, render_wordmark
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

render_wordmark()
render_audit_header(audit)

interview = load_interview(audit_id)
answers = interview.get("answers", {})
results = calculate_results(interview)

st.markdown('<div class="inc-eyebrow">Lectura ejecutiva</div>', unsafe_allow_html=True)
st.title("Diagnóstico")
st.caption("Una lectura clara de la madurez, los patrones y las decisiones prioritarias.")

if not answers:
    st.info("Completa algunas respuestas para generar el diagnóstico.")
    st.stop()

area_scores = results.get("area_scores", {})
weakest = sorted(area_scores.items(), key=lambda item: item[1])[:2]
priority_text = (
    " y ".join(f"{area} ({score}%)" for area, score in weakest)
    if weakest else "Por definir"
)

st.markdown(
    f"""
    <div class="inc-diagnosis-hero">
        <div class="inc-score">
            <div class="inc-card-kicker">MADUREZ GENERAL</div>
            <div class="inc-score-number">{results['overall_score']}%</div>
            <div class="inc-score-label">{html.escape(str(results['maturity']))}</div>
        </div>
        <div class="inc-priority">
            <div class="inc-card-kicker">FOCO DE INTERVENCIÓN</div>
            <h2 style="margin:.65rem 0 .55rem">{html.escape(priority_text)}</h2>
            <p>Estas áreas concentran la mayor oportunidad preliminar de mejora.
            La lectura se actualizará conforme avance la conversación y la evidencia.</p>
            <div class="inc-tagline">{results['progress']:.0%} de la conversación completada</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="inc-section-title">Mapa de madurez</div>', unsafe_allow_html=True)
rows = []
for area in ["Dirección", "Finanzas", "Comercial", "Operaciones", "Personas"]:
    score = area_scores.get(area)
    value = int(score) if score is not None else 0
    rows.append(
        f"""
        <div class="inc-area-row">
            <div class="inc-area-name">{area}</div>
            <div class="inc-area-track">
                <div class="inc-area-fill" style="width:{value}%"></div>
            </div>
            <div class="inc-area-value">{score if score is not None else "—"}%</div>
        </div>
        """
    )
st.markdown(f'<div class="inc-panel" style="padding:1.35rem 1.55rem">{"".join(rows)}</div>', unsafe_allow_html=True)

summary_tab, findings_tab, hypotheses_tab, plan_tab = st.tabs(
    ["Lectura general", "Hallazgos", "Hipótesis", "Plan de acción"]
)

with summary_tab:
    cols = st.columns(3)
    cols[0].metric("Respuestas", results.get("answered", len(answers)))
    cols[1].metric("Madurez", f"{results['overall_score']}%")
    cols[2].metric("Nivel", results["maturity"])

    st.markdown("### Lo que el sistema está viendo")
    hypotheses = results.get("hypotheses", [])
    if hypotheses:
        st.write(
            "La principal hipótesis es "
            f"**{hypotheses[0]['name']}**, con una intensidad preliminar de "
            f"**{hypotheses[0]['confidence']}%**."
        )
    if weakest:
        st.write(
            "Las áreas con menor madurez son "
            + " y ".join(f"**{area}**" for area, _ in weakest)
            + "."
        )

with findings_tab:
    findings, strengths = [], []
    for code, answer in answers.items():
        question = QUESTIONS_BY_CODE.get(code)
        if question is None:
            continue
        row = {
            "area": question.area,
            "text": question.text,
            "comment": answer.get("comment", ""),
            "evidence": answer.get("evidence_notes", ""),
        }
        if answer.get("answer") in {"No", "Parcialmente"}:
            findings.append(row)
        elif answer.get("answer") == "Sí":
            strengths.append(row)

    left, right = st.columns(2)
    with left:
        st.markdown("### Tensiones y hallazgos")
        if not findings:
            st.caption("No hay hallazgos críticos con las respuestas actuales.")
        for finding in findings:
            with st.container(border=True):
                st.caption(finding["area"])
                st.write(f"**{finding['text']}**")
                if finding["comment"]:
                    st.write(finding["comment"])
                if finding["evidence"]:
                    st.caption(f"Evidencia: {finding['evidence']}")

    with right:
        st.markdown("### Fortalezas")
        if not strengths:
            st.caption("Aparecerán conforme se registren respuestas afirmativas.")
        for strength in strengths[:10]:
            with st.container(border=True):
                st.caption(strength["area"])
                st.write(f"**{strength['text']}**")
                if strength["comment"]:
                    st.write(strength["comment"])

with hypotheses_tab:
    hypotheses = results.get("hypotheses", [])
    if not hypotheses:
        st.info("Todavía no hay hipótesis suficientes.")
    for index, hypothesis in enumerate(hypotheses, start=1):
        with st.container(border=True):
            col_1, col_2 = st.columns([3, 1])
            col_1.markdown(f"### {index}. {hypothesis['name']}")
            col_1.caption("Patrón preliminar sujeto a validación con evidencia.")
            col_2.metric("Intensidad", f"{hypothesis['confidence']}%")
            st.progress(hypothesis["confidence"] / 100)

with plan_tab:
    plan = load_action_plan(audit_id)
    if not plan:
        st.info("El plan todavía no ha sido formalizado.")
        recommendations = results.get("recommendations", [])
        for index, recommendation in enumerate(recommendations, start=1):
            with st.container(border=True):
                st.caption(f"PRIORIDAD {index}")
                st.write(f"**{recommendation}**")
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

render_footer()
