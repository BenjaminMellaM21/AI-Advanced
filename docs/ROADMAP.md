# Roadmap — cómo ir evolucionando el sistema

La idea es ir mergeando estas versiones como PRs incrementales en GitHub,
cada una con sus propios tests, sin romper lo anterior.

## v1 — Base (este scaffold) ✅
- Chat con memoria vectorial (ChromaDB)
- Búsqueda e investigación web bajo demanda
- Extracción automática de hechos desde conversaciones y desde la web
- Job de reflexión básico (consolidación, sin borrado real)

## v2 — Memoria más inteligente
- [ ] Borrado real de duplicados tras consolidar (usar `vector_store.knowledge.delete(ids=[...])`)
- [ ] Metadatos de "confianza"/veces reforzado por hecho, para priorizar en retrieval
- [ ] Expiración de hechos viejos no reforzados (ej. > 90 días sin uso)
- [ ] Migrar de DuckDuckGo a Brave Search API o Serper.dev (más estable)

## v3 — Feedback y refuerzo
- [ ] Endpoint `POST /feedback` (👍/👎 por respuesta)
- [ ] Usar el feedback para bajar la prioridad de hechos que llevaron a malas respuestas
- [ ] Dashboard simple (HTML/Streamlit) para ver qué ha aprendido el sistema

## v4 — Investigación autónoma programada
- [ ] Job que, en horarios definidos, elige temas de interés (basado en lo más
      preguntado) y los investiga proactivamente sin que el usuario pregunte
- [ ] Cola de tareas (ej. `APScheduler` o `Celery`) para no bloquear la API

## v5 — Multimodal (conectar con tus proyectos anteriores)
- [ ] Integrar reconocimiento de voz (retomando tu proyecto JARVIS con voz)
- [ ] Salida por voz (TTS)
- [ ] Empaquetar como app de escritorio (Electron) o app Android

## Cómo contribuir mejoras (flujo sugerido en GitHub)

1. Crear rama `feature/nombre-corto` desde `main`
2. Implementar + agregar tests en `tests/`
3. Actualizar este ROADMAP marcando el ítem como hecho
4. Pull Request con descripción de qué mejora y por qué
5. Merge a `main` solo si los tests pasan (configurar GitHub Actions, ver abajo)

### Sugerencia de CI (GitHub Actions)

Crea `.github/workflows/tests.yml` con un job simple que instale
`requirements.txt` y corra `pytest`. Así cada PR se valida automáticamente
antes de mergear — clave para que el proyecto "evolucione" sin romperse.
