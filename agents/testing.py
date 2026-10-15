"""Ingeniero de pruebas: ajusta el objetivo y las instrucciones de tu agente básico."""

from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'testing'
LABEL = 'Ingeniero de pruebas'
SPEC_FILE = 'testing_report.md'
EXTRACT_CODE = True

agent = Agent(
    role='Testing',
    goal='Proponer pruebas básicas del cambio.',
    backstory='Revisas un caso válido y un caso inválido.',
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
            'Usa el requisito y las entregas anteriores. Escribe una prueba válida y una inválida con '
            'las dependencias existentes. Indica comandos y resultados esperados. Para Java usa JUnit '
            '5 y package pe.bcp.login; para Angular usa archivos .spec.ts e imports de los archivos '
            'entregados. Cada archivo completo va en un bloque de código con su nombre como '
            'comentario en la primera línea. No cambies producción. Marca los resultados NO '
            'EJECUTADO: no ejecutas herramientas.'
        ),
        expected_output=(
            'Dos casos, sus archivos de prueba, comandos y resultados esperados. Estado: NO '
            'EJECUTADO.'
        ),
        agent=agent,
    )
