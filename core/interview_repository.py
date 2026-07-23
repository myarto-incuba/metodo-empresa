"""Persistencia de respuestas y observaciones de auditoría."""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any


DEFAULT_INTERVIEW_PATH = Path("data/interviews.json")


def load_interview(
    audit_id: str,
    *,
    data_path: Path | str = DEFAULT_INTERVIEW_PATH,
) -> dict[str, Any]:
    data = _read_all(data_path)
    return data.get(
        audit_id,
        {
            "audit_id": audit_id,
            "answers": {},
            "observations": [],
            "updated_at": None,
        },
    )


def save_answer(
    audit_id: str,
    question_code: str,
    answer: str,
    comment: str = "",
    evidence_notes: str = "",
    *,
    data_path: Path | str = DEFAULT_INTERVIEW_PATH,
) -> None:
    if answer not in {"Sí", "Parcialmente", "No", "No aplica"}:
        raise ValueError("Respuesta no válida.")

    data = _read_all(data_path)
    interview = data.setdefault(
        audit_id,
        {"audit_id": audit_id, "answers": {}, "observations": []},
    )
    interview["answers"][question_code] = {
        "answer": answer,
        "comment": comment.strip(),
        "evidence_notes": evidence_notes.strip(),
        "updated_at": _now(),
    }
    interview["updated_at"] = _now()
    _write_all(data, data_path)


def add_observation(
    audit_id: str,
    text: str,
    question_code: str | None = None,
    *,
    data_path: Path | str = DEFAULT_INTERVIEW_PATH,
) -> None:
    text = text.strip()
    if not text:
        raise ValueError("La observación no puede estar vacía.")

    data = _read_all(data_path)
    interview = data.setdefault(
        audit_id,
        {"audit_id": audit_id, "answers": {}, "observations": []},
    )
    interview["observations"].append(
        {
            "text": text,
            "question_code": question_code,
            "created_at": _now(),
        }
    )
    interview["updated_at"] = _now()
    _write_all(data, data_path)


def _read_all(data_path: Path | str) -> dict[str, Any]:
    path = Path(data_path)
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON inválido en {path}.") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"{path} debe contener un objeto JSON.")
    return payload


def _write_all(data: dict[str, Any], data_path: Path | str) -> None:
    path = Path(data_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    temporary.replace(path)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
