# Tesseract for Antigravity

Tesseract brings professional video editing, motion graphics, sound design, and static visual composition directly into Antigravity.

## Available Skills

- `tesseract-video`: Edit footage, assemble sequences, match cuts, balance audio, and render final video files.
- `tesseract-motion`: Create kinetic typography, animated lower-thirds, shape layers, diagrams, and video overlays.
- `tesseract-design`: Create static graphic designs, posters, social media banners, and UI mockups as PNGs with editable `.tsrct` files.
- `tesseract-editor`: Build interactive web-based players and editors for `.tsrct` projects using the Tesseract Web runtime.
- `news-review-video`: House standard for news-review and commentary episodes — block structure, insert cadence, mandatory moves on every still, sourced inserts with a provenance ledger, and pacing QC before delivery.

## CLI Runtime Execution in Antigravity

1. **CLI Location**:
   - Windows: `$env:LOCALAPPDATA\Tesseract\bin\tsrct.cmd` (or `tsrct` in PATH).
   - macOS: `~/Library/Application Support/Tesseract/bin/tsrct`
   - Linux: `~/.local/share/Tesseract/bin/tsrct`
2. **Version Pin**: Always check the CLI version (`tsrct --version`) against `skills/tesseract-video/references/cli-version.txt` (pinned to `0.3.1`).
3. **Non-Destructive Projects**: Tesseract projects are stored as portable `.tsrct` bundles. Always preserve and commit the `.tsrct` project file alongside exported media (MP4, PNG) so future edits remain editable.
4. **Previews**: Generate quick visual previews with `tsrct preview --project <path> --time <seconds> --output <path>`.

## Journalistic & Investigative News Editing Standard (YouTube Explainer Archetype)

When producing or editing video in the YouTube news analysis / investigative report style (e.g. *"Осторожно, Собчак"*, benchmark `https://www.youtube.com/watch?v=B5ZqL31RY_w`):

1. **Montage Dynamics & Pacing (2.5–5.0s Cut Rhythm)**:
   - Never allow a talking-head shot to sit static for longer than 5 seconds without a cut, punch-in, or visual insert.
   - Alternate between baseline Medium Shot (100%) and Medium-Close digital punch-in (115%–125%) on key thesis statements, ironies, or topic changes.
   - Preserve strict eyeline continuity across all punch-ins (matching speaker's eye height).
   - Use J-cuts (audio lead-in) and L-cuts (audio carry-over) to create continuous narrative drive.
2. **Dynamic Graphic Slide-Ins ("Выезды")**:
   - **Headline Cards**: Tilted (-2° to +3°) white or dark cards with authentic publisher logos (Reuters, CNN, The Atlantic, Сноб, РБК), sliding in with snappy cubic-bezier easing (`cubicBezier(0.16, 1.0, 0.3, 1.0)`).
   - **Personality Cutouts**: High-res cutout portraits with transparent PNG backgrounds sliding in on the opposite side of the host with a soft pop/settle.
   - **Telegram / Social Bubbles**: Platform-authentic chat bubbles with avatars, verification badges, and bolded key quotes.
   - **Document Highlights**: Scanned decrees, reports, and articles with animated yellow highlighter strokes drawn across key phrases in sync with voiceover.
   - **Radar & Maps**: Animated flight trajectories, territory lines, and waypoint callouts.
   - **Framed Archival Video**: Archival footage and speeches placed inside stylized editorial HUD frames with timecodes or in split-screens.
3. **Mandatory Sourcing of Authentic External Material (Достоверные врезки)**:
   - Always source and download real third-party assets rather than using generic stock footage.
   - Use `yt-dlp --download-sections "*MM:SS-MM:SS"` (Windows: `%LOCALAPPDATA%\Programs\yt-dlp\yt-dlp.exe`) to extract exact archival footage, speeches, and news clips locally. Note: `--download-ranges` covers byte ranges, not time ranges, and `python -m yt_dlp` only works where that module is installed.
   - Source real high-res publisher logos, official portraits (for cutouts), and real article screenshots.
   - Conform media with FFmpeg (framerate, 1080p scaling) and store in `assets/inserts/` before importing with `tsrct project import-video` / `import-asset`.
4. **Synchronized Sound Design**:
   - Pair every graphic movement with a subtle sound cue: air whoosh on cards, soft pop/shutter on photos, paper rustle on documents, marker squeak on highlights, sub-bass thud on breaking alerts.
   - Layer an investigative, pulsing ambient music bed ducked by -6 to -10 dB under voice.
   - Use dramatic silence cuts (complete music dropouts of 150–300 ms) before punchlines, ironies, or cliffhangers.
5. **Mandatory Output in Adobe Premiere Pro & After Effects Formats**:
   - Deliverables must always include the project in Adobe-compatible interchange formats alongside the master MP4 and `.tsrct` project bundle:
     - **Premiere Pro**: Final Cut Pro / Premiere XML (`<project>_premiere.xml`) preserving timeline tracks, cuts, in/out points, and audio mix.
     - **After Effects**: ExtendScript (`<project>_aftereffects.jsx`) and/or transparent ProRes 4444 MOV overlays (`--format prores --fx-solo`) recreating the composition layers, cards, text, and keyframed motion.
   - Use `python skills/tesseract-video/scripts/tesseract_adobe.py bundle --input <project.tsrct> --output-dir <output-dir>` to automatically produce both files.
6. **Measured Benchmark & Pacing QC**:
   - The rules above are qualitative. The measured profile of the benchmark episode lives in `skills/news-review-video/references/style-standard.md`: intro teaser ≈ 26 cuts/min, body 5–12 cuts/min, no frozen frame ≥ 2 s, narration ≈ 140 words/min, blocks 26–247 s.
   - Read that standard before assembling a full episode, and load the `news-review-video` skill for the workflow, sourcing ledger, and acceptance checklist.
   - "Change the visual every 2.5–5 s" means any change — hard cut, punch-in, slide-in, cutout, highlight — while pure hard cuts in the body run 5–12 per minute.
   - Check a finished render with `python skills/news-review-video/scripts/measure_pacing.py <render.mp4> --intro 66` and deliver the report with the episode.


