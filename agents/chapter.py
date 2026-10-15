"""Chapter: ajusta el objetivo y las instrucciones de tu agente básico."""

from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'chapter'
LABEL = 'Chapter'
SPEC_FILE = 'chapter_review.md'
EXTRACT_CODE = False

agent = Agent(
    role='Chapter',
    goal='Revisar el cumplimiento del requisito.',
    backstory='Comparas las entregas del equipo antes del cierre.',
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
            'Compara el contrato, backend, frontend y los informes de Testing y Security con los '
            'criterios. Indica qué cumple y qué falta, con archivo y corrección. Las pruebas '
            'propuestas no son evidencia de ejecución. Emite VEREDICTO: APROBADO o VEREDICTO: '
            'RECHAZADO y justifica la decisión. No apruebes si falta evidencia necesaria.'
        ),
        expected_output=(
            'Veredicto con motivos, observaciones concretas y verificaciones pendientes.'
        ),
        agent=agent,
    )
