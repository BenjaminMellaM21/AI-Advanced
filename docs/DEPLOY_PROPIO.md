# Tu propia IA, 100% tuya (local + accesible por internet)

Esta guía te deja el sistema corriendo enteramente en tu PC, sin depender de
ninguna empresa externa, y accesible desde internet con tu propio dominio/URL.

## Parte 1: El modelo — Ollama (100% local)

1. Descarga Ollama: https://ollama.com (Windows, Mac, Linux)
2. Instálalo y abre una terminal:
   ```bash
   ollama pull llama3.1
   ```
   Esto descarga el modelo a tu PC (unos 4-5 GB). Una vez descargado, Ollama
   queda corriendo en segundo plano en `http://localhost:11434`.
3. En tu `.env`, deja la configuración de la "Opción A" (ya viene así por defecto).
4. Corre tu API como siempre:
   ```bash
   uvicorn src.main:app --reload
   ```

Con esto, **nadie fuera de tu PC** procesa tus datos. Todo el razonamiento del
modelo ocurre localmente.

### Requisitos de hardware

- Llama 3.1 8B: funciona razonablemente bien con 8 GB de RAM (mejor con 16 GB)
- Si tu PC es más limitada, usa un modelo más chico: `ollama pull llama3.2:1b`
  o `ollama pull phi3` y cambia `LLM_MODEL` en `.env` acorde.

## Parte 2: El servidor — tu propia API accesible por internet

Tu FastAPI ya es "tu propia API" (tu código, corriendo bajo tu control). El
único paso que falta es exponerla más allá de `localhost` para que puedas
llamarla desde tu celular, o para que otra persona la use.

### Opción recomendada: Cloudflare Tunnel (gratis, sin tarjeta)

1. Instala `cloudflared`: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/
2. Con tu API corriendo en `localhost:8000`, en otra terminal:
   ```bash
   cloudflared tunnel --url http://localhost:8000
   ```
3. Te dará una URL pública tipo `https://algo-random.trycloudflare.com` que
   apunta directo a tu API local. Compártela o úsala desde donde quieras.

**Importante**: esta URL solo funciona mientras tu PC esté prendida y el
túnel corriendo. Para algo permanente 24/7 necesitarías un servidor propio
(VPS) o una Raspberry Pi encendida siempre en tu casa — ambas opciones
siguen siendo "100% tuyas" en el sentido de que no dependes de servicios
de IA de terceros, solo de infraestructura que tú controlas.

### Alternativa: ngrok

Igual de simple, gratis con cuenta:
```bash
ngrok http 8000
```

## Checklist de "100% mío"

- [x] El modelo corre en tu hardware (Ollama), no en la nube de otra empresa
- [x] El código del servidor es tuyo (este repo)
- [x] La base de datos vectorial (ChromaDB) se guarda en tu disco (`./data/chroma`)
- [x] Puedes exponerlo a internet sin pagar hosting (Cloudflare Tunnel/ngrok)
- [ ] Si quieres que esté disponible 24/7 sin tu PC prendida, ahí sí necesitas
      un servidor (VPS) — eso ya no es gratis, pero sigue siendo "tuyo" en el
      sentido de que tú eliges el modelo y controlas los datos.
