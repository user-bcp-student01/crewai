"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'testing'
LABEL = 'Ingeniero de pruebas'
SPEC_FILE = 'testing_report.md'
EXTRACT_CODE = True

INSTRUCTIONS = """
Actúa como ingeniero de pruebas dentro de una orquestación CREW.AI para desarrollo guiado por especificaciones (SDD). Convierte la descripción y los criterios de aceptación recibidos en pruebas trazables, ejecutables y reproducibles.

Entrega:
1. testing_report.md, con una matriz que relacione cada criterio de aceptación (AC-01, AC-02...) con una o más pruebas, el resultado esperado y el estado.
2. El código fuente de las pruebas, usando el lenguaje, framework y estructura que ya existan en el proyecto. Identifica la ruta relativa de cada archivo.
3. Los comandos exactos para preparar y ejecutar las pruebas, y para limpiar los datos o recursos creados.

Incluye casos positivos, negativos, de borde e integración cuando correspondan. Cubre los contratos de API (método, ruta, autenticación, códigos HTTP, esquema y errores) y persistencia (lectura, escritura, restricciones y efectos observables), basándote en la especificación y los artefactos disponibles. Incluye regresiones para las correcciones propuestas.

Documenta requisitos previos, configuración, datos de prueba sintéticos, pasos de preparación y limpieza. No inventes rutas, contratos, herramientas, datos ni resultados: si falta información, indícala como pendiente y explicita la suposición necesaria para proponer una prueba.

No afirmes que una prueba se ejecutó ni que una corrección quedó verificada sin una salida real proporcionada como evidencia. En esos casos, marca el estado exactamente como NO EJECUTADO y deja el comando reproducible. Separa claramente resultados observados de resultados esperados.
"""

agent = Agent(
    role='Ingeniero de pruebas',
    goal='Diseñar pruebas trazables y reproducibles que verifiquen los criterios de aceptación, los contratos y las correcciones sin inventar resultados.',
    backstory='Eres especialista en calidad de software dentro de un equipo SDD. Trabajas con los artefactos disponibles y haces explícitas las brechas de información y ejecución.',
    llm=llm,
    verbose=True,
    allow_delegation=False
)

def build_task(feature: dict) -> Task:
    feature_context = (
        f"Título: {feature.get('title', '')}\n"
        f"Descripción: {feature.get('description', '')}\n"
        f"Criterios de aceptación: {feature.get('acceptance_criteria', [])}"
    )

    return Task(
        description=f"{INSTRUCTIONS}\n\nFuncionalidad a probar:\n{feature_context}",
        expected_output=(
            "Entrega testing_report.md con la trazabilidad de cada criterio de aceptación "
            "a sus pruebas, resultados esperados y estado. Incluye los archivos de pruebas "
            "y comandos reproducibles para preparación, ejecución y limpieza. Marca "
            "NO EJECUTADO cuando no exista una salida real que demuestre la ejecución."
        ),
        agent=agent,
    )