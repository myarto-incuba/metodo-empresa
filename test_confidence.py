from knowledge.phenomena import BASE_PHENOMENA, get_phenomenon
from modules.confidence_engine import (
    ConfidenceLevel,
    DiagnosticEvidence,
    EvidenceDirection,
    EvidenceQuality,
    assess_phenomenon_confidence,
    rank_phenomenon_hypotheses,
)


def main() -> None:
    phenomenon = get_phenomenon("FEN-001")
    assert phenomenon is not None

    evidence = [
        DiagnosticEvidence(
            evidence_id="EVD-001",
            source_type="Entrevista",
            description="El equipo afirma que todas las decisiones requieren al dueño.",
            direction=EvidenceDirection.SUPPORTS,
            quality=EvidenceQuality.STRONG,
            reliability=0.95,
            phenomenon_codes=("FEN-001",),
        ),
        DiagnosticEvidence(
            evidence_id="EVD-002",
            source_type="Documento",
            description="La matriz de autorizaciones concentra todas las firmas.",
            direction=EvidenceDirection.SUPPORTS,
            quality=EvidenceQuality.STRONG,
            reliability=0.90,
            control_codes=("DIR-002",),
        ),
        DiagnosticEvidence(
            evidence_id="EVD-003",
            source_type="Indicador",
            description="El 82 % de las decisiones se escalan a dirección.",
            direction=EvidenceDirection.SUPPORTS,
            quality=EvidenceQuality.STRONG,
            reliability=1.00,
            phenomenon_codes=("FEN-001",),
        ),
    ]

    strong_assessment = assess_phenomenon_confidence(
        phenomenon=phenomenon,
        failed_control_codes=[
            "DIR-002",
            "PER-001",
            "OPE-001",
            "COM-002",
            "FIN-003",
        ],
        evidence=evidence,
    )

    assert strong_assessment.level == ConfidenceLevel.VERY_HIGH
    assert strong_assessment.score >= 0.85
    assert not strong_assessment.missing_controls

    weak_assessment = assess_phenomenon_confidence(
        phenomenon=phenomenon,
        failed_control_codes=["DIR-002"],
        evidence=[],
    )

    assert weak_assessment.level in {
        ConfidenceLevel.VERY_LOW,
        ConfidenceLevel.LOW,
    }
    assert weak_assessment.missing_controls

    contradictory_evidence = evidence + [
        DiagnosticEvidence(
            evidence_id="EVD-004",
            source_type="Observación",
            description="Dos responsables aprobaron operaciones sin intervención del dueño.",
            direction=EvidenceDirection.CONTRADICTS,
            quality=EvidenceQuality.STRONG,
            reliability=0.90,
            phenomenon_codes=("FEN-001",),
        )
    ]

    contradictory_assessment = assess_phenomenon_confidence(
        phenomenon=phenomenon,
        failed_control_codes=[
            "DIR-002",
            "PER-001",
            "OPE-001",
        ],
        evidence=contradictory_evidence,
    )

    assert contradictory_assessment.evidence_contradiction_score > 0
    assert contradictory_assessment.contradicting_evidence == ["EVD-004"]

    ranking = rank_phenomenon_hypotheses(
        phenomena=BASE_PHENOMENA,
        failed_control_codes=[
            "DIR-002",
            "PER-001",
            "OPE-001",
            "COM-002",
        ],
        evidence=evidence,
    )

    assert ranking
    assert ranking[0].phenomenon_code == "FEN-001"

    print("Motor de confianza válido")
    print(
        "Hipótesis fuerte:",
        strong_assessment.phenomenon_code,
        "-",
        strong_assessment.level.value,
        f"({strong_assessment.score:.0%})",
    )
    print(
        "Hipótesis débil:",
        weak_assessment.phenomenon_code,
        "-",
        weak_assessment.level.value,
        f"({weak_assessment.score:.0%})",
    )
    print(
        "Primera hipótesis del ranking:",
        ranking[0].phenomenon_code,
        "-",
        ranking[0].phenomenon_name,
    )
    print("Explicación:", strong_assessment.explanation)


if __name__ == "__main__":
    main()
