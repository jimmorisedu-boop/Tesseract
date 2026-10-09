# Tesseract Agent Guidelines

When working with video, motion graphics, audio, or static design tasks using Tesseract:

1. **CLI Location**: Use the Tesseract CLI executable at:
   - Windows: `$env:LOCALAPPDATA\Tesseract\bin\tsrct.cmd` (or `tsrct` if in PATH)
   - macOS: `~/Library/Application Support/Tesseract/bin/tsrct`
   - Linux: `~/.local/share/Tesseract/bin/tsrct`
2. **Version Verification**: The CLI version must match `0.3.1` (pinned in `references/cli-version.txt`). Verify via `tsrct --version` once per session.
3. **Editable Projects**: Always maintain and commit the `.tsrct` project bundle (`project commit` / `project apply`) alongside exported media (MP4, PNG, MOV) so edits remain non-destructive.
4. **Editorial & Motion Principles**:
   - For video editing: assess dialogue, eyeline continuity, music pacing, and sound design.
   - For motion graphics: use native layers, keyframes, bezier easing, and font imports rather than static flattened images.
   - For previews: render PNG frames using `tsrct preview --project <path> --time <seconds> --output <path>`.
