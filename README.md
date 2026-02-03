# Core-Web

Proyecto consolidado de la web de Core Competent, incluyendo manual de identidad, marca, scripts de migración y contenido histórico.

## 📁 Estructura del Proyecto

```
Core-Web/
├── 00_Brand_Assets/          # Recursos de marca (logos, colores, tipografías)
├── 01_Alignment/             # Guías de alineación visual y de voz
├── 02_Content/               # Contenido editorial
├── 03_Content_Resources/     # Recursos adicionales de contenido
├── scripts/                  # Scripts de migración y utilidades
│   ├── export_to_webflow.py  # Exportar contenido de WordPress a Webflow
│   └── restore_site.py       # Restaurar sitio desde backup
├── data/                     # Datos de migración y backups
│   ├── webflow_export.csv    # Datos exportados de WordPress
│   └── restored_site/        # 113 posts HTML del blog legacy
├── docs/                     # Documentación del proyecto
│   ├── BRAND_GUIDELINES.md   # Guías de marca
│   ├── WEB_CONTENT_SUMMARY.md # Resumen del contenido web
│   └── VOICE_AND_VISUAL_ALIGNMENT.md # Alineación de voz y visual
├── archive/                  # Archivos históricos
│   ├── notion_temp/          # Migración de Notion
│   └── web-prototype/        # Versión anterior del sitio
├── css/                      # Estilos del sitio actual
├── js/                       # JavaScript del sitio
├── images/                   # Imágenes del sitio
├── index.html                # Página principal
├── executive-search.html     # Página de Executive Search
├── desarrollo-organizacional.html
├── coaching-ejecutivo.html
├── consultoria-organizacional.html
├── recursos.html
└── contacto.html
```

## 🎯 Propósito

Este repositorio centraliza todo lo relacionado con el proyecto web de Core Competent:

- **Sitio web actual**: HTML, CSS, JS y assets
- **Identidad de marca**: Guías visuales y de contenido
- **Migración histórica**: Scripts y datos de WordPress/Webflow
- **Documentación**: Guías de marca y contenido

## 🚀 Uso

### Sitio Web
Los archivos HTML en la raíz son el sitio web actual. Abrir `index.html` en un navegador para ver la página principal.

### Scripts de Migración
Los scripts en `/scripts` fueron utilizados para migrar contenido desde WordPress. Requieren Python 3.

### Datos Legacy
El contenido histórico del blog (113 posts) está preservado en `/data/restored_site/` para referencia.

## 📝 Notas

- Este proyecto está versionado con Git
- Los archivos grandes en `/data` pueden estar excluidos del versionado (ver `.gitignore`)
- La documentación de marca está en `/docs` y `/01_Alignment`
