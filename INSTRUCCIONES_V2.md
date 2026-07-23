# Método Empresa — Look & Feel Incubatour

Esta actualización aplica una identidad visual inspirada en la comunicación
actual de Incubatour:

- "Le ponemos método a tu locura."
- enfoque en resultados;
- lenguaje directo;
- energía latinoamericana;
- estética oscura, contrastes vivos y tarjetas editoriales.

## Instalación

Desde la raíz del proyecto:

```bash
git add .
git commit -m "Backup before Incubatour visual system"
```

Copia sobre el proyecto:

```bash
cp -R metodo_empresa_incubatour_v2/components/* components/
cp -R metodo_empresa_incubatour_v2/views/* views/
cp metodo_empresa_incubatour_v2/app.py .
```

Reinicia Streamlit:

```bash
python -m streamlit run app.py --server.port 8512
```

## Archivos que se reemplazan

- app.py
- views/dashboard.py
- views/interview.py

## Archivo nuevo

- components/brand.py

El resto de las funciones y datos se conserva.
