from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("data/ux_data.json")


DEFAULT_EVIDENCE = (
    ("Dirección", "Plan estratégico u objetivos anuales"),
    ("Dirección", "Organigrama y responsabilidades"),
    ("Finanzas", "Estado de resultados"),
    ("Finanzas", "Flujo de efectivo o presupuesto"),
    ("Comercial", "Base de clientes o CRM"),
    ("Comercial", "Reporte de ventas"),
    ("Operaciones", "Checklist o proceso de eventos"),
    ("Operaciones", "Ejemplo de cronograma de proyecto"),
    ("Personas", "Descripciones de puesto"),
    ("Personas", "Indicadores o evaluaciones del equipo"),
)


def load_evidence(audit_id: str) -> list[dict[str, Any]]:
    data = _read()
    audit = data.setdefault(audit_id, {})
    if "evidence" not in audit:
        audit["evidence"] = [
            {
                "area": area,
                "name": name,
                "status": "Pendiente",
                "notes": "",
            }
            for area, name in DEFAULT_EVIDENCE
        ]
        _write(data)
    return audit["evidence"]


def save_evidence(audit_id: str, rows: list[dict[str, Any]]) -> None:
    data = _read()
    audit = data.setdefault(audit_id, {})
    audit["evidence"] = rows
    audit["updated_at"] = _now()
    _write(data)


def load_action_plan(audit_id: str) -> list[dict[str, Any]]:
    return _read().get(audit_id, {}).get("action_plan", [])


def save_action_plan(audit_id: str, rows: list[dict[str, Any]]) -> None:
    data = _read()
    audit = data.setdefault(audit_id, {})
    audit["action_plan"] = rows
    audit["updated_at"] = _now()
    _write(data)


def _read() -> dict[str, Any]:
    if not DATA_PATH.exists():
        return {}
    try:
        payload = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON inválido en {DATA_PATH}") from exc
    return payload if isinstance(payload, dict) else {}


def _write(data: dict[str, Any]) -> None:
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    temporary = DATA_PATH.with_suffix(".tmp")
    temporary.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    temporary.replace(DATA_PATH)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
