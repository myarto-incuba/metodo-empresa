from __future__ import annotations

import streamlit as st

from components.audit_ui import render_audit_header
from components.brand import render_footer, render_wordmark
from core.audit_facade import get_audit
from core.interview_repository import add_observation, load_interview, save_answer
from core.pattern_engine import build_copilot
from core.scoring_engine import calculate_results
from knowledge.interview_questions import INTERVIEW_QUESTIONS


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
copilot = build_copilot(interview)

blocks = list(dict.fromkeys(q.conversation_block for q in INTERVIEW_QUESTIONS))
if "ux_question_index" not in st.session_state:
    unanswered = [
        index for index, question in enumerate(INTERVIEW_QUESTIONS)
        if question.code not in answers
    ]
    st.session_state.ux_question_index = unanswered[0] if unanswered else 0

index = min(max(st.session_state.ux_question_index, 0), len(INTERVIEW_QUESTIONS) - 1)
question = INTERVIEW_QUESTIONS[index]
saved = answers.get(question.code, {})

st.markdown('<div class="inc-eyebrow">Conversación estratégica</div>', unsafe_allow_html=True)
st.title(question.conversation_block)
st.caption(
    f"Punto {index + 1} de {len(INTERVIEW_QUESTIONS)} · "
    f"{results['progress']:.0%} de la conversación completada"
)

main, side = st.columns([3.25, 1.35], gap="large")

with main:
    st.markdown('<div class="inc-question-shell">', unsafe_allow_html=True)
    st.markdown(
        f'<div class="inc-question-number">{question.area} · {question.code}</div>',
        unsafe_allow_html=True,
    )
    st.progress((index + 1) / len(INTERVIEW_QUESTIONS))
    st.markdown(
        f'<div class="inc-question">{question.text}</div>',
        unsafe_allow_html=True,
    )

    options = ["Sin responder", "Sí", "Parcialmente", "No", "No aplica"]
    selected = saved.get("answer", "Sin responder")
    answer = st.radio(
        "Respuesta",
        options,
        index=options.index(selected) if selected in options else 0,
        horizontal=True,
        label_visibility="collapsed",
        key=f"answer-{audit_id}-{question.code}",
    )

    comment = st.text_area(
        "Lo que escuchamos",
        value=saved.get("comment", ""),
        placeholder=(
            "Registra ejemplos, nombres, decisiones, tensiones, excepciones "
            "y frases relevantes de la conversación."
        ),
        height=145,
        key=f"comment-{audit_id}-{question.code}",
    )

    with st.expander("Evidencias que ayudarían a validar esta respuesta"):
        for item in question.evidence_suggestions:
            st.write(f"• {item}")
        evidence_notes = st.text_area(
            "Evidencia disponible, solicitada o pendiente",
            value=saved.get("evidence_notes", ""),
            key=f"evidence-{audit_id}-{question.code}",
        )

    c1, c2, c3 = st.columns([1, 2, 1])
    if c1.button("← Anterior", disabled=index == 0, use_container_width=True):
        st.session_state.ux_question_index -= 1
        st.rerun()

    if c2.button("Guardar y continuar →", type="primary", use_container_width=True):
        if answer == "Sin responder":
            st.warning("Selecciona una respuesta.")
        else:
            save_answer(audit_id, question.code, answer, comment, evidence_notes)
            if index < len(INTERVIEW_QUESTIONS) - 1:
                st.session_state.ux_question_index += 1
            st.rerun()

    if c3.button("Saltar", disabled=index == len(INTERVIEW_QUESTIONS) - 1, use_container_width=True):
        st.session_state.ux_question_index += 1
        st.rerun()

    with st.expander("Observación metodológica"):
        observation = st.text_area(
            "Observación",
            placeholder="La pregunta fue confusa, hace falta profundizar o debería ajustarse.",
            key=f"observation-{audit_id}-{question.code}",
        )
        if st.button("Guardar observación", key=f"save-observation-{audit_id}-{question.code}"):
            try:
                add_observation(audit_id, observation, question.code)
            except ValueError as exc:
                st.warning(str(exc))
            else:
                st.success("Observación registrada.")

    st.markdown("</div>", unsafe_allow_html=True)

with side:
    st.markdown("### Copiloto")

    if not copilot["patterns"]:
        with st.container(border=True):
            st.caption("ESCUCHANDO")
            st.write(
                "Las hipótesis aparecerán cuando existan suficientes respuestas relacionadas."
            )
    else:
        for pattern in copilot["patterns"]:
            with st.container(border=True):
                st.caption("HIPÓTESIS EN CONSTRUCCIÓN")
                st.markdown(f"#### {pattern['name']}")
                st.progress(pattern["confidence"] / 100)
                st.caption(
                    f"{pattern['confidence']}% de intensidad · "
                    f"{pattern['signal_count']} señales"
                )
                st.write(pattern["summary"])

    st.markdown("#### Preguntas para profundizar")
    if not copilot["follow_up_questions"]:
        st.caption("Aparecerán conforme avance la conversación.")
    for item in copilot["follow_up_questions"][:3]:
        st.write(f"• {item}")

    st.markdown("#### Evidencias sugeridas")
    if not copilot["evidence"]:
        st.caption("El sistema las sugerirá según los patrones detectados.")
    for item in copilot["evidence"][:5]:
        st.write(f"• {item}")

    if results["answered"] >= 5 and st.button("Ver lectura estratégica", use_container_width=True):
        st.switch_page("views/diagnosis.py")

render_footer()
