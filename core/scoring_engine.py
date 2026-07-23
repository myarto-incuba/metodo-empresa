"""Cálculo simple y explicable para el dashboard del piloto."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from knowledge.interview_questions import INTERVIEW_QUESTIONS


ANSWER_SCORE = {
    "Sí": 1.0,
    "Parcialmente": 0.5,
    "No": 0.0,
}


def calculate_results(interview: dict[str, Any]) -> dict[str, Any]:
    answers = interview.get("answers", {})
    area_values: dict[str, list[float]] = defaultdict(list)
    hypothesis_points: dict[str, float] = defaultdict(float)
    hypothesis_possible: dict[str, float] = defaultdict(float)

    answered = 0
    applicable = 0

    for question in INTERVIEW_QUESTIONS:
        row = answers.get(question.code)
        if not row:
            continue

        answered += 1
        answer = row.get("answer")
        if answer == "No aplica":
            continue
        if answer not in ANSWER_SCORE:
            continue

        applicable += 1
        score = ANSWER_SCORE[answer]
        area_values[question.area].append(score)

        weakness = 1.0 - score
        for tag in question.hypothesis_tags:
            hypothesis_points[tag] += weakness
            hypothesis_possible[tag] += 1.0

    area_scores = {
        area: round(sum(values) / len(values) * 100)
        for area, values in area_values.items()
        if values
    }

    overall = (
        round(sum(sum(values) for values in area_values.values())
              / sum(len(values) for values in area_values.values()) * 100)
        if any(area_values.values())
        else 0
    )

    hypotheses = []
    for name, points in hypothesis_points.items():
        possible = hypothesis_possible[name]
        confidence = round(points / possible * 100) if possible else 0
        if confidence > 0:
            hypotheses.append({"name": name, "confidence": confidence})

    hypotheses.sort(key=lambda item: item["confidence"], reverse=True)

    return {
        "answered": answered,
        "applicable": applicable,
        "total": len(INTERVIEW_QUESTIONS),
        "progress": answered / len(INTERVIEW_QUESTIONS),
        "overall_score": overall,
        "maturity": maturity_label(overall),
        "area_scores": area_scores,
        "hypotheses": hypotheses[:6],
        "recommendations": recommendations_from_hypotheses(hypotheses[:6]),
    }


def maturity_label(score: int) -> str:
    if score >= 85:
        return "Consolidada"
    if score >= 70:
        return "En desarrollo"
    if score >= 50:
        return "Básica"
    return "Inicial"


def recommendations_from_hypotheses(
    hypotheses: list[dict[str, Any]],
) -> list[str]:
    mapping = {
        "Dependencia del dueño": "Delegar decisiones y documentar niveles de autoridad.",
        "Responsabilidades difusas": "Definir responsables, entregables y límites de autoridad.",
        "Planeación insuficiente": "Formalizar objetivos, presupuesto y seguimiento mensual.",
        "Falta de indicadores": "Crear un tablero ejecutivo con indicadores por área.",
        "Control financiero débil": "Implementar flujo de efectivo y revisión financiera mensual.",
        "Procesos no documentados": "Documentar los procesos críticos mediante checklists y plantillas.",
        "Proceso comercial informal": "Estandarizar el embudo comercial y registrar todos los prospectos.",
        "Información dispersa": "Centralizar clientes, acuerdos y proyectos en una sola herramienta.",
        "Gestión reactiva": "Incorporar planeación preventiva, riesgos y cierres de proyecto.",
        "Ejecución inconsistente": "Adoptar una metodología única para planear y cerrar proyectos.",
        "Rentabilidad desconocida": "Medir costo y margen por evento, curso y línea de servicio.",
        "Dependencia de personas clave": "Crear respaldos operativos y transferencia de conocimiento.",
        "Marketing sin estrategia": "Definir públicos, propuesta de valor, canales y objetivos comerciales.",
        "Experiencia no medida": "Medir satisfacción y aprendizajes después de cada servicio.",
        "Oportunidades perdidas": "Crear seguimiento de recompra, referidos y clientes inactivos.",
        "Gestión de personas informal": "Formalizar perfiles, incorporación, capacitación y evaluación.",
        "Liderazgo reactivo": "Establecer reuniones periódicas de seguimiento y retroalimentación.",
        "Comunicación deficiente": "Crear espacios seguros para reportar problemas y proponer mejoras.",
        "Sobrecarga operativa": "Medir cargas de trabajo y redistribuir tareas críticas.",
        "Cobranza débil": "Implementar calendario, responsables y alertas de cobranza.",
    }

    recommendations = []
    for hypothesis in hypotheses:
        recommendation = mapping.get(hypothesis["name"])
        if recommendation and recommendation not in recommendations:
            recommendations.append(recommendation)
    return recommendations[:5]
