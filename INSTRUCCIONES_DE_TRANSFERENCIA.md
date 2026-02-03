# 📋 Instrucciones de Transferencia - Core-Web Consolidation

## ✅ Archivos Preparados

Esta carpeta contiene **128 archivos** organizados y listos para integrar en `Core-Web`:

```
/tmp/core-web-consolidation/
├── scripts/              (2 archivos Python)
│   ├── export_to_webflow.py
│   └── restore_site.py
├── data/                 (115 archivos: CSV + posts HTML)
│   ├── webflow_export.csv
│   └── restored_site/
├── docs/                 (3 archivos Markdown)
│   ├── BRAND_GUIDELINES.md
│   ├── WEB_CONTENT_SUMMARY.md
│   └── VOICE_AND_VISUAL_ALIGNMENT.md
└── archive/              (8 archivos)
    ├── notion_temp/
    └── web-prototype/
```

---

## 🎯 Pasos para Completar la Consolidación

### 1. Arrastra las carpetas a Core-Web

Desde esta ventana de Finder, arrastra estas **4 carpetas** a la ventana de `Core-Web`:

- ✅ `scripts/`
- ✅ `data/`
- ✅ `docs/`
- ✅ `archive/`

### 2. Elimina la carpeta duplicada

En `Core-Web`, **elimina** la carpeta:
- ❌ `css 2` (está vacía, es un duplicado)

### 3. Limpia la carpeta General

Una vez que confirmes que todo está en `Core-Web`, puedes **eliminar** de `/General`:

- ❌ `scripts/`
- ❌ `data/`
- ❌ `archive/`
- ❌ `web/`
- ❌ `documentation/BRAND_GUIDELINES.md`
- ❌ `documentation/WEB_CONTENT_SUMMARY.md`
- ❌ `documentation/VOICE_AND_VISUAL_ALIGNMENT.md`

**MANTÉN en General**:
- ✅ `documentation/ANTIGRAVITY_TUTORIAL.md` (es documentación general, no específica de Core-Web)

### 4. Actualiza el README de Core-Web

Antigravity actualizará el `README.md` de Core-Web para documentar la nueva estructura.

---

## 📊 Verificación Final

Después de mover todo, `Core-Web` debe tener esta estructura:

```
Core-Web/
├── scripts/              ← NUEVO
├── data/                 ← NUEVO
├── docs/                 ← NUEVO
├── archive/              ← NUEVO
├── 01_Alignment/
├── 02_Content/
├── css/
├── js/
├── images/
├── index.html
├── executive-search.html
├── desarrollo-organizacional.html
├── coaching-ejecutivo.html
├── consultoria-organizacional.html
├── recursos.html
├── contacto.html
└── README.md
```

---

## ⚠️ Nota Importante

Esta carpeta temporal (`/tmp/core-web-consolidation/`) se borrará automáticamente cuando reinicies tu Mac. Asegúrate de completar la transferencia antes de cerrar sesión.

---

**¿Listo?** Una vez que hayas arrastrado las carpetas, avísale a Antigravity para que actualice el README y verifique que todo esté correcto.
