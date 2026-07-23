"""Motor narrativo explicable de Método Empresa."""

from __future__ import annotations

from typing import Any

from core.pattern_engine import detect_patterns
from core.scoring_engine import calculate_results


AREA_LABELS = {
    "Dirección": "la dirección y el gobierno del negocio",
    "Finanzas": "el control financiero",
    "Comercial": "la gestión comercial",
    "Operaciones": "la operación",
    "Personas": "la gestión del equipo",
}


def build_strategic_reading(
    interview: dict[str, Any],
    *,
    company_name: str = "La empresa",
) -> dict[str, Any]:
    results = calculate_results(interview)
    patterns = detect_patterns(interview)
    area_scores = results.get("area_scores", {})

    strongest = sorted(area_scores.items(), key=lambda item: item[1], reverse=True)[:2]
    weakest = sorted(area_scores.items(), key=lambda item: item[1])[:2]

    opening = _opening(company_name, results)
    strengths_text = _strengths_sentence(strongest)
    tension_text = _tension_sentence(patterns, weakest)
    priority_text = _priority_sentence(patterns, weakest)
    closing = _closing(results, patterns)

    paragraphs = [
        text for text in (opening, strengths_text, tension_text, priority_text, closing)
        if text
    ]

    risks = [
        {
            "name": pattern["name"],
            "risk": pattern["risk"],
            "confidence": pattern["confidence"],
        }
        for pattern in patterns[:4]
    ]

    priorities = []
    for pattern in patterns[:4]:
        priorities.append(
            {
                "name": pattern["name"],
                "reason": pattern["summary"],
                "confidence": pattern["confidence"],
            }
        )

    return {
        "executive_summary": "\n\n".join(paragraphs),
        "headline": _headline(patterns, weakest),
        "maturity": results.get("maturity", "Inicial"),
        "overall_score": results.get("overall_score", 0),
        "progress": results.get("progress", 0),
        "strongest_areas": strongest,
        "weakest_areas": weakest,
        "patterns": patterns,
        "risks": risks,
        "priorities": priorities,
        "roadmap": build_roadmap(patterns),
        "validation_note": (
            "Lectura preliminar construida con las respuestas disponibles. "
            "Debe validarse con evidencias, observación y conversación con las personas responsables."
        ),
    }


def build_roadmap(patterns: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()

    for pattern in patterns[:5]:
        for period, actions in pattern["roadmap"].items():
            for action in actions:
                if action in seen:
                    continue
                seen.add(action)
                rows.append(
                    {
                        "period": period,
                        "action": action,
                        "priority": "Alta" if pattern["confidence"] >= 60 else "Media",
                        "owner": "",
                        "deadline": period,
                        "status": "Pendiente",
                        "source_pattern": pattern["name"],
                        "reason": pattern["risk"],
                    }
                )
    return rows[:12]


def _opening(company_name: str, results: dict[str, Any]) -> str:
    score = results.get("overall_score", 0)
    maturity = results.get("maturity", "Inicial").lower()
    if score >= 70:
        return (
            f"{company_name} muestra una estructura de gestión {maturity}, "
            "con capacidades que ya permiten ordenar y sostener parte de su crecimiento."
        )
    if score >= 50:
        return (
            f"{company_name} se encuentra en una etapa {maturity}: cuenta con prácticas valiosas, "
            "pero todavía conviven con mecanismos informales y una ejecución dependiente de personas."
        )
    return (
        f"{company_name} presenta una etapa de gestión {maturity}. "
        "La prioridad no debe ser añadir complejidad, sino instalar controles básicos y una cadencia de dirección."
    )


def _strengths_sentence(strongest: list[tuple[str, int]]) -> str:
    if not strongest:
        return ""
    labels = [f"{AREA_LABELS.get(area, area.lower())} ({score}%)" for area, score in strongest]
    return (
        "Las bases comparativamente más sólidas aparecen en "
        + _join_spanish(labels)
        + ". Estas capacidades pueden utilizarse como punto de apoyo para el cambio."
    )


def _tension_sentence(
    patterns: list[dict[str, Any]],
    weakest: list[tuple[str, int]],
) -> str:
    if patterns:
        names = [f"{pattern['name'].lower()} ({pattern['confidence']}%)" for pattern in patterns[:3]]
        return (
            "La conversación revela tres tensiones principales: "
            + _join_spanish(names)
            + ". No son fallas aisladas; forman un sistema que afecta la capacidad de ejecutar con consistencia."
        )
    if weakest:
        labels = [AREA_LABELS.get(area, area.lower()) for area, _ in weakest]
        return (
            "Las oportunidades más visibles se concentran en "
            + _join_spanish(labels)
            + "."
        )
    return ""


def _priority_sentence(
    patterns: list[dict[str, Any]],
    weakest: list[tuple[str, int]],
) -> str:
    if patterns:
        main = patterns[0]
        first_actions = main["roadmap"].get("0–30 días", [])
        actions_text = _join_spanish([action.rstrip(".").lower() for action in first_actions[:2]])
        return (
            f"La prioridad estratégica es reducir {main['name'].lower()}. "
            f"Durante los primeros 30 días conviene {actions_text}."
        )
    if weakest:
        return (
            "La primera intervención debe concentrarse en las áreas con menor madurez, "
            "evitando desplegar demasiadas iniciativas al mismo tiempo."
        )
    return ""


def _closing(results: dict[str, Any], patterns: list[dict[str, Any]]) -> str:
    progress = results.get("progress", 0)
    if progress < 0.75:
        return (
            "La lectura todavía es provisional porque la entrevista no está completa. "
            "Las siguientes preguntas y evidencias deben utilizarse para confirmar o descartar estas hipótesis."
        )
    if patterns:
        return (
            "El objetivo de los próximos 90 días no es documentar por documentar, "
            "sino transferir capacidad desde las personas hacia un sistema de gestión repetible."
        )
    return (
        "El siguiente paso es validar la consistencia de estas prácticas mediante evidencias y observación."
    )


def _headline(
    patterns: list[dict[str, Any]],
    weakest: list[tuple[str, int]],
) -> str:
    if patterns:
        return f"El crecimiento está limitado por {patterns[0]['name'].lower()}."
    if weakest:
        return f"La principal oportunidad está en {weakest[0][0].lower()}."
    return "La lectura estratégica está en construcción."


def _join_spanish(items: list[str]) -> str:
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    return ", ".join(items[:-1]) + " y " + items[-1]
