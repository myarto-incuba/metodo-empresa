from pathlib import Path
from tempfile import TemporaryDirectory

from core.interview_repository import add_observation, load_interview, save_answer
from core.scoring_engine import calculate_results


def main() -> None:
    with TemporaryDirectory() as temp:
        path = Path(temp) / "interviews.json"
        audit_id = "AUD-TEST"

        save_answer(audit_id, "DIR-001", "No", "No existe documento.", data_path=path)
        save_answer(audit_id, "DIR-002", "Parcialmente", data_path=path)
        save_answer(audit_id, "FIN-001", "Sí", data_path=path)
        add_observation(
            audit_id,
            "La pregunta sobre socios debe ampliarse.",
            "DIR-002",
            data_path=path,
        )

        interview = load_interview(audit_id, data_path=path)
        assert len(interview["answers"]) == 3
        assert len(interview["observations"]) == 1

        results = calculate_results(interview)
        assert results["answered"] == 3
        assert results["overall_score"] == 50
        assert results["hypotheses"]
        assert results["recommendations"]

        print("Entrevista y dashboard válidos")
        print("Respondidas:", results["answered"])
        print("Madurez:", results["maturity"])
        print("Resultado general:", f'{results["overall_score"]}%')
        print("Hipótesis principal:", results["hypotheses"][0]["name"])


if __name__ == "__main__":
    main()
