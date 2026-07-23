"""Cuestionario MVP para la primera auditoría de Método Empresa."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class InterviewQuestion:
    code: str
    area: str
    conversation_block: str
    text: str
    evidence_suggestions: tuple[str, ...]
    hypothesis_tags: tuple[str, ...]


INTERVIEW_QUESTIONS: tuple[InterviewQuestion, ...] = (
    # Dirección
    InterviewQuestion(
        "DIR-001", "Dirección", "La empresa",
        "¿Existe un plan estratégico documentado con objetivos y prioridades claras?",
        ("Plan estratégico", "Objetivos anuales", "Presentación de dirección"),
        ("Planeación insuficiente",),
    ),
    InterviewQuestion(
        "DIR-002", "Dirección", "La empresa",
        "¿Las decisiones relevantes pueden tomarse sin depender siempre de una sola persona?",
        ("Matriz de autorizaciones", "Organigrama", "Delegación de funciones"),
        ("Dependencia del dueño", "Responsabilidades difusas"),
    ),
    InterviewQuestion(
        "DIR-003", "Dirección", "La empresa",
        "¿Los objetivos de la empresa son conocidos por las personas responsables de ejecutarlos?",
        ("Objetivos por área", "Minutas", "Comunicaciones internas"),
        ("Desalineación estratégica",),
    ),
    InterviewQuestion(
        "DIR-004", "Dirección", "Cómo controlan",
        "¿La dirección revisa resultados y acuerdos al menos una vez al mes?",
        ("Minutas de dirección", "Tablero de seguimiento", "Calendario de reuniones"),
        ("Seguimiento insuficiente",),
    ),
    InterviewQuestion(
        "DIR-005", "Dirección", "Cómo controlan",
        "¿Existen indicadores definidos para evaluar el desempeño general del negocio?",
        ("Tablero de indicadores", "Reportes mensuales", "Metas"),
        ("Falta de indicadores",),
    ),
    InterviewQuestion(
        "DIR-006", "Dirección", "La empresa",
        "¿Las funciones y niveles de autoridad de socios y líderes están claramente definidos?",
        ("Acuerdos de socios", "Descripciones de puesto", "Organigrama"),
        ("Responsabilidades difusas", "Dependencia del dueño"),
    ),
    InterviewQuestion(
        "DIR-007", "Dirección", "Cómo controlan",
        "¿La empresa cuenta con un presupuesto anual vinculado con sus objetivos?",
        ("Presupuesto anual", "Proyección de ingresos", "Plan de inversiones"),
        ("Planeación insuficiente", "Control financiero débil"),
    ),
    InterviewQuestion(
        "DIR-008", "Dirección", "Qué les preocupa",
        "¿Los principales riesgos del negocio están identificados y cuentan con acciones preventivas?",
        ("Mapa de riesgos", "Planes de contingencia", "Pólizas"),
        ("Gestión reactiva",),
    ),

    # Finanzas
    InterviewQuestion(
        "FIN-001", "Finanzas", "Cómo controlan",
        "¿La empresa proyecta su flujo de efectivo por lo menos para los próximos tres meses?",
        ("Flujo proyectado", "Calendario de pagos", "Saldo bancario"),
        ("Control financiero débil",),
    ),
    InterviewQuestion(
        "FIN-002", "Finanzas", "Cómo controlan",
        "¿Se generan y revisan estados financieros mensuales?",
        ("Estado de resultados", "Balance general", "Reporte contable"),
        ("Control financiero débil", "Falta de indicadores"),
    ),
    InterviewQuestion(
        "FIN-003", "Finanzas", "Cómo controlan",
        "¿Existe seguimiento sistemático de las cuentas por cobrar?",
        ("Antigüedad de saldos", "Política de crédito", "Reporte de cobranza"),
        ("Cobranza débil",),
    ),
    InterviewQuestion(
        "FIN-004", "Finanzas", "Cómo controlan",
        "¿Existe control de cuentas por pagar y fechas de vencimiento?",
        ("Antigüedad de proveedores", "Calendario de pagos", "Órdenes de compra"),
        ("Control financiero débil",),
    ),
    InterviewQuestion(
        "FIN-005", "Finanzas", "La empresa",
        "¿Se conoce el costo y margen real de cada capacitación, evento o servicio?",
        ("Costeo por evento", "Presupuesto por proyecto", "Margen por servicio"),
        ("Rentabilidad desconocida",),
    ),
    InterviewQuestion(
        "FIN-006", "Finanzas", "Cómo trabajan",
        "¿Los gastos y compras requieren autorización según montos definidos?",
        ("Política de gastos", "Matriz de autorización", "Comprobaciones"),
        ("Control financiero débil", "Dependencia del dueño"),
    ),
    InterviewQuestion(
        "FIN-007", "Finanzas", "Cómo controlan",
        "¿Se compara periódicamente el presupuesto contra el resultado real?",
        ("Presupuesto vs. real", "Reporte de variaciones", "Minutas"),
        ("Planeación insuficiente", "Control financiero débil"),
    ),
    InterviewQuestion(
        "FIN-008", "Finanzas", "Qué les preocupa",
        "¿La empresa puede identificar con anticipación meses o proyectos con riesgo de falta de liquidez?",
        ("Escenarios de flujo", "Punto de equilibrio", "Proyección comercial"),
        ("Control financiero débil", "Gestión reactiva"),
    ),

    # Comercial
    InterviewQuestion(
        "COM-001", "Comercial", "Cómo crecen",
        "¿Existe un proceso comercial definido desde el primer contacto hasta el cierre?",
        ("Proceso comercial", "Embudo de ventas", "Guiones"),
        ("Proceso comercial informal",),
    ),
    InterviewQuestion(
        "COM-002", "Comercial", "Cómo crecen",
        "¿Todos los prospectos se registran y reciben seguimiento?",
        ("CRM", "Base de prospectos", "Agenda de seguimiento"),
        ("Proceso comercial informal", "Oportunidades perdidas"),
    ),
    InterviewQuestion(
        "COM-003", "Comercial", "Cómo crecen",
        "¿La empresa mide cuántos prospectos avanzan y se convierten en clientes?",
        ("Tasa de conversión", "Embudo", "Reporte de ventas"),
        ("Falta de indicadores", "Proceso comercial informal"),
    ),
    InterviewQuestion(
        "COM-004", "Comercial", "Cómo crecen",
        "¿Existe una base de clientes actualizada con historial de compras e intereses?",
        ("CRM", "Base de clientes", "Historial de eventos"),
        ("Información dispersa",),
    ),
    InterviewQuestion(
        "COM-005", "Comercial", "Cómo crecen",
        "¿La estrategia de marketing define públicos, mensajes, canales y objetivos?",
        ("Plan de marketing", "Calendario de contenidos", "Campañas"),
        ("Marketing sin estrategia",),
    ),
    InterviewQuestion(
        "COM-006", "Comercial", "Cómo crecen",
        "¿Se conoce qué servicios, canales o alianzas generan más ventas y rentabilidad?",
        ("Ventas por canal", "Margen por servicio", "Reporte de alianzas"),
        ("Rentabilidad desconocida", "Falta de indicadores"),
    ),
    InterviewQuestion(
        "COM-007", "Comercial", "Cómo crecen",
        "¿Se mide la satisfacción de participantes, clientes y aliados después de cada servicio o evento?",
        ("Encuestas", "NPS", "Testimonios", "Incidencias"),
        ("Experiencia no medida",),
    ),
    InterviewQuestion(
        "COM-008", "Comercial", "Cómo crecen",
        "¿Existe una estrategia para lograr recompra, recomendación y ventas recurrentes?",
        ("Programa de fidelización", "Campañas de recompra", "Ventas recurrentes"),
        ("Oportunidades perdidas",),
    ),

    # Operaciones
    InterviewQuestion(
        "OPE-001", "Operaciones", "Cómo trabajan",
        "¿Los procesos críticos para organizar capacitaciones y eventos están documentados?",
        ("Manuales", "Checklists", "Cronogramas", "Plantillas"),
        ("Procesos no documentados",),
    ),
    InterviewQuestion(
        "OPE-002", "Operaciones", "Cómo trabajan",
        "¿Cada actividad y entregable tiene una persona responsable y una fecha definida?",
        ("Cronograma", "RACI", "Tablero de tareas"),
        ("Responsabilidades difusas", "Ejecución inconsistente"),
    ),
    InterviewQuestion(
        "OPE-003", "Operaciones", "Cómo trabajan",
        "¿Se utiliza una metodología común para planear y ejecutar cada proyecto o evento?",
        ("Plantilla de proyecto", "Cronograma maestro", "Checklist"),
        ("Ejecución inconsistente", "Procesos no documentados"),
    ),
    InterviewQuestion(
        "OPE-004", "Operaciones", "Cómo controlan",
        "¿Se controlan cambios, pendientes, incidencias y acuerdos durante cada proyecto?",
        ("Bitácora", "Control de cambios", "Minutas", "Tablero"),
        ("Gestión reactiva", "Información dispersa"),
    ),
    InterviewQuestion(
        "OPE-005", "Operaciones", "Cómo trabajan",
        "¿Los proveedores se seleccionan y evalúan con criterios definidos?",
        ("Padrón de proveedores", "Evaluaciones", "Cotizaciones"),
        ("Dependencia de proveedores",),
    ),
    InterviewQuestion(
        "OPE-006", "Operaciones", "Cómo controlan",
        "¿Se revisa la calidad del servicio antes, durante y después de cada evento o capacitación?",
        ("Checklist de calidad", "Encuestas", "Reporte de cierre"),
        ("Experiencia no medida", "Ejecución inconsistente"),
    ),
    InterviewQuestion(
        "OPE-007", "Operaciones", "Cómo controlan",
        "¿Se comparan tiempos, costos y resultados reales contra lo planeado?",
        ("Cierre de proyecto", "Presupuesto vs. real", "Lecciones aprendidas"),
        ("Falta de indicadores", "Gestión reactiva"),
    ),
    InterviewQuestion(
        "OPE-008", "Operaciones", "Qué les preocupa",
        "¿La operación puede continuar correctamente cuando falta una persona clave?",
        ("Manuales", "Respaldos", "Matriz de sustitución"),
        ("Dependencia del dueño", "Dependencia de personas clave"),
    ),

    # Personas
    InterviewQuestion(
        "PER-001", "Personas", "Cómo trabajan",
        "¿Cada puesto tiene funciones, resultados esperados y límites de autoridad claros?",
        ("Descripciones de puesto", "Organigrama", "Matriz RACI"),
        ("Responsabilidades difusas",),
    ),
    InterviewQuestion(
        "PER-002", "Personas", "Cómo trabajan",
        "¿Existe un proceso definido para seleccionar e incorporar colaboradores?",
        ("Perfil de puesto", "Proceso de selección", "Onboarding"),
        ("Gestión de personas informal",),
    ),
    InterviewQuestion(
        "PER-003", "Personas", "Cómo trabajan",
        "¿Las personas reciben capacitación para desempeñar sus responsabilidades?",
        ("Plan de capacitación", "Registros", "Evaluaciones"),
        ("Gestión de personas informal",),
    ),
    InterviewQuestion(
        "PER-004", "Personas", "Cómo controlan",
        "¿El desempeño se evalúa con objetivos y criterios conocidos?",
        ("Evaluaciones", "Objetivos individuales", "Retroalimentación"),
        ("Falta de indicadores", "Gestión de personas informal"),
    ),
    InterviewQuestion(
        "PER-005", "Personas", "Cómo trabajan",
        "¿Los líderes dan seguimiento y retroalimentación de forma periódica?",
        ("Reuniones uno a uno", "Minutas", "Planes de mejora"),
        ("Liderazgo reactivo",),
    ),
    InterviewQuestion(
        "PER-006", "Personas", "Qué les preocupa",
        "¿La empresa cuenta con reemplazos o planes de respaldo para funciones críticas?",
        ("Plan de sucesión", "Matriz de respaldo", "Manual de funciones"),
        ("Dependencia de personas clave",),
    ),
    InterviewQuestion(
        "PER-007", "Personas", "Cómo controlan",
        "¿Se monitorean rotación, ausentismo, carga de trabajo y necesidades del equipo?",
        ("Indicadores de personas", "Encuestas", "Registro de carga"),
        ("Falta de indicadores", "Sobrecarga operativa"),
    ),
    InterviewQuestion(
        "PER-008", "Personas", "Qué les preocupa",
        "¿El equipo puede plantear problemas y proponer mejoras sin temor?",
        ("Encuesta de clima", "Canales de propuestas", "Reuniones"),
        ("Comunicación deficiente", "Liderazgo reactivo"),
    ),
)


QUESTIONS_BY_CODE = {question.code: question for question in INTERVIEW_QUESTIONS}
AREAS = tuple(dict.fromkeys(question.area for question in INTERVIEW_QUESTIONS))
