from __future__ import annotations

import streamlit as st
from components.audit_ui import render_audit_header
from components.brand import render_footer
from components.page_header import render_page_header
from core.audit_facade import get_audit
from core.interview_repository import load_interview
from core.narrative_engine import build_strategic_reading
from core.ux_repository import load_action_plan, save_action_plan


audit_id = st.session_state.get("active_audit_id")
audit = get_audit(audit_id) if audit_id else None
if audit is None:
    st.warning("Selecciona una auditoría desde Auditorías.")
    st.stop()

reading = build_strategic_reading(
    load_interview(audit_id), company_name=getattr(audit, "company_name", "La empresa")
)
render_page_header(
    title="Diagnóstico",
    eyebrow="Adapta",
    description="Lectura ejecutiva de madurez, patrones, riesgos y prioridades.",
)
render_audit_header(audit)

if reading["progress"] == 0:
    st.info("Completa algunas respuestas para generar la lectura estratégica.")
    st.stop()

score, headline = st.columns([1, 3], vertical_alignment="center")
score.metric("Índice de madurez", f"{reading['overall_score']}%")
headline.subheader(reading["maturity"])
headline.write(reading["headline"])
headline.caption(reading["validation_note"])
st.divider()

st.subheader("Resumen ejecutivo")
for paragraph in reading["executive_summary"].split("\n\n"):
    st.write(paragraph)

st.divider()
st.subheader("Madurez por área")
area_rows = sorted(
    reading.get("strongest_areas", []) + reading.get("weakest_areas", []), key=lambda x: x[0]
)
for area, area_score in area_rows:
    label, bar, number = st.columns([1.5, 4, .7], vertical_alignment="center")
    label.write(area)
    bar.progress(max(0, min(area_score / 100, 1)))
    number.write(f"{area_score}%")

st.divider()
tab1, tab2, tab3, tab4 = st.tabs(["Patrones", "Riesgos", "Preguntas", "Roadmap"])
with tab1:
    for pattern in reading["patterns"]:
        title, intensity = st.columns([4, 1], vertical_alignment="center")
        title.markdown(f"**{pattern['name']}**")
        intensity.write(f"{pattern['confidence']}%")
        st.write(pattern["summary"])
        st.progress(pattern["confidence"] / 100)
        with st.expander(f"Ver {pattern['signal_count']} señales"):
            for signal in pattern["signals"]:
                st.write(
                    f"**{signal['question_code']} · {signal['answer']}** — {signal['question']}"
                )
        st.divider()
with tab2:
    for risk in reading["risks"]:
        title, intensity = st.columns([4, 1], vertical_alignment="center")
        title.markdown(f"**{risk['name']}**")
        intensity.write(f"{risk['confidence']}%")
        st.write(risk["risk"])
        st.divider()
with tab3:
    questions = []
    for pattern in reading["patterns"][:4]:
        questions.extend(item for item in pattern["follow_up_questions"] if item not in questions)
    for number, item in enumerate(questions, start=1):
        cols = st.columns([.35, 4])
        cols[0].caption(f"{number:02d}")
        cols[1].write(item)
        st.divider()
with tab4:
    current = load_action_plan(audit_id)
    roadmap = current or reading["roadmap"]
    for period in ("0–30 días", "31–60 días", "61–90 días"):
        st.subheader(period)
        for row in [item for item in roadmap if item.get("period", item.get("deadline")) == period]:
            action_col, priority_col = st.columns([4, 1], vertical_alignment="center")
            action_col.markdown(f"**{row.get('action', 'Acción')}**")
            action_col.caption(row.get("source_pattern", "Diagnóstico"))
            priority_col.caption(f"PRIORIDAD {row.get('priority', 'Media').upper()}")
            st.divider()
    if not current and reading["roadmap"] and st.button("Convertir en plan de acción", type="primary"):
        save_action_plan(audit_id, reading["roadmap"])
        st.success("Plan creado.")
        st.rerun()

render_footer()
