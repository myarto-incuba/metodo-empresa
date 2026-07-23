"""
Motor de hipótesis de Método Empresa.

Este módulo transforma señales preliminares en hipótesis estructuradas.
Por ahora no modifica la base de datos ni la interfaz.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Iterable


VALID_IMPACTS = {"Bajo", "Medio", "Alto", "Crítico"}
VALID_STATUSES = {
    "Pendiente",
    "En validación",
    "Confirmada",
    "Descartada",
}


@dataclass
class Hypothesis:
    """
    Representa una hipótesis empresarial pendiente de validación.
    """

    code: str
    name: str
    description: str
    category: str
    probability: float
    impact: str
    evidence_required: list[str] = field(default_factory=list)
    source_questions: list[str] = field(default_factory=list)
    status: str = "Pendiente"
    rationale: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.probability = normalize_probability(self.probability)

        if self.impact not in VALID_IMPACTS:
            raise ValueError(
                f"Impacto no válido: {self.impact}. "
                f"Valores permitidos: {sorted(VALID_IMPACTS)}"
            )

        if self.status not in VALID_STATUSES:
            raise ValueError(
                f"Estado no válido: {self.status}. "
                f"Valores permitidos: {sorted(VALID_STATUSES)}"
            )

        self.evidence_required = unique_strings(self.evidence_required)
        self.source_questions = unique_strings(self.source_questions)

    @property
    def probability_percent(self) -> int:
        """Probabilidad expresada como porcentaje entero."""
        return round(self.probability * 100)

    @property
    def priority_score(self) -> float:
        """
        Calcula una prioridad preliminar entre 0 y 100.

        Combina la probabilidad de la hipótesis con el impacto estimado.
        """
        impact_weights = {
            "Bajo": 25,
            "Medio": 50,
            "Alto": 75,
            "Crítico": 100,
        }

        return round(
            self.probability * impact_weights[self.impact],
            2,
        )

    def to_dict(self) -> dict[str, Any]:
        """Convierte la hipótesis en un diccionario serializable."""
        result = asdict(self)
        result["probability_percent"] = self.probability_percent
        result["priority_score"] = self.priority_score
        return result


def normalize_probability(value: float | int) -> float:
    """
    Normaliza una probabilidad al rango 0.0–1.0.

    Acepta:
    - 0.82
    - 82
    """
    try:
        probability = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(
            "La probabilidad debe ser un número."
        ) from exc

    if probability > 1:
        probability = probability / 100

    if not 0 <= probability <= 1:
        raise ValueError(
            "La probabilidad debe estar entre 0 y 1, "
            "o entre 0 y 100."
        )

    return round(probability, 4)


def unique_strings(values: Iterable[str] | None) -> list[str]:
    """Limpia, elimina vacíos y evita duplicados conservando el orden."""
    if not values:
        return []

    result: list[str] = []
    seen: set[str] = set()

    for value in values:
        clean_value = str(value).strip()

        if not clean_value:
            continue

        normalized = clean_value.casefold()

        if normalized in seen:
            continue

        seen.add(normalized)
        result.append(clean_value)

    return result


def create_hypothesis(
    *,
    code: str,
    name: str,
    description: str,
    category: str,
    probability: float,
    impact: str,
    evidence_required: list[str] | None = None,
    source_questions: list[str] | None = None,
    rationale: str = "",
    metadata: dict[str, Any] | None = None,
) -> Hypothesis:
    """
    Crea una hipótesis validada.

    Esta función será el punto de entrada para risk_engine,
    interview_engine y futuros módulos de IA.
    """
    clean_code = code.strip().upper()
    clean_name = name.strip()
    clean_description = description.strip()
    clean_category = category.strip()

    if not clean_code:
        raise ValueError("La hipótesis debe tener un código.")

    if not clean_name:
        raise ValueError("La hipótesis debe tener un nombre.")

    if not clean_description:
        raise ValueError("La hipótesis debe tener una descripción.")

    if not clean_category:
        raise ValueError("La hipótesis debe tener una categoría.")

    return Hypothesis(
        code=clean_code,
        name=clean_name,
        description=clean_description,
        category=clean_category,
        probability=probability,
        impact=impact,
        evidence_required=evidence_required or [],
        source_questions=source_questions or [],
        rationale=rationale.strip(),
        metadata=metadata or {},
    )


def sort_hypotheses(
    hypotheses: Iterable[Hypothesis],
) -> list[Hypothesis]:
    """Ordena las hipótesis de mayor a menor prioridad."""
    return sorted(
        hypotheses,
        key=lambda hypothesis: hypothesis.priority_score,
        reverse=True,
    )


def summarize_hypotheses(
    hypotheses: Iterable[Hypothesis],
) -> dict[str, Any]:
    """Genera un resumen ejecutivo básico."""
    hypothesis_list = list(hypotheses)

    by_status = {
        status: sum(
            1
            for hypothesis in hypothesis_list
            if hypothesis.status == status
        )
        for status in sorted(VALID_STATUSES)
    }

    by_impact = {
        impact: sum(
            1
            for hypothesis in hypothesis_list
            if hypothesis.impact == impact
        )
        for impact in ("Crítico", "Alto", "Medio", "Bajo")
    }

    return {
        "total": len(hypothesis_list),
        "by_status": by_status,
        "by_impact": by_impact,
        "average_probability": (
            round(
                sum(
                    hypothesis.probability
                    for hypothesis in hypothesis_list
                )
                / len(hypothesis_list),
                4,
            )
            if hypothesis_list
            else 0
        ),
    }