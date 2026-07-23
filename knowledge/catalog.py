"""
Catálogo central de conocimiento de Método Empresa.

Este módulo no reemplaza controls.py, phenomena.py ni relationships.py.
Los organiza en un catálogo único, valida consistencia y prepara la base
para incorporar indicadores, preguntas, riesgos y recomendaciones.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, is_dataclass
from enum import Enum
from typing import Any, Iterable, Mapping


class KnowledgeEntityType(str, Enum):
    CONTROL = "control"
    PHENOMENON = "phenomenon"
    RELATIONSHIP = "relationship"
    INDICATOR = "indicator"
    QUESTION = "question"
    RECOMMENDATION = "recommendation"
    RISK = "risk"
    MATURITY_LEVEL = "maturity_level"


@dataclass(frozen=True)
class KnowledgeReference:
    entity_type: KnowledgeEntityType
    code: str


@dataclass
class CatalogValidationIssue:
    severity: str
    message: str
    entity_type: str | None = None
    entity_code: str | None = None


@dataclass
class KnowledgeCatalog:
    """
    Registro central de entidades de conocimiento.

    Cada colección se indexa por código y puede contener dataclasses,
    diccionarios u objetos con atributos.
    """

    entities: dict[KnowledgeEntityType, dict[str, Any]] = field(
        default_factory=lambda: {
            entity_type: {}
            for entity_type in KnowledgeEntityType
        }
    )

    def register(
        self,
        entity_type: KnowledgeEntityType,
        entity: Any,
        *,
        replace: bool = False,
    ) -> str:
        code = _extract_code(entity)

        if not code:
            raise ValueError(
                f"La entidad de tipo {entity_type.value} no tiene código."
            )

        normalized_code = code.strip().upper()
        bucket = self.entities[entity_type]

        if normalized_code in bucket and not replace:
            raise ValueError(
                f"Ya existe {entity_type.value} con código {normalized_code}."
            )

        bucket[normalized_code] = entity
        return normalized_code

    def register_many(
        self,
        entity_type: KnowledgeEntityType,
        entities: Iterable[Any],
        *,
        replace: bool = False,
    ) -> list[str]:
        return [
            self.register(entity_type, entity, replace=replace)
            for entity in entities
        ]

    def get(
        self,
        entity_type: KnowledgeEntityType,
        code: str,
    ) -> Any | None:
        return self.entities[entity_type].get(code.strip().upper())

    def require(
        self,
        entity_type: KnowledgeEntityType,
        code: str,
    ) -> Any:
        entity = self.get(entity_type, code)
        if entity is None:
            raise KeyError(
                f"No existe {entity_type.value} con código {code}."
            )
        return entity

    def list(
        self,
        entity_type: KnowledgeEntityType,
    ) -> list[Any]:
        return list(self.entities[entity_type].values())

    def count(
        self,
        entity_type: KnowledgeEntityType | None = None,
    ) -> int:
        if entity_type is not None:
            return len(self.entities[entity_type])

        return sum(len(bucket) for bucket in self.entities.values())

    def codes(
        self,
        entity_type: KnowledgeEntityType,
    ) -> set[str]:
        return set(self.entities[entity_type])

    def summary(self) -> dict[str, int]:
        return {
            entity_type.value: len(self.entities[entity_type])
            for entity_type in KnowledgeEntityType
        }

    def validate(self) -> list[CatalogValidationIssue]:
        issues: list[CatalogValidationIssue] = []

        for entity_type, bucket in self.entities.items():
            for code, entity in bucket.items():
                name = _extract_name(entity)
                if not name:
                    issues.append(
                        CatalogValidationIssue(
                            severity="error",
                            message="La entidad no tiene nombre.",
                            entity_type=entity_type.value,
                            entity_code=code,
                        )
                    )

                embedded_code = _extract_code(entity)
                if embedded_code and embedded_code.strip().upper() != code:
                    issues.append(
                        CatalogValidationIssue(
                            severity="error",
                            message=(
                                "El código interno de la entidad no coincide "
                                "con el índice del catálogo."
                            ),
                            entity_type=entity_type.value,
                            entity_code=code,
                        )
                    )

        issues.extend(self._validate_relationship_references())
        return issues

    def assert_valid(self) -> None:
        issues = self.validate()
        errors = [
            issue
            for issue in issues
            if issue.severity.lower() == "error"
        ]

        if errors:
            detail = "\n".join(
                f"- [{issue.entity_type}:{issue.entity_code}] "
                f"{issue.message}"
                for issue in errors
            )
            raise ValueError(
                "El catálogo de conocimiento contiene errores:\n"
                f"{detail}"
            )

    def export(self) -> dict[str, list[dict[str, Any]]]:
        return {
            entity_type.value: [
                _to_dict(entity)
                for entity in bucket.values()
            ]
            for entity_type, bucket in self.entities.items()
        }

    def _validate_relationship_references(
        self,
    ) -> list[CatalogValidationIssue]:
        issues: list[CatalogValidationIssue] = []
        phenomenon_codes = self.codes(
            KnowledgeEntityType.PHENOMENON
        )

        for relationship_code, relationship in self.entities[
            KnowledgeEntityType.RELATIONSHIP
        ].items():
            source = _extract_first(
                relationship,
                "source_code",
                "source",
                "from_code",
                "origin_code",
            )
            target = _extract_first(
                relationship,
                "target_code",
                "target",
                "to_code",
                "destination_code",
            )

            if source and str(source).upper() not in phenomenon_codes:
                issues.append(
                    CatalogValidationIssue(
                        severity="error",
                        message=(
                            f"El fenómeno origen {source} no existe "
                            "en el catálogo."
                        ),
                        entity_type=KnowledgeEntityType.RELATIONSHIP.value,
                        entity_code=relationship_code,
                    )
                )

            if target and str(target).upper() not in phenomenon_codes:
                issues.append(
                    CatalogValidationIssue(
                        severity="error",
                        message=(
                            f"El fenómeno destino {target} no existe "
                            "en el catálogo."
                        ),
                        entity_type=KnowledgeEntityType.RELATIONSHIP.value,
                        entity_code=relationship_code,
                    )
                )

        return issues


def build_base_catalog(
    *,
    controls: Iterable[Any] = (),
    phenomena: Iterable[Any] = (),
    relationships: Iterable[Any] = (),
) -> KnowledgeCatalog:
    catalog = KnowledgeCatalog()
    catalog.register_many(
        KnowledgeEntityType.CONTROL,
        controls,
    )
    catalog.register_many(
        KnowledgeEntityType.PHENOMENON,
        phenomena,
    )

    for index, relationship in enumerate(relationships, start=1):
        try:
            catalog.register(
                KnowledgeEntityType.RELATIONSHIP,
                relationship,
            )
        except ValueError as exc:
            if "no tiene código" not in str(exc):
                raise

            generated_code = f"REL-{index:03d}"
            wrapped = _relationship_with_generated_code(
                relationship,
                generated_code,
            )
            catalog.register(
                KnowledgeEntityType.RELATIONSHIP,
                wrapped,
            )

    return catalog


def _extract_code(entity: Any) -> str | None:
    value = _extract_first(
        entity,
        "code",
        "id",
        "control_code",
        "phenomenon_code",
        "relationship_code",
    )
    return str(value) if value is not None else None


def _extract_name(entity: Any) -> str | None:
    value = _extract_first(
        entity,
        "name",
        "title",
        "label",
        "description",
        "relationship_type",
        "type",
    )
    return str(value) if value is not None else None


def _extract_first(
    entity: Any,
    *keys: str,
) -> Any | None:
    if isinstance(entity, Mapping):
        for key in keys:
            if key in entity:
                return entity[key]
        return None

    for key in keys:
        if hasattr(entity, key):
            return getattr(entity, key)

    return None


def _to_dict(entity: Any) -> dict[str, Any]:
    if is_dataclass(entity):
        return asdict(entity)

    if isinstance(entity, Mapping):
        return dict(entity)

    if hasattr(entity, "__dict__"):
        return dict(vars(entity))

    return {"value": entity}


def _relationship_with_generated_code(
    relationship: Any,
    generated_code: str,
) -> dict[str, Any]:
    data = _to_dict(relationship)
    data["code"] = generated_code

    if not _extract_name(data):
        data["name"] = (
            f"{data.get('source_code', data.get('source', 'origen'))}"
            " → "
            f"{data.get('target_code', data.get('target', 'destino'))}"
        )

    return data
