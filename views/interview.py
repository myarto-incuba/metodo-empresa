from __future__ import annotations

import streamlit as st

from components.audit_ui import render_audit_header
from components.brand import render_footer, render_wordmark
from core.audit_facade import get_audit
from core.interview_repository import add_observation, load_interview, save_answer
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

blocks = list(dict.fromkeys(q.conversation_block for q in INTERVIEW_QUESTIONS))
block_counts = {
    block: sum(1 for q in INTERVIEW_QUESTIONS if q.conversation_block == block)
    for block in blocks
}
block_answered = {
    block: sum(
        1 for q in INTERVIEW_QUESTIONS
        if q.conversation_block == block and q.code in answers
    )
    for block in blocks
}

if "ux_question_index" not in st.session_state:
    unanswered = [
        index for index, question in enumerate(INTERVIEW_QUESTIONS)
        if question.code not in answers
    ]
    st.session_state.ux_question_index = unanswered[0] if unanswered else 0

index = min(max(st.session_state.ux_question_index, 0), len(INTERVIEW_QUESTIONS) - 1)
question = INTERVIEW_QUESTIONS[index]
saved = answers.get(question.code, {})
current_block_index = blocks.index(question.conversation_block)

st.markdown(
    f"""
    <section class="inc-panel" style="padding:1rem 1.2rem;margin-bottom:1rem;">
        <div class="inc-card-kicker">CONVERSACIÓN ESTRATÉGICA</div>
        <div style="display:flex;justify-content:space-between;gap:1rem;align-items:end;">
            <div>
                <div style="font-size:1.65rem;font-weight:900;letter-spacing:-.04em;">
                    {question.conversation_block}
                </div>
                <div class="inc-meta">
                    Bloque {current_block_index + 1} de {len(blocks)} ·
                    {block_answered[question.conversation_block]}/{block_counts[question.conversation_block]} respondidas
                </div>
            </div>
            <div class="inc-badge">{results['progress']:.0%} COMPLETADO</div>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

main, live = st.columns([3.4, 1.15], gap="large")

with main:
    st.markdown('<div class="inc-question-shell">', unsafe_allow_html=True)
    st.markdown(
        f'<div class="inc-question-number">'
        f'Punto de conversación {index + 1} de {len(INTERVIEW_QUESTIONS)}</div>',
        unsafe_allow_html=True,
    )
    st.progress((index + 1) / len(INTERVIEW_QUESTIONS))
    st.markdown(
        '<div class="inc-conversation-title">Profundicemos en este tema.</div>',
        unsafe_allow_html=True,
    )
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
        key=f"ux-answer-{audit_id}-{question.code}",
        label_visibility="collapsed",
    )

    comment = st.text_area(
        "Notas de la conversación",
        value=saved.get("comment", ""),
        placeholder="Escribe ejemplos, tensiones, decisiones, responsables o contexto relevante.",
        key=f"ux-comment-{audit_id}-{question.code}",
        height=130,
    )

    with st.expander("Evidencias y señales para validar"):
        for evidence in question.evidence_suggestions:
            st.write(f"• {evidence}")
        evidence_notes = st.text_area(
            "Evidencia disponible o pendiente",
            value=saved.get("evidence_notes", ""),
            key=f"ux-evidence-{audit_id}-{question.code}",
        )

    nav_1, nav_2, nav_3 = st.columns([1, 2, 1])
    if nav_1.button("← Anterior", disabled=index == 0, use_container_width=True):
        st.session_state.ux_question_index -= 1
        st.rerun()

    if nav_2.button(
        "Guardar y continuar →",
        type="primary",
        use_container_width=True,
        key=f"ux-save-{audit_id}-{question.code}",
    ):
        if answer == "Sin responder":
            st.warning("Selecciona una respuesta.")
        else:
            save_answer(audit_id, question.code, answer, comment, evidence_notes)
            if index < len(INTERVIEW_QUESTIONS) - 1:
                st.session_state.ux_question_index += 1
            st.rerun()

    if nav_3.button(
        "Saltar",
        disabled=index == len(INTERVIEW_QUESTIONS) - 1,
        use_container_width=True,
    ):
        st.session_state.ux_question_index += 1
        st.rerun()

    with st.expander("Observación sobre la metodología"):
        note = st.text_area(
            "Observación",
            placeholder="La pregunta fue confusa, sobró o hace falta otra.",
            key=f"ux-note-{audit_id}-{question.code}",
        )
        if st.button("Guardar observación", key=f"ux-note-save-{audit_id}-{question.code}"):
            try:
                add_observation(audit_id, note, question.code)
            except ValueError as exc:
                st.warning(str(exc))
            else:
                st.success("Observación registrada.")

    st.markdown("</div>", unsafe_allow_html=True)

with live:
    st.markdown('<div class="inc-section-title">Copiloto</div>', unsafe_allow_html=True)

    with st.container(border=True):
        st.caption("LECTURA PRELIMINAR")
        st.metric("Madurez", f"{results['overall_score']}%")
        st.metric("Conversación", f"{results['progress']:.0%}")

    st.markdown("#### Señales por bloque")
    for block in blocks:
        value = block_answered[block] / block_counts[block]
        st.caption(f"{block} · {block_answered[block]}/{block_counts[block]}")
        st.progress(value)

    st.markdown("#### Patrones detectados")
    hypotheses = results.get("hypotheses", [])
    if not hypotheses:
        st.caption("Aparecerán conforme avance la conversación.")
    for hypothesis in hypotheses[:4]:
        with st.container(border=True):
            st.caption("HIPÓTESIS")
            st.write(f"**{hypothesis['name']}**")
            st.progress(hypothesis["confidence"] / 100)
            st.caption(f"{hypothesis['confidence']}% de intensidad")

    weak_areas = sorted(
        results.get("area_scores", {}).items(),
        key=lambda item: item[1]
    )[:2]
    if weak_areas:
        st.markdown("#### Áreas a profundizar")
        for area, score in weak_areas:
            st.write(f"• **{area}** · {score}%")

render_footer()
