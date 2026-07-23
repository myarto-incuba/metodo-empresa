from __future__ import annotations

import streamlit as st

from core.audit_repository import get_audit, list_audits, update_audit_status
from core.interview_repository import add_observation, load_interview, save_answer
from knowledge.interview_questions import INTERVIEW_QUESTIONS


st.set_page_config(
    page_title="Entrevista | Método Empresa",
    page_icon="💬",
    layout="wide",
)

st.title("Conversación estratégica")
st.caption("Entrevista guiada para la auditoría empresarial.")

audits = list_audits()
if not audits:
    st.warning("Primero crea una auditoría en la página Auditorías.")
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
st.session_state.active_audit_id = audit_id
audit = get_audit(audit_id)
interview = load_interview(audit_id)
answers = interview.get("answers", {})

if audit is None:
    st.error("No fue posible cargar la auditoría.")
    st.stop()

if audit.status == "Creada":
    update_audit_status(audit_id, "En proceso")

answered_count = len(answers)
progress = answered_count / len(INTERVIEW_QUESTIONS)

header_1, header_2, header_3 = st.columns([2, 1, 1])
header_1.markdown(f"## {audit.company_name}")
header_1.caption(f"{audit.sector or 'Sector no indicado'} · Auditor: {audit.auditor_name}")
header_2.metric("Respondidas", f"{answered_count}/{len(INTERVIEW_QUESTIONS)}")
header_3.metric("Avance", f"{progress:.0%}")
st.progress(progress)

if "question_index" not in st.session_state:
    st.session_state.question_index = 0

st.session_state.question_index = min(
    max(st.session_state.question_index, 0),
    len(INTERVIEW_QUESTIONS) - 1,
)
question = INTERVIEW_QUESTIONS[st.session_state.question_index]
saved = answers.get(question.code, {})

st.caption(
    f"{question.conversation_block} · {question.area} · "
    f"Pregunta {st.session_state.question_index + 1} de {len(INTERVIEW_QUESTIONS)}"
)

with st.container(border=True):
    st.markdown(f"### {question.text}")

    response_options = ["Sin responder", "Sí", "Parcialmente", "No", "No aplica"]
    saved_answer = saved.get("answer", "Sin responder")
    response_index = (
        response_options.index(saved_answer)
        if saved_answer in response_options
        else 0
    )

    answer = st.radio(
        "Respuesta",
        response_options,
        index=response_index,
        horizontal=True,
        key=f"answer-{audit_id}-{question.code}",
    )

    comment = st.text_area(
        "Comentarios del auditor",
        value=saved.get("comment", ""),
        placeholder="Contexto, ejemplos, responsables o situaciones relevantes.",
        key=f"comment-{audit_id}-{question.code}",
    )

    with st.expander("Evidencias sugeridas"):
        for item in question.evidence_suggestions:
            st.write(f"• {item}")

        evidence_notes = st.text_area(
            "Evidencia disponible o pendiente",
            value=saved.get("evidence_notes", ""),
            placeholder="Ej. Solicitar presupuesto anual durante la visita presencial.",
            key=f"evidence-{audit_id}-{question.code}",
        )

    save_col, status_col = st.columns([1, 3])
    if save_col.button(
        "Guardar respuesta",
        type="primary",
        use_container_width=True,
        key=f"save-{audit_id}-{question.code}",
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
            st.success("Respuesta guardada.")
            st.rerun()

    if saved:
        status_col.success("Esta pregunta ya tiene una respuesta guardada.")

nav_left, nav_center, nav_right = st.columns([1, 2, 1])

if nav_left.button(
    "← Anterior",
    disabled=st.session_state.question_index == 0,
    use_container_width=True,
):
    st.session_state.question_index -= 1
    st.rerun()

nav_center.caption(
    "Guarda la respuesta antes de avanzar para conservar comentarios y evidencias."
)

if nav_right.button(
    "Siguiente →",
    disabled=st.session_state.question_index == len(INTERVIEW_QUESTIONS) - 1,
    use_container_width=True,
):
    st.session_state.question_index += 1
    st.rerun()

st.divider()

with st.expander("💡 Registrar observación para mejorar Método Empresa"):
    observation = st.text_area(
        "Observación",
        placeholder="Ej. Esta pregunta fue confusa o hace falta preguntar por socios.",
        key=f"observation-{audit_id}",
    )
    if st.button("Guardar observación", key=f"save-observation-{audit_id}"):
        try:
            add_observation(audit_id, observation, question.code)
        except ValueError as exc:
            st.warning(str(exc))
        else:
            st.success("Observación registrada.")
