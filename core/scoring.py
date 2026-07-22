from config import AUDIT_MODULES

def weighted_score(reviews):
    weights = {m["code"]: m["weight"] for m in AUDIT_MODULES}
    numerator = 0
    denominator = 0
    for row in reviews:
        weight = weights.get(row["module_code"], 0)
        numerator += float(row["score"]) * weight
        denominator += weight
    return round(numerator / denominator, 1) if denominator else 0

def maturity_label(score):
    if score < 40:
        return "Crítico"
    if score < 60:
        return "Vulnerable"
    if score < 75:
        return "Funcional"
    if score < 90:
        return "Optimizado"
    return "Escalable"
