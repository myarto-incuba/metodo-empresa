"""
Modelos de conocimiento empresarial para Método Empresa.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Iterable


class ControlImportance(str, Enum):
    BAJA = "Baja"
    MEDIA = "Media"
    ALTA = "Alta"
    CRITICA = "Crítica"


@dataclass(frozen=True)
class EvidenceRequirement:
    name: str
    description: str = ""
    required: bool = False
    acceptable_formats: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("La evidencia debe tener un nombre.")


@dataclass(frozen=True)
class InterviewQuestion:
    code: str
    text: str
    purpose: str = ""
    respondent_roles: tuple[str, ...] = ()
    evidence_prompts: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.code.strip():
            raise ValueError("La pregunta debe tener un código.")
        if not self.text.strip():
            raise ValueError("La pregunta debe contener texto.")


@dataclass
class Control:
    code: str
    name: str
    area: str
    objective: str
    description: str = ""
    importance: ControlImportance = ControlImportance.MEDIA
    expected_evidence: list[EvidenceRequirement] = field(default_factory=list)
    interview_questions: list[InterviewQuestion] = field(default_factory=list)
    related_controls: list[str] = field(default_factory=list)
    related_phenomena: list[str] = field(default_factory=list)
    generated_risks: list[str] = field(default_factory=list)
    suggested_actions: list[str] = field(default_factory=list)
    indicators: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.code = self.code.strip().upper()
        self.name = self.name.strip()
        self.area = self.area.strip()
        self.objective = self.objective.strip()
        self.description = self.description.strip()
        self.related_controls = _unique_codes(self.related_controls)
        self.related_phenomena = _unique_strings(self.related_phenomena)
        self.generated_risks = _unique_strings(self.generated_risks)
        self.suggested_actions = _unique_strings(self.suggested_actions)
        self.indicators = _unique_strings(self.indicators)
        self.tags = _unique_strings(self.tags)

        if not self.code:
            raise ValueError("El control debe tener un código.")
        if not self.name:
            raise ValueError("El control debe tener un nombre.")
        if not self.area:
            raise ValueError("El control debe pertenecer a un área.")
        if not self.objective:
            raise ValueError("El control debe tener un objetivo.")

        if isinstance(self.importance, str):
            self.importance = ControlImportance(self.importance)

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["importance"] = self.importance.value
        return result

    @property
    def is_transversal(self) -> bool:
        return len(self.related_controls) >= 2 or len(self.related_phenomena) >= 2


def _unique_strings(values: Iterable[str] | None) -> list[str]:
    if not values:
        return []

    result: list[str] = []
    seen: set[str] = set()

    for value in values:
        clean = str(value).strip()
        if not clean:
            continue

        key = clean.casefold()
        if key in seen:
            continue

        seen.add(key)
        result.append(clean)

    return result


def _unique_codes(values: Iterable[str] | None) -> list[str]:
    return [value.upper() for value in _unique_strings(values)]
