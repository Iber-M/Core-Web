# Core Competent - Design System & Visual Guidelines

> [!IMPORTANT]
> This document serves as the **Source of Truth** for the visual identity of the Core Competent website. All future design implementations must adhere to these guidelines to ensure consistency, premium aesthetics, and "Editorial" quality.

## 1. Design Philosophy: "Editorial Luxury"
- **Keywords:** Authority, Cleanliness, Precision, Seniority.
- **Approach:** We avoid visual noise. We prefer **structure** (grids, delicate dividers) over "decorations" (heavy shadows, complex borders).
- **Core Vibe:** "Architectural" — everything must feel aligned, intentional, and solid.

## 2. Color Palette & Gradients
### The "Luxury Gold" Gradient
Used for high-impact metrics and key numbers. It unifies the aesthetic and adds volume without using multiple solid colors.
```css
background: linear-gradient(135deg, #F9EAC8 0%, #C6A87C 50%, #9E8356 100%);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
```

### Typography Colors
- **Primary Text (Headings):** White (`#FFFFFF`) or the Gold Gradient above.
- **Secondary Text (Subtitles/Labels):** White (`#FFFFFF`) in uppercase, strictly tracked (`letter-spacing: 0.1em`).
- **Body/Supporting Text:** Cool Grey (`#8B949E`) for readability on dark backgrounds.

## 3. UI Components: Hero Stats
**Style: "Gradient Luxury Aligned"**
- **Structure:** 4-column grid with thin vertical dividers (`border-right: 1px solid rgba(255,255,255,0.1)`).
- **Typography Hierarchy:**
    - **Big Number:** Font `Outfit`, Weight `700`, Size `3.5rem`.
    - **Unit/Label:** Font `Outfit`, Weight `400`, Size `1.5rem`.
- **Alignment Rules (CRITICAL):**
    - **Baseline Alignment:** The Big Number and the Unit MUST share the same baseline. Use `display: flex; align-items: baseline;`.
    - **Fixed Height:** The header container (Number + Unit) must have a `height` (e.g., `4.5rem`) to ensure that the subtitles below start at the exact same vertical position, regardless of the number's height. **No visual "steps" allowed.**

## 4. General Spacing & Layout
- **Vertical Dividers:** Use them to create order in horizontal lists. elegance comes from the subtle separation.
- **Whitespace:** Generous padding (e.g., `padding: 1rem` inside grid items) is essential to maintain the "Editorial" look.

---
*Last Updated: Session "Hero Stats Design Refinement" - Implemented "Gradient Luxury" style.*
