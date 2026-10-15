"""Desarrollador backend: ajusta el objetivo y las instrucciones de tu agente básico."""

from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'backend'
LABEL = 'Desarrollador backend'
SPEC_FILE = 'backend_spec.md'
EXTRACT_CODE = True

agent = Agent(
    role='Backend',
    goal='Implementar el backend del requisito.',
    backstory='Escribes el código necesario para el contrato acordado.',
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
            'Sigue el contrato de Architect. Implementa solo el cambio solicitado, con validación de '
            'entrada y manejo de errores. Usa Quarkus 3.x y las dependencias existentes: Spring '
            'Web/DI/Data JPA, Jakarta Validation, H2/PostgreSQL y BCrypt. No agregues dependencias. '
            'Usa nombres en inglés y packages bajo pe.bcp.login: model, dto, service, resource o '
            'repository. Incluye package e imports completos. No regeneres pom.xml ni '
            'application.properties. Entrega archivos completos en bloques de código con su nombre '
            'como comentario en la primera línea.'
        ),
        expected_output=(
            'Código backend del cambio y una explicación breve. Cada archivo lleva su bloque con '
            'nombre.'
        ),
        agent=agent,
    )
