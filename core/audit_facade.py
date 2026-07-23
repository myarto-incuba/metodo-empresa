from __future__ import annotations

from datetime import date
import inspect
from typing import Any

from core import audit_repository


def list_audits() -> list[Any]:
    return list(audit_repository.list_audits())


def get_audit(audit_id: str) -> Any | None:
    getter = getattr(audit_repository, "get_audit", None)
    if getter:
        return getter(audit_id)
    for audit in list_audits():
        if getattr(audit, "audit_id", None) == audit_id:
            return audit
    return None


def create_audit_compatible(
    company_name: str,
    sector: str,
    auditor_name: str,
    audit_date: str | None = None,
) -> Any:
    creator = getattr(audit_repository, "create_audit")
    signature = inspect.signature(creator)
    today = audit_date or date.today().isoformat()

    aliases = {
        "company_name": company_name,
        "empresa": company_name,
        "name": company_name,
        "sector": sector,
        "industry": sector,
        "employee_count": None,
        "annual_revenue": None,
        "auditor_name": auditor_name,
        "auditor": auditor_name,
        "audit_date": today,
        "date": today,
        "fecha": today,
    }

    kwargs = {}
    missing = []
    for name, parameter in signature.parameters.items():
        if name in aliases:
            kwargs[name] = aliases[name]
        elif parameter.default is inspect.Parameter.empty:
            missing.append(name)

    if missing:
        raise TypeError(
            "La función create_audit requiere campos no reconocidos: "
            + ", ".join(missing)
        )
    return creator(**kwargs)
