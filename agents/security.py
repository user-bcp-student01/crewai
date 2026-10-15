"""Revisor de seguridad: ajusta el objetivo y las instrucciones de tu agente básico."""

from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'security'
LABEL = 'Revisor de seguridad'
SPEC_FILE = 'security_report.md'
EXTRACT_CODE = False

agent = Agent(
    role='Security',
    goal='Revisar la entrada y los secretos del cambio.',
    backstory='Revisas el código recibido y señalas riesgos concretos.',
    llm=llm,
    verbose=True,
    allow_delegation=False,
)


def build_task(feature: dict) -> Task:
    title = feature.get("title", "(sin título)")
    description = feature.get("description", "")
    criteria = "\n".join(f"- {item}" for item in feature.get("acceptance_criteria", []))
    return Task(
        description=(
            f"Feature: {title}\n{description}\nCriterios de aceptación:\n{criteria}\n\n"
            'Revisa la validación del lado servidor y los secretos en las entregas anteriores. Si '
            'cambia autenticación o autorización, revisa también esos controles. Por cada hallazgo '
            'cita archivo, evidencia y corrección. Si no ves hallazgos, indica qué revisaste. Señala '
            'las verificaciones pendientes. No cambies código ni afirmes haber ejecutado pruebas.'
        ),
        expected_output=(
            'Lista breve de hallazgos o comprobaciones, con evidencia y pendientes.'
        ),
        agent=agent,
    )
