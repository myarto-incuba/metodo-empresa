from __future__ import annotations

import streamlit as st
from components.audit_ui import render_audit_header
from components.brand import render_footer
from components.page_header import render_page_header
from core.audit_facade import get_audit
from core.interview_repository import add_observation, load_interview, save_answer
from core.pattern_engine import build_copilot
from core.scoring_engine import calculate_results
from knowledge.interview_questions import INTERVIEW_QUESTIONS


def clamp(value: float) -> float:
    return max(0.0, min(float(value), 1.0))


audit_id = st.session_state.get("active_audit_id")
audit = get_audit(audit_id) if audit_id else None
if audit is None:
    render_page_header(
        title="Sin expediente activo",
        eyebrow="Conversación estratégica",
        description="Selecciona una auditoría antes de comenzar.",
    )
    if st.button("Ir a Auditorías", type="primary"):
        st.switch_page("views/audits.py")
    st.stop()

interview = load_interview(audit_id)
answers = interview.get("answers", {}) if isinstance(interview, dict) else {}
results = calculate_results(interview)
copilot = build_copilot(interview) or {}
total = len(INTERVIEW_QUESTIONS)
state_key = f"ux_question_index_{audit_id}"
if state_key not in st.session_state:
    unanswered = [i for i, q in enumerate(INTERVIEW_QUESTIONS) if q.code not in answers]
    st.session_state[state_key] = unanswered[0] if unanswered else max(total - 1, 0)
index = max(0, min(int(st.session_state[state_key]), total - 1))
question = INTERVIEW_QUESTIONS[index]
saved = answers.get(question.code, {}) if isinstance(answers.get(question.code, {}), dict) else {}
progress = clamp(results.get("progress", 0))

render_page_header(
    title="Conversación",
    eyebrow="Analiza",
    description="Escucha, registra señales y profundiza en los patrones que aparecen.",
)
render_audit_header(audit)

status, answered, phase = st.columns([3, 1, 1], vertical_alignment="center")
status.progress(progress)
status.caption(f"{progress:.0%} de la conversación completada")
answered.metric("Respondidas", f"{results.get('answered', 0)}/{total}")
phase.metric("Pregunta", f"{index + 1}/{total}")
st.divider()

main, side = st.columns([3.2, 1.15], gap="large")
with main:
    label, counter = st.columns([3, 1])
    label.caption(f"{question.area.upper()} · {question.code}")
    counter.caption(f"PREGUNTA {index + 1} DE {total}")
    st.header(question.text)
    st.write("")

    options = ["Sin responder", "Sí", "Parcialmente", "No", "No aplica"]
    current = saved.get("answer", "Sin responder")
    if current not in options:
        current = "Sin responder"
    answer = st.radio(
        "Respuesta",
        options,
        index=options.index(current),
        horizontal=True,
        key=f"answer-{audit_id}-{question.code}",
    )
    comment = st.text_area(
        "Notas de la conversación",
        value=saved.get("comment", ""),
        placeholder="Decisiones, tensiones, ejemplos, excepciones y personas clave.",
        height=170,
        key=f"comment-{audit_id}-{question.code}",
    )
    with st.expander("Evidencias sugeridas"):
        for item in question.evidence_suggestions:
            st.write(f"• {item}")
        evidence_notes = st.text_area(
            "Evidencia disponible o pendiente",
            value=saved.get("evidence_notes", ""),
            height=110,
            key=f"evidence-{audit_id}-{question.code}",
        )

    previous, save_col, skip = st.columns([1, 2, 1])
    if previous.button("← Anterior", disabled=index == 0, use_container_width=True):
        st.session_state[state_key] = index - 1
        st.rerun()
    if save_col.button("Guardar y continuar", type="primary", use_container_width=True):
        if answer == "Sin responder":
            st.warning("Selecciona una respuesta.")
        else:
            save_answer(audit_id, question.code, answer, comment, evidence_notes)
            if index < total - 1:
                st.session_state[state_key] = index + 1
            st.rerun()
    if skip.button("Saltar →", disabled=index == total - 1, use_container_width=True):
        st.session_state[state_key] = index + 1
        st.rerun()

    with st.expander("Añadir observación metodológica"):
        observation = st.text_area("Observación", key=f"observation-{audit_id}-{question.code}")
        if st.button("Guardar observación", key=f"save-observation-{audit_id}-{question.code}"):
            try:
                add_observation(audit_id, observation, question.code)
                st.success("Observación registrada.")
            except ValueError as exc:
                st.warning(str(exc))

with side:
    st.caption("COPILOTO INCUBATOUR®")
    st.subheader("Lectura en vivo")
    patterns = copilot.get("patterns", [])
    if not patterns:
        st.caption("Las hipótesis aparecerán cuando existan suficientes señales relacionadas.")
    for pattern in patterns[:4]:
        st.markdown(f"**{pattern.get('name', 'Patrón')}**")
        confidence = clamp(pattern.get("confidence", 0) / 100)
        st.progress(confidence)
        st.caption(f"{confidence:.0%} · {pattern.get('signal_count', 0)} señales")
        st.caption(pattern.get("summary", ""))
        st.divider()

    st.subheader("Profundiza")
    followups = copilot.get("follow_up_questions", [])[:3]
    if not followups:
        st.caption("Sin preguntas adicionales por ahora.")
    for item in followups:
        st.write(f"• {item}")

    if results.get("answered", 0) >= 5 and st.button("Ver diagnóstico", use_container_width=True):
        st.switch_page("views/diagnosis.py")

render_footer()
