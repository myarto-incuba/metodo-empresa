APP_NAME = "Le ponemos método a tu empresa"
APP_SUBTITLE = "Diagnóstico integral, decisiones claras y acciones concretas."

AUDIT_MODULES = [
    {
        "code": "FIN",
        "name": "Finanzas y rentabilidad",
        "weight": 25,
        "description": "Ingresos, costos, gastos, nómina, rentabilidad, liquidez, deuda, cartera y control financiero.",
    },
    {
        "code": "EST",
        "name": "Estrategia y modelo de negocio",
        "weight": 10,
        "description": "Propuesta de valor, líneas de negocio, objetivos, diferenciadores y capacidad de crecimiento.",
    },
    {
        "code": "ORG",
        "name": "Organización y recursos humanos",
        "weight": 12,
        "description": "Organigrama, puestos, responsabilidades, jerarquías, productividad y costo laboral.",
    },
    {
        "code": "PRO",
        "name": "Procesos y flujos de trabajo",
        "weight": 12,
        "description": "Procesos, tareas, responsables, tiempos, controles y documentación.",
    },
    {
        "code": "OPE",
        "name": "Operación",
        "weight": 12,
        "description": "Capacidad, entrega, calidad, incidencias, retrabajos y proveedores.",
    },
    {
        "code": "VEN",
        "name": "Ventas y desarrollo comercial",
        "weight": 12,
        "description": "Pipeline, bases de datos, seguimiento, comisiones, conversión y cartera.",
    },
    {
        "code": "MAR",
        "name": "Marca, marketing y comunicación",
        "weight": 7,
        "description": "Marca paraguas, narrativa, canales, campañas y consistencia.",
    },
    {
        "code": "TEC",
        "name": "Tecnología y automatización",
        "weight": 6,
        "description": "Software, herramientas, integraciones y tareas automatizables.",
    },
    {
        "code": "COM",
        "name": "Comunicación interna y cultura",
        "weight": 4,
        "description": "Canales, reuniones, decisiones, liderazgo y gestión del conocimiento.",
    },
]

STATUS_OPTIONS = ["No iniciado", "En curso", "En validación", "Completado"]
RISK_LEVELS = ["Crítico", "Alto", "Medio", "Bajo"]
CONFIDENCE_LEVELS = [
    "Verificado",
    "Parcialmente verificado",
    "Declarado",
    "Estimado",
    "Inconsistente",
]
ACTION_HORIZONS = [
    "Inmediata",
    "Primeros 30 días",
    "31 a 90 días",
    "3 a 6 meses",
    "Más de 6 meses",
]
ACTION_STATUS = ["Pendiente", "En curso", "Bloqueada", "Completada"]
CURRENCIES = ["MXN", "EUR", "USD", "COP"]
