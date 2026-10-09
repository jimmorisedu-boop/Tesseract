# Tesseract for Antigravity

Tesseract brings professional video editing, motion graphics, sound design, and static visual composition directly into Antigravity.

## Available Skills

- `tesseract-video`: Edit footage, assemble sequences, match cuts, balance audio, and render final video files.
- `tesseract-motion`: Create kinetic typography, animated lower-thirds, shape layers, diagrams, and video overlays.
- `tesseract-design`: Create static graphic designs, posters, social media banners, and UI mockups as PNGs with editable `.tsrct` files.
- `tesseract-editor`: Build interactive web-based players and editors for `.tsrct` projects using the Tesseract Web runtime.

## CLI Runtime Execution in Antigravity

1. **CLI Location**:
   - Windows: `$env:LOCALAPPDATA\Tesseract\bin\tsrct.cmd` (or `tsrct` in PATH).
   - macOS: `~/Library/Application Support/Tesseract/bin/tsrct`
   - Linux: `~/.local/share/Tesseract/bin/tsrct`
2. **Version Pin**: Always check the CLI version (`tsrct --version`) against `skills/tesseract-video/references/cli-version.txt` (pinned to `0.3.1`).
3. **Non-Destructive Projects**: Tesseract projects are stored as portable `.tsrct` bundles. Always preserve and commit the `.tsrct` project file alongside exported media (MP4, PNG) so future edits remain editable.
4. **Previews**: Generate quick visual previews with `tsrct preview --project <path> --time <seconds> --output <path>`.
