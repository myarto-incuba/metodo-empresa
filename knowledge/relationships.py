"""
Relaciones explícitas entre fenómenos empresariales.
"""

from __future__ import annotations

from dataclasses import dataclass


VALID_RELATION_TYPES = {
    "Causa",
    "Consecuencia",
    "Amplifica",
    "Depende de",
    "Retroalimenta",
}


@dataclass(frozen=True)
class PhenomenonRelationship:
    source_code: str
    target_code: str
    relation_type: str
    strength: float
    explanation: str

    def __post_init__(self) -> None:
        source = self.source_code.strip().upper()
        target = self.target_code.strip().upper()

        object.__setattr__(self, "source_code", source)
        object.__setattr__(self, "target_code", target)

        if not source or not target:
            raise ValueError("La relación necesita origen y destino.")
        if source == target:
            raise ValueError("Un fenómeno no puede relacionarse consigo mismo.")
        if self.relation_type not in VALID_RELATION_TYPES:
            raise ValueError(f"Tipo de relación no válido: {self.relation_type}")
        if not 0 <= self.strength <= 1:
            raise ValueError("La fuerza debe estar entre 0 y 1.")
        if not self.explanation.strip():
            raise ValueError("La relación debe incluir una explicación.")


PHENOMENON_RELATIONSHIPS: list[PhenomenonRelationship] = [
    PhenomenonRelationship(
        "FEN-001",
        "FEN-003",
        "Causa",
        0.85,
        "La concentración de decisiones provoca respuestas tardías y reactivas.",
    ),
    PhenomenonRelationship(
        "FEN-001",
        "FEN-006",
        "Causa",
        0.90,
        "La dependencia de una persona impide estandarizar la operación.",
    ),
    PhenomenonRelationship(
        "FEN-008",
        "FEN-001",
        "Amplifica",
        0.90,
        "La falta de responsables obliga al dueño a absorber decisiones y tareas.",
    ),
    PhenomenonRelationship(
        "FEN-008",
        "FEN-006",
        "Causa",
        0.85,
        "La ambigüedad de funciones genera variación, omisiones y duplicidad.",
    ),
    PhenomenonRelationship(
        "FEN-002",
        "FEN-003",
        "Causa",
        0.80,
        "La ausencia de prioridades favorece decisiones improvisadas.",
    ),
    PhenomenonRelationship(
        "FEN-010",
        "FEN-003",
        "Causa",
        0.90,
        "Sin información oportuna, la empresa actúa cuando el problema ya ocurrió.",
    ),
    PhenomenonRelationship(
        "FEN-004",
        "FEN-005",
        "Causa",
        0.85,
        "La imprevisibilidad de ingresos dificulta anticipar la posición de caja.",
    ),
    PhenomenonRelationship(
        "FEN-004",
        "FEN-006",
        "Amplifica",
        0.70,
        "La demanda impredecible provoca saturación o capacidad ociosa.",
    ),
    PhenomenonRelationship(
        "FEN-006",
        "FEN-007",
        "Causa",
        0.90,
        "La variabilidad operativa genera errores, retrabajos y costos no visibles.",
    ),
    PhenomenonRelationship(
        "FEN-009",
        "FEN-007",
        "Causa",
        0.75,
        "La baja productividad incrementa el costo real de entregar resultados.",
    ),
    PhenomenonRelationship(
        "FEN-007",
        "FEN-005",
        "Amplifica",
        0.75,
        "Los costos no controlados reducen la disponibilidad de efectivo.",
    ),
    PhenomenonRelationship(
        "FEN-005",
        "FEN-003",
        "Retroalimenta",
        0.70,
        "La presión de caja obliga a tomar decisiones urgentes y de corto plazo.",
    ),
]


def validate_phenomenon_relationships(
    phenomenon_codes: set[str],
) -> list[str]:
    errors: list[str] = []

    for relationship in PHENOMENON_RELATIONSHIPS:
        if relationship.source_code not in phenomenon_codes:
            errors.append(
                f"Origen inexistente: {relationship.source_code}"
            )
        if relationship.target_code not in phenomenon_codes:
            errors.append(
                f"Destino inexistente: {relationship.target_code}"
            )

    return errors
