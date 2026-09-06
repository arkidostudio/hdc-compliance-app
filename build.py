#!/usr/bin/env python3
"""
Wraps the artifact fragment (index.html) into a standalone HTML page for
static hosting (docs/index.html). Run this after any edit to index.html.

    python3 build.py
"""
import pathlib

ROOT = pathlib.Path(__file__).parent
src = (ROOT / "index.html").read_text()

wrapped = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="HDC Compliance App — review architectural drawings against HDC requirements. Runs entirely in the browser.">
<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf-lib/1.17.1/pdf-lib.min.js"></script>
<script>
// Downloads shim for hosts without the Anthropic Artifacts runtime (e.g. GitHub Pages).
if (typeof window.claude === "undefined" || !window.claude.use) {
  window.claude = window.claude || {};
  window.claude.use = async (name) => {
    if (name !== "downloads") return null;
    return {
      save: async ({ filename, data, mimeType }) => {
        const blob = new Blob([data], { type: mimeType || "application/octet-stream" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url; a.download = filename;
        document.body.appendChild(a); a.click(); a.remove();
        setTimeout(() => URL.revokeObjectURL(url), 1000);
        return true;
      }
    };
  };
}
</script>
</head>
<body>
''' + src + '''
</body>
</html>
'''

out = ROOT / "docs" / "index.html"
out.parent.mkdir(exist_ok=True)
out.write_text(wrapped)
print(f"wrote {out} ({len(wrapped):,} bytes)")
