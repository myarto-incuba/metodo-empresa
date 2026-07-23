"""
Biblioteca base de controles empresariales.
"""

from __future__ import annotations

from .models import Control, ControlImportance, EvidenceRequirement, InterviewQuestion


BASE_CONTROLS: list[Control] = [
    Control(
        code="DIR-001",
        name="Existe una dirección estratégica formal",
        area="Dirección",
        objective="Alinear decisiones, recursos y prioridades con objetivos definidos.",
        importance=ControlImportance.CRITICA,
        expected_evidence=[
            EvidenceRequirement("Plan estratégico", required=True),
            EvidenceRequirement("Objetivos anuales"),
        ],
        interview_questions=[
            InterviewQuestion(
                code="DIR-001-Q1",
                text="¿Cuáles son las tres prioridades estratégicas de la empresa para este año?",
                respondent_roles=("Dirección general", "Socios"),
            ),
        ],
        related_controls=["DIR-002", "FIN-001", "COM-001", "OPE-001"],
        related_phenomena=["Falta de dirección", "Decisiones reactivas"],
        generated_risks=["Dispersión de recursos", "Prioridades contradictorias"],
        suggested_actions=["Definir objetivos estratégicos", "Crear un tablero ejecutivo"],
        indicators=["Cumplimiento de objetivos"],
        tags=["estrategia", "dirección"],
    ),
    Control(
        code="DIR-002",
        name="Las decisiones relevantes tienen responsables definidos",
        area="Dirección",
        objective="Evitar dependencia excesiva del propietario y retrasos en decisiones.",
        importance=ControlImportance.CRITICA,
        expected_evidence=[
            EvidenceRequirement("Matriz de responsabilidades"),
            EvidenceRequirement("Organigrama"),
        ],
        interview_questions=[
            InterviewQuestion(
                code="DIR-002-Q1",
                text="¿Qué decisiones solo puede aprobar el dueño o director general?",
                respondent_roles=("Dirección general", "Mandos medios"),
            ),
        ],
        related_controls=["PER-001", "OPE-001", "COM-002", "FIN-003"],
        related_phenomena=["Dependencia del dueño", "Cuellos de botella"],
        generated_risks=["Parálisis operativa", "Riesgo de continuidad"],
        suggested_actions=["Definir niveles de autoridad", "Delegar decisiones recurrentes"],
        indicators=["Tiempo de aprobación"],
        tags=["gobierno", "delegación"],
    ),
    Control(
        code="DIR-003",
        name="La empresa utiliza información periódica para decidir",
        area="Dirección",
        objective="Asegurar decisiones basadas en información actualizada y confiable.",
        importance=ControlImportance.ALTA,
        expected_evidence=[EvidenceRequirement("Tablero de indicadores")],
        interview_questions=[
            InterviewQuestion(
                code="DIR-003-Q1",
                text="¿Qué información revisa la dirección cada semana o cada mes?",
                respondent_roles=("Dirección general",),
            ),
        ],
        related_controls=["FIN-002", "COM-003", "OPE-003"],
        related_phenomena=["Falta de información", "Decisiones intuitivas"],
        generated_risks=["Reacción tardía", "Priorización incorrecta"],
        suggested_actions=["Definir indicadores ejecutivos"],
        indicators=["Indicadores actualizados"],
        tags=["datos", "gestión"],
    ),
    Control(
        code="COM-001",
        name="Existe un proceso comercial definido",
        area="Comercial",
        objective="Estandarizar la captación, seguimiento y cierre de oportunidades.",
        importance=ControlImportance.CRITICA,
        expected_evidence=[
            EvidenceRequirement("Proceso comercial documentado"),
            EvidenceRequirement("Pipeline o CRM"),
        ],
        interview_questions=[
            InterviewQuestion(
                code="COM-001-Q1",
                text="¿Cuáles son las etapas desde que llega un prospecto hasta que compra?",
                respondent_roles=("Dirección comercial", "Ventas"),
            ),
        ],
        related_controls=["COM-002", "COM-003", "FIN-001", "OPE-002"],
        related_phenomena=["Ventas impredecibles", "Pérdida de oportunidades"],
        generated_risks=["Ingresos inestables"],
        suggested_actions=["Documentar el proceso comercial"],
        indicators=["Conversión", "Ciclo de venta"],
        tags=["ventas", "pipeline"],
    ),
    Control(
        code="COM-002",
        name="Las oportunidades comerciales tienen seguimiento formal",
        area="Comercial",
        objective="Evitar pérdidas por falta de seguimiento.",
        importance=ControlImportance.ALTA,
        expected_evidence=[EvidenceRequirement("CRM o registro de oportunidades", required=True)],
        interview_questions=[
            InterviewQuestion(
                code="COM-002-Q1",
                text="¿Cómo se sabe cuál es el siguiente paso de cada oportunidad?",
                respondent_roles=("Ventas", "Dirección comercial"),
            ),
        ],
        related_controls=["COM-001", "COM-003", "DIR-003", "FIN-003"],
        related_phenomena=["Falta de seguimiento", "Información fragmentada"],
        generated_risks=["Prospectos abandonados", "Forecast poco confiable"],
        suggested_actions=["Centralizar oportunidades en un CRM"],
        indicators=["Seguimientos vencidos", "Tasa de cierre"],
        tags=["crm", "seguimiento"],
    ),
    Control(
        code="COM-003",
        name="Existe un pronóstico comercial actualizado",
        area="Comercial",
        objective="Proyectar ingresos y coordinar decisiones financieras y operativas.",
        importance=ControlImportance.ALTA,
        expected_evidence=[EvidenceRequirement("Forecast comercial")],
        interview_questions=[
            InterviewQuestion(
                code="COM-003-Q1",
                text="¿Cuánto espera vender la empresa en los próximos 90 días y con qué certeza?",
                respondent_roles=("Dirección comercial",),
            ),
        ],
        related_controls=["FIN-003", "OPE-002", "DIR-003"],
        related_phenomena=["Falta de previsibilidad", "Planeación reactiva"],
        generated_risks=["Falta de liquidez", "Capacidad insuficiente"],
        suggested_actions=["Crear forecast ponderado"],
        indicators=["Precisión del forecast"],
        tags=["forecast", "planeación"],
    ),
    Control(
        code="FIN-001",
        name="Existe un presupuesto anual",
        area="Finanzas",
        objective="Asignar recursos con anticipación y controlar desviaciones.",
        importance=ControlImportance.CRITICA,
        expected_evidence=[EvidenceRequirement("Presupuesto anual", required=True)],
        interview_questions=[
            InterviewQuestion(
                code="FIN-001-Q1",
                text="¿Cómo se determina cuánto puede gastar cada área?",
                respondent_roles=("Finanzas", "Dirección general"),
            ),
        ],
        related_controls=["DIR-001", "FIN-002", "FIN-003", "COM-003"],
        related_phenomena=["Descontrol financiero", "Gasto reactivo"],
        generated_risks=["Desviaciones no detectadas"],
        suggested_actions=["Construir presupuesto anual"],
        indicators=["Desviación presupuestaria"],
        tags=["presupuesto", "control"],
    ),
    Control(
        code="FIN-002",
        name="Los estados financieros son oportunos y confiables",
        area="Finanzas",
        objective="Permitir decisiones basadas en la situación económica real.",
        importance=ControlImportance.CRITICA,
        expected_evidence=[
            EvidenceRequirement("Estado de resultados", required=True),
            EvidenceRequirement("Balance general"),
        ],
        interview_questions=[
            InterviewQuestion(
                code="FIN-002-Q1",
                text="¿Cuántos días después del cierre se conoce el resultado del mes?",
                respondent_roles=("Finanzas", "Contabilidad"),
            ),
        ],
        related_controls=["DIR-003", "FIN-001", "FIN-003"],
        related_phenomena=["Falta de información financiera", "Decisiones tardías"],
        generated_risks=["Pérdidas ocultas"],
        suggested_actions=["Definir cierre financiero mensual"],
        indicators=["Días de cierre"],
        tags=["contabilidad", "datos"],
    ),
    Control(
        code="FIN-003",
        name="Existe una proyección de flujo de efectivo",
        area="Finanzas",
        objective="Anticipar faltantes de liquidez.",
        importance=ControlImportance.CRITICA,
        expected_evidence=[EvidenceRequirement("Flujo de caja proyectado", required=True)],
        interview_questions=[
            InterviewQuestion(
                code="FIN-003-Q1",
                text="¿Con cuánta anticipación puede detectarse un faltante de efectivo?",
                respondent_roles=("Finanzas", "Dirección general"),
            ),
        ],
        related_controls=["COM-003", "FIN-001", "OPE-002", "DIR-002"],
        related_phenomena=["Falta de liquidez", "Dependencia de deuda"],
        generated_risks=["Incumplimiento de pagos", "Financiamiento costoso"],
        suggested_actions=["Crear flujo de caja de 13 semanas"],
        indicators=["Semanas de cobertura"],
        tags=["flujo", "liquidez"],
    ),
    Control(
        code="OPE-001",
        name="Los procesos críticos están documentados",
        area="Operaciones",
        objective="Reducir variaciones, dependencia de personas y errores.",
        importance=ControlImportance.CRITICA,
        expected_evidence=[EvidenceRequirement("Manuales de proceso")],
        interview_questions=[
            InterviewQuestion(
                code="OPE-001-Q1",
                text="¿Qué pasaría si la persona que domina el proceso no estuviera mañana?",
                respondent_roles=("Operaciones",),
            ),
        ],
        related_controls=["DIR-002", "PER-001", "OPE-002", "OPE-003"],
        related_phenomena=["Dependencia de personas clave", "Desorden operativo"],
        generated_risks=["Errores recurrentes", "Pérdida de conocimiento"],
        suggested_actions=["Documentar procesos críticos"],
        indicators=["Procesos documentados"],
        tags=["procesos", "continuidad"],
    ),
    Control(
        code="OPE-002",
        name="La capacidad operativa se planifica con base en la demanda",
        area="Operaciones",
        objective="Evitar saturación, tiempos muertos y compromisos incumplibles.",
        importance=ControlImportance.ALTA,
        expected_evidence=[EvidenceRequirement("Plan de capacidad")],
        interview_questions=[
            InterviewQuestion(
                code="OPE-002-Q1",
                text="¿Cómo se decide cuántos recursos se necesitan para atender la demanda?",
                respondent_roles=("Operaciones", "Comercial"),
            ),
        ],
        related_controls=["COM-003", "FIN-003", "PER-003"],
        related_phenomena=["Sobrecarga operativa", "Capacidad ociosa"],
        generated_risks=["Retrasos", "Sobrecostos"],
        suggested_actions=["Vincular forecast con capacidad"],
        indicators=["Utilización de capacidad"],
        tags=["capacidad", "demanda"],
    ),
    Control(
        code="OPE-003",
        name="Los errores y retrabajos se registran y analizan",
        area="Operaciones",
        objective="Identificar causas recurrentes y reducir pérdidas.",
        importance=ControlImportance.ALTA,
        expected_evidence=[EvidenceRequirement("Registro de incidencias")],
        interview_questions=[
            InterviewQuestion(
                code="OPE-003-Q1",
                text="¿Cuáles son los errores que más se repiten y cuánto cuestan?",
                respondent_roles=("Operaciones", "Calidad", "Finanzas"),
            ),
        ],
        related_controls=["DIR-003", "FIN-002", "PER-002"],
        related_phenomena=["Retrabajo", "Pérdida de margen"],
        generated_risks=["Costos ocultos", "Deterioro del servicio"],
        suggested_actions=["Analizar causas recurrentes"],
        indicators=["Tasa de retrabajo"],
        tags=["calidad", "mejora continua"],
    ),
    Control(
        code="PER-001",
        name="Los roles y responsabilidades están definidos",
        area="Personas",
        objective="Asegurar claridad de funciones, autoridad y rendición de cuentas.",
        importance=ControlImportance.CRITICA,
        expected_evidence=[EvidenceRequirement("Descripciones de puesto")],
        interview_questions=[
            InterviewQuestion(
                code="PER-001-Q1",
                text="¿Qué responsabilidades suelen quedar sin dueño o duplicadas?",
                respondent_roles=("Dirección", "Mandos medios", "Colaboradores"),
            ),
        ],
        related_controls=["DIR-002", "OPE-001", "PER-002"],
        related_phenomena=["Responsabilidades difusas", "Conflictos internos"],
        generated_risks=["Tareas omitidas", "Duplicidad de trabajo"],
        suggested_actions=["Construir matriz RACI"],
        indicators=["Tareas sin responsable"],
        tags=["roles", "organización"],
    ),
    Control(
        code="PER-002",
        name="El desempeño se evalúa con criterios definidos",
        area="Personas",
        objective="Alinear resultados individuales con prioridades empresariales.",
        importance=ControlImportance.ALTA,
        expected_evidence=[EvidenceRequirement("Evaluaciones de desempeño")],
        interview_questions=[
            InterviewQuestion(
                code="PER-002-Q1",
                text="¿Cómo sabe cada persona si está haciendo bien su trabajo?",
                respondent_roles=("Recursos Humanos", "Mandos medios"),
            ),
        ],
        related_controls=["DIR-001", "OPE-003", "PER-001"],
        related_phenomena=["Bajo desempeño", "Falta de rendición de cuentas"],
        generated_risks=["Resultados inconsistentes"],
        suggested_actions=["Definir objetivos por puesto"],
        indicators=["Cumplimiento individual"],
        tags=["desempeño", "objetivos"],
    ),
    Control(
        code="PER-003",
        name="La capacitación responde a necesidades reales del puesto",
        area="Personas",
        objective="Cerrar brechas que afectan calidad, productividad y crecimiento.",
        importance=ControlImportance.ALTA,
        expected_evidence=[EvidenceRequirement("Matriz de competencias")],
        interview_questions=[
            InterviewQuestion(
                code="PER-003-Q1",
                text="¿Qué errores o retrasos ocurren por falta de conocimiento o habilidad?",
                respondent_roles=("Recursos Humanos", "Operaciones"),
            ),
        ],
        related_controls=["OPE-001", "OPE-002", "OPE-003"],
        related_phenomena=["Brechas de capacidad", "Errores operativos"],
        generated_risks=["Calidad inconsistente"],
        suggested_actions=["Crear matriz de competencias"],
        indicators=["Brechas críticas"],
        tags=["capacitación", "productividad"],
    ),
]


def get_control(code: str) -> Control | None:
    clean_code = code.strip().upper()
    return next((control for control in BASE_CONTROLS if control.code == clean_code), None)


def get_controls_by_area(area: str) -> list[Control]:
    clean_area = area.strip().casefold()
    return [control for control in BASE_CONTROLS if control.area.casefold() == clean_area]


def validate_control_library() -> list[str]:
    errors: list[str] = []
    codes = [control.code for control in BASE_CONTROLS]

    duplicates = sorted({code for code in codes if codes.count(code) > 1})
    if duplicates:
        errors.append(f"Códigos duplicados: {', '.join(duplicates)}")

    known_codes = set(codes)

    for control in BASE_CONTROLS:
        missing = [code for code in control.related_controls if code not in known_codes]
        if missing:
            errors.append(
                f"{control.code} referencia controles inexistentes: {', '.join(missing)}"
            )

    return errors
