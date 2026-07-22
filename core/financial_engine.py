import pandas as pd

REQUIRED_COLUMNS = ["period", "category", "subcategory", "description", "amount"]

def normalize_financial_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    normalized = df.copy()
    normalized.columns = [str(c).strip().lower().replace(" ", "_") for c in normalized.columns]

    aliases = {
        "periodo": "period",
        "categoría": "category",
        "categoria": "category",
        "subcategoría": "subcategory",
        "subcategoria": "subcategory",
        "concepto": "description",
        "descripcion": "description",
        "descripción": "description",
        "monto": "amount",
        "importe": "amount",
    }
    normalized = normalized.rename(columns=aliases)

    missing = [c for c in REQUIRED_COLUMNS if c not in normalized.columns]
    if missing:
        raise ValueError("Faltan columnas: " + ", ".join(missing))

    normalized["amount"] = pd.to_numeric(normalized["amount"], errors="coerce").fillna(0)
    normalized["source"] = "Archivo importado"
    return normalized[REQUIRED_COLUMNS + ["source"]]

def financial_summary(df: pd.DataFrame) -> dict:
    if df.empty:
        return {
            "income": 0,
            "costs": 0,
            "expenses": 0,
            "payroll": 0,
            "profit": 0,
            "margin": 0,
        }

    categories = df["category"].astype(str).str.lower().str.strip()
    amount = pd.to_numeric(df["amount"], errors="coerce").fillna(0)

    income = amount[categories.isin(["ingreso", "ingresos", "venta", "ventas"])].sum()
    costs = amount[categories.isin(["costo", "costos", "coste", "costes"])].sum()
    expenses = amount[categories.isin(["gasto", "gastos"])].sum()
    payroll = amount[categories.isin(["nomina", "nómina", "payroll"])].sum()
    profit = income - costs - expenses - payroll
    margin = (profit / income * 100) if income else 0

    return {
        "income": float(income),
        "costs": float(costs),
        "expenses": float(expenses),
        "payroll": float(payroll),
        "profit": float(profit),
        "margin": float(margin),
    }

def financial_alerts(summary: dict) -> list[dict]:
    alerts = []
    income = summary["income"]
    payroll = summary["payroll"]
    profit = summary["profit"]
    margin = summary["margin"]

    if income <= 0:
        alerts.append({
            "level": "Crítico",
            "title": "No hay ingresos identificados",
            "message": "El archivo no contiene ingresos reconocibles o la clasificación necesita revisión."
        })
        return alerts

    payroll_ratio = payroll / income * 100
    if payroll_ratio > 40:
        alerts.append({
            "level": "Alto",
            "title": "Nómina elevada frente a ingresos",
            "message": f"La nómina representa {payroll_ratio:.1f}% de los ingresos."
        })

    if profit < 0:
        alerts.append({
            "level": "Crítico",
            "title": "Resultado operativo negativo",
            "message": "Los costos, gastos y nómina superan los ingresos del periodo."
        })
    elif margin < 10:
        alerts.append({
            "level": "Alto",
            "title": "Margen operativo vulnerable",
            "message": f"El margen estimado es de {margin:.1f}%."
        })

    if not alerts:
        alerts.append({
            "level": "Bajo",
            "title": "Sin alertas automáticas críticas",
            "message": "La lectura inicial no detectó umbrales críticos. Aún se requiere validación humana."
        })
    return alerts
