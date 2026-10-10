---
name: tesseract-video
description: Edit existing footage into finished videos locally with Tesseract. Make cuts, preserve dialogue, add purposeful sound design, mix audio, and decide where native motion-graphics scenes or overlays improve the story. Use for video editing and revising Tesseract projects, not avatar or video generation.
---

# Edit video with Tesseract

For news roundups, digests, and commentary episodes, also load the `news-review-video` skill and
follow its house standard: block structure, insert cadence, mandatory camera moves on every
still, sourced inserts with a provenance ledger, and pacing QC before delivery.
# Edit video with Tesseract

For converting files to or from other editing tools, such as Premiere Pro or After Effects, read [conversion](references/conversion.md). When opening shared or older `.tsrct` files, updating tools, or investigating load/render differences, read [versions and compatibility](references/versions.md).

The CLI may send basic usage telemetry for some commands. You can provide optional attribution via `TESSERACT_SKILL=tesseract-video` and the [other attribution variables](references/telemetry.md). Respect the CLI's telemetry opt-out setting; never enable telemetry on the user's behalf.

Make a deliberate edit from the user's material. Tesseract is the local editing and rendering engine; the agent supplies editorial judgment. The output is both a playable video and its editable project.

## Start with the material

1. Resolve this skill's root from the directory containing this `SKILL.md`. Read [CLI installation](references/installation.md) and check the required Tesseract version once per session. Use the resolved executable path throughout the task. Scripts and references are relative to the installed skill, not a guessed home directory or development checkout.
2. Read [local operation](references/local-operation.md). Probe the supplied media, sample frames at meaningful points, and listen to its audio using the host's available media tools. Metadata does not tell you what a shot depicts. If audio cannot be auditioned, disclose that limit rather than claiming a complete review.
3. Establish the deliverable, audience, aspect ratio, duration, must-keep moments, and supplied brand assets from the request. Ask only for missing information that materially changes the edit. For a small correction, preserve the existing edit's style and scope.
4. Read [editorial decisions](references/editorial-decisions.md) before planning a new edit. For each beat decide **footage**, **footage with graphics**, or **full graphics** and why. This is not a quota: do not add motion graphics just to demonstrate the engine.

When creating or revising a journalistic video, news analysis, or investigative explainer (the YouTube news standard exemplified by *"Осторожно, Собчак"*; see [investigative news style](references/investigative-news-style.md)):
- **Montage Dynamics & Pacing**: Keep the rhythm punchy and engaging. Cut or change visual framing every 2.5–5.0 seconds. Alternate between baseline medium shots (100%) and digital punch-ins (115%–125%) on rhetorical points, thesis statements, or tone shifts while strictly preserving [eyeline continuity](references/editorial-decisions.md#talking-head-eyeline-continuity). Use J-cuts and L-cuts to maintain narrative momentum.
- **Sourcing Authentic External Material**: For authentic and credible inserts (врезки), actively download and conform genuine third-party materials rather than using generic stock footage. Follow [media import](references/media-import.md#sourcing--downloading-authentic-third-party-material-сторонний-материал-для-врезок) to download real news clips, speeches, and archival video using `python -m yt_dlp`, and source high-res publisher logos, official portraits (for cutouts), and real article screenshots.
- **Dynamic Slide-Ins ("Выезды")**: Embellish the narrative with authentic graphic slide-ins: tilted headline cards with official publisher logos, silhouette cutout portraits of mentioned figures, Telegram/social bubbles, scanned documents with animated yellow marker highlights, and flight radar / map route animations. See [motion design](references/motion-design.md#выезды--dynamic-news-graphics-slide-ins-pop-ins-callouts).
- **Sound-Choreographed Motion**: Pair every graphic slide-in and pop-in with a motivated, subtle sound accent (whoosh, pop, paper rustle, marker squeak). Layer an investigative music bed ducked by -6 to -10 dB under dialogue, using dramatic silence dropouts before punchlines or key revelations. See [sound design](references/sound-design.md#sound-design-for-journalistic--news-analysis-edits).

For a new ad or a revision to its opening, read [ad hooks](references/ad-hooks.md). Build a visual hook in the opening seconds from the actual footage, proposition, and evidence. Consider distinct concepts, select the strongest, and map its reveal/motion and purposeful SFX to confirmed opening music cues when music is provided. Render and inspect the hook plus its handoff into the ad before polishing the rest. Preserve the scope of unrelated revisions.

Read [waveform editing](references/waveform-editing.md) when music sets the pacing or when trimming talking footage. Generate and **open** the music waveform before planning picture timing; confirm beats, phrases, and major changes by listening and map visual arrivals to them. For speech, use overview and zoomed source waveforms to choose pause trims, protect quiet word boundaries, and retain natural breathing. Waveform markers are candidates, never automatic cut decisions.

For a substantial new video, share a concise edit plan with the source moments, their narrative purpose, graphic treatment, and audio intent. Routine authorized edits can proceed. Do not require a new approval for every local preview or revision.

## Author the edit

- New edit: `tsrct project create` creates a portable `.tsrct` document; import local footage before placing its layers. Existing `.tsrct`: inspect and check out a copy of its editable JSON. Preserve the original and stable IDs. Save JSON through `project commit`, or apply supported action batches with `project apply`, before rendering.
- Read [native authoring](references/native-authoring.md) before changing project structure. Source time, edit time, and layer time are different clocks. In particular, moving a clip must not silently change which source moment it plays.
- Keep footage cuts, full scenes, and editable overlays as native layers in the document's single composition. Use groups for scenes. `activeRange` places a clip in its parent; `sourceRange` selects the source moment. Do not create base-video, caption, or audio tracks.
- For talking-head cuts, follow [eyeline continuity](references/editorial-decisions.md#talking-head-eyeline-continuity): align the speaker’s eye height and screen position across cuts with appropriate framing, including punch-ins. Check the rendered outgoing/incoming frames and playback while preserving natural head movement and intentional camera changes.
- For motion work, read [motion design](references/motion-design.md), then only the relevant authoring reference. The examples demonstrate real schema; their visual style is not a required template.
- For every new edit or sound pass, read [sound design](references/sound-design.md). Consider dialogue, music, micro-SFX, structural cues, and foley/ambience; use the roles the piece needs. Add appropriate sounds from supplied/local assets or the procedural helper without per-cue approval. Import the selected files with `project import-asset --kind audio`, then keep them as editable Audio layers. Use [audio and timing](references/audio-and-timing.md) for placement, ducking, local preparation, and measurement. Preserve useful source audio and chosen music. Do not produce invented speech or captions.
- When talking audio needs cleanup, read [speech cleanup](references/speech-cleanup.md). Diagnose room noise versus reverb/echo, use restrained EQ/dynamics or local noise reduction as appropriate, and compare at matched loudness. Preserve voice detail and timing; the plugin has no bundled dereverberation model.
- Keep typography, graphics, footage, and audio native and editable. Import supplied and downloaded images (including transparent cutout portraits, publication logos, and document scans) with `project import-asset --kind image`, not as a flattened replacement for text, vector graphics, or entire scenes. Sourced video clips and conformed archival B-roll use `project import-video`. Use existing footage and authentic third-party inserts; this plugin provides no generative-video or avatar service.
- Respect the user's brand references. Mirage branding identifies this plugin, not every video created with it.

## Look up capabilities only as needed

Use the installed CLI's schemas through [local operation](references/local-operation.md).

Read [capabilities](references/capabilities.md) for the feature map and limits,
[FX authoring](references/fx-authoring.md) for native layers and footage, and
[motion](references/motion.md) for supported keyframe and script actions. Search
for the specific definition needed rather than dumping the whole schema. The
action schema includes supported standalone operations and their field restrictions; use
[local operation](references/local-operation.md) to choose actions versus JSON
checkout/commit. The installed schema and actual render are authoritative.

## Review and handoff

Use [filmstrip review](references/filmstrip-review.md) to inspect and correct visual
changes. For dialogue cuts and music timing, follow [waveform editing](references/waveform-editing.md).
Finish with [review and delivery](references/review-and-delivery.md); report actual
checks and any limitations. Use absolute local file links and show the video inline
when supported. Cloud sync and publishing are not implemented.

**Mandatory Deliverable Package (Tesseract & Adobe Suites)**:
Every completed edit must be delivered with four synchronized assets:
1. **Master Video**: Rendered `.mp4` (H.264 / AAC, 1080p).
2. **Editable Tesseract Project**: Portable `.tsrct` bundle.
3. **Adobe Premiere Pro Timeline**: Final Cut Pro / Premiere XML (`<project>_premiere.xml`) preserving cuts, source clip in/out points, track structure, and audio levels.
4. **Adobe After Effects Composition**: ExtendScript (`<project>_aftereffects.jsx`) and/or transparent ProRes 4444 MOV overlays (`--format prores --fx-solo`) to recreate native layers, text, cards, and keyframes in After Effects.
Generate the Adobe package via `python <skill-root>/scripts/tesseract_adobe.py bundle --input <project.tsrct> --output-dir <output-dir>`; see [Adobe export](references/conversion.md).


If the host cannot execute local commands or access the local GPU/filesystem, explain that this package needs a local execution environment. Do not substitute a hosted service or silently switch rendering engines.
