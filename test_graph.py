from knowledge.controls import BASE_CONTROLS
from knowledge.phenomena import BASE_PHENOMENA, validate_phenomena
from knowledge.relationships import (
    PHENOMENON_RELATIONSHIPS,
    validate_phenomenon_relationships,
)
from modules.graph_engine import (
    calculate_influence_scores,
    controls_to_phenomena,
    trace_effects,
)


def main() -> None:
    control_codes = {control.code for control in BASE_CONTROLS}
    phenomenon_codes = {phenomenon.code for phenomenon in BASE_PHENOMENA}

    errors = validate_phenomena(control_codes)
    errors.extend(
        validate_phenomenon_relationships(phenomenon_codes)
    )

    assert not errors, errors
    assert len(BASE_PHENOMENA) == 10
    assert len(PHENOMENON_RELATIONSHIPS) == 12

    ranking = calculate_influence_scores(
        BASE_PHENOMENA,
        PHENOMENON_RELATIONSHIPS,
    )

    matches = controls_to_phenomena(
        ["DIR-002", "PER-001", "OPE-001", "COM-002"],
        BASE_PHENOMENA,
    )

    effects = trace_effects(
        "FEN-008",
        PHENOMENON_RELATIONSHIPS,
        max_depth=3,
    )

    assert ranking
    assert matches
    assert effects
    assert matches[0]["phenomenon_code"] in {"FEN-001", "FEN-008"}

    print("Grafo válido")
    print(f"Fenómenos: {len(BASE_PHENOMENA)}")
    print(f"Relaciones: {len(PHENOMENON_RELATIONSHIPS)}")
    print(
        "Mayor candidato a causa raíz:",
        ranking[0]["code"],
        "-",
        ranking[0]["name"],
    )
    print(
        "Fenómeno más compatible con los controles fallidos:",
        matches[0]["phenomenon_code"],
        "-",
        matches[0]["phenomenon_name"],
    )
    print(f"Efectos encontrados desde FEN-008: {len(effects)}")


if __name__ == "__main__":
    main()
