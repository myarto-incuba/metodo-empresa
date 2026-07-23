from knowledge.catalog import (
    KnowledgeEntityType,
    build_base_catalog,
)
from knowledge.controls import BASE_CONTROLS
from knowledge.phenomena import BASE_PHENOMENA
from knowledge.relationships import PHENOMENON_RELATIONSHIPS


def main() -> None:
    catalog = build_base_catalog(
        controls=BASE_CONTROLS,
        phenomena=BASE_PHENOMENA,
        relationships=PHENOMENON_RELATIONSHIPS,
    )

    catalog.assert_valid()

    assert catalog.count(KnowledgeEntityType.CONTROL) == 15
    assert catalog.count(KnowledgeEntityType.PHENOMENON) == 10
    assert catalog.count(KnowledgeEntityType.RELATIONSHIP) == 12
    assert catalog.count() == 37

    summary = catalog.summary()
    exported = catalog.export()

    assert summary["control"] == 15
    assert summary["phenomenon"] == 10
    assert summary["relationship"] == 12
    assert len(exported["control"]) == 15

    print("Catálogo central válido")
    print("Entidades totales:", catalog.count())
    print("Controles:", summary["control"])
    print("Fenómenos:", summary["phenomenon"])
    print("Relaciones:", summary["relationship"])
    print("Errores de validación:", len(catalog.validate()))


if __name__ == "__main__":
    main()
