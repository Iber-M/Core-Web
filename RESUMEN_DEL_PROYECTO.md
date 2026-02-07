# Resumen del Proyecto: Core-Web (Core Competent)

## 📌 Visión General

**Core-Web** es la plataforma digital corporativa de **Core Competent**, una firma especializada en Executive Search, Coaching Ejecutivo y Consultoría Organizacional.

El proyecto tiene como objetivo consolidar una presencia digital premium, autoritaria y moderna bajo la identidad visual **"Executive Deep Navy"**, reflejando sofisticación y profesionalismo en cada interacción. Actualmente, el sitio funge como el punto central de contacto y credibilidad para la firma.

---

## 💻 Tecnología y Stack Técnico

El proyecto está construido bajo una filosofía de **rendimiento, control total y estándares web modernos**, sin depender de frameworks pesados para la interfaz de usuario.

### **Frontend (Interfaz de Usuario)**

- **HTML5 Semántico**: Estructura limpia y optimizada para SEO, con uso adecuado de etiquetas de contenido.
- **CSS3 (Vanilla Moderno)**:
  - Uso extensivo de **Variables CSS (`:root`)** para un sistema de diseño mantenible (colores, espaciados, tipografía).
  - Diseños responsivos utilizando **Flexbox** y **CSS Grid**.
  - Estilos avanzados como **Glassmorphism** (efectos de vidrio esmerilado), gradientes metálicos y sombras sutiles.
  - No utiliza frameworks de estilos (como Bootstrap o Tailwind); todo el diseño es personalizado ("Bespoke Design").
- **JavaScript (Vanilla)**:
  - Lógica ligera para interacciones de interfaz (menú móvil, header pegajoso, acordeones).
  - Animaciones de fondo (partículas de red) y efectos de scroll (`IntersectionObserver`) sin librerías externas pesadas, asegurando tiempos de carga rápidos.

### **Backend / Procesamiento de Datos**

- **Python (Scripts de Automatización)**:
  - Ubicados en la carpeta `scripts/`, se utilizan para la gestión y migración de contenido.
  - Funciones principales: Procesamiento de 111 artículos de blog históricos, limpieza de datos, y generación de archivos CSV compatibles con CMS externos (Webflow).
- **Shell Scripts**: Automatización de tareas de sincronización (`sync.sh`).

### **Activos y Recursos**

- **Fuentes**: Integración de Google Fonts (`Outfit` para títulos, `Inter` y `Poppins` para cuerpo).
- **Gráficos**: Uso de SVGs para iconos (nítidos en cualquier resolución) e imágenes optimizadas en formato WebP/PNG.

---

## 📂 Estructura del Proyecto

El proyecto sigue una estructura organizada y semántica:

```
Core-Web/
├── assets/                 # Recursos estáticos
│   ├── css/                # Hojas de estilo (styles.css es el núcleo)
│   ├── images/             # Imágenes de marca, fondos y logotipos de clientes
│   └── js/                 # Scripts del frontend (transiciones, animaciones)
├── scripts/                # Herramientas de automatización en Python (migración de blog)
├── data/                   # Datos crudos para el blog y recursos
├── blog/                   # Archivos relacionados con la sección de noticias
├── index.html              # Página de inicio (Home)
├── executive-search.html   # Pilar: Búsqueda de Ejecutivos
├── coaching-ejecutivo.html # Pilar: Coaching
├── contacto.html           # Página de contacto
├── STATUS.md               # Bitácora de estado del proyecto y tareas pendientes
└── DESIGN_SYSTEM.md        # Documentación de la identidad visual
```

---

## 🎨 Identidad Visual: "Executive Deep Navy"

El diseño se centra en transmitir **lujo corporativo y profundidad**:

- **Paleta de Colores**:
  - Fondo: *Deep Navy / Dark Wood* (#0F1216, #161B22).
  - Acentos: *Metallic Gold* (#C6A87C).
  - Texto: Blanco roto y grises fríos para alta legibilidad.
- **Experiencia de Usuario (UX)**:
  - Navegación fluida con barra superior inteligente (se oculta al bajar, aparece al subir).
  - Micro-interacciones en botones y tarjetas para dar una sensación "táctil" y premium.

---

## 🚀 Estado Actual y Próximos Pasos

El sitio se encuentra **en vivo** y funcional. Las páginas principales (Pilares) están completas y estandarizadas.

**Foco actual:**

1. **Migración a Webflow**: Se está preparando la transferencia del blog a Webflow para facilitar la gestión de contenido (CMS), utilizando los scripts de Python para exportar los datos actuales.
2. **Optimización Móvil**: Refinamiento final de la experiencia en dispositivos móviles.
3. **SEO**: Implementación detallada de metadatos para mejorar la visibilidad orgánica.

Este archivo sirve como referencia central para entender la arquitectura y propósito de **Core-Web**.
