from __future__ import annotations

import html
import streamlit as st

from components.audit_ui import render_audit_header
from components.brand import render_footer, render_wordmark
from core.audit_facade import get_audit
from core.interview_repository import load_interview
from core.scoring_engine import calculate_results
from core.ux_repository import load_action_plan
from knowledge.interview_questions import QUESTIONS_BY_CODE


audit_id = st.session_state.get("active_audit_id")
audit = get_audit(audit_id) if audit_id else None
if audit is None:
    st.warning("Selecciona una auditoría desde Auditorías.")
    st.stop()

render_wordmark()
render_audit_header(audit)

interview = load_interview(audit_id)
answers = interview.get("answers", {})
results = calculate_results(interview)

st.markdown('<div class="inc-eyebrow">Diagnóstico ejecutivo</div>', unsafe_allow_html=True)
st.title("La historia detrás de la empresa")
st.caption("Madurez, tensiones, fortalezas y prioridades en una sola lectura.")

if not answers:
    st.info("Completa algunas respuestas para generar el diagnóstico.")
    st.stop()

area_scores = results.get("area_scores", {})
weakest = sorted(area_scores.items(), key=lambda x: x[1])[:2]
strongest = sorted(area_scores.items(), key=lambda x: x[1], reverse=True)[:2]
hypotheses = results.get("hypotheses", [])
main = hypotheses[0] if hypotheses else {"name":"Sin hipótesis dominante","confidence":0}

weak_text = " y ".join(f"{a} ({s}%)" for a,s in weakest) if weakest else "Por definir"
strong_text = " y ".join(f"{a} ({s}%)" for a,s in strongest) if strongest else "Por definir"

st.markdown(
    f"""
    <div class="inc-diagnosis-grid">
      <div class="inc-diagnosis-card primary">
        <div class="inc-metric-kicker">Madurez general</div>
        <div class="inc-score">{results['overall_score']}%</div>
        <div class="inc-metric-label">{html.escape(str(results['maturity']))}</div>
      </div>
      <div class="inc-diagnosis-card">
        <div class="inc-metric-kicker">Patrón dominante</div>
        <h2>{html.escape(main['name'])}</h2>
        <div class="inc-pill">{main['confidence']}% de intensidad</div>
      </div>
      <div class="inc-diagnosis-card">
        <div class="inc-metric-kicker">Foco de intervención</div>
        <h2>{html.escape(weak_text)}</h2>
        <div class="inc-metric-label">Áreas con menor madurez relativa</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="inc-section-title">Mapa de madurez</div>', unsafe_allow_html=True)
rows = []
for area in ["Dirección","Finanzas","Comercial","Operaciones","Personas"]:
    score = area_scores.get(area)
    val = int(score) if score is not None else 0
    shown = f"{score}%" if score is not None else "—"
    rows.append(f"""
      <div class="inc-area-row">
        <div>{area}</div>
        <div class="inc-area-track"><div class="inc-area-fill" style="width:{val}%"></div></div>
        <div style="text-align:right;font-weight:850">{shown}</div>
      </div>
    """)
st.markdown(
    '<div class="inc-diagnosis-card">' + "".join(rows) + '</div>',
    unsafe_allow_html=True,
)

tab1,tab2,tab3,tab4 = st.tabs(["Historia ejecutiva","Hallazgos","Hipótesis","Plan 90 días"])

with tab1:
    st.write(f"Las mayores oportunidades están en **{weak_text}**.")
    st.write(f"Las bases más sólidas están en **{strong_text}**.")
    for i,rec in enumerate(results.get("recommendations",[])[:5],1):
        with st.container(border=True):
            st.caption(f"PRIORIDAD {i}")
            st.write(f"**{rec}**")

with tab2:
    findings=[]; strengths=[]
    for code,ans in answers.items():
        q=QUESTIONS_BY_CODE.get(code)
        if not q: continue
        row=(q.area,q.text,ans.get("comment",""),ans.get("evidence_notes",""))
        if ans.get("answer") in {"No","Parcialmente"}: findings.append(row)
        elif ans.get("answer")=="Sí": strengths.append(row)
    c1,c2=st.columns(2)
    with c1:
        st.subheader("Tensiones")
        for area,text,comment,evidence in findings:
            with st.container(border=True):
                st.caption(area.upper()); st.write(f"**{text}**")
                if comment: st.write(comment)
                if evidence: st.caption(f"Evidencia: {evidence}")
    with c2:
        st.subheader("Fortalezas")
        for area,text,comment,evidence in strengths[:10]:
            with st.container(border=True):
                st.caption(area.upper()); st.write(f"**{text}**")
                if comment: st.write(comment)

with tab3:
    for i,h in enumerate(hypotheses,1):
        with st.container(border=True):
            c1,c2=st.columns([3,1])
            c1.caption(f"HIPÓTESIS {i}")
            c1.subheader(h["name"])
            c2.metric("Intensidad",f'{h["confidence"]}%')
            st.progress(h["confidence"]/100)

with tab4:
    plan=load_action_plan(audit_id)
    if not plan:
        st.info("El plan de 90 días todavía no ha sido formalizado.")
        if st.button("Construir plan de acción",type="primary"):
            st.switch_page("views/action_plan.py")
    else:
        for row in plan:
            with st.container(border=True):
                st.subheader(row.get("action","Acción"))
                st.caption(f'{row.get("priority","Media")} · {row.get("deadline","Por definir")}')
                st.write(f'**Responsable:** {row.get("owner","Por definir")} · **Estado:** {row.get("status","Pendiente")}')

render_footer()
