"""
Motor de confianza diagnóstica de Método Empresa.

Convierte controles, evidencias y señales contradictorias en una evaluación
explicable de la solidez de una hipótesis empresarial.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Iterable, Protocol


class ConfidenceLevel(str, Enum):
    VERY_LOW = "Muy baja"
    LOW = "Baja"
    MODERATE = "Moderada"
    HIGH = "Alta"
    VERY_HIGH = "Muy alta"


class EvidenceDirection(str, Enum):
    SUPPORTS = "Apoya"
    CONTRADICTS = "Contradice"
    NEUTRAL = "Neutral"


class EvidenceQuality(str, Enum):
    WEAK = "Débil"
    MEDIUM = "Media"
    STRONG = "Fuerte"


QUALITY_WEIGHTS: dict[EvidenceQuality, float] = {
    EvidenceQuality.WEAK: 0.35,
    EvidenceQuality.MEDIUM: 0.65,
    EvidenceQuality.STRONG: 1.00,
}


class PhenomenonLike(Protocol):
    code: str
    name: str
    control_codes: list[str]


@dataclass(frozen=True)
class DiagnosticEvidence:
    evidence_id: str
    source_type: str
    description: str
    direction: EvidenceDirection
    quality: EvidenceQuality = EvidenceQuality.MEDIUM
    reliability: float = 1.0
    control_codes: tuple[str, ...] = ()
    phenomenon_codes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        evidence_id = self.evidence_id.strip()
        source_type = self.source_type.strip()
        description = self.description.strip()

        object.__setattr__(self, "evidence_id", evidence_id)
        object.__setattr__(self, "source_type", source_type)
        object.__setattr__(self, "description", description)
        object.__setattr__(
            self,
            "control_codes",
            tuple(
                dict.fromkeys(
                    code.strip().upper()
                    for code in self.control_codes
                    if str(code).strip()
                )
            ),
        )
        object.__setattr__(
            self,
            "phenomenon_codes",
            tuple(
                dict.fromkeys(
                    code.strip().upper()
                    for code in self.phenomenon_codes
                    if str(code).strip()
                )
            ),
        )

        if not evidence_id:
            raise ValueError("La evidencia debe tener un identificador.")
        if not source_type:
            raise ValueError("La evidencia debe indicar su fuente.")
        if not description:
            raise ValueError("La evidencia debe incluir una descripción.")
        if not 0 <= self.reliability <= 1:
            raise ValueError("La confiabilidad debe estar entre 0 y 1.")

    @property
    def weighted_value(self) -> float:
        return round(QUALITY_WEIGHTS[self.quality] * self.reliability, 4)


@dataclass
class ConfidenceAssessment:
    phenomenon_code: str
    phenomenon_name: str
    score: float
    level: ConfidenceLevel
    control_coverage: float
    evidence_support_score: float
    evidence_contradiction_score: float
    source_diversity_score: float
    supporting_evidence: list[str] = field(default_factory=list)
    contradicting_evidence: list[str] = field(default_factory=list)
    matched_controls: list[str] = field(default_factory=list)
    missing_controls: list[str] = field(default_factory=list)
    missing_information: list[str] = field(default_factory=list)
    recommended_next_steps: list[str] = field(default_factory=list)
    explanation: str = ""

    def to_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["level"] = self.level.value
        return data


def confidence_level(score: float) -> ConfidenceLevel:
    if score < 0.20:
        return ConfidenceLevel.VERY_LOW
    if score < 0.40:
        return ConfidenceLevel.LOW
    if score < 0.65:
        return ConfidenceLevel.MODERATE
    if score < 0.85:
        return ConfidenceLevel.HIGH
    return ConfidenceLevel.VERY_HIGH


def assess_phenomenon_confidence(
    phenomenon: PhenomenonLike,
    failed_control_codes: Iterable[str],
    evidence: Iterable[DiagnosticEvidence] = (),
) -> ConfidenceAssessment:
    failed = {
        str(code).strip().upper()
        for code in failed_control_codes
        if str(code).strip()
    }
    phenomenon_controls = {
        str(code).strip().upper()
        for code in phenomenon.control_codes
        if str(code).strip()
    }

    matched_controls = sorted(failed.intersection(phenomenon_controls))
    missing_controls = sorted(phenomenon_controls.difference(failed))

    control_coverage = (
        len(matched_controls) / len(phenomenon_controls)
        if phenomenon_controls
        else 0.0
    )

    relevant_evidence = [
        item
        for item in evidence
        if _evidence_is_relevant(
            item,
            phenomenon_code=phenomenon.code,
            phenomenon_controls=phenomenon_controls,
        )
    ]

    supporting = [
        item
        for item in relevant_evidence
        if item.direction == EvidenceDirection.SUPPORTS
    ]
    contradicting = [
        item
        for item in relevant_evidence
        if item.direction == EvidenceDirection.CONTRADICTS
    ]

    support_score = _aggregate_evidence(supporting)
    contradiction_score = _aggregate_evidence(contradicting)
    source_diversity = _source_diversity_score(supporting)

    # Cobertura de controles: 55 %
    # Evidencia que apoya: 30 %
    # Diversidad de fuentes: 15 %
    # Evidencia contradictoria resta hasta 35 %
    raw_score = (
        control_coverage * 0.55
        + support_score * 0.30
        + source_diversity * 0.15
        - contradiction_score * 0.35
    )
    score = round(min(max(raw_score, 0.0), 1.0), 4)
    level = confidence_level(score)

    missing_information = _build_missing_information(
        missing_controls=missing_controls,
        supporting=supporting,
        relevant_evidence=relevant_evidence,
    )
    next_steps = _build_next_steps(
        missing_controls=missing_controls,
        supporting=supporting,
        contradicting=contradicting,
        source_diversity=source_diversity,
    )

    explanation = _build_explanation(
        phenomenon_name=phenomenon.name,
        score=score,
        level=level,
        matched_controls=matched_controls,
        total_controls=len(phenomenon_controls),
        supporting_count=len(supporting),
        contradicting_count=len(contradicting),
    )

    return ConfidenceAssessment(
        phenomenon_code=phenomenon.code,
        phenomenon_name=phenomenon.name,
        score=score,
        level=level,
        control_coverage=round(control_coverage, 4),
        evidence_support_score=round(support_score, 4),
        evidence_contradiction_score=round(contradiction_score, 4),
        source_diversity_score=round(source_diversity, 4),
        supporting_evidence=[item.evidence_id for item in supporting],
        contradicting_evidence=[item.evidence_id for item in contradicting],
        matched_controls=matched_controls,
        missing_controls=missing_controls,
        missing_information=missing_information,
        recommended_next_steps=next_steps,
        explanation=explanation,
    )


def rank_phenomenon_hypotheses(
    phenomena: Iterable[PhenomenonLike],
    failed_control_codes: Iterable[str],
    evidence: Iterable[DiagnosticEvidence] = (),
    minimum_score: float = 0.0,
) -> list[ConfidenceAssessment]:
    failed = list(failed_control_codes)
    evidence_list = list(evidence)

    assessments = [
        assess_phenomenon_confidence(
            phenomenon=phenomenon,
            failed_control_codes=failed,
            evidence=evidence_list,
        )
        for phenomenon in phenomena
    ]

    return sorted(
        (
            assessment
            for assessment in assessments
            if assessment.score >= minimum_score
        ),
        key=lambda assessment: (
            assessment.score,
            assessment.control_coverage,
            assessment.evidence_support_score,
        ),
        reverse=True,
    )


def _evidence_is_relevant(
    evidence: DiagnosticEvidence,
    phenomenon_code: str,
    phenomenon_controls: set[str],
) -> bool:
    clean_phenomenon_code = phenomenon_code.strip().upper()

    if clean_phenomenon_code in evidence.phenomenon_codes:
        return True

    if phenomenon_controls.intersection(evidence.control_codes):
        return True

    return False


def _aggregate_evidence(
    evidence: list[DiagnosticEvidence],
) -> float:
    if not evidence:
        return 0.0

    total = sum(item.weighted_value for item in evidence)

    # Saturación progresiva: varias evidencias suman valor,
    # pero ninguna cantidad eleva el componente por encima de 1.
    return min(total / 2.0, 1.0)


def _source_diversity_score(
    supporting_evidence: list[DiagnosticEvidence],
) -> float:
    if not supporting_evidence:
        return 0.0

    sources = {
        item.source_type.strip().casefold()
        for item in supporting_evidence
        if item.source_type.strip()
    }

    # Tres fuentes independientes ya se consideran una triangulación sólida.
    return min(len(sources) / 3.0, 1.0)


def _build_missing_information(
    missing_controls: list[str],
    supporting: list[DiagnosticEvidence],
    relevant_evidence: list[DiagnosticEvidence],
) -> list[str]:
    missing: list[str] = []

    if missing_controls:
        missing.append(
            "Evaluar los controles aún no confirmados: "
            + ", ".join(missing_controls)
        )

    if not supporting:
        missing.append(
            "Obtener evidencia independiente que respalde la hipótesis."
        )

    source_types = {
        item.source_type.strip().casefold()
        for item in relevant_evidence
        if item.source_type.strip()
    }

    if len(source_types) < 2:
        missing.append(
            "Triangular la hipótesis con al menos dos tipos de fuente."
        )

    return missing


def _build_next_steps(
    missing_controls: list[str],
    supporting: list[DiagnosticEvidence],
    contradicting: list[DiagnosticEvidence],
    source_diversity: float,
) -> list[str]:
    steps: list[str] = []

    if missing_controls:
        steps.append(
            "Aplicar preguntas o pruebas específicas para los controles faltantes."
        )

    if not supporting:
        steps.append(
            "Solicitar documentos, indicadores o entrevistas que puedan confirmar el patrón."
        )

    if contradicting:
        steps.append(
            "Investigar las evidencias contradictorias antes de emitir un diagnóstico definitivo."
        )

    if source_diversity < 0.67:
        steps.append(
            "Añadir una fuente independiente para reducir sesgos de interpretación."
        )

    if not steps:
        steps.append(
            "Mantener seguimiento mediante indicadores y validar la hipótesis en el cierre de auditoría."
        )

    return steps


def _build_explanation(
    phenomenon_name: str,
    score: float,
    level: ConfidenceLevel,
    matched_controls: list[str],
    total_controls: int,
    supporting_count: int,
    contradicting_count: int,
) -> str:
    control_text = (
        f"{len(matched_controls)} de {total_controls} controles relacionados"
    )

    return (
        f"La hipótesis «{phenomenon_name}» presenta confianza "
        f"{level.value.lower()} ({score:.0%}). "
        f"Se observaron {control_text}, "
        f"{supporting_count} evidencias de apoyo y "
        f"{contradicting_count} evidencias contradictorias."
    )
