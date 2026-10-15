"""Desarrollador backend: edita aquí el rol, el objetivo y las instrucciones de su tarea."""

from crewai import Agent, Task
from crew.llm_config import llm

KEY = "backend"
LABEL = "Desarrollador backend"
SPEC_FILE = "backend_spec.md"
EXTRACT_CODE = True

agent = Agent(
    role="Backend Developer",
    goal=(
        "Implementar el backend del feature siguiendo la especificación del "
        "Designer. Entregar código limpio, tipado, con manejo de errores y "
        "comentarios que el Frontend y el Reviewer puedan entender y validar."
    ),
    backstory=(
        "Eres un desarrollador backend senior especializado en Java Quarkus 3.x "
        "y microservicios bancarios. Aplicas principios SOLID, implementas "
        "seguridad con BCrypt y JWT, y siempre entregas código que incluye "
        "manejo explícito de errores, logging estructurado y tests unitarios. "
        "Tu output principal es código funcional con su contrato de "
        "entrada/salida bien definido."
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
            f"Basándote en la especificación técnica generada por el Designer "
            f"para el feature **{title}**, implementa el backend en Java Quarkus 3.x.\n\n"
            "IMPORTANTE: Todo el código fuente (nombres de clases, atributos, métodos, DTOs y nombres de archivo) "
            "debe generarse estrictamente en INGLÉS siguiendo las mejores prácticas bancarias del BCP.\n\n"
            "CONTRATO DEL ANDAMIAJE (ya existe en disco, no lo generas tú):\n"
            "`pom.xml` y `application.properties` ya están escritos. El proyecto compila con estas "
            "dependencias y NINGUNA otra — no uses librerías fuera de esta lista:\n"
            "  quarkus-spring-web (@RestController, @PostMapping, @GetMapping, @PutMapping)\n"
            "  quarkus-spring-di (@Service, @Component, @Autowired)\n"
            "  quarkus-spring-data-jpa (@Repository, JpaRepository<T, ID>)\n"
            "  quarkus-hibernate-validator (jakarta.validation: @NotNull, @NotBlank, @Email)\n"
            "  quarkus-jdbc-h2 / quarkus-jdbc-postgresql (la BD ya está configurada)\n"
            "  org.mindrot.jbcrypt.BCrypt (hasheo de contraseñas/PIN)\n"
            "  quarkus-junit5 (@QuarkusTest)\n\n"
            "PAQUETES FIJOS: los archivos se guardan en `src/main/java/pe/bcp/login/<capa>/`, y Java "
            "exige que el package coincida con el directorio. Usa exactamente uno de estos, sin "
            "importar cómo se llame el feature:\n"
            "  pe.bcp.login.model · pe.bcp.login.dto · pe.bcp.login.service · "
            "pe.bcp.login.resource · pe.bcp.login.repository\n"
            "Un package distinto (ej: pe.bcp.transfer.model) NO compila.\n\n"
            "Requisitos de entrega:\n"
            "- Cada archivo Java DEBE incluir su sentencia `package` de la lista de arriba e imports completos.\n"
            "- Entidad JPA principal: con @Entity, @Table, @Id, constructores y getters/setters completos.\n"
            "- Repositorio JPA: interfaz Spring Data JPA o Panache para la entidad principal.\n"
            "- DTOs tipados (Request y Response): con validaciones Jakarta (@NotNull, @NotBlank, etc.), constructores y getters/setters.\n"
            "- Service: con lógica de negocio, validaciones y tratamiento seguro de datos sensibles (hasheo seguro si aplica contraseñas/PIN).\n"
            "- Resource / Controller: con endpoints REST (ej: @PostMapping, @PutMapping, @GetMapping) y códigos HTTP adecuados (200 OK, 201 Created, 400 Bad Request, 404 Not Found, 409 Conflict).\n"
            "- Al menos un test unitario con JUnit 5.\n\n"
            "OBLIGATORIO: Cada archivo de código debe presentarse dentro de su propio bloque markdown "
            "con su nombre exacto en la primera línea en un comentario (ej: // AuthService.java, // DebitCardService.java, etc.):\n"
            "```java\n"
            "// <NombreDeLaClase>.java\n"
            "...\n"
            "```\n"
            "```sql\n"
            "-- schema.sql\n"
            "...\n"
            "```\n"
        ),
        expected_output=(
            "Código Java completo y funcional en inglés para cada archivo solicitado con package e imports, "
            "dentro de bloques de código marcados con el nombre de archivo en comentario. "
            "Cada archivo debe compilar y cubrir los criterios de aceptación del feature."
        ),
        agent=agent,
    )
