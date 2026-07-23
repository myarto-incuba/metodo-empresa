"""
Motor de relaciones sistémicas para Método Empresa.

Permite conectar controles, hallazgos, áreas, fenómenos e indicadores
para representar cómo una condición empresarial influye en otra.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Iterable


VALID_RELATION_TYPES = {
    "Causa",
    "Consecuencia",
    "Dependencia",
    "Amplificación",
    "Compensación",
    "Indicador compartido",
    "Evidencia compartida",
}

VALID_STRENGTHS = {
    "Baja",
    "Media",
    "Alta",
    "Crítica",
}

VALID_NODE_TYPES = {
    "Área",
    "Control",
    "Hallazgo",
    "Hipótesis",
    "Fenómeno",
    "Indicador",
    "Evidencia",
    "Acción",
}


@dataclass
class SystemNode:
    """
    Representa un elemento dentro del sistema empresarial.
    """

    code: str
    name: str
    node_type: str
    area: str = ""
    description: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.code = self.code.strip().upper()
        self.name = self.name.strip()
        self.node_type = self.node_type.strip()
        self.area = self.area.strip()
        self.description = self.description.strip()

        if not self.code:
            raise ValueError("El nodo debe tener un código.")

        if not self.name:
            raise ValueError("El nodo debe tener un nombre.")

        if self.node_type not in VALID_NODE_TYPES:
            raise ValueError(
                f"Tipo de nodo no válido: {self.node_type}. "
                f"Valores permitidos: {sorted(VALID_NODE_TYPES)}"
            )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class SystemRelationship:
    """
    Representa una relación dirigida entre dos elementos empresariales.
    """

    code: str
    source_code: str
    target_code: str
    relation_type: str
    strength: str
    explanation: str
    confidence: float = 1.0
    activation_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.code = self.code.strip().upper()
        self.source_code = self.source_code.strip().upper()
        self.target_code = self.target_code.strip().upper()
        self.relation_type = self.relation_type.strip()
        self.strength = self.strength.strip()
        self.explanation = self.explanation.strip()
        self.confidence = normalize_confidence(self.confidence)
        self.activation_conditions = unique_strings(
            self.activation_conditions
        )

        if not self.code:
            raise ValueError("La relación debe tener un código.")

        if not self.source_code:
            raise ValueError("La relación debe tener un nodo de origen.")

        if not self.target_code:
            raise ValueError("La relación debe tener un nodo de destino.")

        if self.source_code == self.target_code:
            raise ValueError(
                "Una relación no puede conectar un nodo consigo mismo."
            )

        if self.relation_type not in VALID_RELATION_TYPES:
            raise ValueError(
                f"Tipo de relación no válido: {self.relation_type}. "
                f"Valores permitidos: {sorted(VALID_RELATION_TYPES)}"
            )

        if self.strength not in VALID_STRENGTHS:
            raise ValueError(
                f"Fuerza no válida: {self.strength}. "
                f"Valores permitidos: {sorted(VALID_STRENGTHS)}"
            )

        if not self.explanation:
            raise ValueError(
                "La relación debe incluir una explicación."
            )

    @property
    def strength_score(self) -> int:
        weights = {
            "Baja": 25,
            "Media": 50,
            "Alta": 75,
            "Crítica": 100,
        }
        return weights[self.strength]

    @property
    def influence_score(self) -> float:
        """
        Combina fuerza y confianza en una escala de 0 a 100.
        """
        return round(
            self.strength_score * self.confidence,
            2,
        )

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["strength_score"] = self.strength_score
        result["influence_score"] = self.influence_score
        return result


def normalize_confidence(value: float | int) -> float:
    """
    Normaliza confianza al rango 0.0–1.0.

    Acepta:
    - 0.85
    - 85
    """
    try:
        confidence = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(
            "La confianza debe ser un número."
        ) from exc

    if confidence > 1:
        confidence = confidence / 100

    if not 0 <= confidence <= 1:
        raise ValueError(
            "La confianza debe estar entre 0 y 1, "
            "o entre 0 y 100."
        )

    return round(confidence, 4)


def unique_strings(values: Iterable[str] | None) -> list[str]:
    """
    Limpia valores y elimina duplicados conservando el orden.
    """
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


def create_node(
    *,
    code: str,
    name: str,
    node_type: str,
    area: str = "",
    description: str = "",
    metadata: dict[str, Any] | None = None,
) -> SystemNode:
    return SystemNode(
        code=code,
        name=name,
        node_type=node_type,
        area=area,
        description=description,
        metadata=metadata or {},
    )


def create_relationship(
    *,
    code: str,
    source_code: str,
    target_code: str,
    relation_type: str,
    strength: str,
    explanation: str,
    confidence: float = 1.0,
    activation_conditions: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> SystemRelationship:
    return SystemRelationship(
        code=code,
        source_code=source_code,
        target_code=target_code,
        relation_type=relation_type,
        strength=strength,
        explanation=explanation,
        confidence=confidence,
        activation_conditions=activation_conditions or [],
        metadata=metadata or {},
    )


def validate_relationship_nodes(
    relationship: SystemRelationship,
    nodes: Iterable[SystemNode],
) -> bool:
    """
    Comprueba que origen y destino existan en la colección de nodos.
    """
    node_codes = {
        node.code
        for node in nodes
    }

    return (
        relationship.source_code in node_codes
        and relationship.target_code in node_codes
    )


def get_outgoing_relationships(
    node_code: str,
    relationships: Iterable[SystemRelationship],
) -> list[SystemRelationship]:
    clean_code = node_code.strip().upper()

    return [
        relationship
        for relationship in relationships
        if relationship.source_code == clean_code
    ]


def get_incoming_relationships(
    node_code: str,
    relationships: Iterable[SystemRelationship],
) -> list[SystemRelationship]:
    clean_code = node_code.strip().upper()

    return [
        relationship
        for relationship in relationships
        if relationship.target_code == clean_code
    ]


def get_connected_node_codes(
    node_code: str,
    relationships: Iterable[SystemRelationship],
) -> list[str]:
    """
    Devuelve todos los nodos directamente conectados,
    sin importar la dirección.
    """
    clean_code = node_code.strip().upper()
    connected: list[str] = []

    for relationship in relationships:
        if relationship.source_code == clean_code:
            connected.append(relationship.target_code)

        elif relationship.target_code == clean_code:
            connected.append(relationship.source_code)

    return unique_strings(connected)


def calculate_node_influence(
    node_code: str,
    relationships: Iterable[SystemRelationship],
) -> float:
    """
    Calcula la influencia saliente total de un nodo.

    Más adelante servirá para detectar problemas raíz.
    """
    outgoing = get_outgoing_relationships(
        node_code,
        relationships,
    )

    return round(
        sum(
            relationship.influence_score
            for relationship in outgoing
        ),
        2,
    )


def calculate_node_dependency(
    node_code: str,
    relationships: Iterable[SystemRelationship],
) -> float:
    """
    Calcula cuánto depende un nodo de otros elementos.
    """
    incoming = get_incoming_relationships(
        node_code,
        relationships,
    )

    return round(
        sum(
            relationship.influence_score
            for relationship in incoming
        ),
        2,
    )


def rank_root_candidates(
    nodes: Iterable[SystemNode],
    relationships: Iterable[SystemRelationship],
) -> list[dict[str, Any]]:
    """
    Ordena nodos candidatos a problema raíz.

    Un nodo con mucha influencia saliente y poca dependencia entrante
    tiene mayor probabilidad de ser una causa raíz.
    """
    node_list = list(nodes)
    relationship_list = list(relationships)

    ranking: list[dict[str, Any]] = []

    for node in node_list:
        influence = calculate_node_influence(
            node.code,
            relationship_list,
        )

        dependency = calculate_node_dependency(
            node.code,
            relationship_list,
        )

        root_score = round(
            max(influence - dependency, 0),
            2,
        )

        ranking.append(
            {
                "code": node.code,
                "name": node.name,
                "node_type": node.node_type,
                "area": node.area,
                "influence_score": influence,
                "dependency_score": dependency,
                "root_score": root_score,
            }
        )

    return sorted(
        ranking,
        key=lambda item: item["root_score"],
        reverse=True,
    )