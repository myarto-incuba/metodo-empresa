from knowledge.phenomena import BASE_PHENOMENA
from knowledge.relationships import PHENOMENON_RELATIONSHIPS
from modules.confidence_engine import (
    DiagnosticEvidence,
    EvidenceDirection,
    EvidenceQuality,
)
from modules.diagnosis_engine import generate_audit_diagnosis


def main() -> None:
    evidence = [
        DiagnosticEvidence(
            evidence_id="EVD-001",
            source_type="Entrevista",
            description="Las decisiones relevantes dependen de la persona propietaria.",
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
            description="El 82 % de las decisiones se escala a dirección.",
            direction=EvidenceDirection.SUPPORTS,
            quality=EvidenceQuality.STRONG,
            reliability=1.00,
            phenomenon_codes=("FEN-001",),
        ),
    ]

    audit = generate_audit_diagnosis(
        phenomena=BASE_PHENOMENA,
        relationships=PHENOMENON_RELATIONSHIPS,
        failed_control_codes=[
            "DIR-002",
            "PER-001",
            "OPE-001",
            "COM-002",
            "FIN-003",
        ],
        evidence=evidence,
        minimum_confidence=0.20,
        maximum_diagnoses=5,
    )

    assert audit.primary_diagnosis is not None
    assert audit.primary_diagnosis.phenomenon_code == "FEN-001"
    assert audit.primary_diagnosis.confidence_score >= 0.85
    assert audit.primary_diagnosis.priority_score > 0
    assert audit.primary_diagnosis.systemic_effects
    assert audit.primary_diagnosis.executive_summary
    assert audit.evidence_count == 3

    print("Motor de diagnóstico válido")
    print(
        "Diagnóstico principal:",
        audit.primary_diagnosis.phenomenon_code,
        "-",
        audit.primary_diagnosis.phenomenon_name,
    )
    print(
        "Confianza:",
        audit.primary_diagnosis.confidence_level,
        f"({audit.primary_diagnosis.confidence_score:.0%})",
    )
    print(
        "Prioridad:",
        f"{audit.primary_diagnosis.priority_score:.0%}",
    )
    print(
        "Impactos sistémicos encontrados:",
        len(audit.primary_diagnosis.systemic_effects),
    )
    print("Resumen ejecutivo:")
    print(audit.primary_diagnosis.executive_summary)


if __name__ == "__main__":
    main()
