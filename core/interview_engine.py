from typing import Any


def parse_answer(question: dict, raw_answer: str | None) -> Any:
    """
    Convierte la respuesta almacenada en texto al tipo necesario
    para evaluaciones y condiciones.
    """
    if raw_answer is None:
        return None

    question_type = question.get("type")

    if question_type == "number":
        try:
            return float(raw_answer)
        except (TypeError, ValueError):
            return None

    if question_type == "multiselect":
        if not raw_answer:
            return []
        return [
            item.strip()
            for item in raw_answer.split("|||")
            if item.strip()
        ]

    return raw_answer


def serialize_answer(question: dict, answer: Any) -> str:
    """
    Convierte una respuesta a texto antes de guardarla en SQLite.
    """
    if answer is None:
        return ""

    if question.get("type") == "multiselect":
        return "|||".join(answer)

    if question.get("type") == "number":
        return str(float(answer))

    return str(answer)


def is_answered(question: dict, raw_answer: str | None) -> bool:
    """
    Determina si una pregunta tiene una respuesta válida.
    """
    if raw_answer is None:
        return False

    question_type = question.get("type")

    if question_type == "number":
        try:
            float(raw_answer)
            return True
        except (TypeError, ValueError):
            return False

    if question_type == "multiselect":
        return bool(raw_answer.strip())

    return bool(str(raw_answer).strip())


def evaluate_condition(
    condition: dict | None,
    answers: dict,
    questions_by_id: dict,
) -> bool:
    """
    Evalúa si una pregunta debe mostrarse.
    """
    if not condition:
        return True

    dependency_id = condition.get("question_id")
    dependency_question = questions_by_id.get(dependency_id)

    if not dependency_question:
        return False

    raw_answer = answers.get(dependency_id)
    answer = parse_answer(dependency_question, raw_answer)

    operator = condition.get("operator")

    if operator == "equals":
        return answer == condition.get("value")

    if operator == "not_equals":
        return answer != condition.get("value")

    if operator == "in":
        return answer in condition.get("values", [])

    if operator == "not_in":
        return answer not in condition.get("values", [])

    if operator == "greater_than":
        if answer is None:
            return False
        return answer > condition.get("value", 0)

    if operator == "less_than":
        if answer is None:
            return False
        return answer < condition.get("value", 0)

    if operator == "not_empty":
        return answer not in (None, "", [])

    return True


def get_visible_questions(interview: dict, answers: dict) -> list[dict]:
    """
    Devuelve únicamente las preguntas visibles según las respuestas actuales.
    """
    questions = interview.get("questions", [])
    questions_by_id = {
        question["id"]: question
        for question in questions
    }

    return [
        question
        for question in questions
        if evaluate_condition(
            question.get("condition"),
            answers,
            questions_by_id,
        )
    ]


def get_next_question(
    interview: dict,
    answers: dict,
) -> dict | None:
    """
    Encuentra la primera pregunta visible que aún no ha sido respondida.
    """
    visible_questions = get_visible_questions(interview, answers)

    for question in visible_questions:
        if not is_answered(
            question,
            answers.get(question["id"]),
        ):
            return question

    return None


def calculate_progress(
    interview: dict,
    answers: dict,
) -> dict:
    """
    Calcula el avance considerando solo preguntas actualmente visibles.
    """
    visible_questions = get_visible_questions(interview, answers)

    required_questions = [
        question
        for question in visible_questions
        if question.get("required", False)
    ]

    answered_questions = [
        question
        for question in required_questions
        if is_answered(
            question,
            answers.get(question["id"]),
        )
    ]

    total = len(required_questions)
    completed = len(answered_questions)

    percentage = round(
        completed / total * 100,
        1,
    ) if total else 0

    return {
        "total": total,
        "completed": completed,
        "percentage": percentage,
    }


def _rule_matches(
    rule: dict,
    answer: Any,
) -> bool:
    operator = rule.get("operator")

    if operator == "equals":
        return answer == rule.get("value")

    if operator == "in":
        return answer in rule.get("values", [])

    if operator == "greater_than":
        if answer is None:
            return False
        return answer > rule.get("value", 0)

    if operator == "less_than":
        if answer is None:
            return False
        return answer < rule.get("value", 0)

    if operator == "not_empty":
        return answer not in (None, "", [])

    return False


def generate_preliminary_signals(
    interview: dict,
    answers: dict,
) -> list[dict]:
    """
    Evalúa las reglas de riesgo del banco de preguntas.

    Estas señales no son todavía hallazgos confirmados.
    Deben validarse con entrevistas, documentos o datos.
    """
    signals = []

    for question in get_visible_questions(interview, answers):
        raw_answer = answers.get(question["id"])

        if not is_answered(question, raw_answer):
            continue

        answer = parse_answer(question, raw_answer)

        for rule in question.get("risk_rules", []):
            if _rule_matches(rule, answer):
                signals.append(
                    {
                        "question_id": question["id"],
                        "section": question.get(
                            "section",
                            "Sin sección",
                        ),
                        "level": rule.get("level", "Medio"),
                        "title": rule.get(
                            "title",
                            "Señal preliminar",
                        ),
                        "message": rule.get(
                            "message",
                            "",
                        ),
                        "answer": answer,
                    }
                )

    priority = {
        "Crítico": 1,
        "Alto": 2,
        "Medio": 3,
        "Bajo": 4,
    }

    return sorted(
        signals,
        key=lambda signal: priority.get(
            signal["level"],
            99,
        ),
    )


def group_answers_by_section(
    interview: dict,
    answers: dict,
) -> dict[str, list[dict]]:
    """
    Organiza las respuestas para mostrarlas en el resumen.
    """
    grouped = {}

    for question in get_visible_questions(interview, answers):
        raw_answer = answers.get(question["id"])

        if not is_answered(question, raw_answer):
            continue

        section = question.get("section", "Sin sección")

        grouped.setdefault(section, []).append(
            {
                "question": question["text"],
                "answer": parse_answer(
                    question,
                    raw_answer,
                ),
            }
        )

    return grouped