from core.narrative_engine import build_strategic_reading
from core.pattern_engine import build_copilot, detect_patterns


def sample_interview():
    return {
        "answers": {
            "DIR-001": {"answer": "No", "comment": "No existe plan anual."},
            "DIR-002": {"answer": "No", "comment": "Todo lo autoriza la fundadora."},
            "DIR-004": {"answer": "Parcialmente", "comment": "Solo se reúnen cuando hay problemas."},
            "DIR-005": {"answer": "No", "comment": "No cuentan con tablero."},
            "DIR-006": {"answer": "Parcialmente", "comment": "Los roles se cruzan."},
            "DIR-007": {"answer": "No", "comment": "No hay presupuesto anual."},
            "COM-001": {"answer": "No", "comment": "Venden por relaciones."},
            "COM-002": {"answer": "Parcialmente", "comment": "Usan hojas separadas."},
            "COM-003": {"answer": "No", "comment": "No miden conversión."},
            "OPE-001": {"answer": "No", "comment": "Los procesos no están escritos."},
            "OPE-003": {"answer": "Parcialmente", "comment": "Cada proyecto se lleva distinto."},
        }
    }


def test_patterns():
    patterns = detect_patterns(sample_interview())
    names = {pattern["name"] for pattern in patterns}
    assert "Gestión reactiva" in names
    assert "Dependencia de la dirección" in names
    assert "Comercial reactivo" in names
    assert "Operación basada en conocimiento tácito" in names


def test_copilot():
    copilot = build_copilot(sample_interview())
    assert copilot["patterns"]
    assert copilot["evidence"]
    assert copilot["follow_up_questions"]


def test_narrative():
    reading = build_strategic_reading(sample_interview(), company_name="Synoni")
    assert "Synoni" in reading["executive_summary"]
    assert reading["roadmap"]
    assert reading["headline"]


if __name__ == "__main__":
    test_patterns()
    test_copilot()
    test_narrative()
    print("Consultor digital válido")
