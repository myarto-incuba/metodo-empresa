"""
Motor de grafo sistémico de Método Empresa.

Trabaja con controles, fenómenos y relaciones para identificar
nodos con mayor influencia y posibles problemas raíz.
"""

from __future__ import annotations

from collections import defaultdict, deque
from typing import Iterable

from knowledge.phenomena import BusinessPhenomenon
from knowledge.relationships import PhenomenonRelationship


def build_adjacency(
    relationships: Iterable[PhenomenonRelationship],
) -> dict[str, list[PhenomenonRelationship]]:
    graph: dict[str, list[PhenomenonRelationship]] = defaultdict(list)

    for relationship in relationships:
        graph[relationship.source_code].append(relationship)

    return dict(graph)


def calculate_influence_scores(
    phenomena: Iterable[BusinessPhenomenon],
    relationships: Iterable[PhenomenonRelationship],
) -> list[dict[str, object]]:
    phenomenon_list = list(phenomena)
    relationship_list = list(relationships)

    outgoing: dict[str, float] = defaultdict(float)
    incoming: dict[str, float] = defaultdict(float)

    for relationship in relationship_list:
        outgoing[relationship.source_code] += relationship.strength
        incoming[relationship.target_code] += relationship.strength

    ranking: list[dict[str, object]] = []

    for phenomenon in phenomenon_list:
        influence = outgoing[phenomenon.code]
        dependency = incoming[phenomenon.code]
        transversal_bonus = max(phenomenon.transversal_score - 1, 0) * 0.15

        root_score = round(
            max(influence - (dependency * 0.45), 0) + transversal_bonus,
            4,
        )

        ranking.append(
            {
                "code": phenomenon.code,
                "name": phenomenon.name,
                "areas": phenomenon.affected_areas,
                "influence": round(influence, 4),
                "dependency": round(dependency, 4),
                "transversal_score": phenomenon.transversal_score,
                "root_score": root_score,
            }
        )

    return sorted(
        ranking,
        key=lambda item: float(item["root_score"]),
        reverse=True,
    )


def trace_effects(
    start_code: str,
    relationships: Iterable[PhenomenonRelationship],
    max_depth: int = 3,
) -> list[dict[str, object]]:
    clean_code = start_code.strip().upper()
    graph = build_adjacency(relationships)

    queue: deque[tuple[str, int, float, list[str]]] = deque(
        [(clean_code, 0, 1.0, [clean_code])]
    )
    results: list[dict[str, object]] = []
    visited_depth: dict[str, int] = {clean_code: 0}

    while queue:
        current, depth, cumulative_strength, path = queue.popleft()

        if depth >= max_depth:
            continue

        for relationship in graph.get(current, []):
            next_code = relationship.target_code
            next_depth = depth + 1
            next_strength = cumulative_strength * relationship.strength
            next_path = path + [next_code]

            results.append(
                {
                    "source": relationship.source_code,
                    "target": next_code,
                    "relation_type": relationship.relation_type,
                    "depth": next_depth,
                    "cumulative_strength": round(next_strength, 4),
                    "path": next_path,
                    "explanation": relationship.explanation,
                }
            )

            previous_depth = visited_depth.get(next_code)
            if previous_depth is None or next_depth < previous_depth:
                visited_depth[next_code] = next_depth
                queue.append(
                    (
                        next_code,
                        next_depth,
                        next_strength,
                        next_path,
                    )
                )

    return sorted(
        results,
        key=lambda item: (
            int(item["depth"]),
            -float(item["cumulative_strength"]),
        ),
    )


def controls_to_phenomena(
    failed_control_codes: Iterable[str],
    phenomena: Iterable[BusinessPhenomenon],
) -> list[dict[str, object]]:
    failed = {
        code.strip().upper()
        for code in failed_control_codes
        if str(code).strip()
    }

    matches: list[dict[str, object]] = []

    for phenomenon in phenomena:
        matched_controls = sorted(
            failed.intersection(phenomenon.control_codes)
        )

        if not matched_controls:
            continue

        coverage = len(matched_controls) / len(phenomenon.control_codes)

        matches.append(
            {
                "phenomenon_code": phenomenon.code,
                "phenomenon_name": phenomenon.name,
                "matched_controls": matched_controls,
                "matched_count": len(matched_controls),
                "control_count": len(phenomenon.control_codes),
                "coverage": round(coverage, 4),
                "areas": phenomenon.affected_areas,
            }
        )

    return sorted(
        matches,
        key=lambda item: (
            -float(item["coverage"]),
            -int(item["matched_count"]),
        ),
    )
