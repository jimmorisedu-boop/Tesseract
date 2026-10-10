# Adobe Premiere Pro & After Effects Export and Interchange

Tesseract projects can be exported directly into Adobe Premiere Pro and Adobe After Effects. When completing an edit, **always deliver the project in Adobe formats alongside the master MP4 and non-destructive `.tsrct` project bundle.**

---

## 1. Dual Adobe Deliverable Formats

1. **Adobe Premiere Pro**:
   - **Format**: Final Cut Pro / Premiere Pro XML (`.xml`, xmeml v4/v5).
   - **What it preserves**: Timeline sequence, multiple video and audio tracks, clip in/out boundaries, source clip mapping, cuts, and audio volume levels.
   - **How to open in Premiere**: `File > Import...` (Ctrl+I / Cmd+I), select the `.xml` file. Premiere creates a ready-to-edit Sequence.
2. **Adobe After Effects**:
   - **Format**: After Effects ExtendScript (`.jsx`) and/or transparent ProRes 4444 MOV overlays (`.mov`).
   - **What it preserves**: Full composition hierarchy, native text layers (with fonts, sizes, and colors), shape/solid card layers, layer anchor points, positions, scale, opacity, rotation, and animation timing.
   - **How to open in AE**: `File > Scripts > Run Script File...` in After Effects, choose the `.jsx` file. The script programmatically reconstructs the comp, layers, and keyframes.
   - **Transparent Overlays**: Export ProRes 4444 alpha passes via `tsrct export --format prores --fx-solo <compId>:<layerId> --output overlay.mov`.

---

## 2. Automated Adobe Exporter Script (`tesseract_adobe.py`)

The skill includes a local automated converter in `scripts/tesseract_adobe.py`.

### Generating Complete Adobe Bundle
To export both Premiere Pro XML and After Effects JSX in one command:
```sh
python <skill-root>/scripts/tesseract_adobe.py bundle \
  --input project.tsrct \
  --output-dir ./adobe_exports/
```
Outputs:
- `./adobe_exports/<project>_premiere.xml`
- `./adobe_exports/<project>_aftereffects.jsx`

### Generating Individual Files from Checked-Out JSON
```sh
# 1. Export Premiere Pro XML:
python <skill-root>/scripts/tesseract_adobe.py premiere \
  --json .tesseract-work/editable.json \
  --output project_premiere.xml \
  --fps 25

# 2. Export After Effects JSX:
python <skill-root>/scripts/tesseract_adobe.py aftereffects \
  --json .tesseract-work/editable.json \
  --output project_aftereffects.jsx \
  --fps 25
```

---

## 3. Using `tsrct-conv` for Bidirectional Conversion

For advanced bidirectional conversion (including round-tripping `.prproj` and `.aep` files), the standalone `tsrct-conv` tool converts between `.tsrct` and external editing formats. Check the [Tesseract Converter repository](https://github.com/mirage-hq/Tesseract-Converter) for releases, diagnostics, and supported schema features.

Always keep the original `.tsrct` project bundle and conformed raw assets alongside exported Adobe files so future edits remain editable across both Tesseract and Adobe suites.

