from pathlib import Path
from tempfile import TemporaryDirectory
import json

import core.ux_repository as repository


def main() -> None:
    with TemporaryDirectory() as temp:
        original = repository.DATA_PATH
        repository.DATA_PATH = Path(temp) / "ux.json"
        try:
            evidence = repository.load_evidence("AUD-UX")
            assert len(evidence) == 10
            evidence[0]["status"] = "Disponible"
            repository.save_evidence("AUD-UX", evidence)
            assert repository.load_evidence("AUD-UX")[0]["status"] == "Disponible"

            plan = [{
                "action": "Formalizar estrategia",
                "priority": "Alta",
                "owner": "Dirección",
                "deadline": "30 días",
                "status": "Pendiente",
            }]
            repository.save_action_plan("AUD-UX", plan)
            assert repository.load_action_plan("AUD-UX") == plan
        finally:
            repository.DATA_PATH = original

    print("UX Foundation válida")
    print("Evidencias, diagnóstico y plan de acción listos")


if __name__ == "__main__":
    main()
