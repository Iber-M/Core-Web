# Notion Integration & Migration Guide

> [!NOTE]
> This document captures the logic and tools built to integrate Core Competent's content with Notion. It serves as a manual for future agents or developers to understand how data flows between the codebase and Notion.

## 1. Overview
The project uses Notion as a CMS/Database for:
1.  **Blog Content Calendar:** Managing articles before publication.
2.  **Downloadable Resources:** Tracking PDFs and guides available for users.

## 2. Key Scripts
Located in `/scripts/`, these Python tools handle the automation:

### A. `execute_import.py` (Blog Migration)
*   **Purpose:** Imports structured content (from JSON payloads) into the Notion Content Calendar.
*   **Key Dependencies:** `NOTION_TOKEN`, `NOTION_DATABASE_ID`.
*   **Workflow:**
    1.  Reads data from `scripts/notion_import_payload.json`.
    2.  Authenticates with Notion API.
    3.  Creates new pages in the target database.

### B. `populate_resources_placeholders.py` (PDF Sync)
*   **Purpose:** Scans the local `assets/documents/` folder for PDF files and creates corresponding "Placeholder" entries in the "Recursos Descargables" Notion database.
*   **Workflow:**
    1.  Searches Notion for a DB named "Recursos Descargables".
    2.  Glob-matches `*.pdf` files locally.
    3.  Creates a "Draft" entry for each PDF found, allowing the user to manually drag-and-drop the file later.

## 3. Configuration (.env)
To run these scripts, the following environment variables are required in `.env`:
```bash
NOTION_TOKEN=secret_...
NOTION_DATABASE_ID=... # ID for the Content Calendar
```

## 4. Current Status
- **Scripts:** ✅ Fully implemented and functional.
- **Migration:** ✅ Blog post structure logic is ready.
- **Dependencies:** Uses standard Python libraries (`urllib`, `json`, `os`) to avoid complex `pip install` requirements where possible.

---
*Created during: Session "Consolidating Notion Migration Knowledge" - To ensure persistence of work done by previous agents.*
