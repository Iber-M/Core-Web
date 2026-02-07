# Core-Web Backend (AI Brain)

Este es el backend de Core-Web encargado de procesar la lógica de IA de forma segura.

## Setup

1. Asegúrate de tener configurada la `GOOGLE_API_KEY` en el archivo `.env` en la raíz del proyecto.
2. Instala las dependencias (si no se hizo): `npm install`
3. Corre el servidor: `npm run dev`

## Endpoints

- **GET `/api/ai/health`**: Verifica que el cerebro esté activo y la API key sea válida.
- **POST `/api/ai/prompt`**: Envía un prompt a Gemini y recibe una respuesta.
  - Body: `{ "prompt": "Tu consulta aquí" }`

## Seguridad

Toda la lógica de Gemini vive aquí. El frontend nunca debe llamar directamente a la API de Google ni exponer la llave.
