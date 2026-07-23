"""
Banco inicial de preguntas para las entrevistas inteligentes.

Cada pregunta puede incluir:

- id: identificador único
- section: bloque de la entrevista
- text: pregunta visible
- help: explicación opcional
- type: text, textarea, select, multiselect, number o boolean
- options: opciones cuando corresponda
- required: determina si debe contestarse
- condition: regla para mostrarla
- risk_rules: reglas de señales preliminares
"""

DIRECTOR_INTERVIEW_CODE = "direccion_inicial"

DIRECTOR_INTERVIEW = {
    "code": DIRECTOR_INTERVIEW_CODE,
    "name": "Entrevista inicial de Dirección",
    "description": (
        "Comprende cómo funciona la empresa, cómo genera dinero, "
        "qué problemas percibe la dirección y dónde pueden existir "
        "riesgos o cuellos de botella."
    ),
    "questions": [
        {
            "id": "business_type",
            "section": "Modelo de negocio",
            "text": "¿Qué vende principalmente la empresa?",
            "help": (
                "Esta respuesta determinará qué preguntas se mostrarán "
                "más adelante."
            ),
            "type": "select",
            "options": [
                "Servicios",
                "Productos",
                "Productos y servicios",
                "Suscripciones o membresías",
                "Comisiones o intermediación",
                "Otro",
            ],
            "required": True,
        },
        {
            "id": "business_type_other",
            "section": "Modelo de negocio",
            "text": "Describe el modelo de negocio principal.",
            "type": "textarea",
            "required": True,
            "condition": {
                "question_id": "business_type",
                "operator": "equals",
                "value": "Otro",
            },
        },
        {
            "id": "main_products",
            "section": "Modelo de negocio",
            "text": "¿Cuáles son los principales productos o servicios?",
            "help": (
                "Incluye las líneas que más venden y también aquellas "
                "que la empresa considera estratégicas."
            ),
            "type": "textarea",
            "required": True,
        },
        {
            "id": "revenue_knowledge",
            "section": "Finanzas",
            "text": (
                "¿La dirección conoce con precisión cuánto ingresa "
                "mensualmente la empresa?"
            ),
            "type": "select",
            "options": [
                "Sí, con información actualizada",
                "Sí, pero con retraso",
                "Solo de manera aproximada",
                "No",
            ],
            "required": True,
            "risk_rules": [
                {
                    "operator": "in",
                    "values": [
                        "Solo de manera aproximada",
                        "No",
                    ],
                    "level": "Alto",
                    "title": "Falta de visibilidad sobre ingresos",
                    "message": (
                        "La dirección no cuenta con información precisa "
                        "y actualizada sobre los ingresos mensuales."
                    ),
                }
            ],
        },
        {
            "id": "profitability_knowledge",
            "section": "Finanzas",
            "text": (
                "¿La empresa conoce la rentabilidad real de cada producto, "
                "servicio o línea de negocio?"
            ),
            "type": "select",
            "options": [
                "Sí, con costos completos",
                "Parcialmente",
                "Solo se conoce la facturación",
                "No",
            ],
            "required": True,
            "risk_rules": [
                {
                    "operator": "in",
                    "values": [
                        "Solo se conoce la facturación",
                        "No",
                    ],
                    "level": "Crítico",
                    "title": "Ventas sin control de rentabilidad",
                    "message": (
                        "La empresa podría estar vendiendo productos o "
                        "servicios que no generan utilidad."
                    ),
                }
            ],
        },
        {
            "id": "cash_flow_control",
            "section": "Finanzas",
            "text": "¿Existe una proyección de flujo de efectivo?",
            "type": "select",
            "options": [
                "Sí, se actualiza semanalmente",
                "Sí, se actualiza mensualmente",
                "Existe, pero no se actualiza",
                "No existe",
            ],
            "required": True,
            "risk_rules": [
                {
                    "operator": "in",
                    "values": [
                        "Existe, pero no se actualiza",
                        "No existe",
                    ],
                    "level": "Crítico",
                    "title": "Ausencia de control de flujo de efectivo",
                    "message": (
                        "La empresa puede enfrentar problemas de liquidez "
                        "aunque sea rentable."
                    ),
                }
            ],
        },
        {
            "id": "expense_authorization",
            "section": "Finanzas",
            "text": "¿Cómo se autorizan los gastos?",
            "type": "select",
            "options": [
                "Existe una política formal por montos y responsables",
                "Se autorizan por correo o sistema",
                "Se autorizan por WhatsApp o verbalmente",
                "No existe un proceso definido",
            ],
            "required": True,
            "risk_rules": [
                {
                    "operator": "in",
                    "values": [
                        "Se autorizan por WhatsApp o verbalmente",
                        "No existe un proceso definido",
                    ],
                    "level": "Alto",
                    "title": "Control débil de gastos",
                    "message": (
                        "La autorización informal aumenta el riesgo de "
                        "errores, duplicidades y gastos no justificados."
                    ),
                }
            ],
        },
        {
            "id": "customer_concentration",
            "section": "Finanzas",
            "text": (
                "¿Qué porcentaje aproximado de los ingresos depende "
                "del cliente principal?"
            ),
            "type": "number",
            "minimum": 0,
            "maximum": 100,
            "step": 1,
            "suffix": "%",
            "required": True,
            "risk_rules": [
                {
                    "operator": "greater_than",
                    "value": 30,
                    "level": "Alto",
                    "title": "Concentración de ingresos",
                    "message": (
                        "Más del 30% de los ingresos depende de un solo cliente."
                    ),
                }
            ],
        },
        {
            "id": "service_capacity",
            "section": "Operación",
            "text": (
                "¿Cómo calcula la empresa cuántos proyectos o servicios "
                "puede atender al mismo tiempo?"
            ),
            "type": "select",
            "options": [
                "Existe un cálculo de capacidad y carga de trabajo",
                "Se estima con base en la experiencia",
                "Depende de la disponibilidad del equipo",
                "No se calcula",
            ],
            "required": True,
            "condition": {
                "question_id": "business_type",
                "operator": "in",
                "values": [
                    "Servicios",
                    "Productos y servicios",
                ],
            },
            "risk_rules": [
                {
                    "operator": "in",
                    "values": [
                        "Depende de la disponibilidad del equipo",
                        "No se calcula",
                    ],
                    "level": "Alto",
                    "title": "Capacidad operativa no controlada",
                    "message": (
                        "La empresa puede vender más trabajo del que puede "
                        "entregar correctamente."
                    ),
                }
            ],
        },
        {
            "id": "inventory_control",
            "section": "Operación",
            "text": "¿Cómo se controla el inventario?",
            "type": "select",
            "options": [
                "Sistema integrado y actualizado",
                "Hoja de cálculo",
                "Registros manuales",
                "No existe un control confiable",
            ],
            "required": True,
            "condition": {
                "question_id": "business_type",
                "operator": "in",
                "values": [
                    "Productos",
                    "Productos y servicios",
                ],
            },
            "risk_rules": [
                {
                    "operator": "in",
                    "values": [
                        "Registros manuales",
                        "No existe un control confiable",
                    ],
                    "level": "Alto",
                    "title": "Control vulnerable de inventarios",
                    "message": (
                        "Puede haber diferencias, mermas o compras innecesarias."
                    ),
                }
            ],
        },
        {
            "id": "strategic_objectives",
            "section": "Estrategia",
            "text": (
                "¿La empresa tiene objetivos estratégicos definidos "
                "para los próximos 12 meses?"
            ),
            "type": "select",
            "options": [
                "Sí, están documentados y medidos",
                "Sí, pero no tienen indicadores",
                "Existen solo de manera informal",
                "No",
            ],
            "required": True,
            "risk_rules": [
                {
                    "operator": "in",
                    "values": [
                        "Existen solo de manera informal",
                        "No",
                    ],
                    "level": "Alto",
                    "title": "Dirección estratégica insuficiente",
                    "message": (
                        "La organización puede operar sin prioridades "
                        "compartidas ni criterios claros de decisión."
                    ),
                }
            ],
        },
        {
            "id": "decision_dependency",
            "section": "Organización",
            "text": (
                "¿Qué porcentaje de las decisiones operativas necesita "
                "autorización de la dirección general?"
            ),
            "type": "number",
            "minimum": 0,
            "maximum": 100,
            "step": 5,
            "suffix": "%",
            "required": True,
            "risk_rules": [
                {
                    "operator": "greater_than",
                    "value": 60,
                    "level": "Alto",
                    "title": "Dirección general como cuello de botella",
                    "message": (
                        "Una proporción elevada de decisiones depende "
                        "directamente de la dirección general."
                    ),
                }
            ],
        },
        {
            "id": "organization_chart",
            "section": "Organización",
            "text": "¿Existe un organigrama actualizado?",
            "type": "select",
            "options": [
                "Sí, refleja la operación real",
                "Sí, pero está desactualizado",
                "Existe informalmente",
                "No existe",
            ],
            "required": True,
            "risk_rules": [
                {
                    "operator": "in",
                    "values": [
                        "Existe informalmente",
                        "No existe",
                    ],
                    "level": "Medio",
                    "title": "Estructura organizacional poco clara",
                    "message": (
                        "Puede existir confusión sobre jerarquías, "
                        "responsabilidades y líneas de reporte."
                    ),
                }
            ],
        },
        {
            "id": "role_clarity",
            "section": "Organización",
            "text": (
                "¿Cada puesto tiene responsabilidades, entregables "
                "e indicadores claramente definidos?"
            ),
            "type": "select",
            "options": [
                "Sí, todos",
                "La mayoría",
                "Solo algunos",
                "No",
            ],
            "required": True,
            "risk_rules": [
                {
                    "operator": "in",
                    "values": [
                        "Solo algunos",
                        "No",
                    ],
                    "level": "Alto",
                    "title": "Responsabilidades ambiguas",
                    "message": (
                        "La falta de claridad puede provocar duplicidades, "
                        "omisiones y conflictos internos."
                    ),
                }
            ],
        },
        {
            "id": "sales_process",
            "section": "Ventas",
            "text": "¿Existe un proceso comercial documentado?",
            "type": "select",
            "options": [
                "Sí, se sigue y se mide",
                "Sí, pero no siempre se aplica",
                "Cada vendedor trabaja de forma diferente",
                "No existe",
            ],
            "required": True,
            "risk_rules": [
                {
                    "operator": "in",
                    "values": [
                        "Cada vendedor trabaja de forma diferente",
                        "No existe",
                    ],
                    "level": "Alto",
                    "title": "Proceso comercial no estandarizado",
                    "message": (
                        "La conversión y el seguimiento dependen de prácticas "
                        "individuales en lugar de un método común."
                    ),
                }
            ],
        },
        {
            "id": "crm_usage",
            "section": "Ventas",
            "text": "¿Dónde se administra la cartera de clientes y prospectos?",
            "type": "select",
            "options": [
                "CRM centralizado",
                "Sistema o base de datos interna",
                "Hojas de cálculo",
                "WhatsApp, correos o agendas personales",
                "No existe una base consolidada",
            ],
            "required": True,
            "risk_rules": [
                {
                    "operator": "in",
                    "values": [
                        "WhatsApp, correos o agendas personales",
                        "No existe una base consolidada",
                    ],
                    "level": "Crítico",
                    "title": "Información comercial dependiente de personas",
                    "message": (
                        "La cartera comercial no pertenece plenamente a "
                        "la organización y puede perderse."
                    ),
                }
            ],
        },
        {
            "id": "process_documentation",
            "section": "Procesos",
            "text": "¿Qué porcentaje de los procesos críticos está documentado?",
            "type": "number",
            "minimum": 0,
            "maximum": 100,
            "step": 5,
            "suffix": "%",
            "required": True,
            "risk_rules": [
                {
                    "operator": "less_than",
                    "value": 50,
                    "level": "Alto",
                    "title": "Procesos críticos sin documentar",
                    "message": (
                        "La operación depende del conocimiento individual "
                        "y dificulta la capacitación o sustitución de personal."
                    ),
                }
            ],
        },
        {
            "id": "manual_tasks",
            "section": "Tecnología",
            "text": (
                "¿Existen tareas administrativas repetitivas que consumen "
                "muchas horas cada semana?"
            ),
            "type": "boolean",
            "required": True,
        },
        {
            "id": "manual_tasks_detail",
            "section": "Tecnología",
            "text": (
                "Describe las principales tareas repetitivas y quién las realiza."
            ),
            "type": "textarea",
            "required": True,
            "condition": {
                "question_id": "manual_tasks",
                "operator": "equals",
                "value": "Sí",
            },
            "risk_rules": [
                {
                    "operator": "not_empty",
                    "level": "Medio",
                    "title": "Oportunidad de automatización",
                    "message": (
                        "Se identificaron tareas repetitivas que deben evaluarse "
                        "por tiempo, costo y viabilidad de automatización."
                    ),
                }
            ],
        },
        {
            "id": "main_bottleneck",
            "section": "Cierre",
            "text": (
                "Desde la perspectiva de la dirección, ¿cuál es el principal "
                "problema que impide crecer o mejorar la rentabilidad?"
            ),
            "type": "textarea",
            "required": True,
        },
        {
            "id": "audit_expectation",
            "section": "Cierre",
            "text": "¿Qué resultado concreto espera obtener de esta auditoría?",
            "type": "textarea",
            "required": True,
        },
    ],
}