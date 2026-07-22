# Método Empresa

Beta profesional en Streamlit para auditorías empresariales integrales de Incubatour.

## Propósito

Convertir entrevistas, formularios, documentos y datos financieros en:

- hallazgos comprobables
- causas raíz
- riesgos
- oportunidades de ahorro
- acciones concretas
- una ruta de transformación empresarial

## Instalación

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

En Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Flujo de trabajo

1. Registrar empresa
2. Crear auditoría
3. Completar expediente
4. Evaluar los nueve módulos
5. Registrar hallazgos
6. Convertir hallazgos en acciones
7. Consultar dashboard y roadmap

## Alcance de esta beta

Incluye:

- SQLite local
- empresas y auditorías
- expediente general
- diagnóstico por módulos
- hallazgos accionables
- plan de acción
- dashboard ejecutivo
- importación base de datos financiera desde Excel o CSV
- motor inicial de alertas financieras

No incluye todavía:

- autenticación
- almacenamiento en nube
- permisos avanzados
- IA generativa
- exportación PDF final
- formularios externos para clientes
