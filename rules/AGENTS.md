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
5. **Journalistic & News Explainer Standard (YouTube News Format)**:
   - For news analysis and investigative reporting (e.g. *"Осторожно, Собчак"*, benchmark `https://www.youtube.com/watch?v=B5ZqL31RY_w`):
     - **Montage Dynamics**: Cut frequency 2.5–5.0 seconds. Alternate baseline medium shots with punch-ins (115%–125%) on rhetorical points, keeping eyeline locked. Use J/L cuts for narrative velocity.
     - **Dynamic Slide-Ins ("Выезды")**: Headline cards with authentic publisher logos (tilted -2° to +3°), personality cutout portraits (transparent PNGs), Telegram/social bubbles, scanned documents with animated yellow highlighter strokes, and interactive radar/map routes.
     - **Authentic External Material**: Actively source and download real archival footage using `python -m yt_dlp --download-ranges`, high-res logos, official portraits, and real articles into `assets/inserts/`. Never use generic stock footage when real material can be acquired.
     - **Sound Design**: Pair graphic movements with whooshes, pops, paper rustles, and marker squeaks; duck background music -6 to -10 dB under voice, and use dramatic silence cuts before punchlines.
     - **Adobe Premiere Pro & After Effects Deliverables**: Always export Final Cut Pro / Premiere XML (`<project>_premiere.xml`) and After Effects ExtendScript (`<project>_aftereffects.jsx`) or transparent ProRes 4444 MOV overlays alongside MP4 and `.tsrct` using `tesseract_adobe.py`.

