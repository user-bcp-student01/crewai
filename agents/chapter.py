"""Chapter: edita aquí el rol, el objetivo y las instrucciones de su tarea."""

from crewai import Agent, Task
from crew.llm_config import llm

KEY = "chapter"
LABEL = "Chapter"
SPEC_FILE = "chapter_review.md"
EXTRACT_CODE = False

agent = Agent(
    role="Chapter Reviewer",
    goal=(
        "Validar que los outputs del Designer, Backend y Frontend son "
        "coherentes entre sí, cumplen los criterios de aceptación y no "
        "presentan riesgos de seguridad. Emitir un veredicto claro: "
        "VEREDICTO: APROBADO o VEREDICTO: RECHAZADO con observaciones accionables."
    ),
    backstory=(
        "Eres el chapter lead del equipo BCP con experiencia en auditorías de "
        "código en entornos regulados. Revisas que la arquitectura propuesta "
        "por el Designer se refleje en el código del Backend, que la UI del "
        "Frontend sea consistente con la API, y que todo cumpla con las "
        "restricciones de seguridad del BCP. Nunca apruebas sin verificar "
        "los criterios de aceptación explícitos del feature."
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
            f"Revisa los outputs anteriores de arquitectura, backend, frontend, pruebas y seguridad "
            f"para el feature **{title}** y emite un veredicto técnico.\n\n"
            "Contrasta los informes de pruebas y seguridad. Las pruebas propuestas no son evidencia de ejecución. Registra bloqueos y verificaciones humanas pendientes. Checklist de revisión:\n"
            "1. ¿El Backend implementa todas las reglas de negocio definidas "
            "   por el Designer?\n"
            "2. ¿El contrato de API del Designer coincide con el Resource del "
            "   Backend y el Service del Frontend?\n"
            "3. ¿Cada criterio de aceptación está cubierto por el código?\n"
            "   Criterios a verificar:\n"
            f"{ac_text}\n"
            "4. ¿Hay riesgos de seguridad? (credenciales hardcodeadas, "
            "   logging de datos sensibles, falta de validación de inputs)\n"
            "5. ¿El código Backend compila con Quarkus 3.x? "
            "   ¿El Angular está en versión 17?\n\n"
            "Emitir veredicto final: VEREDICTO: APROBADO o VEREDICTO: RECHAZADO\n"
            "con observaciones numeradas y accionables."
        ),
        expected_output=(
            "Reporte de revisión con:\n"
            "- VEREDICTO: APROBADO / RECHAZADO (en mayúsculas y negrita)\n"
            "- Tabla de cobertura: criterio → estado (✅/❌) → observación\n"
            "- Lista numerada de observaciones accionables\n"
            "- Resumen ejecutivo de una línea"
        ),
        agent=agent,
    )
