# JARVIS-Auto 🧠

Asistente conversacional con **memoria vectorial** y **auto-aprendizaje**: cada conversación
enriquece su base de conocimiento, y puede salir a internet a investigar cuando no sabe algo.

## ¿Por qué este stack?

| Componente | Elección | Motivo |
|---|---|---|
| Lenguaje | **Python 3.11+** | Estándar de facto en IA/ML, mejor soporte de librerías de embeddings, scraping y LLMs |
| API framework | **FastAPI** | Async, moderno, documentación automática (Swagger) |
| Memoria vectorial | **ChromaDB** | Embebido (no requiere servidor separado), fácil de empezar, escalable a Chroma Cloud/Qdrant después |
| LLM | **Anthropic Claude API** | Configurable vía `.env`, fácil de cambiar a otro proveedor |
| Búsqueda web | **DuckDuckGo Search** (sin API key) | Gratis para desarrollo; migrar a Brave/Serper en producción |

## Arquitectura (resumen)

```
Usuario → API (/chat) → Assistant
                           ├─ 1. Busca en memoria vectorial (ChromaDB) contexto relevante
                           ├─ 2. Si falta info → busca en internet → scrapea → guarda en memoria
                           ├─ 3. Genera respuesta con el LLM (contexto + memoria + web)
                           └─ 4. Extrae "hechos nuevos" de la conversación → los embebe → los guarda
```

Ver `docs/ARCHITECTURE.md` para el detalle y `docs/ROADMAP.md` para las mejoras planeadas.

## Instalación

```bash
git clone <tu-repo>
cd jarvis-ai
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edita .env y agrega tu ANTHROPIC_API_KEY
```

## Uso

```bash
uvicorn src.main:app --reload
```

Luego abre `http://localhost:8000/docs` para probar la API interactiva, o usa:

```bash
curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" \
  -d '{"message": "¿Qué sabes sobre Dead by Daylight?"}'
```

### Forzar aprendizaje de un tema

```bash
curl -X POST http://localhost:8000/learn -H "Content-Type: application/json" \
  -d '{"topic": "Minecraft 1.21 novedades"}'
```

### Job de reflexión (limpieza/consolidación de memoria)

```bash
python scripts/reflect_job.py
```

Puedes programarlo con cron/Task Scheduler para que corra cada noche.

## Estructura del repo

```
jarvis-ai/
├── src/
│   ├── main.py              # entrypoint FastAPI
│   ├── config.py            # configuración centralizada
│   ├── core/
│   │   ├── assistant.py     # orquestador de la conversación
│   │   └── llm_client.py    # wrapper del LLM (Claude)
│   ├── memory/
│   │   ├── vector_store.py  # wrapper de ChromaDB
│   │   └── learning.py      # extracción y guardado de conocimiento nuevo
│   ├── web/
│   │   ├── search.py        # búsqueda en internet
│   │   └── scraper.py       # extracción de contenido de páginas
│   └── api/
│       └── routes.py        # endpoints HTTP
├── scripts/
│   └── reflect_job.py       # job periódico de consolidación de memoria
├── tests/
├── docs/
│   ├── ARCHITECTURE.md
│   └── ROADMAP.md
└── requirements.txt
```

## Próximos pasos

Revisa `docs/ROADMAP.md` — está pensado en versiones (v1 → v5) para que vayas
incorporando mejoras de forma incremental sin romper lo que ya funciona.
