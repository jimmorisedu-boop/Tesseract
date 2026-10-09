# Tesseract for Antigravity

> **The creative suite built for your AI agent.**  
> Video editing, motion graphics, sound design, and static composition — connected in one local project.

Tesseract brings professional creative tools into your **Google Antigravity** workflow. Work with video layers, compositions, keyframes, waveforms, and audio in one connected project. Preview the result, direct revisions interactively, and render the finished video locally.

---

## Overview & Highlights

- **Editable `.tsrct` Projects**: Keep footage, graphics, timing, keyframes, and sound available for non-destructive revisions.
- **Professional Controls**: Native keyframes, adjustment layers, text/shape animation, camera reframing, and audio ducking.
- **Free Local Rendering**: Renders locally on Windows, macOS, or Linux using hardware GPU acceleration (or software Vulkan fallback). No Mirage account required and no cloud rendering costs.

---

## Antigravity Installation Guide

### Step 1: Open your project in Antigravity

Open your workspace directory containing your media assets or start a fresh workspace in the Antigravity IDE.

### Step 2: Install Tesseract for Antigravity

You can install Tesseract in Antigravity in three ways:

#### Option A: Global Plugin (Recommended for all workspaces)
Install Tesseract as a global Antigravity plugin so its skills are available across all your projects:

```powershell
# Windows PowerShell
$pluginDir = "$HOME\.gemini\config\plugins\tesseract"
git clone https://github.com/mirage-hq/tesseract.git $pluginDir
```
```bash
# macOS / Linux
git clone https://github.com/mirage-hq/tesseract.git ~/.gemini/config/plugins/tesseract
```

Restart Antigravity or trigger a plugin reload to register the plugin.

#### Option B: Workspace Customization (Project-level)
Add Tesseract directly into your project's `.agents/` folder:

```powershell
# Inside your project root:
New-Item -ItemType Directory -Force .agents\skills | Out-Null
Copy-Item -Recurse path\to\tesseract\skills\* .agents\skills\
Copy-Item path\to\tesseract\GEMINI.md .
```

#### Option C: Autonomous Setup by Antigravity Agent
Copy the prompt below into Antigravity, and the agent will install the CLI runtime, verify checksums, and test a render autonomously!

---

## Paste this prompt into Antigravity

```text
Set up Tesseract by Mirage so you can create editable designs, edit videos, and make motion graphics in Antigravity. Check this system's environment, download the required Tesseract CLI (v0.3.1) matching my architecture, verify the SHA-256 checksum, run the installer, and verify `tsrct --version`. Confirm a short preview renders correctly. Then ask me for my footage or the video/motion project I want to create. Keep the editable .tsrct project and source assets with the finished render.
```

---

## Directing Your First Edit

Once installed, give Antigravity your brief and assets:

### Video Editing Prompt
```text
Use Tesseract to make a 15-second video from the footage in this folder. Start with a strong opening, add a clean animated title, balance dialogue with background music, and show me a preview before the final render. Keep the .tsrct project editable for revisions.
```

### Motion Graphics Prompt
```text
Use Tesseract to animate a 3-step feature walkthrough diagram. Use our brand palette (#1D1F20, #00D0FF), smooth bezier easing, and export both an MP4 preview and an editable .tsrct project.
```

### Design / Banner Prompt
```text
Use Tesseract to design a promotional graphic to accompany this video. Match its typography and colors. Deliver the PNG and the editable .tsrct document.
```

### Project Revisions
```text
Make the title appear 0.5s earlier with a soft scale-in. Lower the music volume when dialogue starts, and render an updated preview.
```

---

## Skills Included

| Skill | Description | Use Case |
|---|---|---|
| **`tesseract-video`** | Full video editing pipeline | Cutting footage, pacing, audio ducking, dialogue preservation, and MP4 export. |
| **`tesseract-motion`** | Kinetic typography & 2D motion | Title animations, lower-thirds, shape layers, diagrams, and video overlays. |
| **`tesseract-design`** | Static visual compositions | Posters, social media banners, slide layouts, and UI mockups as PNGs. |
| **`tesseract-editor`** | Browser-based project editor | Interactive web applications to open, preview, and edit `.tsrct` files in browser. |

---

## Runtime CLI Requirements

- **Windows**: 64-bit Windows 10 or later (`%LOCALAPPDATA%\Tesseract\bin\tsrct.cmd`).
- **macOS**: Apple Silicon (`arm64`) or Intel (`x86_64`) (`~/Library/Application Support/Tesseract/bin/tsrct`).
- **Linux**: x86_64 with glibc 2.35+ and Vulkan support (`~/.local/share/Tesseract/bin/tsrct`).
- **Telemetry**: Opt-out anytime with `$env:TESSERACT_TELEMETRY = "0"` or `export TESSERACT_TELEMETRY=0`.
