# Import images and audio

Import copies bytes into the portable document. It does not create timeline layers.
Use a unique flat asset ID; existing IDs cannot be replaced accidentally.

```sh
tsrct project import-asset --project project.tsrct --file /absolute/path/logo.png --asset-id logo --kind image
tsrct project import-asset --project project.tsrct --file /absolute/path/music.wav --asset-id music --kind audio
```

Accepted image suffixes: PNG, JPG/JPEG, WebP. Audio: WAV, MP3, M4A, AAC, FLAC, OGG.
The underlying decoder must support the file's encoding; import checks the file
and suffix and packages it, but does not decode or return dimensions/duration.
Probe metadata with local media tools, then verify decoding in a preview/export.
Use `project import-video` for footage and `project import-font --file` for local font files.

Check out the document after import. Add an Image or Audio layer using the
installed document schema and the imported asset ID, then commit. Preserve
existing layers and use unused numeric layer IDs. For a 200×100 image:

```json
{"type":"Image","id":1,"name":"Logo","activeRange":{"start":0,"duration":3000},"transform":{"anchorPoint":[100,50],"position":[320,180],"scale":[100,100],"rotation":0,"opacity":100},"source":{"assetId":"logo","fit":"contain"}}
```

Use actual image dimensions for the anchor and choose placement for the canvas.
For Audio layer fields, source timing, gain, and envelopes, read
[audio and timing](audio-and-timing.md). Generated cues and FFmpeg-processed
derivatives follow the same import path. Keep originals and processing recipes;
mute the original dialogue when replacing it to avoid doubled playback.

## Sourcing & Downloading Authentic Third-Party Material (Сторонний материал для врезок)

In journalistic analysis, news explainers, and investigative reporting (e.g. *"Осторожно, Собчак"*; see [investigative news style](investigative-news-style.md)), credibility depends on authentic evidence. **Generic stock clips or fabricated placeholders are unacceptable when real historical, news, or documentary materials exist.**

The agent must proactively find, download, and prepare genuine external assets for the edit:

### 1. Downloading Video Footage with `yt-dlp`
When referencing actual news events, speeches, press conferences, court sessions, or incidents, download precise sections of public broadcasts or online video using local command-line tools:

```sh
# Download only the specific needed segment (e.g. from 01:20 to 01:50) at 1080p or 720p:
yt-dlp --download-sections "*01:20-01:50" \
  -f "bestvideo[height<=1080]+bestaudio/best[height<=1080]" \
  --force-keyframes-at-cuts \
  -o "assets/inserts/footage/speech_clip.mp4" \
  "<VIDEO_URL>"
```

Time ranges require `--download-sections`; `--download-ranges` only covers byte ranges. On Windows the binary is `%LOCALAPPDATA%\Programs\yt-dlp\yt-dlp.exe`; `python -m yt_dlp` works only where that module is installed.

### 2. Conforming Footage with FFmpeg
Raw downloaded clips may have mismatched framerates, odd aspect ratios, or audio imbalances. Conform them before import:

```sh
# Conform to project framerate (25 or 30 fps), scale to 1080p, conform stereo audio:
ffmpeg -i assets/inserts/footage/speech_clip.mp4 \
  -r 25 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" \
  -c:v libx264 -crf 20 -preset fast \
  -c:a aac -b:a 192k \
  assets/inserts/footage/speech_clip_conformed.mp4 -y
```

### 3. Sourcing Authentic Photos, Logos, and Documents
- **Outlet Logos**: Download authentic vector/high-res PNG logos for mentioned publishers (Reuters, CNN, The Atlantic, Bloomberg, Сноб, РБК, etc.).
- **Personality Portraits**: Download official press photos or high-res portraits of politicians, experts, and subjects. Remove the background to produce a transparent PNG cutout (`assets/inserts/photos/<name>_cutout.png`).
- **News Articles & Headlines**: Download real screenshots or high-res scans of the published articles, decrees, or social media posts.

### 4. Project Workspace Organization
Organize downloaded materials in a dedicated asset structure:
```
assets/
  inserts/
    footage/       # Downloaded archival clips, press briefings, b-roll
    photos/        # Cutout portraits with transparent background (PNG)
    graphics/      # Headline cards, document scans, radar/flight maps
    logos/         # Publisher and company logos
  audio/
    sfx/           # Whooshes, pops, marker sounds, camera clicks
    music/         # Ambient investigative soundtrack
```

### 5. Packaging into Tesseract
Import all prepared local files before placing timeline layers:
```sh
# Import conformed video b-roll:
tsrct project import-video --project project.tsrct \
  --file assets/inserts/footage/speech_clip_conformed.mp4 --asset-id broll-speech-1

# Import cutout images, graphics, and logos:
tsrct project import-asset --project project.tsrct \
  --file assets/inserts/photos/subject_cutout.png --asset-id photo-subject-1 --kind image

# Import SFX and audio:
tsrct project import-asset --project project.tsrct \
  --file assets/audio/sfx/whoosh.wav --asset-id sfx-whoosh --kind audio
```

