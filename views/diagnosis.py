from __future__ import annotations

import streamlit as st

from components.audit_ui import render_audit_header
from components.brand import render_footer, render_wordmark
from core.audit_facade import get_audit
from core.interview_repository import load_interview
from core.narrative_engine import build_strategic_reading
from core.ux_repository import load_action_plan, save_action_plan


audit_id = st.session_state.get("active_audit_id")
audit = get_audit(audit_id) if audit_id else None
if audit is None:
    st.warning("Selecciona una auditoría desde Auditorías.")
    st.stop()

render_wordmark()
render_audit_header(audit)

interview = load_interview(audit_id)
company_name = getattr(audit, "company_name", "La empresa")
reading = build_strategic_reading(interview, company_name=company_name)

if reading["progress"] == 0:
    st.info("Completa algunas respuestas para generar la lectura estratégica.")
    st.stop()

st.markdown('<div class="inc-eyebrow">Lectura estratégica</div>', unsafe_allow_html=True)
st.title(reading["headline"])
st.caption(reading["validation_note"])

m1, m2, m3 = st.columns(3)
m1.metric("Madurez", f'{reading["overall_score"]}%')
m2.metric("Etapa", reading["maturity"])
m3.metric("Entrevista", f'{reading["progress"]:.0%}')

st.markdown("## Resumen ejecutivo")
with st.container(border=True):
    for paragraph in reading["executive_summary"].split("\n\n"):
        st.write(paragraph)

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Patrones", "Riesgos", "Evidencias", "Preguntas", "Roadmap"]
)

with tab1:
    if not reading["patterns"]:
        st.info("Todavía no hay suficientes señales combinadas.")
    for index, pattern in enumerate(reading["patterns"], start=1):
        with st.container(border=True):
            c1, c2 = st.columns([3, 1])
            c1.caption(f"PATRÓN {index}")
            c1.markdown(f"### {pattern['name']}")
            c1.write(pattern["summary"])
            c2.metric("Intensidad", f'{pattern["confidence"]}%')
            st.progress(pattern["confidence"] / 100)
            with st.expander(f"Ver {pattern['signal_count']} señales"):
                for signal in pattern["signals"]:
                    st.write(
                        f"**{signal['question_code']} · {signal['answer']}** — "
                        f"{signal['question']}"
                    )
                    if signal["comment"]:
                        st.caption(signal["comment"])

with tab2:
    for risk in reading["risks"]:
        with st.container(border=True):
            st.caption(risk["name"].upper())
            st.markdown(f"### {risk['risk']}")
            st.caption(f"Intensidad de la hipótesis: {risk['confidence']}%")

with tab3:
    evidence = []
    for pattern in reading["patterns"][:4]:
        for item in pattern["suggested_evidence"]:
            if item not in evidence:
                evidence.append(item)
    if not evidence:
        st.caption("Sin evidencias sugeridas todavía.")
    for item in evidence:
        st.checkbox(item, key=f"evidence-check-{audit_id}-{item}")

with tab4:
    questions = []
    for pattern in reading["patterns"][:4]:
        for item in pattern["follow_up_questions"]:
            if item not in questions:
                questions.append(item)
    if not questions:
        st.caption("Sin preguntas adicionales todavía.")
    for item in questions:
        with st.container(border=True):
            st.write(f"**{item}**")

with tab5:
    current_plan = load_action_plan(audit_id)
    roadmap = current_plan or reading["roadmap"]

    for period in ("0–30 días", "31–60 días", "61–90 días"):
        st.markdown(f"### {period}")
        period_rows = [
            row for row in roadmap
            if row.get("period", row.get("deadline")) == period
        ]
        if not period_rows:
            st.caption("Sin acciones asignadas.")
        for row in period_rows:
            with st.container(border=True):
                st.write(f"**{row.get('action', 'Acción')}**")
                st.caption(
                    f"Origen: {row.get('source_pattern', 'Diagnóstico')} · "
                    f"Prioridad: {row.get('priority', 'Media')}"
                )

    if not current_plan and reading["roadmap"]:
        if st.button("Convertir en plan de acción", type="primary"):
            save_action_plan(audit_id, reading["roadmap"])
            st.success("Roadmap guardado como plan de acción.")
            st.rerun()

render_footer()
