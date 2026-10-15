"""Desarrollador frontend: edita aquí el rol, el objetivo y las instrucciones de su tarea."""

from crewai import Agent, Task
from crew.llm_config import llm

KEY = "frontend"
LABEL = "Desarrollador frontend"
SPEC_FILE = "frontend_spec.md"
EXTRACT_CODE = True

agent = Agent(
    role="Frontend Developer",
    goal=(
        "Diseñar e implementar la interfaz Angular 17 del feature para los "
        "usuarios finales del BCP. Entregar componentes, servicios y guards "
        "listos para producción, con UX clara y segura."
    ),
    backstory=(
        "Eres un desarrollador frontend Angular 17 especializado en "
        "aplicaciones financieras del BCP. Priorizas seguridad (AuthGuard, "
        "interceptors de token), accesibilidad y claridad de la información. "
        "Describes y generas los componentes con sus servicios, guards e "
        "interceptors en TypeScript, con sus eventos y ciclo de vida."
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
            f"Basándote en la API definida por el Designer y el Backend "
            f"para el feature **{title}**, implementa los componentes Angular 17.\n\n"
            "IMPORTANTE: Todo el código fuente (interfaces, servicios, componentes, selectores y archivos) "
            "debe generarse estrictamente en INGLÉS bajo estándares Angular 17.\n\n"
            "Requisitos de entrega:\n"
            "- models.ts: exportar todas las interfaces TypeScript del feature con `export interface ...`\n"
            "- <feature>.service.ts: servicio HTTP que consume los endpoints del backend, importando los modelos.\n"
            "- auth.guard.ts o <feature>.guard.ts: guard de acceso para proteger la vista.\n"
            "- <feature>.component.ts: componente STANDALONE (`standalone: true, imports: [CommonModule, ReactiveFormsModule]`) adaptado a este feature.\n"
            "- <feature>.component.html: plantilla con formulario/interfaz, controles interactivos, validaciones visuales y mensajes al usuario.\n"
            "- auth.interceptor.ts: interceptor HTTP si se requiere manejo de token.\n"
            "- <feature>.component.css: estilos del componente, con las clases que usa su HTML.\n"
            "- app.routes.ts: `export const routes: Routes = [...]` con las rutas que este feature necesita.\n"
            "- app.component.ts: componente raíz standalone, selector `app-root`, con `<router-outlet>`.\n\n"
            "CONTRATO DE ARRANQUE (el andamiaje ya existe en disco, no lo generas tú):\n"
            "`src/main.ts`, `src/index.html`, `src/styles.css`, `package.json`, `angular.json` y los "
            "tsconfig ya están escritos. `main.ts` arranca la app exactamente así:\n"
            "```typescript\n"
            "import { AppComponent } from './app/app.component';\n"
            "import { routes } from './app/app.routes';\n"
            "bootstrapApplication(AppComponent, {\n"
            "  providers: [provideRouter(routes, withComponentInputBinding()), provideHttpClient(withInterceptorsFromDi())]\n"
            "});\n"
            "```\n"
            "Por lo tanto, sin excepción:\n"
            "- `app.component.ts` DEBE exportar la clase con el nombre EXACTO `AppComponent` "
            "y declarar `selector: 'app-root'` (index.html contiene `<app-root></app-root>`).\n"
            "- `app.routes.ts` DEBE exportar `export const routes: Routes = [...]` con ese nombre EXACTO.\n"
            "- Los componentes del feature se guardan en `src/app/auth/`, así que `app.routes.ts` los "
            "importa desde `'./auth/<nombre>.component'`.\n"
            "- Si el componente usa `styleUrls`, el .css debe llamarse igual que el .ts y estar en la misma carpeta.\n"
            "- `provideHttpClient` y `provideRouter` ya están provistos: no los repitas en los "
            "`providers` de los componentes.\n"
            "Si falta cualquiera de esos tres archivos, o el nombre exportado no coincide, "
            "`npm start` no compila.\n\n"
            "Estándares BCP:\n"
            "- Componentes Standalone de Angular 17.\n"
            "- Manejo de errores HTTP con mensajes amigables al usuario\n"
            "- TypeScript estricto sin `any`\n\n"
            "OBLIGATORIO: Cada archivo de código debe presentarse dentro de su propio bloque markdown "
            "con su nombre exacto en la primera línea en un comentario (ej: // debit-card.service.ts, // card.component.ts, etc.):\n"
            "```typescript\n"
            "// models.ts\n"
            "export interface ...\n"
            "```\n"
            "```typescript\n"
            "// <nombre>.service.ts\n"
            "...\n"
            "```\n"
            "```html\n"
            "<!-- <nombre>.component.html -->\n"
            "...\n"
            "```\n"
            "```css\n"
            "/* <nombre>.component.css */\n"
            "...\n"
            "```\n"
        ),
        expected_output=(
            "Código TypeScript/HTML completo en inglés para cada archivo, dentro de "
            "bloques de código marcados con el nombre de archivo en comentario. "
            "Los componentes deben ser standalone y consumir la API del Backend."
        ),
        agent=agent,
    )
