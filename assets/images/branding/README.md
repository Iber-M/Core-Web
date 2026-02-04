# 00_Brand_Assets

Esta carpeta está diseñada para recibir todos los archivos del kit de marca de Core Competent.

## Estructura Sugerida

```
00_Brand_Assets/
├── logos/
│   ├── logo-principal.svg
│   ├── logo-horizontal.svg
│   ├── logo-vertical.svg
│   ├── logo-monocromo.svg
│   └── logo-blanco.svg
│
├── favicon/
│   ├── favicon-16x16.png
│   ├── favicon-32x32.png
│   ├── favicon-180x180.png
│   └── favicon.ico
│
├── tipografia/
│   └── (archivos de fuentes custom si existen)
│
├── colores/
│   └── paleta-oficial.md (o archivo de referencia)
│
└── otros/
    └── (imágenes, iconos, patterns, etc.)
```

## Instrucciones de Uso

1. **Arrastra y suelta** tus archivos de marca en las subcarpetas correspondientes
2. **Mantén los nombres originales** o usa nombres descriptivos
3. **Formatos preferidos:**
   - Logos: SVG (vectorial) o PNG con transparencia
   - Favicon: ICO, PNG (múltiples tamaños)
   - Tipografías: WOFF2, WOFF, TTF

## Integración Automática

Una vez que agregues los archivos aquí, puedo:
- ✅ Integrar el logo en el header de todas las páginas
- ✅ Reemplazar el favicon placeholder actual
- ✅ Actualizar la paleta de colores en `css/styles.css`
- ✅ Cargar tipografías custom si las proporcionas
- ✅ Optimizar imágenes para web si es necesario

## Notas

- Esta carpeta está **fuera del flujo principal** del sitio web
- No afecta la estructura actual de archivos
- Es fácil de limpiar o reorganizar después
- Los archivos aquí no se cargan automáticamente (requieren integración manual)
