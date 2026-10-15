"""Arquitecto: ajusta el objetivo y las instrucciones de tu agente básico."""

from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'architect'
LABEL = 'Arquitecto'
SPEC_FILE = 'user_story.md'
EXTRACT_CODE = False

agent = Agent(
    role='Architect',
    goal='Definir el cambio mínimo para el requisito.',
    backstory='Ayudas al equipo a acordar una solución pequeña.',
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
            'Lee el requisito y los criterios. Describe los archivos afectados y el contrato de API: '
            'método, ruta, entrada, respuesta y errores. Conserva los criterios recibidos.'
        ),
        expected_output=(
            'Plan breve, contrato de API y criterios de aceptación.'
        ),
        agent=agent,
    )
