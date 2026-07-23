from __future__ import annotations

from typing import Any

import streamlit as st

from core.interview_repository import load_interview
from core.scoring_engine import calculate_results


def apply_product_style() -> None:
    st.markdown(
        """
        <style>
        .block-container {
            max-width: 1320px;
            padding-top: 2rem;
            padding-bottom: 4rem;
        }
        [data-testid="stSidebar"] {
            border-right: 1px solid rgba(128, 128, 128, 0.18);
        }
        .me-kicker {
            font-size: .78rem;
            letter-spacing: .12em;
            text-transform: uppercase;
            opacity: .62;
            margin-bottom: .35rem;
        }
        .me-title {
            font-size: 2rem;
            font-weight: 760;
            line-height: 1.1;
            margin-bottom: .25rem;
        }
        .me-subtitle {
            opacity: .7;
            margin-bottom: 1rem;
        }
        .me-card {
            border: 1px solid rgba(128, 128, 128, 0.22);
            border-radius: 16px;
            padding: 1rem 1.15rem;
            margin-bottom: .8rem;
            background: rgba(128, 128, 128, 0.035);
        }
        .me-step {
            font-size: .78rem;
            text-transform: uppercase;
            letter-spacing: .06em;
            opacity: .66;
        }
        .me-step-value {
            font-size: 1.05rem;
            font-weight: 700;
        }
        .me-muted {
            opacity: .67;
        }
        div[data-testid="stMetric"] {
            border: 1px solid rgba(128, 128, 128, 0.20);
            border-radius: 14px;
            padding: .8rem 1rem;
            background: rgba(128, 128, 128, 0.025);
        }
        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 16px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def audit_label(audit: Any) -> str:
    company = getattr(audit, "company_name", "Empresa")
    audit_id = getattr(audit, "audit_id", "")
    return f"{company} · {audit_id}"


def render_audit_selector(audits: list[Any], key: str) -> Any | None:
    if not audits:
        st.info("Primero crea una auditoría.")
        return None

    options = {audit_label(audit): audit for audit in audits}
    active_id = st.session_state.get("active_audit_id")
    labels = list(options)
    index = 0

    for position, label in enumerate(labels):
        if getattr(options[label], "audit_id", None) == active_id:
            index = position
            break

    selected = st.selectbox(
        "Auditoría activa",
        labels,
        index=index,
        key=key,
    )
    audit = options[selected]
    st.session_state.active_audit_id = getattr(audit, "audit_id", None)
    return audit


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
        "Entrevista": interview_progress,
        "Evidencias": evidence_progress,
        "Diagnóstico": diagnosis_progress,
        "Plan": plan_progress,
        "overall": min(overall, 1.0),
    }


def render_audit_header(audit: Any) -> None:
    audit_id = getattr(audit, "audit_id", "")
    progress = audit_progress(audit_id)
    company = getattr(audit, "company_name", "Empresa")
    sector = getattr(audit, "sector", "") or "Sector no indicado"
    auditor = getattr(audit, "auditor_name", "") or "Sin auditor asignado"
    status = getattr(audit, "status", "") or "En proceso"

    st.markdown('<div class="me-kicker">Auditoría activa</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="me-title">{company}</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="me-subtitle">{sector} · Auditor: {auditor} · Estado: {status}</div>',
        unsafe_allow_html=True,
    )

    columns = st.columns(5)
    for column, step in zip(columns, ["Datos", "Entrevista", "Evidencias", "Diagnóstico", "Plan"]):
        value = progress[step]
        with column:
            st.markdown(f'<div class="me-step">{step}</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="me-step-value">{round(value * 100)}%</div>',
                unsafe_allow_html=True,
            )
            st.progress(value)

    st.caption(f"Avance integral de la auditoría: {round(progress['overall'] * 100)}%")
    st.divider()


def _evidence_progress(audit_id: str) -> float:
    try:
        from core.ux_repository import load_evidence
        rows = load_evidence(audit_id)
    except Exception:
        return 0.0
    if not rows:
        return 0.0
    complete = sum(1 for row in rows if row.get("status") == "Disponible")
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
