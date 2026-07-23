"""
Biblioteca inicial de fenómenos empresariales de Método Empresa.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class BusinessPhenomenon:
    code: str
    name: str
    description: str
    affected_areas: list[str] = field(default_factory=list)
    control_codes: list[str] = field(default_factory=list)
    symptoms: list[str] = field(default_factory=list)
    consequences: list[str] = field(default_factory=list)
    indicators: list[str] = field(default_factory=list)
    suggested_actions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.code = self.code.strip().upper()
        self.name = self.name.strip()
        self.description = self.description.strip()
        self.affected_areas = _unique(self.affected_areas)
        self.control_codes = [value.upper() for value in _unique(self.control_codes)]
        self.symptoms = _unique(self.symptoms)
        self.consequences = _unique(self.consequences)
        self.indicators = _unique(self.indicators)
        self.suggested_actions = _unique(self.suggested_actions)

        if not self.code:
            raise ValueError("El fenómeno debe tener un código.")
        if not self.name:
            raise ValueError("El fenómeno debe tener un nombre.")
        if not self.description:
            raise ValueError("El fenómeno debe tener una descripción.")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @property
    def transversal_score(self) -> int:
        return len(self.affected_areas)


def _unique(values: list[str] | None) -> list[str]:
    if not values:
        return []

    result: list[str] = []
    seen: set[str] = set()

    for value in values:
        clean = str(value).strip()
        if not clean:
            continue

        key = clean.casefold()
        if key in seen:
            continue

        seen.add(key)
        result.append(clean)

    return result


BASE_PHENOMENA: list[BusinessPhenomenon] = [
    BusinessPhenomenon(
        code="FEN-001",
        name="Dependencia del dueño",
        description="Las decisiones y operaciones críticas dependen excesivamente de una sola persona.",
        affected_areas=["Dirección", "Personas", "Operaciones", "Comercial", "Finanzas"],
        control_codes=["DIR-002", "PER-001", "OPE-001", "COM-002", "FIN-003"],
        symptoms=[
            "Todo requiere autorización",
            "El propietario concentra información",
            "La operación se detiene en su ausencia",
        ],
        consequences=[
            "Cuellos de botella",
            "Sobrecarga directiva",
            "Riesgo de continuidad",
        ],
        indicators=["Tiempo de aprobación", "Decisiones escaladas"],
        suggested_actions=[
            "Definir niveles de autoridad",
            "Documentar procesos críticos",
            "Delegar decisiones recurrentes",
        ],
    ),
    BusinessPhenomenon(
        code="FEN-002",
        name="Falta de dirección estratégica",
        description="La empresa opera sin prioridades claras ni seguimiento formal de objetivos.",
        affected_areas=["Dirección", "Finanzas", "Comercial", "Operaciones", "Personas"],
        control_codes=["DIR-001", "DIR-003", "FIN-001", "COM-003", "PER-002"],
        symptoms=[
            "Proyectos contradictorios",
            "Cambios frecuentes de prioridad",
            "Recursos dispersos",
        ],
        consequences=[
            "Crecimiento desordenado",
            "Baja ejecución",
            "Desalineación organizacional",
        ],
        indicators=["Cumplimiento de objetivos", "Iniciativas retrasadas"],
        suggested_actions=[
            "Definir objetivos estratégicos",
            "Crear tablero ejecutivo",
        ],
    ),
    BusinessPhenomenon(
        code="FEN-003",
        name="Decisiones reactivas",
        description="Las decisiones se toman tarde, sin previsión o únicamente ante urgencias.",
        affected_areas=["Dirección", "Finanzas", "Comercial", "Operaciones"],
        control_codes=["DIR-003", "FIN-002", "FIN-003", "COM-003", "OPE-002"],
        symptoms=[
            "Urgencias frecuentes",
            "Compras de último minuto",
            "Falta de anticipación",
        ],
        consequences=[
            "Sobrecostos",
            "Pérdida de oportunidades",
            "Estrés organizacional",
        ],
        indicators=["Compras urgentes", "Desviaciones no previstas"],
        suggested_actions=[
            "Establecer ciclos de planeación",
            "Crear indicadores anticipados",
        ],
    ),
    BusinessPhenomenon(
        code="FEN-004",
        name="Ventas impredecibles",
        description="La empresa no puede estimar con suficiente certeza sus ingresos futuros.",
        affected_areas=["Comercial", "Finanzas", "Operaciones", "Dirección"],
        control_codes=["COM-001", "COM-002", "COM-003", "FIN-003", "OPE-002"],
        symptoms=[
            "Pipeline incompleto",
            "Seguimientos vencidos",
            "Forecast poco confiable",
        ],
        consequences=[
            "Ingresos inestables",
            "Problemas de capacidad",
            "Falta de liquidez",
        ],
        indicators=["Precisión del forecast", "Cobertura de pipeline"],
        suggested_actions=[
            "Definir proceso comercial",
            "Centralizar oportunidades",
            "Crear forecast ponderado",
        ],
    ),
    BusinessPhenomenon(
        code="FEN-005",
        name="Falta de liquidez",
        description="La empresa no dispone oportunamente del efectivo necesario para operar.",
        affected_areas=["Finanzas", "Comercial", "Operaciones", "Dirección"],
        control_codes=["FIN-001", "FIN-002", "FIN-003", "COM-003", "OPE-002"],
        symptoms=[
            "Pagos atrasados",
            "Uso recurrente de deuda",
            "Cobros no planificados",
        ],
        consequences=[
            "Financiamiento costoso",
            "Incumplimiento con proveedores",
            "Parálisis operativa",
        ],
        indicators=["Semanas de cobertura", "Cuentas vencidas"],
        suggested_actions=[
            "Crear flujo de caja de 13 semanas",
            "Vincular forecast con tesorería",
        ],
    ),
    BusinessPhenomenon(
        code="FEN-006",
        name="Desorden operativo",
        description="La ejecución presenta variaciones, improvisación y falta de consistencia.",
        affected_areas=["Operaciones", "Personas", "Dirección", "Finanzas"],
        control_codes=["OPE-001", "OPE-002", "OPE-003", "PER-001", "DIR-002"],
        symptoms=[
            "Formas distintas de hacer el mismo trabajo",
            "Retrasos recurrentes",
            "Dependencia de personas clave",
        ],
        consequences=[
            "Errores",
            "Retrabajos",
            "Sobrecostos",
        ],
        indicators=["Errores por proceso", "Cumplimiento de entregas"],
        suggested_actions=[
            "Documentar procesos",
            "Definir responsables",
            "Implementar listas de verificación",
        ],
    ),
    BusinessPhenomenon(
        code="FEN-007",
        name="Costos ocultos",
        description="La empresa incurre en pérdidas que no identifica ni mide con claridad.",
        affected_areas=["Finanzas", "Operaciones", "Personas"],
        control_codes=["FIN-002", "OPE-003", "PER-002", "PER-003"],
        symptoms=[
            "Retrabajos no cuantificados",
            "Horas extra recurrentes",
            "Errores repetitivos",
        ],
        consequences=[
            "Margen insuficiente",
            "Precios mal definidos",
            "Rentabilidad deteriorada",
        ],
        indicators=["Costo de no calidad", "Tasa de retrabajo"],
        suggested_actions=[
            "Registrar incidencias",
            "Cuantificar costos de no calidad",
        ],
    ),
    BusinessPhenomenon(
        code="FEN-008",
        name="Responsabilidades difusas",
        description="No existe claridad suficiente sobre quién decide, ejecuta o responde por los resultados.",
        affected_areas=["Personas", "Dirección", "Operaciones", "Comercial"],
        control_codes=["PER-001", "DIR-002", "OPE-001", "COM-002"],
        symptoms=[
            "Tareas sin dueño",
            "Duplicidad de trabajo",
            "Conflictos por responsabilidades",
        ],
        consequences=[
            "Retrasos",
            "Falta de rendición de cuentas",
            "Sobrecarga de personas clave",
        ],
        indicators=["Tareas sin responsable", "Escalamientos"],
        suggested_actions=[
            "Crear matriz RACI",
            "Actualizar descripciones de puesto",
        ],
    ),
    BusinessPhenomenon(
        code="FEN-009",
        name="Baja productividad",
        description="Los recursos humanos y operativos generan menos resultados de los esperados.",
        affected_areas=["Personas", "Operaciones", "Finanzas"],
        control_codes=["PER-002", "PER-003", "OPE-001", "OPE-003"],
        symptoms=[
            "Tiempos excesivos",
            "Errores frecuentes",
            "Resultados inconsistentes",
        ],
        consequences=[
            "Mayores costos",
            "Sobrecarga",
            "Menor capacidad de crecimiento",
        ],
        indicators=["Producción por persona", "Tasa de errores"],
        suggested_actions=[
            "Definir estándares de desempeño",
            "Cerrar brechas de competencia",
        ],
    ),
    BusinessPhenomenon(
        code="FEN-010",
        name="Falta de información para decidir",
        description="La dirección carece de datos oportunos, confiables o integrados.",
        affected_areas=["Dirección", "Finanzas", "Comercial", "Operaciones"],
        control_codes=["DIR-003", "FIN-002", "COM-002", "COM-003", "OPE-003"],
        symptoms=[
            "Reportes tardíos",
            "Versiones distintas de los datos",
            "Decisiones basadas en intuición",
        ],
        consequences=[
            "Reacción tardía",
            "Errores de priorización",
            "Riesgos no detectados",
        ],
        indicators=["Días de cierre", "Indicadores actualizados"],
        suggested_actions=[
            "Definir fuentes oficiales de información",
            "Crear tablero de gestión",
        ],
    ),
]


def get_phenomenon(code: str) -> BusinessPhenomenon | None:
    clean_code = code.strip().upper()
    return next(
        (phenomenon for phenomenon in BASE_PHENOMENA if phenomenon.code == clean_code),
        None,
    )


def validate_phenomena(control_codes: set[str]) -> list[str]:
    errors: list[str] = []
    codes = [phenomenon.code for phenomenon in BASE_PHENOMENA]

    duplicates = sorted({code for code in codes if codes.count(code) > 1})
    if duplicates:
        errors.append(f"Fenómenos duplicados: {', '.join(duplicates)}")

    for phenomenon in BASE_PHENOMENA:
        missing = [
            code
            for code in phenomenon.control_codes
            if code not in control_codes
        ]
        if missing:
            errors.append(
                f"{phenomenon.code} referencia controles inexistentes: "
                f"{', '.join(missing)}"
            )

    return errors
