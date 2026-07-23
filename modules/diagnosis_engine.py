"""
Motor integrador de diagnóstico de Método Empresa.

Combina controles fallidos, fenómenos compatibles, confianza diagnóstica,
influencia sistémica y efectos indirectos para producir diagnósticos
explicables y priorizados.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Iterable

from knowledge.phenomena import BusinessPhenomenon
from knowledge.relationships import PhenomenonRelationship
from modules.confidence_engine import (
    ConfidenceAssessment,
    DiagnosticEvidence,
    rank_phenomenon_hypotheses,
)
from modules.graph_engine import calculate_influence_scores, trace_effects


@dataclass
class DiagnosisResult:
    phenomenon_code: str
    phenomenon_name: str
    priority_score: float
    confidence_score: float
    confidence_level: str
    root_score: float
    control_coverage: float
    matched_controls: list[str] = field(default_factory=list)
    missing_controls: list[str] = field(default_factory=list)
    supporting_evidence: list[str] = field(default_factory=list)
    contradicting_evidence: list[str] = field(default_factory=list)
    affected_areas: list[str] = field(default_factory=list)
    systemic_effects: list[dict[str, object]] = field(default_factory=list)
    missing_information: list[str] = field(default_factory=list)
    recommended_next_steps: list[str] = field(default_factory=list)
    executive_summary: str = ""

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass
class AuditDiagnosis:
    diagnoses: list[DiagnosisResult]
    discarded_hypotheses: list[dict[str, object]]
    failed_controls: list[str]
    evidence_count: int

    @property
    def primary_diagnosis(self) -> DiagnosisResult | None:
        return self.diagnoses[0] if self.diagnoses else None

    def to_dict(self) -> dict[str, object]:
        return {
            "diagnoses": [diagnosis.to_dict() for diagnosis in self.diagnoses],
            "discarded_hypotheses": self.discarded_hypotheses,
            "failed_controls": self.failed_controls,
            "evidence_count": self.evidence_count,
        }


def generate_audit_diagnosis(
    phenomena: Iterable[BusinessPhenomenon],
    relationships: Iterable[PhenomenonRelationship],
    failed_control_codes: Iterable[str],
    evidence: Iterable[DiagnosticEvidence] = (),
    minimum_confidence: float = 0.20,
    maximum_diagnoses: int = 5,
    effects_depth: int = 3,
) -> AuditDiagnosis:
    phenomenon_list = list(phenomena)
    relationship_list = list(relationships)
    evidence_list = list(evidence)

    failed_controls = sorted(
        {
            str(code).strip().upper()
            for code in failed_control_codes
            if str(code).strip()
        }
    )

    confidence_assessments = rank_phenomenon_hypotheses(
        phenomena=phenomenon_list,
        failed_control_codes=failed_controls,
        evidence=evidence_list,
        minimum_score=0.0,
    )

    influence_rows = calculate_influence_scores(
        phenomena=phenomenon_list,
        relationships=relationship_list,
    )
    influence_by_code = {
        str(row["code"]): row
        for row in influence_rows
    }
    phenomena_by_code = {
        phenomenon.code: phenomenon
        for phenomenon in phenomenon_list
    }

    diagnoses: list[DiagnosisResult] = []
    discarded: list[dict[str, object]] = []

    for assessment in confidence_assessments:
        influence = influence_by_code.get(assessment.phenomenon_code, {})
        root_score = float(influence.get("root_score", 0.0))
        normalized_root_score = _normalize_root_score(
            root_score=root_score,
            influence_rows=influence_rows,
        )

        priority_score = _calculate_priority_score(
            confidence_score=assessment.score,
            normalized_root_score=normalized_root_score,
            control_coverage=assessment.control_coverage,
            contradiction_score=assessment.evidence_contradiction_score,
        )

        if assessment.score < minimum_confidence:
            discarded.append(
                {
                    "phenomenon_code": assessment.phenomenon_code,
                    "phenomenon_name": assessment.phenomenon_name,
                    "confidence_score": assessment.score,
                    "reason": (
                        "Confianza inferior al umbral mínimo "
                        f"de {minimum_confidence:.0%}."
                    ),
                }
            )
            continue

        phenomenon = phenomena_by_code[assessment.phenomenon_code]
        effects = trace_effects(
            start_code=assessment.phenomenon_code,
            relationships=relationship_list,
            max_depth=effects_depth,
        )

        diagnoses.append(
            DiagnosisResult(
                phenomenon_code=assessment.phenomenon_code,
                phenomenon_name=assessment.phenomenon_name,
                priority_score=priority_score,
                confidence_score=assessment.score,
                confidence_level=assessment.level.value,
                root_score=round(root_score, 4),
                control_coverage=assessment.control_coverage,
                matched_controls=assessment.matched_controls,
                missing_controls=assessment.missing_controls,
                supporting_evidence=assessment.supporting_evidence,
                contradicting_evidence=assessment.contradicting_evidence,
                affected_areas=phenomenon.affected_areas,
                systemic_effects=effects,
                missing_information=assessment.missing_information,
                recommended_next_steps=assessment.recommended_next_steps,
                executive_summary=_build_executive_summary(
                    assessment=assessment,
                    phenomenon=phenomenon,
                    priority_score=priority_score,
                    effects=effects,
                ),
            )
        )

    diagnoses.sort(
        key=lambda diagnosis: (
            diagnosis.priority_score,
            diagnosis.confidence_score,
            diagnosis.root_score,
        ),
        reverse=True,
    )

    return AuditDiagnosis(
        diagnoses=diagnoses[:maximum_diagnoses],
        discarded_hypotheses=discarded,
        failed_controls=failed_controls,
        evidence_count=len(evidence_list),
    )


def _calculate_priority_score(
    confidence_score: float,
    normalized_root_score: float,
    control_coverage: float,
    contradiction_score: float,
) -> float:
    score = (
        confidence_score * 0.50
        + normalized_root_score * 0.30
        + control_coverage * 0.20
        - contradiction_score * 0.15
    )
    return round(min(max(score, 0.0), 1.0), 4)


def _normalize_root_score(
    root_score: float,
    influence_rows: list[dict[str, object]],
) -> float:
    maximum = max(
        (
            float(row.get("root_score", 0.0))
            for row in influence_rows
        ),
        default=0.0,
    )

    if maximum <= 0:
        return 0.0

    return min(max(root_score / maximum, 0.0), 1.0)


def _build_executive_summary(
    assessment: ConfidenceAssessment,
    phenomenon: BusinessPhenomenon,
    priority_score: float,
    effects: list[dict[str, object]],
) -> str:
    areas = ", ".join(phenomenon.affected_areas)
    direct_effects = {
        str(effect["target"])
        for effect in effects
        if int(effect["depth"]) == 1
    }

    effects_text = (
        ", ".join(sorted(direct_effects))
        if direct_effects
        else "sin efectos directos confirmados en el grafo"
    )

    contradiction_text = ""
    if assessment.contradicting_evidence:
        contradiction_text = (
            f" Existen {len(assessment.contradicting_evidence)} "
            "evidencias contradictorias que deben revisarse."
        )

    return (
        f"Se detectó el fenómeno «{phenomenon.name}» con confianza "
        f"{assessment.level.value.lower()} ({assessment.score:.0%}) y "
        f"prioridad diagnóstica de {priority_score:.0%}. "
        f"El patrón está respaldado por "
        f"{len(assessment.matched_controls)} controles fallidos y afecta "
        f"principalmente a {areas}. "
        f"Sus efectos sistémicos directos se relacionan con: {effects_text}."
        f"{contradiction_text}"
    )
