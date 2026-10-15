# Trabajar en equipo

## Crear el repositorio del equipo

Una persona crea el repo desde esta plantilla. Sustituye `equipo-01` por el nombre acordado:

```sh
gh repo create NTTData-Academy/crewai-equipo-01 --template NTTData-Academy/crewai --private --clone
```

Agrega a tus compañeros como colaboradores con permiso de escritura en el repo del equipo.
Los demás integrantes clonan ese mismo repo:

```sh
gh repo clone NTTData-Academy/crewai-equipo-01
cd crewai-equipo-01
```

## Repartir los archivos

Anota un responsable por archivo. Si hay menos de seis personas, una persona puede tomar varios roles.

- `agents/architect.py`: responsable pendiente. Define la solución y el contrato de API.
- `agents/backend.py`: responsable pendiente. Implementa el backend.
- `agents/frontend.py`: responsable pendiente. Implementa el frontend.
- `agents/testing.py`: responsable pendiente. Diseña las pruebas y sus comandos de ejecución.
- `agents/security.py`: responsable pendiente. Revisa riesgos y propone correcciones verificables.
- `agents/chapter.py`: responsable pendiente. Revisa todas las entregas y emite el veredicto final.

## Entregar un cambio

1. Acuerden un requerimiento y sus criterios de aceptación.
2. Crea tu rama, por ejemplo `git switch -c agents/backend`.
3. Edita las instrucciones de tu agente en su archivo. Coordina los cambios de contratos con el arquitecto.
4. Ejecuta `python tools/verify.py`.
5. Publica tu rama y abre un PR hacia el repo de tu equipo.
6. Pide a un compañero que revise el cambio antes de integrarlo.

Una persona ejecuta el pipeline integrado desde `main`. El equipo participa en las aprobaciones
humanas y aporta feedback en cada etapa. Cada integrante conserva su propia `.env`, autenticación
y entorno virtual. No compartan checkpoints entre ejecuciones de distintas computadoras.

Los agentes generan texto y archivos. El agente de pruebas propone tests y comandos;
una persona los ejecuta y adjunta la salida real al PR. Un informe del modelo no demuestra que las pruebas pasaron.
