"""Ingeniero de pruebas: edita aquí el rol, el objetivo y las instrucciones de su tarea."""

from crewai import Agent, Task
from crew.llm_config import llm

KEY = "testing"
LABEL = "Ingeniero de pruebas"
SPEC_FILE = "testing_report.md"
EXTRACT_CODE = True
agent = Agent(
    role="Testing Engineer",
    goal="Diseñar pruebas para los criterios de aceptación y generar tests del backend y del frontend.",
    backstory=(
        "Eres un ingeniero de pruebas de aplicaciones Quarkus 3.x y Angular 17. Distingues pruebas\n"
        "propuestas de pruebas ejecutadas. Solo recibes texto y no ejecutas herramientas."
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
            "Revisa la especificación y las implementaciones aprobadas del feature. Entrega una matriz\n"
            "criterio → caso → resultado esperado, casos negativos y de integración, tests JUnit 5 y\n"
            "tests Angular cuando apliquen, y los comandos para ejecutarlos. Usa únicamente las\n"
            "dependencias existentes del andamiaje. Cada archivo va en su bloque markdown con el nombre\n"
            "como comentario en la primera línea. Para Java usa package pe.bcp.login; para Angular\n"
            "nombra los tests <feature>.spec.ts y respeta las rutas de importación. Marca los\n"
            "resultados como NO EJECUTADO hasta que una persona aporte la salida real. No cambies\n"
            "código de producción ni inventes resultados."
        )
        + feature_brief,
        expected_output="Matriz de cobertura, archivos de prueba, comandos reproducibles y pendientes de verificación humana.",
        agent=agent,
    )
