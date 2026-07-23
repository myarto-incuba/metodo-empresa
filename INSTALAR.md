# Método Empresa — UX Foundation

## 1. Haz un respaldo

Desde la raíz del proyecto:

```bash
git status
git add .
git commit -m "Backup before UX Foundation"
```

## 2. Copia el contenido del ZIP

Copia las carpetas y archivos sobre la raíz de:

```text
/Users/mac1/Projects/metodo-empresa
```

Esta versión reemplaza `app.py` y agrega:

```text
components/
views/
core/audit_facade.py
core/ux_repository.py
test_ux_foundation.py
```

No es necesario borrar la carpeta `pages/`. La navegación definida en `app.py`
pasa a controlar el menú.

## 3. Activa el entorno

```bash
source .venv/bin/activate
```

## 4. Ejecuta las pruebas

```bash
python test_interview_mvp.py
python test_ux_foundation.py
```

## 5. Ejecuta Streamlit

```bash
python -m streamlit run app.py --server.port 8511
```

El menú nuevo será:

- Dashboard
- Empresas
- Auditorías

Al seleccionar una auditoría aparecerán:

- Entrevista
- Evidencias
- Diagnóstico
- Plan de acción
