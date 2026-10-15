"""Desarrollador frontend: ajusta el objetivo y las instrucciones de tu agente básico."""

from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'frontend'
LABEL = 'Desarrollador frontend'
SPEC_FILE = 'frontend_spec.md'
EXTRACT_CODE = True

agent = Agent(
    role='Frontend',
    goal='Crear una interfaz pequeña para el requisito.',
    backstory='Conectas una vista con la API acordada.',
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
            'Sigue el contrato de Architect y Backend. Crea una vista Angular 17 standalone que envíe '
            'la entrada y muestre el resultado o el error. Usa TypeScript estricto, nombres en inglés '
            'y las dependencias existentes. Conserva la sesión si existe. Entrega los componentes del '
            'feature en src/app/auth/, su servicio HTTP y los archivos de arranque '
            'src/app/app.component.ts y src/app/app.routes.ts. Exporta AppComponent con selector app- '
            'root y routes: Routes; la raíz usa router-outlet y las rutas importan desde ./auth/. '
            'Incluye los imports del template y cualquier CSS referenciado. main.ts ya provee HTTP y '
            'router; no regeneres la configuración. Entrega archivos completos en bloques de código '
            'con su nombre como comentario en la primera línea.'
        ),
        expected_output=(
            'Código de la vista, su servicio y el arranque necesario, en bloques con nombre de '
            'archivo.'
        ),
        agent=agent,
    )
