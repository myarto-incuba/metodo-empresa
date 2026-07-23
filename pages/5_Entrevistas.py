import streamlit as st

from core.database import (
    clear_interview_answers,
    get_interview_answers,
    init_db,
    save_interview_answer,
)
from core.interview_engine import (
    calculate_progress,
    get_next_question,
    group_answers_by_section,
    serialize_answer,
)
from core.selectors import audit_selector
from modules.evidence_engine import (
    build_document_request_list,
    build_evidence_plan,
)
from modules.question_bank import (
    DIRECTOR_INTERVIEW,
)
from modules.risk_engine import (
    generate_risk_signals,
    summarize_risks,
)
from utils.styles import apply_styles


st.set_page_config(
    page_title="Entrevistas",
    page_icon="🎙️",
    layout="wide",
)

apply_styles()
init_db()

st.title("Entrevistas inteligentes")
st.caption(
    "La entrevista adapta sus preguntas, interpreta "
    "las respuestas y genera un plan de validación."
)

audit_id = audit_selector()

interview = DIRECTOR_INTERVIEW
interview_code = interview["code"]

answers = get_interview_answers(
    audit_id,
    interview_code,
)

progress = calculate_progress(
    interview,
    answers,
)

signals = generate_risk_signals(
    interview,
    answers,
)

risk_summary = summarize_risks(
    signals
)

evidence_plan = build_evidence_plan(
    signals
)

document_request = build_document_request_list(
    signals
)

header_left, header_right = st.columns(
    [4, 1]
)

with header_left:
    st.subheader(interview["name"])
    st.write(interview["description"])

with header_right:
    st.metric(
        "Avance",
        f"{progress['percentage']:.0f}%",
        (
            f"{progress['completed']} "
            f"de {progress['total']}"
        ),
    )

st.progress(
    progress["percentage"] / 100
    if progress["percentage"]
    else 0
)

next_question = get_next_question(
    interview,
    answers,
)

if next_question:
    st.markdown("---")

    st.caption(
        next_question.get(
            "section",
            "Entrevista",
        ).upper()
    )

    st.markdown(
        f"## {next_question['text']}"
    )

    if next_question.get("help"):
        st.info(next_question["help"])

    question_type = next_question.get(
        "type"
    )

    question_id = next_question["id"]

    with st.form(
        f"question_form_{question_id}"
    ):
        answer = None

        if question_type == "text":
            answer = st.text_input(
                "Respuesta",
                label_visibility="collapsed",
            )

        elif question_type == "textarea":
            answer = st.text_area(
                "Respuesta",
                height=180,
                label_visibility="collapsed",
            )

        elif question_type == "select":
            options = next_question.get(
                "options",
                [],
            )

            answer = st.selectbox(
                "Respuesta",
                options,
                index=None,
                placeholder=(
                    "Selecciona una opción"
                ),
                label_visibility="collapsed",
            )

        elif question_type == "multiselect":
            answer = st.multiselect(
                "Respuesta",
                next_question.get(
                    "options",
                    [],
                ),
                label_visibility="collapsed",
            )

        elif question_type == "number":
            number_col, suffix_col = st.columns(
                [4, 1]
            )

            with number_col:
                answer = st.number_input(
                    "Respuesta",
                    min_value=float(
                        next_question.get(
                            "minimum",
                            0,
                        )
                    ),
                    max_value=float(
                        next_question.get(
                            "maximum",
                            1_000_000_000,
                        )
                    ),
                    step=float(
                        next_question.get(
                            "step",
                            1,
                        )
                    ),
                    label_visibility="collapsed",
                )

            with suffix_col:
                suffix = next_question.get(
                    "suffix",
                    "",
                )

                if suffix:
                    st.markdown(
                        f"### {suffix}"
                    )

        elif question_type == "boolean":
            answer = st.radio(
                "Respuesta",
                [
                    "Sí",
                    "No",
                ],
                index=None,
                horizontal=True,
                label_visibility="collapsed",
            )

        submitted = st.form_submit_button(
            "Guardar y continuar",
            type="primary",
            use_container_width=True,
        )

        if submitted:
            if answer is None:
                st.error(
                    "Selecciona o escribe "
                    "una respuesta."
                )

            elif (
                isinstance(answer, str)
                and not answer.strip()
            ):
                st.error(
                    "La respuesta no puede "
                    "quedar vacía."
                )

            elif (
                isinstance(answer, list)
                and not answer
            ):
                st.error(
                    "Selecciona al menos "
                    "una opción."
                )

            else:
                serialized = serialize_answer(
                    next_question,
                    answer,
                )

                save_interview_answer(
                    audit_id,
                    interview_code,
                    question_id,
                    serialized,
                )

                st.rerun()

else:
    st.success(
        "La entrevista inicial está completa."
    )

    st.markdown(
        """
        La información ya puede utilizarse para:

        - solicitar evidencia;
        - preparar entrevistas por área;
        - validar contradicciones;
        - convertir señales en hallazgos.
        """
    )

st.markdown("---")

if signals:
    metric_1, metric_2, metric_3, metric_4 = (
        st.columns(4)
    )

    with metric_1:
        st.metric(
            "Señales activas",
            risk_summary["total"],
        )

    with metric_2:
        st.metric(
            "Riesgos críticos",
            risk_summary["Crítico"],
        )

    with metric_3:
        st.metric(
            "Riesgos altos",
            risk_summary["Alto"],
        )

    with metric_4:
        st.metric(
            "Índice preliminar",
            f"{risk_summary['risk_index']:.0f}/100",
        )

summary_tab, signals_tab, evidence_tab, request_tab, controls_tab = (
    st.tabs(
        [
            "Respuestas",
            "Señales preliminares",
            "Plan de evidencias",
            "Solicitud documental",
            "Controles",
        ]
    )
)

with summary_tab:
    grouped_answers = group_answers_by_section(
        interview,
        answers,
    )

    if not grouped_answers:
        st.info(
            "Todavía no hay respuestas registradas."
        )

    else:
        for section, section_answers in (
            grouped_answers.items()
        ):
            with st.expander(
                section,
                expanded=False,
            ):
                for item in section_answers:
                    st.markdown(
                        f"**{item['question']}**"
                    )

                    st.write(
                        item["answer"]
                    )

                    st.markdown("---")

with signals_tab:
    if not signals:
        st.info(
            "No hay señales preliminares activas."
        )

    else:
        st.warning(
            "Estas señales no son hallazgos "
            "confirmados. Deben validarse con "
            "documentos, datos y entrevistas."
        )

        for signal in signals:
            with st.expander(
                (
                    f"{signal['level']} · "
                    f"{signal['title']}"
                ),
                expanded=(
                    signal["level"] == "Crítico"
                ),
            ):
                level = signal["level"]

                if level == "Crítico":
                    st.error(signal["message"])

                elif level == "Alto":
                    st.warning(signal["message"])

                else:
                    st.info(signal["message"])

                detail_1, detail_2 = st.columns(2)

                with detail_1:
                    st.markdown(
                        "**Respuesta que activó "
                        "la señal**"
                    )
                    st.write(signal["answer"])

                    st.markdown(
                        "**Área de origen**"
                    )
                    st.write(signal["section"])

                    st.markdown(
                        "**Módulos relacionados**"
                    )

                    for module in signal[
                        "related_modules"
                    ]:
                        st.write(f"- {module}")

                with detail_2:
                    st.markdown(
                        "**Confianza inicial**"
                    )
                    st.progress(
                        signal[
                            "confidence_percentage"
                        ] / 100
                    )
                    st.write(
                        (
                            f"{signal['confidence_percentage']}%"
                        )
                    )

                    st.markdown(
                        "**Estado de validación**"
                    )
                    st.write(
                        signal[
                            "validation_status"
                        ]
                    )

                    st.markdown(
                        "**Hipótesis de causa raíz**"
                    )
                    st.write(
                        signal[
                            "possible_root_cause"
                        ]
                    )

                consequences = signal.get(
                    "potential_consequences",
                    [],
                )

                if consequences:
                    st.markdown(
                        "**Consecuencias potenciales**"
                    )

                    for consequence in consequences:
                        st.write(
                            f"- {consequence}"
                        )

with evidence_tab:
    if not evidence_plan:
        st.info(
            "El plan aparecerá cuando existan "
            "señales preliminares."
        )

    else:
        st.markdown(
            """
            Cada bloque indica cómo debe validarse una
            hipótesis antes de convertirla en hallazgo.
            """
        )

        for item in evidence_plan:
            requirements = item[
                "evidence_requirements"
            ]

            with st.expander(
                (
                    f"{item['level']} · "
                    f"{item['title']}"
                ),
                expanded=(
                    item["level"] == "Crítico"
                ),
            ):
                st.markdown(
                    "### Documentos requeridos"
                )

                for document in requirements[
                    "documents"
                ]:
                    st.checkbox(
                        document,
                        key=(
                            f"document_"
                            f"{item['signal_code']}_"
                            f"{document}"
                        ),
                        disabled=True,
                    )

                st.markdown(
                    "### Datos a analizar"
                )

                for data_item in requirements[
                    "data"
                ]:
                    st.write(
                        f"- {data_item}"
                    )

                st.markdown(
                    "### Personas a entrevistar"
                )

                for interviewee in requirements[
                    "interviews"
                ]:
                    st.write(
                        f"- {interviewee}"
                    )

                st.markdown(
                    "### Pruebas de validación"
                )

                for validation in requirements[
                    "validations"
                ]:
                    st.write(
                        f"- {validation}"
                    )

with request_tab:
    if not document_request:
        st.info(
            "La solicitud documental se generará "
            "cuando existan señales activas."
        )

    else:
        st.markdown(
            """
            ## Solicitud documental preliminar

            La lista está consolidada: un mismo documento
            puede servir para validar varios riesgos.
            """
        )

        for index, item in enumerate(
            document_request,
            start=1,
        ):
            st.markdown(
                (
                    f"### {index}. "
                    f"{item['document']}"
                )
            )

            st.caption(
                (
                    "Prioridad relacionada: "
                    f"{item['highest_risk']}"
                )
            )

            st.markdown(
                "**Se utilizará para validar:**"
            )

            for related_signal in item[
                "related_signals"
            ]:
                st.write(
                    f"- {related_signal}"
                )

            st.markdown("---")

with controls_tab:
    st.warning(
        "Reiniciar la entrevista eliminará "
        "todas las respuestas registradas "
        "para esta auditoría."
    )

    confirmation = st.checkbox(
        (
            "Confirmo que deseo eliminar "
            "las respuestas."
        )
    )

    if st.button(
        "Reiniciar entrevista",
        disabled=not confirmation,
    ):
        clear_interview_answers(
            audit_id,
            interview_code,
        )

        st.success(
            "La entrevista fue reiniciada."
        )

        st.rerun()