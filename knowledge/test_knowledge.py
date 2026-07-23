from knowledge.controls import (
    BASE_CONTROLS,
    get_control,
    get_controls_by_area,
    validate_control_library,
)


def main() -> None:
    errors = validate_control_library()

    assert not errors, errors
    assert len(BASE_CONTROLS) == 15
    assert get_control("DIR-002") is not None
    assert len(get_controls_by_area("Finanzas")) == 3

    transversal = [control.code for control in BASE_CONTROLS if control.is_transversal]

    print("Biblioteca válida")
    print(f"Controles: {len(BASE_CONTROLS)}")
    print(f"Áreas: {sorted({control.area for control in BASE_CONTROLS})}")
    print(f"Controles transversales: {len(transversal)}")


if __name__ == "__main__":
    main()
