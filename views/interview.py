from __future__ import annotations

import streamlit as st

from components.audit_ui import render_audit_header
from core.audit_facade import get_audit
from core.interview_repository import add_observation, load_interview, save_answer
from core.scoring_engine import calculate_results
from knowledge.interview_questions import INTERVIEW_QUESTIONS


audit_id = st.session_state.get("active_audit_id")
audit = get_audit(audit_id) if audit_id else None
if audit is None:
    st.warning("Selecciona una auditoría desde Auditorías.")
    st.stop()

render_audit_header(audit)
st.title("Entrevista")
st.caption("Una pregunta a la vez. Guarda y continúa.")

interview = load_interview(audit_id)
answers = interview.get("answers", {})
results = calculate_results(interview)

if "ux_question_index" not in st.session_state:
    unanswered = [
        index
        for index, question in enumerate(INTERVIEW_QUESTIONS)
        if question.code not in answers
    ]
    st.session_state.ux_question_index = unanswered[0] if unanswered else 0

index = min(max(st.session_state.ux_question_index, 0), len(INTERVIEW_QUESTIONS) - 1)
question = INTERVIEW_QUESTIONS[index]
saved = answers.get(question.code, {})

main, live = st.columns([3, 1.2], gap="large")

with main:
    st.caption(
        f"{question.conversation_block} · {question.area} · "
        f"Pregunta {index + 1} de {len(INTERVIEW_QUESTIONS)}"
    )
    st.progress((index + 1) / len(INTERVIEW_QUESTIONS))

    with st.container(border=True):
        st.markdown(f"## {question.text}")

        options = ["Sin responder", "Sí", "Parcialmente", "No", "No aplica"]
        selected = saved.get("answer", "Sin responder")
        answer = st.radio(
            "Respuesta",
            options,
            index=options.index(selected) if selected in options else 0,
            horizontal=True,
            key=f"ux-answer-{audit_id}-{question.code}",
        )
        comment = st.text_area(
            "Comentario del auditor",
            value=saved.get("comment", ""),
            placeholder="Contexto, ejemplos, responsables o situaciones relevantes.",
            key=f"ux-comment-{audit_id}-{question.code}",
        )
        with st.expander("Evidencias sugeridas"):
            for evidence in question.evidence_suggestions:
                st.write(f"• {evidence}")
            evidence_notes = st.text_area(
                "Evidencia disponible o pendiente",
                value=saved.get("evidence_notes", ""),
                key=f"ux-evidence-{audit_id}-{question.code}",
            )

        if st.button(
            "Guardar y continuar →",
            type="primary",
            use_container_width=True,
            key=f"ux-save-{audit_id}-{question.code}",
        ):
            if answer == "Sin responder":
                st.warning("Selecciona una respuesta.")
            else:
                save_answer(
                    audit_id,
                    question.code,
                    answer,
                    comment,
                    evidence_notes,
                )
                if index < len(INTERVIEW_QUESTIONS) - 1:
                    st.session_state.ux_question_index += 1
                st.rerun()

    back, position, next_col = st.columns([1, 2, 1])
    if back.button("← Anterior", disabled=index == 0, use_container_width=True):
        st.session_state.ux_question_index -= 1
        st.rerun()
    position.caption(f"{len(answers)} respuestas guardadas")
    if next_col.button(
        "Saltar →",
        disabled=index == len(INTERVIEW_QUESTIONS) - 1,
        use_container_width=True,
    ):
        st.session_state.ux_question_index += 1
        st.rerun()

    with st.expander("💡 Registrar observación sobre el producto"):
        note = st.text_area(
            "Observación",
            placeholder="Esta pregunta fue confusa, sobró o hace falta otra.",
            key=f"ux-note-{audit_id}-{question.code}",
        )
        if st.button("Guardar observación", key=f"ux-note-save-{audit_id}-{question.code}"):
            try:
                add_observation(audit_id, note, question.code)
            except ValueError as exc:
                st.warning(str(exc))
            else:
                st.success("Observación registrada.")

with live:
    st.markdown("### Lectura en vivo")
    st.metric("Madurez preliminar", f"{results['overall_score']}%")
    st.metric("Avance", f"{results['progress']:.0%}")

    st.markdown("#### Hipótesis")
    if not results["hypotheses"]:
        st.caption("Aparecerán al guardar respuestas.")
    for hypothesis in results["hypotheses"][:4]:
        with st.container(border=True):
            st.write(f"**{hypothesis['name']}**")
            st.progress(hypothesis["confidence"] / 100)
            st.caption(f"{hypothesis['confidence']}%")
