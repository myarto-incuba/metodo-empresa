from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory

from core.audit_repository import (
    create_audit,
    get_audit,
    list_audits,
    update_audit_status,
)


def main() -> None:
    with TemporaryDirectory() as temporary_directory:
        data_path = Path(temporary_directory) / "audits.json"

        assert list_audits(data_path=data_path) == []

        created = create_audit(
            company_name="Empresa Piloto",
            sector="Servicios",
            employee_count=12,
            annual_revenue=2_500_000,
            audit_date=date(2026, 7, 23),
            auditor_name="Mariana Yarto",
            data_path=data_path,
        )

        assert created.company_name == "Empresa Piloto"
        assert created.status == "Creada"
        assert created.audit_id.startswith("AUD-")

        audits = list_audits(data_path=data_path)
        assert len(audits) == 1

        found = get_audit(
            created.audit_id,
            data_path=data_path,
        )
        assert found is not None
        assert found.auditor_name == "Mariana Yarto"

        updated = update_audit_status(
            created.audit_id,
            "En proceso",
            data_path=data_path,
        )
        assert updated.status == "En proceso"

        reread = get_audit(
            created.audit_id,
            data_path=data_path,
        )
        assert reread is not None
        assert reread.status == "En proceso"

        print("Repositorio de auditorías válido")
        print("Auditoría:", reread.audit_id)
        print("Empresa:", reread.company_name)
        print("Estado:", reread.status)
        print("Archivo:", data_path)


if __name__ == "__main__":
    main()
