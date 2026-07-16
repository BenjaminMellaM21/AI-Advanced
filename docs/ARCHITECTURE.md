# Arquitectura

## Flujo de una conversación

1. **Usuario envía un mensaje** → `POST /chat`
2. **Recuperación (retrieval)**: `vector_store.query_knowledge()` busca los hechos más
   parecidos semánticamente en ChromaDB.
3. **Decisión de investigar**: si la distancia del mejor resultado es muy alta
   (poca confianza, ver `MEMORY_CONFIDENCE_THRESHOLD` en `.env`), el sistema
   dispara `research_topic()`:
   - Busca en DuckDuckGo (`src/web/search.py`)
   - Scrapea las páginas resultantes (`src/web/scraper.py`)
   - Le pide a Claude que extraiga hechos atómicos del contenido
   - Guarda cada hecho en ChromaDB con su fuente y timestamp
4. **Generación**: se arma un prompt con los recuerdos relevantes + la pregunta,
   y Claude genera la respuesta final.
5. **Auto-aprendizaje pasivo**: la propia pregunta+respuesta también se pasa por
   el extractor de hechos, así el sistema aprende incluso sin salir a internet
   (por ejemplo, si el usuario le enseña algo directamente).
6. **Log de conversación**: se guarda el intercambio crudo en la colección
   `conversations` (separada de `knowledge`) para trazabilidad y futuros
   análisis de feedback.

## Por qué dos colecciones separadas

- `knowledge`: hechos atómicos, reutilizables, la "memoria semántica" del asistente.
- `conversations`: historial crudo, útil para depurar y para futuras mejoras
  (ej. fine-tuning, análisis de qué preguntas se repiten).

## Limitaciones conocidas (v1)

- El job de reflexión (`scripts/reflect_job.py`) **consolida pero no borra** los
  duplicados originales todavía — la memoria sigue creciendo. Está resuelto como
  tarea en el roadmap v2.
- La búsqueda web (DuckDuckGo) es gratuita pero menos estable que una API de pago;
  para producción se recomienda Brave Search API o Serper.dev.
- No hay autenticación en la API — añadir antes de exponerla públicamente.
- El "aprendizaje" es aditivo (RAG + memoria), no fine-tuning real del modelo.
  Es la forma más práctica y barata de lograr un comportamiento que "evoluciona"
  sin necesidad de reentrenar pesos.
