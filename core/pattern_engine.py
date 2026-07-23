"""Motor explicable de patrones para Método Empresa.

Convierte respuestas individuales en patrones empresariales combinados.
No usa IA externa: todas las conclusiones pueden rastrearse a reglas y preguntas.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from knowledge.interview_questions import INTERVIEW_QUESTIONS


ANSWER_WEAKNESS = {
    "Sí": 0.0,
    "Parcialmente": 0.55,
    "No": 1.0,
    "No aplica": 0.0,
}


@dataclass(frozen=True)
class PatternRule:
    code: str
    name: str
    summary: str
    risk: str
    question_codes: tuple[str, ...]
    minimum_signals: int
    suggested_evidence: tuple[str, ...]
    follow_up_questions: tuple[str, ...]
    actions_30: tuple[str, ...]
    actions_60: tuple[str, ...]
    actions_90: tuple[str, ...]


PATTERN_RULES: tuple[PatternRule, ...] = (
    PatternRule(
        code="reactive_management",
        name="Gestión reactiva",
        summary="La empresa opera atendiendo urgencias más que mediante una cadencia formal de planeación y seguimiento.",
        risk="Las decisiones llegan tarde, los problemas se repiten y la dirección absorbe demasiada coordinación.",
        question_codes=("DIR-001", "DIR-004", "DIR-005", "DIR-007", "DIR-008", "FIN-007", "OPE-004", "OPE-007"),
        minimum_signals=3,
        suggested_evidence=("Plan estratégico", "Presupuesto anual", "Tablero de indicadores", "Minutas de dirección", "Mapa de riesgos"),
        follow_up_questions=(
            "¿Qué problemas se repiten cada mes y quién los resuelve?",
            "¿Qué decisiones se toman únicamente cuando aparece una urgencia?",
            "¿Qué reunión debería existir para prevenir estos problemas?",
        ),
        actions_30=("Definir una reunión mensual de dirección con agenda, responsables y acuerdos.", "Crear un tablero ejecutivo con 8 a 12 indicadores."),
        actions_60=("Vincular presupuesto, objetivos y responsables por área.",),
        actions_90=("Implementar revisión trimestral de riesgos y prioridades.",),
    ),
    PatternRule(
        code="founder_dependency",
        name="Dependencia de la dirección",
        summary="El conocimiento, las autorizaciones y varias decisiones críticas permanecen concentradas en una o pocas personas.",
        risk="La empresa pierde velocidad, limita su crecimiento y queda expuesta cuando la persona clave no está disponible.",
        question_codes=("DIR-002", "DIR-006", "FIN-006", "OPE-002", "OPE-008", "PER-001", "PER-006"),
        minimum_signals=2,
        suggested_evidence=("Organigrama", "Matriz de autorizaciones", "Descripciones de puesto", "Manuales", "Matriz de sustitución"),
        follow_up_questions=(
            "¿Qué se detiene cuando la dirección no está?",
            "¿Qué decisiones podrían delegarse esta misma semana?",
            "¿Qué conocimiento crítico solo vive en la cabeza de una persona?",
        ),
        actions_30=("Listar decisiones que hoy requieren autorización de dirección.", "Definir responsables y límites de autoridad."),
        actions_60=("Documentar funciones críticas y crear respaldos operativos.",),
        actions_90=("Medir cuántas decisiones ya se resuelven sin intervención de la dirección.",),
    ),
    PatternRule(
        code="commercial_informality",
        name="Comercial reactivo",
        summary="La captación y el seguimiento comercial dependen de relaciones, memoria personal o esfuerzos aislados.",
        risk="Se pierden oportunidades, no se conoce la conversión y el crecimiento resulta difícil de proyectar.",
        question_codes=("COM-001", "COM-002", "COM-003", "COM-004", "COM-005", "COM-008"),
        minimum_signals=2,
        suggested_evidence=("CRM o base de prospectos", "Embudo de ventas", "Guiones comerciales", "Calendario de marketing", "Reporte de conversión"),
        follow_up_questions=(
            "¿Cuántos prospectos activos existen hoy y en qué etapa están?",
            "¿Qué pasa con quien pide información y no compra?",
            "¿Qué porcentaje de ventas proviene de recompra o recomendación?",
        ),
        actions_30=("Definir etapas del embudo comercial y registrar todos los prospectos.", "Asignar fecha y responsable a cada seguimiento."),
        actions_60=("Medir conversión, ciclo de venta y origen de oportunidades.",),
        actions_90=("Crear campañas de recompra, referidos y reactivación.",),
    ),
    PatternRule(
        code="unknown_profitability",
        name="Rentabilidad poco visible",
        summary="La empresa vende y ejecuta servicios sin una lectura suficientemente clara del costo, margen y flujo asociado.",
        risk="Puede crecer en ingresos mientras deteriora liquidez o rentabilidad.",
        question_codes=("FIN-001", "FIN-002", "FIN-005", "FIN-007", "FIN-008", "COM-006", "OPE-007"),
        minimum_signals=2,
        suggested_evidence=("Estado de resultados", "Flujo de efectivo", "Costeo por servicio", "Presupuesto contra real", "Margen por línea"),
        follow_up_questions=(
            "¿Qué servicio parece vender bien pero deja menos margen?",
            "¿Qué costos no se asignan actualmente a cada proyecto?",
            "¿Cuántas semanas de operación puede cubrir la caja disponible?",
        ),
        actions_30=("Construir flujo de efectivo de 13 semanas.", "Definir costeo y margen por servicio o proyecto."),
        actions_60=("Comparar presupuesto contra resultado real cada mes.",),
        actions_90=("Revisar precios, mezcla comercial y condiciones de cobro con base en margen.",),
    ),
    PatternRule(
        code="undocumented_operation",
        name="Operación basada en conocimiento tácito",
        summary="La ejecución depende de experiencia individual y no de un sistema común, documentado y transferible.",
        risk="La calidad varía, los errores se repiten y la empresa no puede escalar con consistencia.",
        question_codes=("OPE-001", "OPE-002", "OPE-003", "OPE-004", "OPE-006", "OPE-008", "PER-003"),
        minimum_signals=2,
        suggested_evidence=("Checklists", "Cronogramas", "Plantillas de proyecto", "Manual operativo", "Reporte de cierre"),
        follow_up_questions=(
            "¿Qué actividad sale diferente según quién la ejecute?",
            "¿Cuáles son los tres errores operativos más repetidos?",
            "¿Qué proceso debería poder aprender una persona nueva en una semana?",
        ),
        actions_30=("Seleccionar y documentar los tres procesos más críticos.", "Crear checklist de apertura, ejecución y cierre."),
        actions_60=("Implementar una metodología única de proyecto y control de incidencias.",),
        actions_90=("Auditar el cumplimiento de procesos y actualizar lecciones aprendidas.",),
    ),
    PatternRule(
        code="people_informality",
        name="Gestión informal de personas",
        summary="Los roles, expectativas, desarrollo y seguimiento del equipo no están completamente institucionalizados.",
        risk="Aumentan la sobrecarga, los conflictos de responsabilidad y la dependencia de personas clave.",
        question_codes=("PER-001", "PER-002", "PER-003", "PER-004", "PER-005", "PER-006", "PER-007"),
        minimum_signals=2,
        suggested_evidence=("Perfiles de puesto", "Organigrama", "Evaluaciones", "Plan de capacitación", "Indicadores de carga"),
        follow_up_questions=(
            "¿Qué responsabilidades generan más confusión o duplicidad?",
            "¿Cómo sabe una persona si está haciendo bien su trabajo?",
            "¿Qué puesto representa hoy el mayor riesgo de continuidad?",
        ),
        actions_30=("Clarificar funciones, resultados esperados y responsables.", "Establecer reuniones uno a uno para posiciones clave."),
        actions_60=("Formalizar incorporación, capacitación y evaluación.",),
        actions_90=("Crear plan de respaldo para funciones críticas.",),
    ),
)


QUESTION_BY_CODE = {question.code: question for question in INTERVIEW_QUESTIONS}


def detect_patterns(interview: dict[str, Any]) -> list[dict[str, Any]]:
    answers = interview.get("answers", {})
    detected: list[dict[str, Any]] = []

    for rule in PATTERN_RULES:
        signal_rows: list[dict[str, Any]] = []
        weakness_total = 0.0
        answered_count = 0

        for code in rule.question_codes:
            answer_row = answers.get(code)
            if not answer_row:
                continue
            answer = answer_row.get("answer")
            if answer not in ANSWER_WEAKNESS or answer == "No aplica":
                continue

            answered_count += 1
            weakness = ANSWER_WEAKNESS[answer]
            weakness_total += weakness
            if weakness > 0:
                question = QUESTION_BY_CODE.get(code)
                signal_rows.append(
                    {
                        "question_code": code,
                        "question": question.text if question else code,
                        "answer": answer,
                        "comment": answer_row.get("comment", ""),
                        "evidence_notes": answer_row.get("evidence_notes", ""),
                        "weight": weakness,
                    }
                )

        if answered_count == 0 or len(signal_rows) < rule.minimum_signals:
            continue

        confidence = round(weakness_total / answered_count * 100)
        if confidence < 30:
            continue

        detected.append(
            {
                "code": rule.code,
                "name": rule.name,
                "summary": rule.summary,
                "risk": rule.risk,
                "confidence": confidence,
                "signal_count": len(signal_rows),
                "answered_count": answered_count,
                "signals": sorted(signal_rows, key=lambda row: row["weight"], reverse=True),
                "suggested_evidence": list(rule.suggested_evidence),
                "follow_up_questions": list(rule.follow_up_questions),
                "roadmap": {
                    "0–30 días": list(rule.actions_30),
                    "31–60 días": list(rule.actions_60),
                    "61–90 días": list(rule.actions_90),
                },
            }
        )

    detected.sort(key=lambda item: (item["confidence"], item["signal_count"]), reverse=True)
    return detected


def build_copilot(interview: dict[str, Any], *, limit: int = 3) -> dict[str, Any]:
    patterns = detect_patterns(interview)
    top_patterns = patterns[:limit]

    evidence: list[str] = []
    questions: list[str] = []
    observations: list[str] = []

    for pattern in top_patterns:
        observations.append(
            f"{pattern['name']}: {pattern['summary']}"
        )
        _extend_unique(evidence, pattern["suggested_evidence"])
        _extend_unique(questions, pattern["follow_up_questions"])

    return {
        "patterns": top_patterns,
        "observations": observations[:limit],
        "evidence": evidence[:6],
        "follow_up_questions": questions[:5],
    }


def _extend_unique(target: list[str], values: Iterable[str]) -> None:
    for value in values:
        if value not in target:
            target.append(value)
