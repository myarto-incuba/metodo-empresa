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

st.markdown('<div class="inc-eyebrow">Diagnóstico ejecutivo</div>', unsafe_allow_html=True)
st.title("La historia detrás de la empresa")
st.caption("Madurez, tensiones, fortalezas y prioridades reunidas en una sola lectura.")

if not answers:
    st.info("Completa algunas respuestas para generar el diagnóstico.")
    st.stop()

area_scores = results.get("area_scores", {})
weakest = sorted(area_scores.items(), key=lambda item: item[1])[:2]
strongest = sorted(area_scores.items(), key=lambda item: item[1], reverse=True)[:2]
hypotheses = results.get("hypotheses", [])
priority_text = (
    " y ".join(f"{area} ({score}%)" for area, score in weakest)
    if weakest else "Por definir"
)
main_hypothesis = hypotheses[0]["name"] if hypotheses else "Aún sin hipótesis dominante"
main_confidence = hypotheses[0]["confidence"] if hypotheses else 0

st.markdown(
    f"""
    <div class="inc-diagnosis-hero">
        <div class="inc-score">
            <div class="inc-card-kicker">MADUREZ GENERAL</div>
            <div class="inc-score-number">{results['overall_score']}%</div>
            <div class="inc-score-label">{html.escape(str(results['maturity']))}</div>
        </div>
        <div class="inc-priority">
            <div class="inc-card-kicker">LECTURA PRINCIPAL</div>
            <h2 style="margin:.65rem 0 .45rem">{html.escape(main_hypothesis)}</h2>
            <p>
                Es el patrón con mayor intensidad preliminar. Debe validarse con
                evidencia y con la visita final antes de convertirse en conclusión.
            </p>
            <div class="inc-tagline">{main_confidence}% de intensidad</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

story_1, story_2, story_3 = st.columns(3)
with story_1:
    st.markdown(
        f"""
        <div class="inc-card">
            <div class="inc-card-kicker">DÓNDE ESTÁ EL RETO</div>
            <div style="font-size:1.2rem;font-weight:900;margin:.7rem 0;">
                {html.escape(priority_text)}
            </div>
            <div class="inc-card-label">
                Áreas con menor madurez relativa.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with story_2:
    strength_text = (
        " y ".join(f"{area} ({score}%)" for area, score in strongest)
        if strongest else "Por definir"
    )
    st.markdown(
        f"""
        <div class="inc-card">
            <div class="inc-card-kicker">DÓNDE HAY BASE</div>
            <div style="font-size:1.2rem;font-weight:900;margin:.7rem 0;">
                {html.escape(strength_text)}
            </div>
            <div class="inc-card-label">
                Capacidades sobre las que se puede construir.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with story_3:
    st.markdown(
        f"""
        <div class="inc-card">
            <div class="inc-card-kicker">NIVEL DE VALIDACIÓN</div>
            <div style="font-size:1.2rem;font-weight:900;margin:.7rem 0;">
                {results['progress']:.0%} de la conversación
            </div>
            <div class="inc-card-label">
                El diagnóstico seguirá evolucionando.
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
    shown = f"{score}%" if score is not None else "—"
    rows.append(
        f"""
        <div class="inc-area-row">
            <div class="inc-area-name">{area}</div>
            <div class="inc-area-track">
                <div class="inc-area-fill" style="width:{value}%"></div>
            </div>
            <div class="inc-area-value">{shown}</div>
        </div>
        """
    )
st.markdown(
    f'<div class="inc-panel" style="padding:1.35rem 1.55rem">{"".join(rows)}</div>',
    unsafe_allow_html=True,
)

overview_tab, findings_tab, hypotheses_tab, plan_tab = st.tabs(
    ["Historia ejecutiva", "Hallazgos", "Hipótesis", "Plan 90 días"]
)

with overview_tab:
    st.markdown("### Lectura ejecutiva")
    if weakest:
        st.write(
            "La empresa muestra su mayor oportunidad en "
            + " y ".join(f"**{area}**" for area, _ in weakest)
            + "."
        )
    if strongest:
        st.write(
            "Al mismo tiempo, cuenta con una base más sólida en "
            + " y ".join(f"**{area}**" for area, _ in strongest)
            + ", lo que puede facilitar la implementación."
        )
    if hypotheses:
        st.write(
            f"El patrón dominante es **{hypotheses[0]['name']}** "
            f"con una intensidad preliminar de **{hypotheses[0]['confidence']}%**."
        )

    st.markdown("### Prioridades sugeridas")
    for index, recommendation in enumerate(results.get("recommendations", [])[:5], start=1):
        with st.container(border=True):
            st.caption(f"PRIORIDAD {index}")
            st.write(f"**{recommendation}**")

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
                st.caption(finding["area"].upper())
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
                st.caption(strength["area"].upper())
                st.write(f"**{strength['text']}**")
                if strength["comment"]:
                    st.write(strength["comment"])

with hypotheses_tab:
    if not hypotheses:
        st.info("Todavía no hay hipótesis suficientes.")
    for index, hypothesis in enumerate(hypotheses, start=1):
        with st.container(border=True):
            col_1, col_2 = st.columns([3, 1])
            col_1.caption(f"HIPÓTESIS {index}")
            col_1.markdown(f"### {hypothesis['name']}")
            col_1.write("Patrón preliminar sujeto a validación con evidencia.")
            col_2.metric("Intensidad", f"{hypothesis['confidence']}%")
            st.progress(hypothesis["confidence"] / 100)

with plan_tab:
    plan = load_action_plan(audit_id)
    if not plan:
        st.info("El plan de 90 días todavía no ha sido formalizado.")
        for index, recommendation in enumerate(results.get("recommendations", []), start=1):
            with st.container(border=True):
                period = "0–30 días" if index <= 2 else "31–60 días" if index <= 4 else "61–90 días"
                st.caption(period.upper())
                st.write(f"**{recommendation}**")
        if st.button("Construir plan de acción", type="primary"):
            st.switch_page("views/action_plan.py")
    else:
        for row in plan:
            with st.container(border=True):
                st.caption(str(row.get("priority", "Media")).upper())
                st.markdown(f"### {row.get('action', 'Acción')}")
                st.write(
                    f"**Responsable:** {row.get('owner', 'Por definir')}  \n"
                    f"**Plazo:** {row.get('deadline', 'Por definir')}  \n"
                    f"**Estado:** {row.get('status', 'Pendiente')}"
                )

render_footer()
