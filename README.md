# HDC Compliance App

A single-file browser app for reviewing architectural drawings against HDC
(Housing Development Corporation, Maldives) requirements. Everything runs
client-side — no server, no build step, no dependencies to install.

## What it does

Five tabs:

1. **Project Details** — General info (Lot, Owner, Contact, City / Atoll / Island,
   Building type, Project type) and Professionals (Preliminary / Licensed
   Architect & Engineer, Architectural & Structural Checker) with autocomplete
   from saved contacts.
2. **Compliance Checklist** — 18 sections × 156 items, three states each
   (pending / passed ✓ / N/A −). Sidebar navigator, per-section "Check all",
   per-item notes, project-type-driven auto-N/A for the three plot-type
   sections. Output PDF fills the AcroForm fields on the source Checklist PDF
   directly (real checkbox state for passes, `–` glyph rendered at the
   checkbox's own widget rectangle for N/A).
3. **Certificate** — generates the Architectural Checker's Certificate from
   scratch (Times, 11pt body, 1.85 line height, justified paragraphs, ordinal
   date superscripts).
4. **Approval Form** — fills the AcroForm fields on the Drawing Approval Form
   PDF, expanding floor-usage ranges into per-floor entries.
5. **Settings** — contact list (many roles per contact). Import / export /
   clear buttons.

## File structure

```
hdc-compliance-app/
├── index.html         — Anthropic Artifact fragment (source of truth, ~1.6 MB)
├── build.py           — wraps index.html into docs/index.html for static hosting
├── docs/
│   └── index.html     — standalone build served by GitHub Pages
├── sources/           — original PDFs / docx (embedded in index.html as base64)
│   ├── HDC Professionals Checklist.pdf
│   ├── HDC Drawing Approval Form.pdf
│   ├── HDC Drawing Approval Form-label.pdf
│   ├── Arch-Checker-Certificate - HOUSE (ATOLL.ISLAND).docx
│   └── Arch-Checker-Certificate - HOUSE (ATOLL.ISLAND).pdf
├── samples/
│   └── dummy-data.json — full-coverage sample for the Import dialog
└── README.md
```

## Running

### Locally

```bash
python3 -m http.server 8000
# open http://localhost:8000/docs/
```

### On GitHub Pages

1. Push to GitHub:
   ```bash
   git init && git add . && git commit -m "Initial commit"
   gh repo create hdc-compliance-app --public --source=. --push
   ```
2. In the repo settings: **Settings → Pages → Deploy from a branch →
   Branch: `main`, Folder: `/docs`**.
3. Wait a minute for the first build; the app is live at
   `https://<your-username>.github.io/hdc-compliance-app/`.

### On claude.ai (Artifact)

`index.html` is the source-of-truth for the artifact at
`https://claude.ai/code/artifact/1649b8ab-864c-4822-a419-9abcf350d59c`.
Republish by pasting the file content when updating the artifact.

## Editing workflow

1. Edit `index.html` (the artifact fragment).
2. Run `python3 build.py` to regenerate `docs/index.html`.
3. Commit both files.

The wrapper adds `<!doctype>`, loads pdf-lib from cdnjs, and installs a
shim so calls to `claude.use("downloads")` fall back to a plain
`Blob` + `<a download>` when the Anthropic Artifacts runtime isn't
present. That means the same `index.html` works in both environments.

## Data storage

Two `localStorage` keys, kept in the viewer's browser only:

- `hdc-compliance-app-v1` — current project (checklist state, all field
  values, section-N/A flags, floor-usage rows). Cleared by **Start over**.
- `hdc-compliance-app-settings` — contact list. Survives **Start over** and
  project imports.

Both are exportable / importable as JSON via the tab actions.

## Rebuilding embedded PDFs

If a source PDF changes:

```bash
base64 -i "sources/HDC Professionals Checklist.pdf" -o /tmp/cl.txt
# Replace the value of the const PDF_B64 = "..." literal in index.html,
# then run:  python3 build.py
```

`PDF_B64` = Checklist form (AcroForm-filled). `DAF_B64` = Approval Form
template. The certificate is generated from scratch — no embedded PDF.
