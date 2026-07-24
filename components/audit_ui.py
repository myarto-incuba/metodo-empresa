from __future__ import annotations

from typing import Any
import streamlit as st

from core.interview_repository import load_interview
from core.scoring_engine import calculate_results
from core.ux_repository import load_action_plan, load_evidence


def apply_product_style() -> None:
    return None


def audit_progress(audit_id: str) -> dict[str, float]:
    interview = load_interview(audit_id)
    results = calculate_results(interview)
    evidence = load_evidence(audit_id)
    plan = load_action_plan(audit_id)
    evidence_done = sum(1 for row in evidence if row.get("status") in {"Disponible", "No aplica"})
    plan_done = sum(1 for row in plan if row.get("status") == "Completada")
    return {
        "interview": float(results.get("progress", 0.0)),
        "evidence": evidence_done / len(evidence) if evidence else 0.0,
        "diagnosis": 1.0 if results.get("answered", 0) else 0.0,
        "plan": plan_done / len(plan) if plan else 0.0,
    }


def render_audit_header(audit: Any) -> None:
    name, meta, status = st.columns([2.4, 2, 1], vertical_alignment="center")
    name.markdown(f"### {getattr(audit, 'company_name', 'Empresa')}")
    name.caption(getattr(audit, "sector", "Sin sector") or "Sin sector")
    meta.caption("SESIÓN")
    meta.write(f"{getattr(audit, 'audit_date', '—')} · {getattr(audit, 'auditor_name', '—') or '—'}")
    status.caption("ESTADO")
    status.write(getattr(audit, "status", "Creada"))
    st.divider()
