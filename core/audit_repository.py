"""
Persistencia local de empresas y auditorías para el MVP de Método Empresa.

Los datos se guardan en JSON para permitir la primera prueba con una empresa
sin introducir todavía una base de datos.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date, datetime, timezone
import json
from pathlib import Path
from typing import Any
from uuid import uuid4


DEFAULT_DATA_PATH = Path("data/audits.json")


@dataclass(frozen=True)
class Audit:
    audit_id: str
    company_name: str
    sector: str
    employee_count: int | None
    annual_revenue: float | None
    audit_date: str
    auditor_name: str
    status: str
    created_at: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Audit":
        return cls(
            audit_id=str(data["audit_id"]),
            company_name=str(data["company_name"]),
            sector=str(data.get("sector", "")),
            employee_count=_optional_int(data.get("employee_count")),
            annual_revenue=_optional_float(data.get("annual_revenue")),
            audit_date=str(data["audit_date"]),
            auditor_name=str(data.get("auditor_name", "")),
            status=str(data.get("status", "Creada")),
            created_at=str(data["created_at"]),
        )


def create_audit(
    *,
    company_name: str,
    sector: str,
    employee_count: int | None,
    annual_revenue: float | None,
    audit_date: date | str,
    auditor_name: str,
    data_path: Path | str = DEFAULT_DATA_PATH,
) -> Audit:
    company_name = company_name.strip()
    sector = sector.strip()
    auditor_name = auditor_name.strip()

    if not company_name:
        raise ValueError("El nombre de la empresa es obligatorio.")

    if not auditor_name:
        raise ValueError("El nombre del auditor es obligatorio.")

    if employee_count is not None and employee_count < 0:
        raise ValueError("El número de empleados no puede ser negativo.")

    if annual_revenue is not None and annual_revenue < 0:
        raise ValueError("La facturación anual no puede ser negativa.")

    normalized_date = (
        audit_date.isoformat()
        if isinstance(audit_date, date)
        else str(audit_date)
    )

    audit = Audit(
        audit_id=f"AUD-{uuid4().hex[:10].upper()}",
        company_name=company_name,
        sector=sector,
        employee_count=employee_count,
        annual_revenue=annual_revenue,
        audit_date=normalized_date,
        auditor_name=auditor_name,
        status="Creada",
        created_at=datetime.now(timezone.utc).isoformat(),
    )

    audits = list_audits(data_path=data_path)
    audits.append(audit)
    _write_audits(audits, data_path=data_path)
    return audit


def list_audits(
    *,
    data_path: Path | str = DEFAULT_DATA_PATH,
) -> list[Audit]:
    path = Path(data_path)

    if not path.exists():
        return []

    try:
        raw_data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"El archivo {path} contiene JSON inválido."
        ) from exc

    if not isinstance(raw_data, list):
        raise ValueError(
            f"El archivo {path} debe contener una lista de auditorías."
        )

    audits = [Audit.from_dict(item) for item in raw_data]
    return sorted(
        audits,
        key=lambda audit: audit.created_at,
        reverse=True,
    )


def get_audit(
    audit_id: str,
    *,
    data_path: Path | str = DEFAULT_DATA_PATH,
) -> Audit | None:
    normalized_id = audit_id.strip().upper()

    for audit in list_audits(data_path=data_path):
        if audit.audit_id.upper() == normalized_id:
            return audit

    return None


def update_audit_status(
    audit_id: str,
    status: str,
    *,
    data_path: Path | str = DEFAULT_DATA_PATH,
) -> Audit:
    status = status.strip()
    if not status:
        raise ValueError("El estado no puede estar vacío.")

    audits = list_audits(data_path=data_path)
    updated: Audit | None = None
    new_audits: list[Audit] = []

    for audit in audits:
        if audit.audit_id.upper() == audit_id.strip().upper():
            updated = Audit(
                audit_id=audit.audit_id,
                company_name=audit.company_name,
                sector=audit.sector,
                employee_count=audit.employee_count,
                annual_revenue=audit.annual_revenue,
                audit_date=audit.audit_date,
                auditor_name=audit.auditor_name,
                status=status,
                created_at=audit.created_at,
            )
            new_audits.append(updated)
        else:
            new_audits.append(audit)

    if updated is None:
        raise KeyError(f"No existe la auditoría {audit_id}.")

    _write_audits(new_audits, data_path=data_path)
    return updated


def _write_audits(
    audits: list[Audit],
    *,
    data_path: Path | str,
) -> None:
    path = Path(data_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    temporary_path = path.with_suffix(path.suffix + ".tmp")
    payload = [asdict(audit) for audit in audits]
    temporary_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    temporary_path.replace(path)


def _optional_int(value: Any) -> int | None:
    if value in (None, ""):
        return None
    return int(value)


def _optional_float(value: Any) -> float | None:
    if value in (None, ""):
        return None
    return float(value)
