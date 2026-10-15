"""Arquitecto: edita aquí el rol, el objetivo y las instrucciones de su tarea."""

from crewai import Agent, Task
from crew.llm_config import llm

KEY = "architect"
LABEL = "Arquitecto"
SPEC_FILE = "user_story.md"
EXTRACT_CODE = False

agent = Agent(
    role="Technical Designer",
    goal=(
        "Analizar el feature brief recibido y producir una especificación "
        "técnica completa: arquitectura, componentes, contrato de API y "
        "criterios de aceptación medibles — todo alineado a los estándares "
        "de seguridad y calidad del BCP."
    ),
    backstory=(
        "Eres un arquitecto de software senior con 10 años de experiencia en "
        "banca digital peruana. Conoces los estándares PCI-DSS y las normas "
        "de la SBS, y aplicas los patrones de diseño más robustos en sistemas "
        "financieros de alta disponibilidad. Tu output es siempre una "
        "especificación técnica clara con diagramas conceptuales en texto, "
        "decisiones de diseño justificadas y criterios de aceptación explícitos."
    ),
    llm=llm,
    verbose=True,
    allow_delegation=False,
)


def build_task(feature: dict) -> Task:
    title = feature.get("title", "(sin título)")
    description = feature.get("description", "")
    ac_text = (
        "\n".join(f"  - {c}" for c in feature.get("acceptance_criteria", []))
        or description
    )
    feature_brief = (
        f"Feature: {title}\n\n{description}\n\nCriterios de aceptación:\n{ac_text}"
    )
    return Task(
        description=(
            f"Analiza el siguiente brief de feature y produce una especificación "
            f"técnica completa alineada a los estándares BCP:\n\n"
            f"{feature_brief}\n\n"
            "Tu output debe incluir:\n"
            "1. Resumen del módulo (2-3 párrafos)\n"
            "2. Componentes principales con responsabilidades\n"
            "3. Contrato de la API principal (endpoint, método HTTP, "
            "   request body, response body y códigos de error)\n"
            "4. Reglas de negocio formalizadas\n"
            "5. Criterios de aceptación medibles — uno por cada criterio "
            "   listado en el brief, en formato 'Dado / Cuando / Entonces'"
        ),
        expected_output=(
            "Especificación técnica en texto estructurado con secciones "
            "numeradas, contrato de API en formato JSON/pseudocódigo y "
            "lista de criterios de aceptación con formato "
            "'Dado / Cuando / Entonces'. Mínimo un criterio por cada "
            "acceptance criteria del feature."
        ),
        agent=agent,
    )
