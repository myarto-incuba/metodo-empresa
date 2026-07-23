"""
Motor de evidencias.

Determina qué documentos, datos, entrevistas y pruebas
se requieren para validar cada señal preliminar.
"""


DEFAULT_EVIDENCE = {
    "documents": [
        "Política o procedimiento relacionado",
        "Reportes internos disponibles",
    ],
    "data": [
        "Datos históricos del proceso",
    ],
    "interviews": [
        "Responsable directo del área",
    ],
    "validations": [
        "Comparar la respuesta con evidencia documental",
        "Confirmar la práctica con el responsable operativo",
    ],
}


EVIDENCE_CATALOG = {
    "revenue_knowledge": {
        "documents": [
            "Estados de resultados mensuales",
            "Reportes de facturación",
            "Estados de cuenta bancarios",
        ],
        "data": [
            "Ingresos mensuales de los últimos 12 meses",
            "Ingresos por cliente",
            "Ingresos por producto o servicio",
        ],
        "interviews": [
            "Dirección financiera",
            "Contabilidad",
            "Dirección general",
        ],
        "validations": [
            (
                "Comparar la facturación registrada con "
                "los depósitos bancarios."
            ),
            (
                "Confirmar la fecha de cierre y actualización "
                "de la información financiera."
            ),
        ],
    },
    "profitability_knowledge": {
        "documents": [
            "Estados de resultados",
            "Catálogo de costos",
            "Presupuestos o cotizaciones",
            "Estructura de precios",
        ],
        "data": [
            "Ventas por producto o servicio",
            "Costos directos por línea",
            "Horas invertidas por proyecto",
            "Margen bruto por línea de negocio",
        ],
        "interviews": [
            "Dirección financiera",
            "Responsable de operaciones",
            "Responsable comercial",
        ],
        "validations": [
            (
                "Calcular el margen bruto de las principales "
                "líneas de negocio."
            ),
            (
                "Asignar costos indirectos para estimar "
                "la rentabilidad real."
            ),
            (
                "Comparar precios vendidos contra costos completos."
            ),
        ],
    },
    "cash_flow_control": {
        "documents": [
            "Flujo de efectivo",
            "Presupuesto anual",
            "Calendario de pagos",
            "Cuentas por cobrar",
            "Cuentas por pagar",
            "Estados de cuenta bancarios",
        ],
        "data": [
            "Saldo inicial y final por mes",
            "Cobros proyectados",
            "Pagos comprometidos",
            "Vencimientos de deuda",
        ],
        "interviews": [
            "Dirección financiera",
            "Tesorería",
            "Dirección general",
        ],
        "validations": [
            (
                "Construir una proyección mínima de flujo "
                "de efectivo de 13 semanas."
            ),
            (
                "Identificar semanas con déficit de liquidez."
            ),
            (
                "Comparar fechas reales de cobro y pago "
                "con las condiciones pactadas."
            ),
        ],
    },
    "expense_authorization": {
        "documents": [
            "Política de gastos",
            "Matriz de autorización",
            "Comprobantes de gasto",
            "Reportes de reembolsos",
        ],
        "data": [
            "Gastos por responsable",
            "Gastos por categoría",
            "Reembolsos de los últimos seis meses",
        ],
        "interviews": [
            "Dirección financiera",
            "Administración",
            "Responsables de área",
        ],
        "validations": [
            (
                "Seleccionar una muestra de gastos y revisar "
                "su autorización y comprobación."
            ),
            (
                "Identificar gastos duplicados, sin soporte "
                "o fuera de política."
            ),
        ],
    },
    "customer_concentration": {
        "documents": [
            "Reporte de ventas por cliente",
            "Contratos de clientes principales",
            "Cuentas por cobrar",
        ],
        "data": [
            "Ingresos por cliente de los últimos 12 meses",
            "Margen por cliente",
            "Antigüedad de saldos",
        ],
        "interviews": [
            "Dirección comercial",
            "Dirección financiera",
            "Dirección general",
        ],
        "validations": [
            (
                "Calcular el porcentaje de ingresos que representan "
                "los cinco principales clientes."
            ),
            (
                "Simular el efecto financiero de perder "
                "al cliente principal."
            ),
        ],
    },
    "service_capacity": {
        "documents": [
            "Planeación de proyectos",
            "Asignación de personal",
            "Calendario operativo",
            "Registro de horas",
        ],
        "data": [
            "Horas disponibles por persona",
            "Horas comprometidas por proyecto",
            "Número de proyectos simultáneos",
            "Retrasos y reprocesos",
        ],
        "interviews": [
            "Dirección de operaciones",
            "Líderes de proyecto",
            "Equipo operativo",
        ],
        "validations": [
            (
                "Comparar la capacidad disponible con "
                "la carga comprometida."
            ),
            (
                "Identificar personas, equipos o etapas "
                "que actúan como cuello de botella."
            ),
        ],
    },
    "inventory_control": {
        "documents": [
            "Kardex",
            "Inventario físico",
            "Órdenes de compra",
            "Entradas y salidas de almacén",
        ],
        "data": [
            "Existencias por producto",
            "Rotación de inventario",
            "Mermas",
            "Diferencias entre inventario físico y sistema",
        ],
        "interviews": [
            "Responsable de almacén",
            "Compras",
            "Operaciones",
            "Contabilidad",
        ],
        "validations": [
            (
                "Realizar una prueba selectiva entre inventario "
                "físico y registros."
            ),
            (
                "Calcular rotación, días de inventario y mermas."
            ),
        ],
    },
    "strategic_objectives": {
        "documents": [
            "Plan estratégico",
            "Presupuesto anual",
            "Indicadores de desempeño",
            "Presentaciones de dirección",
        ],
        "data": [
            "Metas anuales",
            "Indicadores por área",
            "Avance mensual de objetivos",
        ],
        "interviews": [
            "Dirección general",
            "Líderes de área",
        ],
        "validations": [
            (
                "Confirmar que los responsables conocen "
                "las prioridades estratégicas."
            ),
            (
                "Verificar que cada objetivo tenga indicador, "
                "meta, plazo y responsable."
            ),
        ],
    },
    "decision_dependency": {
        "documents": [
            "Matriz de autoridad",
            "Organigrama",
            "Descripciones de puesto",
            "Políticas de autorización",
        ],
        "data": [
            "Número de decisiones escaladas a dirección",
            "Tiempo promedio de autorización",
            "Procesos detenidos por falta de aprobación",
        ],
        "interviews": [
            "Dirección general",
            "Líderes de área",
            "Personal operativo",
        ],
        "validations": [
            (
                "Registrar durante una semana las decisiones "
                "que requieren intervención de dirección."
            ),
            (
                "Identificar cuáles pueden delegarse mediante "
                "reglas y límites claros."
            ),
        ],
    },
    "organization_chart": {
        "documents": [
            "Organigrama actual",
            "Contratos laborales",
            "Descripciones de puesto",
        ],
        "data": [
            "Listado de personal",
            "Puesto",
            "Jefe directo",
            "Área",
        ],
        "interviews": [
            "Recursos humanos",
            "Dirección general",
            "Líderes de área",
        ],
        "validations": [
            (
                "Comparar el organigrama formal con "
                "las líneas reales de reporte."
            ),
            (
                "Detectar puestos duplicados, vacíos "
                "o dependencias informales."
            ),
        ],
    },
    "role_clarity": {
        "documents": [
            "Descripciones de puesto",
            "Manuales de funciones",
            "Indicadores individuales",
            "Evaluaciones de desempeño",
        ],
        "data": [
            "Entregables por puesto",
            "Indicadores por persona",
            "Incidencias por duplicidad u omisión",
        ],
        "interviews": [
            "Recursos humanos",
            "Líderes de área",
            "Colaboradores",
        ],
        "validations": [
            (
                "Comparar lo que el puesto debería hacer "
                "con lo que realiza en la práctica."
            ),
            (
                "Identificar actividades sin responsable "
                "o con más de un responsable."
            ),
        ],
    },
    "sales_process": {
        "documents": [
            "Proceso comercial",
            "Guiones de venta",
            "Política de seguimiento",
            "Formatos de cotización",
        ],
        "data": [
            "Prospectos generados",
            "Tasa de conversión",
            "Tiempo del ciclo comercial",
            "Motivos de pérdida",
        ],
        "interviews": [
            "Dirección comercial",
            "Vendedores",
            "Marketing",
        ],
        "validations": [
            (
                "Comparar la forma de trabajo de diferentes vendedores."
            ),
            (
                "Medir la conversión por etapa del embudo."
            ),
            (
                "Revisar una muestra de oportunidades ganadas "
                "y perdidas."
            ),
        ],
    },
    "crm_usage": {
        "documents": [
            "Base de clientes",
            "Exportación del CRM",
            "Reportes comerciales",
            "Política de propiedad de datos",
        ],
        "data": [
            "Clientes y prospectos activos",
            "Último contacto",
            "Responsable comercial",
            "Etapa de oportunidad",
        ],
        "interviews": [
            "Dirección comercial",
            "Vendedores",
            "Marketing",
        ],
        "validations": [
            (
                "Verificar si la información comercial está "
                "centralizada y respaldada."
            ),
            (
                "Identificar registros duplicados, incompletos "
                "o pertenecientes a cuentas personales."
            ),
        ],
    },
    "process_documentation": {
        "documents": [
            "Mapa de procesos",
            "Manuales operativos",
            "Procedimientos",
            "Checklists",
        ],
        "data": [
            "Listado de procesos críticos",
            "Responsable de cada proceso",
            "Frecuencia de errores",
            "Tiempo de capacitación",
        ],
        "interviews": [
            "Dirección de operaciones",
            "Líderes de área",
            "Personal operativo",
        ],
        "validations": [
            (
                "Identificar los procesos críticos que dependen "
                "del conocimiento de una sola persona."
            ),
            (
                "Observar la ejecución real de una muestra "
                "de procesos."
            ),
        ],
    },
    "manual_tasks_detail": {
        "documents": [
            "Listado de actividades administrativas",
            "Formatos utilizados",
            "Hojas de cálculo",
            "Reportes recurrentes",
        ],
        "data": [
            "Horas semanales por tarea",
            "Frecuencia",
            "Número de personas involucradas",
            "Errores o reprocesos",
        ],
        "interviews": [
            "Responsables administrativos",
            "Usuarios de los sistemas",
            "Dirección de operaciones",
        ],
        "validations": [
            (
                "Calcular el costo anual de las tareas repetitivas."
            ),
            (
                "Clasificar cada tarea por posibilidad de eliminación, "
                "simplificación o automatización."
            ),
        ],
    },
}


def get_evidence_requirements(
    signal: dict,
) -> dict:
    """
    Obtiene la evidencia requerida para una señal.
    """
    question_id = signal.get(
        "question_id",
        "",
    )

    requirements = EVIDENCE_CATALOG.get(
        question_id,
        DEFAULT_EVIDENCE,
    )

    return {
        "signal_code": signal.get("signal_code"),
        "question_id": question_id,
        "signal_title": signal.get("title"),
        "risk_level": signal.get("level"),
        "documents": list(
            requirements.get(
                "documents",
                [],
            )
        ),
        "data": list(
            requirements.get(
                "data",
                [],
            )
        ),
        "interviews": list(
            requirements.get(
                "interviews",
                [],
            )
        ),
        "validations": list(
            requirements.get(
                "validations",
                [],
            )
        ),
    }


def enrich_signal_with_evidence(
    signal: dict,
) -> dict:
    """
    Añade los requerimientos de evidencia a una señal.
    """
    enriched_signal = dict(signal)

    enriched_signal["evidence_requirements"] = (
        get_evidence_requirements(signal)
    )

    return enriched_signal


def build_evidence_plan(
    signals: list[dict],
) -> list[dict]:
    """
    Genera el plan completo de evidencias para las señales.
    """
    return [
        enrich_signal_with_evidence(signal)
        for signal in signals
    ]


def build_document_request_list(
    signals: list[dict],
) -> list[dict]:
    """
    Construye una lista consolidada de documentos y señala
    qué riesgos pretende validar cada uno.
    """
    document_map = {}

    for signal in signals:
        requirements = get_evidence_requirements(
            signal
        )

        for document in requirements["documents"]:
            if document not in document_map:
                document_map[document] = {
                    "document": document,
                    "related_signals": [],
                    "highest_risk": signal.get(
                        "level",
                        "Medio",
                    ),
                }

            document_map[document][
                "related_signals"
            ].append(
                signal.get(
                    "title",
                    "Señal preliminar",
                )
            )

            current_priority = _risk_priority(
                document_map[document][
                    "highest_risk"
                ]
            )

            new_priority = _risk_priority(
                signal.get(
                    "level",
                    "Medio",
                )
            )

            if new_priority < current_priority:
                document_map[document][
                    "highest_risk"
                ] = signal.get(
                    "level",
                    "Medio",
                )

    return sorted(
        document_map.values(),
        key=lambda item: (
            _risk_priority(
                item["highest_risk"]
            ),
            item["document"],
        ),
    )


def _risk_priority(
    level: str,
) -> int:
    priority = {
        "Crítico": 1,
        "Alto": 2,
        "Medio": 3,
        "Bajo": 4,
    }

    return priority.get(
        level,
        99,
    )