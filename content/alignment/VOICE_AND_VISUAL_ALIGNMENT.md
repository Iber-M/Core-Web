# Propuesta de Alineación: Voz y Sistema Visual

**Para:** Iber (CEO, Core Competent)
**De:** Antigravity (Design & Strategy Partner)
**Objetivo:** Validar criterio estético y tono de voz antes de escalar producción.

---

## 1. Calibración de Voz (Copywriting)

El objetivo es sequedad elegante. Cero grasa.

### Escenario A: Hero Section (Web)
*Contexto: Primera impresión al entrar al sitio.*

**Opción 1 (Aprobada):**
> **Titular:** Decisiones de alto nivel. Sin ruido.
> **Sub:** Acompañamos a líderes y consejos en la definición de talento crítico y estrategia organizacional. Claridad donde suele haber incertidumbre.

**Opción 2 (Aprobada - Más directa):**
> **Titular:** Liderazgo, Criterio y Estrategia.
> **Sub:** Consultoría boutique para momentos donde el margen de error es cero. Executive Search y Desarrollo Organizacional con profundidad de negocio.

*(Nótese la ausencia de palabras como "transformamos", "pasión", "sinergia" o "innovación".)*

---

## 2. Sistema Visual (Tokens Preliminares)

Propuesta de variables CSS para garantizar la atmósfera "Dark Editorial".

```css
:root {
  /* BACKGROUNDS: Profondidad y Sobriedad */
  --color-bg-main: #121212; /* Charcoal profundo, no negro puro */
  --color-bg-secondary: #1E1E1E; /* Para cards/secciones secundarias */
  
  /* TEXT: Jerarquía y Lectura */
  --color-text-primary: #F0F0F0; /* Blanco suavizado (Off-white) */
  --color-text-secondary: #A0A0A0; /* Gris cálido para lectura prolongada */
  --color-text-muted: #666666; /* Metadatos discretos */

  /* ACCENTS: Lujo silencioso */
  --color-accent-gold: #C6A87C; /* Dorado desustarado, metálico mate */
  --color-border-subtle: #333333; /* Líneas finas apenas perceptibles */

  /* TYPOGRAPHY: Modern Sans Editorial */
  /* Propuesta: 'Inter' (Tight tracking) o 'Manrope' (Humanist Sans) */
  --font-display: 'Manrope', sans-serif; 
  --font-body: 'Inter', sans-serif;
}
```

## 3. Concepto de UI: "The Executive Card"

Descripción de un componente clave (ej. Tarjeta de Servicio de Executive Search):

- **Fondo:** `--color-bg-secondary` (Dark Grey).
- **Borde:** 1px sutil en `--color-border-subtle`.
- **Interacción:** Al hacer hover, el borde cambia suavemente a `--color-accent-gold` (0.3s ease). Sin sombras difusas "glowy", sin movimientos bruscos.
- **Tipografía:** Título en blanco, peso medio en vez de bold. Cuerpo en gris secundario.
- **Iconografía:** Un ícono de línea fina (1.5px stroke), trazo simple, sin relleno.

---

## 4. Preguntas de Criterio

1.  ¿La temperatura del "Charcoal" se siente correcta o prefiere ir más hacia un azul nocturno (Midnight Blue) o mantenerse en neutro absoluto?
2.  ¿Preferencia tipográfica específica? (¿Más geométrica tipo Swiss Style o más humanista?)

---
*Esperando validación para proceder a prototipado.*
