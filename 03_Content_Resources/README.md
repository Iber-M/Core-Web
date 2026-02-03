# 03_Content_Resources

Esta carpeta centraliza todos los recursos de contenido para el sitio web de Core Competent.

## Estructura de Carpetas

```
03_Content_Resources/
├── imagenes/
│   ├── hero-backgrounds/
│   ├── servicios/
│   └── generales/
│
├── logos-clientes/
│   └── (logos de empresas cliente para mostrar credibilidad)
│
├── copy/
│   ├── homepage.md
│   ├── executive-search.md
│   ├── desarrollo-organizacional.md
│   ├── coaching-ejecutivo.md
│   ├── consultoria-organizacional.md
│   ├── recursos.md
│   └── contacto.md
│
├── testimonios/
│   └── testimonios.json (o archivos individuales)
│
├── equipo/
│   └── (fotos y bios del equipo de Core Competent)
│
└── casos-estudio/
    └── (PDFs, imágenes, o markdown de casos de éxito)
```

## Guía de Uso por Carpeta

### 📁 `imagenes/`
**Para:** Fotografías, ilustraciones, backgrounds
- **Formatos:** JPG, PNG, WebP
- **Tamaño recomendado:** 
  - Hero backgrounds: 1920x1080px
  - Imágenes de sección: 800-1200px ancho
- **Optimización:** Comprimir antes de subir (TinyPNG, ImageOptim)

### 📁 `logos-clientes/`
**Para:** Logos de empresas que han trabajado con Core Competent
- **Formatos:** SVG (preferido) o PNG con transparencia
- **Tamaño:** Máximo 200px de ancho
- **Naming:** `cliente-nombre-empresa.svg`
- **Uso:** Sección de "Clientes" o "Confían en nosotros"

### 📁 `copy/`
**Para:** Textos finales de cada página
- **Formato:** Markdown (.md) o texto plano (.txt)
- **Estructura sugerida por archivo:**
  ```markdown
  # [Nombre de la Página]
  
  ## Hero
  - Título principal
  - Subtítulo
  - CTA text
  
  ## Sección 1
  - Título
  - Párrafos
  - Bullets
  
  ## Sección 2
  ...
  ```

### 📁 `testimonios/`
**Para:** Testimonios de clientes
- **Formato sugerido (JSON):**
  ```json
  {
    "testimonios": [
      {
        "texto": "Quote del cliente...",
        "autor": "Nombre Apellido",
        "cargo": "Director de RRHH",
        "empresa": "Empresa XYZ",
        "foto": "path/to/foto.jpg" (opcional)
      }
    ]
  }
  ```
- **Alternativa:** Un archivo `.md` por testimonio

### 📁 `equipo/`
**Para:** Fotos y biografías del equipo
- **Fotos:** 400x400px, formato cuadrado, JPG/PNG
- **Bios:** Archivo markdown con nombre, cargo, bio, redes sociales

### 📁 `casos-estudio/`
**Para:** Case studies, historias de éxito
- **Formatos:** PDF, Markdown, o carpetas por caso
- **Incluir:** Problema, solución, resultados, métricas

## Workflow de Integración

1. **Agrega tus archivos** a las carpetas correspondientes
2. **Avísame** qué contenido agregaste
3. **Yo me encargo de:**
   - Integrar el copy en las páginas HTML
   - Optimizar y mover imágenes a `/images/`
   - Crear secciones de testimonios
   - Agregar logos de clientes
   - Estructurar casos de estudio

## Notas Importantes

- ✅ Esta carpeta es **temporal** - los archivos se integrarán al sitio
- ✅ Mantén nombres descriptivos y sin espacios (usa guiones)
- ✅ Organiza por tipo de contenido, no por página
- ✅ Si tienes dudas sobre dónde poner algo, usa la carpeta raíz

## Ejemplos de Nombres de Archivo

✅ **Bien:**
- `hero-background-oficina-moderna.jpg`
- `logo-cliente-empresa-abc.svg`
- `testimonio-director-rrhh-empresa-xyz.md`

❌ **Evitar:**
- `IMG_1234.jpg`
- `Sin título.png`
- `Copia de archivo (2).pdf`
