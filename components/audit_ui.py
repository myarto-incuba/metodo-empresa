from __future__ import annotations

from typing import Any
import html

import streamlit as st

from core.interview_repository import load_interview
from core.scoring_engine import calculate_results


def apply_product_style() -> None:
    # Kept as a compatibility hook. The visual system lives in brand.py.
    return None


def audit_progress(audit_id: str) -> dict[str, float]:
    interview = load_interview(audit_id)
    results = calculate_results(interview)
    interview_progress = float(results.get("progress", 0.0))
    evidence_progress = _evidence_progress(audit_id)
    diagnosis_progress = 1.0 if results.get("answered", 0) else 0.0
    plan_progress = _plan_progress(audit_id)

    overall = (
        0.10
        + interview_progress * 0.40
        + evidence_progress * 0.20
        + diagnosis_progress * 0.15
        + plan_progress * 0.15
    )
    return {
        "Datos": 1.0,
        "Conversación": interview_progress,
        "Evidencias": evidence_progress,
        "Diagnóstico": diagnosis_progress,
        "Plan": plan_progress,
        "overall": min(overall, 1.0),
    }


def render_audit_header(audit: Any) -> None:
    audit_id = getattr(audit, "audit_id", "")
    progress = audit_progress(audit_id)
    company = html.escape(str(getattr(audit, "company_name", "Empresa")))
    sector = html.escape(str(getattr(audit, "sector", "") or "Sector no indicado"))
    auditor = html.escape(str(getattr(audit, "auditor_name", "") or "Sin auditor asignado"))
    status = html.escape(str(getattr(audit, "status", "") or "En proceso"))
    overall = round(progress["overall"] * 100)

    steps = []
    for step in ["Datos", "Conversación", "Evidencias", "Diagnóstico", "Plan"]:
        steps.append(
            f"""
            <div class="inc-step">
                <div class="inc-step-name">{step}</div>
                <div class="inc-step-value">{round(progress[step] * 100)}%</div>
            </div>
            """
        )

    st.markdown(
        f"""
        <section class="inc-workspace">
            <div class="inc-eyebrow">Expediente activo</div>
            <div class="inc-workspace-company">{company}</div>
            <div class="inc-workspace-meta">
                {sector} · Auditor: {auditor} · {status}
            </div>
            <div class="inc-progress-track">
                <div class="inc-progress-fill" style="width:{overall}%"></div>
            </div>
            <div class="inc-workspace-meta">Avance integral · {overall}%</div>
            <div class="inc-steps">{''.join(steps)}</div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(4)
    targets = [
        ("Conversación", "views/interview.py"),
        ("Evidencias", "views/evidence.py"),
        ("Diagnóstico", "views/diagnosis.py"),
        ("Plan de acción", "views/action_plan.py"),
    ]
    for col, (label, target) in zip(cols, targets):
        if col.button(label, key=f"workspace-{audit_id}-{label}", use_container_width=True):
            st.switch_page(target)


def _evidence_progress(audit_id: str) -> float:
    try:
        from core.ux_repository import load_evidence
        rows = load_evidence(audit_id)
    except Exception:
        return 0.0
    if not rows:
        return 0.0
    complete = sum(
        1 for row in rows if row.get("status") in {"Disponible", "No aplica"}
    )
    return complete / len(rows)


def _plan_progress(audit_id: str) -> float:
    try:
        from core.ux_repository import load_action_plan
        rows = load_action_plan(audit_id)
    except Exception:
        return 0.0
    if not rows:
        return 0.0
    completed = sum(1 for row in rows if row.get("status") == "Completada")
    if completed:
        return min(0.5 + completed / len(rows) * 0.5, 1.0)
    return 0.5
