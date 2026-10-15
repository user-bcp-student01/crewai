"""Revisor de seguridad: edita aquí el rol, el objetivo y las instrucciones de su tarea."""

from crewai import Agent, Task
from crew.llm_config import llm

KEY = "security"
LABEL = "Revisor de seguridad"
SPEC_FILE = "security_report.md"
EXTRACT_CODE = False
agent = Agent(
    role="Security Reviewer",
    goal="Revisar la seguridad de la solución y registrar hallazgos verificables.",
    backstory=(
        "Eres un revisor de seguridad de aplicaciones bancarias. Identificas riesgos en el código\n"
        "recibido, sin atribuir certificaciones ni resultados de herramientas que no ejecutaste."
    ),
    llm=llm,
    verbose=True,
    allow_delegation=False,
)


def build_task(feature: dict) -> Task:
    title = feature.get("title", "(sin título)")
    description = feature.get("description", "")
    ac_text = (
        "\n".join((f"  - {c}" for c in feature.get("acceptance_criteria", [])))
        or description
    )
    feature_brief = (
        f"Feature: {title}\n\n{description}\n\nCriterios de aceptación:\n{ac_text}"
    )
    return Task(
        description=(
            "Revisa las especificaciones, backend, frontend y pruebas aprobadas del feature.\n"
            "Inspecciona autenticación, autorización, validación de entradas, inyección, manejo de\n"
            "secretos, datos personales, errores y logs. Para cada hallazgo indica archivo, evidencia,\n"
            "severidad, corrección y prueba de verificación. Separa riesgos confirmados de\n"
            "verificaciones pendientes. No modifiques código. No declares pruebas ejecutadas."
        )
        + feature_brief,
        expected_output="Informe de seguridad con hallazgos, severidad, evidencia y verificaciones pendientes.",
        agent=agent,
    )
