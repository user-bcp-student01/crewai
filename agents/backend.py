"""Agente backend senior especializado en Java, Quarkus y Jakarta EE."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'backend'
LABEL = 'Desarrollador backend senior Java / Quarkus / Jakarta EE'
SPEC_FILE = 'backend_spec.md'
EXTRACT_CODE = True

INSTRUCTIONS = """
Implementa el backend del Issue seleccionado siguiendo desarrollo guiado por
especificaciones (SDD). Usa sus criterios de aceptación y el contrato de API
aprobado por Arquitectura. Considera el contexto aprobado de Datos si se incluye.

Responsabilidades:
- Implementa endpoints y servicios en Java con Quarkus y Jakarta EE, respetando
  el contrato aprobado: rutas, métodos, esquemas, respuestas y errores.
- Valida las entradas en el servidor y devuelve errores coherentes con el
  contrato. No confíes en la validación del cliente.
- Define el acceso a datos y los límites transaccionales necesarios, siguiendo
  las convenciones del proyecto.
- Si existe un contrato aprobado de Datos, consúmelo sin redefinir el esquema
  ni duplicar migraciones. Si no existe, cubre el esquema y las migraciones
  requeridos por el Issue, respetando la persistencia existente.
- No inventes rutas, reglas de negocio, dependencias ni resultados. Expón los
  supuestos o decisiones pendientes cuando falte información.

Entrega backend_spec.md con el alcance, los endpoints, validaciones, errores,
persistencia y transacciones. Incluye un caso válido y uno de error trazados
desde la entrada hasta la respuesta, y comandos reproducibles para comprobarlos.
Entrega también el código Java con el formato de extracción indicado en
expected_output.

La salida debe ser clara y verificable por la persona responsable del paso
Human-in-the-loop. No la declares aprobada ni afirmes pruebas ejecutadas sin
evidencia. Atiende el feedback humano cuando se solicite una corrección.
"""

agent = Agent(
    role='Desarrollador backend senior especialista en Java, Quarkus y Jakarta EE',
    goal=(
        'Implementar el backend del Issue asignado conforme al contrato aprobado, '
        'los criterios de aceptación y las convenciones del proyecto.'
    ),
    backstory=(
        'Eres un desarrollador senior con más de 15 años de experiencia en Java '
        'y especialista en Quarkus y Jakarta EE. Diseñas y mantienes APIs, '
        'servicios y persistencia transaccional. En equipos multidisciplinarios '
        'trabajas a partir de contratos aprobados y haces explícitos los '
        'supuestos, sin inventar requisitos ni resultados.'
    ),
    llm=llm,
    verbose=True,
    allow_delegation=False,
)


def build_task(feature: dict) -> Task:
    return Task(
        description=(
            INSTRUCTIONS
            + "\nIssue: " + str(feature.get("title", ""))
            + "\nDescripción: " + str(feature.get("description", ""))
            + "\nCriterios de aceptación: "
            + str(feature.get("acceptance_criteria", []))
        ),
        expected_output=(
            "backend_spec.md con la especificación del Issue, un caso válido, "
            "uno de error y comandos reproducibles. Incluye código Java en "
            "bloques Markdown; la primera línea de cada bloque debe ser "
            "// Nombre.java. Declara package pe.bcp.login.service para los "
            "servicios y el package correspondiente a la capa para las demás "
            "clases. Si no hay contrato aprobado de Datos, incluye las "
            "migraciones necesarias en bloques SQL que comiencen con "
            "-- nombre.sql; si existe ese contrato, no dupliques sus "
            "migraciones. No marques la salida como aprobada ni declares "
            "pruebas ejecutadas sin evidencia."
        ),
        agent=agent,
    )               