"""
Motor general de riesgos.

Convierte respuestas de entrevistas en señales preliminares
estructuradas. Las señales aún no son hallazgos confirmados:
deben validarse con documentos, datos u otras entrevistas.
"""

from typing import Any

from core.interview_engine import (
    get_visible_questions,
    is_answered,
    parse_answer,
)


RISK_PRIORITY = {
    "Crítico": 1,
    "Alto": 2,
    "Medio": 3,
    "Bajo": 4,
}


RISK_WEIGHTS = {
    "Crítico": 100,
    "Alto": 75,
    "Medio": 50,
    "Bajo": 25,
}


def rule_matches(
    rule: dict,
    answer: Any,
) -> bool:
    """
    Determina si una respuesta activa una regla de riesgo.
    """
    operator = rule.get("operator")

    if operator == "equals":
        return answer == rule.get("value")

    if operator == "not_equals":
        return answer != rule.get("value")

    if operator == "in":
        return answer in rule.get("values", [])

    if operator == "not_in":
        return answer not in rule.get("values", [])

    if operator == "greater_than":
        if answer is None:
            return False

        try:
            return float(answer) > float(
                rule.get("value", 0)
            )
        except (TypeError, ValueError):
            return False

    if operator == "greater_than_or_equal":
        if answer is None:
            return False

        try:
            return float(answer) >= float(
                rule.get("value", 0)
            )
        except (TypeError, ValueError):
            return False

    if operator == "less_than":
        if answer is None:
            return False

        try:
            return float(answer) < float(
                rule.get("value", 0)
            )
        except (TypeError, ValueError):
            return False

    if operator == "less_than_or_equal":
        if answer is None:
            return False

        try:
            return float(answer) <= float(
                rule.get("value", 0)
            )
        except (TypeError, ValueError):
            return False

    if operator == "between":
        if answer is None:
            return False

        try:
            minimum = float(rule.get("minimum", 0))
            maximum = float(rule.get("maximum", 0))
            numeric_answer = float(answer)

            return minimum <= numeric_answer <= maximum
        except (TypeError, ValueError):
            return False

    if operator == "not_empty":
        return answer not in (
            None,
            "",
            [],
        )

    if operator == "empty":
        return answer in (
            None,
            "",
            [],
        )

    if operator == "contains":
        if answer is None:
            return False

        return str(
            rule.get("value", "")
        ).lower() in str(answer).lower()

    return False


def calculate_initial_confidence(
    rule: dict,
    question: dict,
) -> int:
    """
    Calcula la confianza inicial de una señal.

    Una respuesta declarada por una sola persona no debe
    considerarse evidencia definitiva.
    """
    base_confidence = rule.get(
        "initial_confidence",
        55,
    )

    if question.get("type") == "number":
        base_confidence += 5

    if rule.get("operator") in {
        "greater_than",
        "greater_than_or_equal",
        "less_than",
        "less_than_or_equal",
        "between",
    }:
        base_confidence += 5

    return max(
        0,
        min(int(base_confidence), 85),
    )


def determine_validation_status(
    signal: dict,
) -> str:
    """
    Define el estado inicial de validación.
    """
    confidence = signal.get(
        "confidence_percentage",
        0,
    )

    if confidence >= 80:
        return "Requiere confirmación documental"

    if confidence >= 60:
        return "Requiere validación cruzada"

    return "Hipótesis inicial"


def build_signal(
    question: dict,
    rule: dict,
    answer: Any,
    interview: dict,
) -> dict:
    """
    Construye una señal de riesgo estructurada.
    """
    level = rule.get(
        "level",
        "Medio",
    )

    signal = {
        "signal_code": (
            f"{interview.get('code', 'interview')}"
            f"__{question['id']}"
        ),
        "interview_code": interview.get("code"),
        "interview_name": interview.get("name"),
        "question_id": question["id"],
        "question": question.get("text", ""),
        "section": question.get(
            "section",
            "Sin sección",
        ),
        "level": level,
        "risk_weight": RISK_WEIGHTS.get(
            level,
            50,
        ),
        "title": rule.get(
            "title",
            "Señal preliminar",
        ),
        "message": rule.get(
            "message",
            "",
        ),
        "answer": answer,
        "possible_root_cause": rule.get(
            "possible_root_cause",
            (
                "La empresa no cuenta con un método "
                "formal, actualizado o suficientemente "
                "controlado para esta actividad."
            ),
        ),
        "potential_consequences": rule.get(
            "potential_consequences",
            [],
        ),
        "related_modules": rule.get(
            "related_modules",
            [
                question.get(
                    "section",
                    "Sin sección",
                )
            ],
        ),
        "confidence_percentage": (
            calculate_initial_confidence(
                rule,
                question,
            )
        ),
        "source_type": "Entrevista",
        "source_description": (
            f"Respuesta registrada en "
            f"{interview.get('name', 'entrevista')}."
        ),
        "validated": False,
    }

    signal["validation_status"] = (
        determine_validation_status(signal)
    )

    return signal


def generate_risk_signals(
    interview: dict,
    answers: dict,
) -> list[dict]:
    """
    Evalúa todas las respuestas visibles y genera señales
    preliminares de riesgo.
    """
    signals = []

    visible_questions = get_visible_questions(
        interview,
        answers,
    )

    for question in visible_questions:
        raw_answer = answers.get(
            question["id"]
        )

        if not is_answered(
            question,
            raw_answer,
        ):
            continue

        answer = parse_answer(
            question,
            raw_answer,
        )

        for rule in question.get(
            "risk_rules",
            [],
        ):
            if not rule_matches(
                rule,
                answer,
            ):
                continue

            signals.append(
                build_signal(
                    question=question,
                    rule=rule,
                    answer=answer,
                    interview=interview,
                )
            )

    return sorted(
        signals,
        key=lambda signal: (
            RISK_PRIORITY.get(
                signal["level"],
                99,
            ),
            -signal.get(
                "confidence_percentage",
                0,
            ),
            signal.get(
                "section",
                "",
            ),
        ),
    )


def summarize_risks(
    signals: list[dict],
) -> dict:
    """
    Genera un resumen ejecutivo de las señales activas.
    """
    summary = {
        "total": len(signals),
        "Crítico": 0,
        "Alto": 0,
        "Medio": 0,
        "Bajo": 0,
        "average_confidence": 0,
        "risk_index": 0,
    }

    if not signals:
        return summary

    total_confidence = 0
    total_weight = 0

    for signal in signals:
        level = signal.get(
            "level",
            "Medio",
        )

        if level in summary:
            summary[level] += 1

        total_confidence += signal.get(
            "confidence_percentage",
            0,
        )

        total_weight += signal.get(
            "risk_weight",
            0,
        )

    summary["average_confidence"] = round(
        total_confidence / len(signals),
        1,
    )

    maximum_weight = len(signals) * 100

    summary["risk_index"] = round(
        total_weight / maximum_weight * 100,
        1,
    ) if maximum_weight else 0

    return summary


def group_signals_by_section(
    signals: list[dict],
) -> dict[str, list[dict]]:
    """
    Agrupa las señales por sección o área.
    """
    grouped = {}

    for signal in signals:
        section = signal.get(
            "section",
            "Sin sección",
        )

        grouped.setdefault(
            section,
            [],
        ).append(signal)

    return grouped