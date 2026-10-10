# Journalistic & Investigative News Video Style (YouTube News Explainer Standard)

This reference defines the editing, motion graphics, asset sourcing, and sound design principles for high-engagement journalistic analysis, investigative reporting, and news explainer formats (such as *"Осторожно, Собчак"*, *"Редакция"*, Vox/Johnny Harris explainers, and Bloomberg Quicktake). Reference benchmark: [YouTube News Analysis Format](https://www.youtube.com/watch?v=B5ZqL31RY_w).

**Measured benchmark.** The rules below are qualitative. For the measured profile of that
reference episode — cuts per minute, median shot length, frozen-frame tolerance, narration rate —
and a script that checks a finished render against those numbers, see
[news-review house standard](../../news-review-video/references/style-standard.md) and
`news-review-video/scripts/measure_pacing.py`. The two documents agree: a hard *visual* change
lands every 2.5–5 s, while pure hard *cuts* in the reference body run 5–12 per minute.
---

## 1. Core Visual Anatomy & Screen Partitioning

In this format, the presenter / anchor provides the narrative spine, but the screen is constantly enriched by dynamic visual evidence. Never leave a talking head uninterrupted without graphic support or cutaways.

```
+-------------------------------------------------------------+
| [TOP BANNER / CHAPTER TITLE / TICKER]                       |
|                                                             |
|   +-------------------+      +--------------------------+   |
|   |                   |      | [SLIDE-IN HEADLINE CARD] |   |
|   |   PRESENTER /     |      |  - News outlet logo      |   |
|   |   TALKING HEAD    |      |  - Tilted headline card  |   |
|   |   (Left or Center)|      +--------------------------+   |
|   |                   |                                     |
|   |   Medium shot     |      +--------------------------+   |
|   |   or Punch-in     |      | [CUTOUT PORTRAIT]        |   |
|   |                   |      |  - Politician/newsmaker  |   |
|   +-------------------+      |  - Transparent silhouette|   |
|                              +--------------------------+   |
| [LOWER-THIRD / CHYRON]                                      |
+-------------------------------------------------------------+
```

### Screen Zones
1. **Host Safe Zone (Left or Center)**: When graphics appear, the presenter occupies 40–50% of the frame (typically framed to the left or center).
2. **Graphic Staging Zone (Right or Upper-Right)**: Reserved for sliding cards, social posts, documents, and cutouts.
3. **Bottom Zone**: Lower thirds (chyrons), breaking news banners, or captions.
4. **Full-Frame Evidence Windows**: Branded graphic frames containing archival footage, flight radar maps, or split-screen comparisons.

---

## 2. Dynamic Montage Rhythm & Editing Pacing

The tempo must be fast, punchy, and dense with information. Viewers disengage if a single visual composition remains static.

### The 2.5–5.0 Second Rule
- **Cut Frequency**: Change the visual picture every **2.5 to 5.0 seconds**.
- **Maximum Static Hold**: No uninterrupted talking-head shot should hold beyond 5 seconds without either:
  1. A digital punch-in (jump to tighter framing).
  2. A graphic slide-in ("выезд" плашки, цитаты, вырезки).
  3. A cut to an archival B-roll insert (врезка видео).
  4. A full-screen graphic, map, or document highlight.

### The Punch-In Alternation (Крупности и джамп-каты)
- **Baseline Framing**: Medium shot (100% scale), waist or chest up.
- **Punch-In Framing**: Medium-Close shot (115%–125% scale), chest to neck up.
- **Motivation**: Punch in on:
  - Strong thesis statements and rhetorical questions.
  - Irony, sarcasm, or personal commentary from the host.
  - Dramatic revelations or topic introductions.
- **Eyeline Continuity**: The speaker's eyes must remain at the exact same vertical screen line across punch-ins. Reposition the crop vertically and horizontally so the face does not jump sideways or vertically across the cut.

### The Visual Variety Cycle
A typical 20–30 second topic beat follows this cyclical rhythm:
1. **0.0–3.0s**: Host (Medium 100%) introduces the fact.
2. **3.0–5.5s**: Host (Punch-in 120%) poses the paradox.
3. **5.5–8.5s**: Slide-in news card ("выезд") appears next to host with whoosh SFX.
4. **8.5–12.0s**: Cut to authentic archival footage / speech excerpt (врезка).
5. **12.0–15.5s**: Cutout portrait of the subject slides in opposite the host with pop SFX.
6. **15.5–19.0s**: Full-frame document scan with animated yellow marker highlight over the key phrase.
7. **19.0–22.0s**: Interactive flight radar / map animation showing route or territory.
8. **22.0–25.0s**: Return to Host (Punch-in) delivering the editorial conclusion.

### Continuous Audio Momentum (J-cuts & L-cuts)
- **J-Cut**: The audio of the upcoming archival clip, speech, or news sound begins 0.5–1.0s before the visual cut.
- **L-Cut**: The presenter’s voice carries over the start of an archival B-roll insert or document graphic for 1–2 seconds before returning or yielding to diegetic sound.

---

## 3. "Выезды" (Animated Slide-Ins & Motion Graphics Catalog)

All graphic overlays must enter with deliberate, smooth animation curves, hold with complete legibility, and exit cleanly.

### A. Media Headline Cards (Плашки СМИ и заголовки)
- **Visual Design**:
  - Rectangular card with rounded corners (`borderRadius: 8–16px`).
  - Background: Crisp white (`#FFFFFF`) or dark slate (`#1E1E24`) with subtle drop shadow (`boxShadow` or darker backing layer).
  - Outlet Branding: Authentic publication logo in top-left corner (e.g. Reuters, CNN, The Atlantic, Bloomberg, Сноб, РБК, Коммерсантъ).
  - Headline Text: High-contrast, bold sans-serif font (Inter, Roboto, SF Pro) with high legibility.
  - Rotation: Subtle tilt angle of **-2° to +3°** to give a dynamic, editorial feel.
- **Motion Character**:
  - **Entrance (0–350ms)**: Slide in from right edge (`position: [1200, Y] -> [650, Y]`) using a snappy cubic-bezier curve (`x1: 0.16, y1: 1.0, x2: 0.3, y2: 1.0`).
  - **Hold (350–3000ms)**: Perfectly stable hold while the viewer reads the text.
  - **Exit (3000–3300ms)**: Slide out or fade out on the next cut.
- **Sound**: Motivated clean **whoosh / swish** (duration 150–250ms) peaking exactly as the card reaches its resting position.

### B. Personality Cutouts (Фото-вырезки персонажей)
- **Visual Design**:
  - High-resolution photo cutout of the discussed figure with background cleanly removed (transparent PNG).
  - Silhouette framed from torso or bust upwards.
  - Optional subtle white or colored edge contour (stroke) or drop shadow for contrast against background.
  - Placement: Lower-right or right third of the screen, facing inward toward the center.
- **Motion Character**:
  - **Entrance (0–300ms)**: Slide up from bottom or in from right with a slight scale settle (from 92% to 100%).
  - **Hold**: Remains on screen while the speaker discusses their actions or quotes.
- **Sound**: Subtle soft **pop**, **click**, or **camera shutter** SFX on entry.

### C. Telegram & Social Media Callouts (Посты из соцсетей)
- **Visual Design**:
  - Styled chat bubble or card resembling the native platform (Telegram, X/Twitter).
  - Header: Circular channel avatar, bold channel name, verification badge, timestamp.
  - Body: Post text with key quotes bolded or highlighted in yellow.
- **Motion Character**:
  - Slide in from right or bottom with slight overshoot (`cubicBezier(0.34, 1.3, 0.64, 1)`).
- **Sound**: Digital **pop**, soft **interface tap**, or notification click.

### D. Official Documents & Yellow Marker Highlights (Документы и маркер)
- **Visual Design**:
  - Scanned document, decree, court decision, or contract laid out on a dark or neutral background.
  - Slow, subtle camera drift / push-in (Ken Burns effect, scale 100% -> 106% over 4 seconds).
- **Animated Highlight**:
  - A bright yellow (`rgba(255, 235, 59, 0.45)`) or neon green rectangle layer placed directly over the key sentence or paragraph.
  - Animated using scale-X (`anchorPoint: [0, 0]`, `scale: [0, 100] -> [100, 100]` over 400–700ms) to simulate a highlighter pen drawing across the line as the presenter reads it.
- **Sound**: Soft **marker squeak** or subtle **paper rustle** timed with the highlight stroke.

### E. Interactive Maps & Flight Radar Routes (Карты и маршруты)
- **Visual Design**:
  - Clean vector or satellite base map.
  - Route trajectory drawn as a bright contrasting line (e.g. cyan or bright blue `#00E5FF`).
  - Waypoints: Pulsing circle pins or location badges.
  - Vehicle / Flight Icon: Plane or ship icon traveling along the animated path.
- **Motion Character**:
  - Path revealed progressively over 2–4 seconds using path-trim or line-growth animation.
  - Text labels for cities, waypoints, and times popping in as the icon passes them.
- **Sound**: Low electronic drone with subtle radar **blip / ping** at key waypoints.

### F. Branded Archival Video Frames & Split Screens (Видео в рамке)
- **Visual Design**:
  - Archival footage, speech, or field report placed inside a 16:9 window within a stylized editorial HUD frame.
  - Technical / news graphics around the border: timecodes (`00:14:22:18`), audio visualizer bars, source watermarks ("ARCHIVE / REUTERS"), REC indicators, or geometric corner marks.
  - Split-screen: Presenter on left (45% width), archival insert on right (50% width), with a sleek dividing rule.

---

## 4. Sourcing & Downloading External Third-Party Material (Сторонний материал для врезок)

Authenticity is the foundation of journalistic credibility. Never substitute generic abstract stock clips or fabricated claims for real evidence.

### Mandatory Asset Acquisition Rules
1. **Identify Real Entities**:
   - For every event discussed (e.g. Flydubai flight incident, Trump negotiation, Kynev arrest, FIDE chess scandal), identify the real date, location, involved persons, and key documents.
2. **Download Authentic Footage**:
   - Download actual press briefings, parliamentary speeches, news broadcasts, field footage, or interview clips using local command-line tools.
3. **Download Authentic Images & Logos**:
   - Download authentic high-resolution logos of the news outlets quoted (Reuters, CNN, AP, The Atlantic, etc.).
   - Download official portraits and press photos of the persons mentioned.
   - Scribe or capture real news articles and screenshots with real dates and headlines.

### Command-Line Sourcing Workflow
Use local tools (`yt-dlp`, `curl`, `ffmpeg`, python scripts; on Windows the yt-dlp binary is `%LOCALAPPDATA%\Programs\yt-dlp\yt-dlp.exe`) to gather and conform materials directly into the project workspace:

#### 1. Targeted Clip Extraction with `yt-dlp`
Download only the precise seconds needed to save bandwidth and storage:
```sh
# Download exact time section (e.g. 01:15 to 01:45) in 1080p or 720p:
yt-dlp --download-sections "*01:15-01:45" \
  -f "bestvideo[height<=1080]+bestaudio/best[height<=1080]" \
  --force-keyframes-at-cuts \
  -o "assets/inserts/footage/flydubai_landing.mp4" \
  "<YOUTUBE_OR_SOURCE_URL>"
```

Time ranges require `--download-sections`; `--download-ranges` only covers byte ranges. On Windows the binary is `%LOCALAPPDATA%\Programs\yt-dlp\yt-dlp.exe`; `python -m yt_dlp` works only where that module is installed.

#### 2. Media Conforming with FFmpeg
Ensure all downloaded B-roll conforms to project frame rate (e.g. 25 or 30 fps), resolution, and audio levels:
```sh
# Conform framerate, remove unwanted audio or level it, trim precisely:
ffmpeg -i assets/inserts/footage/raw_clip.mp4 \
  -r 25 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" \
  -c:v libx264 -crf 20 -preset fast \
  -c:a aac -b:a 192k \
  assets/inserts/footage/conformed_clip.mp4 -y
```

#### 3. Preparing Transparent Cutout Portraits (PNG with Alpha)
- Fetch official high-res portrait from news archive or public domain source.
- Remove background to produce a transparent PNG silhouette.
- Store under `assets/inserts/photos/<name>_cutout.png`.

#### 4. Project Workspace Organization
Maintain a clean, organized assets directory:
```
assets/
  inserts/
    footage/       # Downloaded B-roll clips, archival speeches, field video
    photos/        # Cutout portraits with transparent background
    graphics/      # Headline cards, document scans, radar maps
    logos/         # Official outlet logos (Reuters, CNN, etc.)
  audio/
    sfx/           # Whooshes, pops, marker sounds, camera shutters
    music/         # Ambient investigative background bed
```

#### 5. Importing into Tesseract
Import all prepared local files before authoring timeline layers:
```sh
# Video inserts:
tsrct project import-video --project project.tsrct \
  --file assets/inserts/footage/conformed_clip.mp4 --asset-id broll-1

# Cutouts, graphics, and logos:
tsrct project import-asset --project project.tsrct \
  --file assets/inserts/photos/tokayev_cutout.png --asset-id photo-tokayev --kind image

# Audio cues:
tsrct project import-asset --project project.tsrct \
  --file assets/audio/sfx/whoosh_clean.wav --asset-id sfx-whoosh-1 --kind audio
```

---

## 5. Sound Design for News & Investigative Edits

Sound must work hand-in-hand with pictures to drive narrative tension and rhythm.

### SFX Palette for Graphic Movements
| Visual Element | Sound Cue | Duration | Level relative to dialogue |
|---|---|---|---|
| Headline card slide-in | Fast air whoosh / swish | 180–250 ms | -12 to -16 dB |
| Cutout photo pop-in | Soft pop / camera shutter / subtle click | 80–150 ms | -14 to -18 dB |
| Telegram / social bubble | Clean UI pop / digital tap | 60–100 ms | -14 to -18 dB |
| Document marker highlight | Soft marker squeak / subtle paper rub | 300–600 ms | -18 to -22 dB |
| Breaking news / chapter alert | Low sub-bass thud / impact stinger | 400–800 ms | -8 to -12 dB |
| Map route drawing | Low electronic data hum / subtle pulse | duration of draw | -20 to -24 dB |

### Background Music Bed & Dynamic Ducking
1. **Style**: Restrained, pulsing, investigative electronic or acoustic bass bed (minimalist pulse, subtle synths, cinematic news tension).
2. **Ducking Under Dialogue**:
   - Duck music by **-6 to -10 dB** when the host is speaking.
   - Attack: 40–80 ms before speech begins.
   - Release: 200–350 ms after speech finishes.
3. **The Dramatic Dropout (Silence Cut)**:
   - Cut music to **complete silence** (dropout of 150–300 ms) right before an absurd statement, dramatic revelation, or ironic comment.
   - Resume music with a subtle accent or downbeat on the punchline.

---

## 6. Practical Timeline Authoring Example

Here is a concrete schema representation of a 15-second journalistic sequence featuring:
- Host speaking with punch-in cut at 3.0s.
- Headline card sliding in at 4.5s with whoosh SFX.
- Archival video insert at 8.0s with J-cut audio.
- Cutout portrait sliding in at 11.5s with pop SFX.

### Action Batch / JSON Structure
```json
[
  {
    "type": "createFxRectLayer",
    "compositionId": "main",
    "layerId": 10,
    "name": "News Card Background",
    "insertIndex": 0,
    "activeRange": {"start": 4500, "duration": 3500},
    "transform": {
      "anchorPoint": [350, 100],
      "position": [680, 260],
      "scale": [100, 100],
      "rotation": -2.5,
      "opacity": 100
    },
    "rect": {"size": [700, 200], "fillColor": [1.0, 1.0, 1.0, 0.98]}
  },
  {
    "type": "setFxPropertyKeyframes",
    "compositionId": "main",
    "property": {"layerId": 10, "propertyType": "position"},
    "keyframes": [
      {
        "id": "card-pos-in-start",
        "layerTime": 0,
        "value": {"type": "vec2", "value": [1300, 260]},
        "easing": {"type": "cubicBezier", "x1": 0.16, "y1": 1.0, "x2": 0.3, "y2": 1.0}
      },
      {
        "id": "card-pos-in-end",
        "layerTime": 350,
        "value": {"type": "vec2", "value": [680, 260]},
        "easing": {"type": "linear"}
      }
    ]
  }
]
```

---

## 7. Quality & Verification Checklist Before Export

1. **Montage Dynamics**:
   - [ ] Are cuts occurring every 2.5–5 seconds?
   - [ ] Are there punch-ins on the host that align with key rhetorical points?
   - [ ] Is eyeline continuity preserved across all speaker cuts?
2. **Graphics & Slide-Ins ("Выезды")**:
   - [ ] Do headline cards include authentic news outlet logos and legible fonts?
   - [ ] Are cards slightly tilted (-2° to +3°) for dynamic editorial feel?
   - [ ] Do personality cutouts have cleanly removed backgrounds?
   - [ ] Do document highlights draw over the exact words being discussed?
3. **Authenticity of Inserts**:
   - [ ] Are all archival B-roll clips, photos, and headlines genuine, verified materials sourced from actual events?
   - [ ] Are materials properly conformed (framerate, scaling) without distortion?
4. **Sound Design**:
   - [ ] Does every slide-in, pop-in, and highlight have an accompanying SFX accent?
   - [ ] Is background music ducked cleanly (-6 to -10 dB) under dialogue?
   - [ ] Are dramatic pauses/dropouts used at key moments?
   - [ ] Does the final mix meet -15 LUFS integrated with true peak <= -1 dBTP?
5. **Adobe Premiere Pro & After Effects Deliverables (Обязательный экспорт в Adobe)**:
   - [ ] Is the Premiere Pro XML timeline (`<project>_premiere.xml`) exported via `tesseract_adobe.py` with all cuts, clips, tracks, and audio levels preserved?
   - [ ] Is the After Effects ExtendScript (`<project>_aftereffects.jsx`) and/or ProRes 4444 transparent overlays (`.mov`) generated to reconstruct native composition layers, text, cards, and keyframes?
   - [ ] Are all four deliverables present: Master MP4, `.tsrct` project bundle, Premiere Pro XML, and After Effects JSX/MOV?

