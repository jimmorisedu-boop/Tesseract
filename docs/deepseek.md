# Tesseract for DeepSeek Harness

> **The creative suite built for your AI agent.**  
> Video editing, motion graphics, sound design, and static composition — connected in one local project.

Tesseract brings professional creative tools into your **DeepSeek Harness (DSH)** session. Work with video layers, compositions, keyframes, waveforms, and audio in one connected project. Preview the result, direct revisions interactively, and render the finished video locally on your own machine.

---

## Overview & Highlights

- **Editable `.tsrct` Projects**: Keep footage, graphics, timing, keyframes, and sound available for non-destructive revisions.
- **Professional Controls**: Native keyframes, adjustment layers, text/shape animation, camera reframing, and audio ducking.
- **Free Local Rendering**: Renders locally on Windows, macOS, or Linux using hardware GPU acceleration (or a software Vulkan fallback). No Mirage account required and no cloud rendering costs.
- **No plugin manifest needed**: DSH discovers skills directly from disk, so installing the four skill bundles is the whole integration.

---

## DeepSeek Harness Installation Guide

### Step 1: Start a local DSH session in your project folder

Open DeepSeek Harness and point the session workspace at the folder that holds your footage, audio, images, and fonts. DSH runs a real local shell (`pwsh`) with file and GPU access, which is exactly what the Tesseract runtime needs.

> **Sandbox note:** DSH's default file policy confines writes to the session workspace. Keep the `.tsrct` project, imported assets, and renders inside that folder; writing outside it (for example into `%LOCALAPPDATA%`) requires an explicit approval.

### Step 2: Install the Tesseract skills

You can install Tesseract for DSH in three ways.

#### Option A: One command (installs into the shared agent skills directory)

```sh
npx skills add mirage-hq/Tesseract
```

Select the four Tesseract skills. The installer writes them to `~/.agents/skills`, which DSH scans at rank 500 — no DSH-specific step is required. Requires Node.js/npm for the installer only; the Tesseract CLI itself does not need Node.

#### Option B: Manual copy (PowerShell, Windows)

```powershell
# 1. Get the skills (a clone, a release ZIP, or an existing checkout)
git clone https://github.com/mirage-hq/Tesseract.git "$HOME\Tesseract"

# 2. Copy all four skill bundles into a root DSH scans
$dst = "$HOME\.agents\skills"          # shared with other agents
# $dst = "$HOME\.dsh\skills"           # or: DSH-only
New-Item -ItemType Directory -Force $dst | Out-Null
Copy-Item -Recurse -Force "$HOME\Tesseract\skills\*" $dst
```

```bash
# macOS / Linux
git clone https://github.com/mirage-hq/Tesseract.git ~/Tesseract
mkdir -p ~/.agents/skills
cp -R ~/Tesseract/skills/* ~/.agents/skills/
```

DSH watches its skill roots, so the four skills appear in the session catalog on the next model step — no restart needed.

#### Option C: Project-local install (per-repository)

Keep the skills next to a specific project instead of installing them globally:

```powershell
New-Item -ItemType Directory -Force .agents\skills | Out-Null   # or .dsh\skills
Copy-Item -Recurse -Force "$HOME\Tesseract\skills\*" .agents\skills\
Copy-Item -Force "$HOME\Tesseract\AGENTS.md" .                     # optional DSH rules
```

#### Option D: Autonomous setup by the DSH agent

Paste this prompt into a DSH session and the agent installs the CLI runtime, verifies the checksum, and confirms a render:

```text
Set up Tesseract by Mirage so you can create editable designs, edit videos, and make motion graphics in this DeepSeek Harness session. Install the four Tesseract skills from https://github.com/mirage-hq/Tesseract into a skill root DSH scans (~/.agents/skills or ~/.dsh/skills), check this system's environment, download the required Tesseract CLI (v0.3.1) matching my architecture, verify the SHA-256 checksum, run the installer, and verify `tsrct --version`. Confirm a short preview renders correctly with `tsrct project create` + `tsrct preview`. Then ask me for my footage or the video/motion project I want to create. Keep the editable .tsrct project and source assets with the finished render.
```

### Step 3: Direct the first edit

Give the agent your footage and a brief. Ask it to use Tesseract, show a preview, and refine the project with your feedback:

```text
Use Tesseract to make a 15-second video from the footage in this folder. Start with a strong opening, add a clean animated title, balance dialogue with background music, and show me a preview before the final render. Keep the .tsrct project editable for revisions.
```

---

## Where DeepSeek Harness looks for skills

DSH discovers a skill as either a directory bundle `<name>/SKILL.md` or a flat `<name>.md` at the top level of a scanned root (nested trees are not discovered). Frontmatter must carry `name` (kebab-case) and `description`.

| Rank | Source | Path | Use it for |
|---|---|---|---|
| 100 | `project-dsh` | `<projectRoot>/.dsh/skills` | DSH-only skills inside one repository |
| 200 | `project-agents` | `<projectRoot>/.agents/skills` | Shared project skills |
| 300 | `custom` | configured `customSkillDirs` | Extra local roots |
| 400 | `user-dsh` | `~/.dsh/skills` | Global, DSH-only |
| 500 | `user-agents` | `~/.agents/skills` | Global, shared across agents (where `npx skills add` writes) |

The project root is the nearest ancestor containing `.git`. This is why Tesseract needs no DSH plugin package: four skill bundles under any of those roots are enough.

## Optional: persistent Tesseract rules for DSH

DSH injects workspace instructions from the user-global `~/.dsh/AGENTS.md` plus the project chain (`AGENTS.md`, `CLAUDE.md`, and their `.local.md` overlays) from the project root down to the working directory. Add the block below to `~/.dsh/AGENTS.md` if you want the CLI path, version pin, and editable-project rules in every session:

```markdown
## Tesseract

- CLI: `$env:LOCALAPPDATA\Tesseract\bin\tsrct.cmd` (Windows), `~/Library/Application Support/Tesseract/bin/tsrct` (macOS), `~/.local/share/Tesseract/bin/tsrct` (Linux); `tsrct` on PATH also works.
- Version must match the pin in the installed skill's `references/cli-version.txt` (currently `0.3.1`); verify with `tsrct --version` once per session.
- Keep the editable `.tsrct` project (`project commit` / `project apply`) alongside every exported MP4/PNG/MOV.
- Preview frames with `tsrct preview --project <path> --time <seconds> --output <path>`.
```

The repository also ships a root `AGENTS.md` with the same guidance, so a DSH session opened inside a Tesseract checkout picks it up automatically.

---

## Directing your first edit

### Video editing prompt

```text
Use Tesseract to make a 15-second video from the footage in this folder. Start with a strong opening, add a clean animated title, balance dialogue with background music, and show me a preview before the final render. Keep the .tsrct project editable for revisions.
```

### Motion graphics prompt

```text
Use Tesseract to animate a 3-step feature walkthrough diagram. Use our brand palette (#1D1F20, #00D0FF), smooth bezier easing, and export both an MP4 preview and an editable .tsrct project.
```

### Design / banner prompt

```text
Use Tesseract to design a promotional graphic to accompany this video. Match its typography and colors. Deliver the PNG and the editable .tsrct document.
```

### Project revisions

```text
Make the title appear 0.5s earlier with a soft scale-in. Lower the music volume when dialogue starts, and render an updated preview.
```

---

## Skills included

| Skill | Description | Use case |
|---|---|---|
| **`tesseract-video`** | Full video editing pipeline | Cutting footage, pacing, audio ducking, dialogue preservation, and MP4 export. |
| **`tesseract-motion`** | Kinetic typography & 2D motion | Title animations, lower-thirds, shape layers, diagrams, and video overlays. |
| **`tesseract-design`** | Static visual compositions | Posters, social banners, slide layouts, and UI mockups as PNGs. |
| **`tesseract-editor`** | Browser-based project editor | Interactive web applications to open, preview, and edit `.tsrct` files in a browser. |

---

## House style skill: news-review-video

Alongside the four Tesseract skills, this repository ships a fifth skill that defines the
house standard for news-review and commentary episodes: block structure, insert cadence,
mandatory camera moves on every still, sourced third-party inserts with a provenance ledger
(`assets/sources.json`), and a pacing QC script (`scripts/measure_pacing.py`) whose thresholds
are calibrated against the reference episode. Install it the same way as the others (copy
`skills/news-review-video` into `~/.agents/skills`), and point your user-global
`~/.dsh/AGENTS.md` at it so every session applies the standard.
## Runtime CLI requirements

- **Windows**: 64-bit Windows 10 or later (`%LOCALAPPDATA%\Tesseract\bin\tsrct.cmd`).
- **macOS**: Apple Silicon (`arm64`) or Intel (`x86_64`) (`~/Library/Application Support/Tesseract/bin/tsrct`).
- **Linux**: x86_64 with glibc 2.35+ and Vulkan support (`~/.local/share/Tesseract/bin/tsrct`).
- **Version pin**: `0.3.1` (`skills/tesseract-video/references/cli-version.txt`).
- **Telemetry**: opt out anytime with `$env:TESSERACT_TELEMETRY = "0"` (Windows) or `export TESSERACT_TELEMETRY=0`.
- **Downloads**: [GitHub releases](https://github.com/mirage-hq/Tesseract/releases) — pick `windows-x86_64`, `darwin-arm64`, `darwin-x86_64`, or `linux-x86_64`, and verify the matching `.sha256`.

## Verify the installation

Run these in the DSH session (or in any terminal) from your project folder:

```powershell
& "$env:LOCALAPPDATA\Tesseract\bin\tsrct.cmd" --version    # expect: tsrct 0.3.1 (<revision>)
& "$env:LOCALAPPDATA\Tesseract\bin\tsrct.cmd" project create -p smoke.tsrct
& "$env:LOCALAPPDATA\Tesseract\bin\tsrct.cmd" preview -p smoke.tsrct -t 0.5 -o smoke-frame.png
```

A new project is empty, so the first frame is a fully transparent PNG at the composition size — that already proves the renderer runs. To confirm real content renders, add a layer and preview again:

```powershell
'[{"type":"createFxRectLayer","compositionId":"main","layerId":1,"name":"Card","insertIndex":0,
  "activeRange":{"start":0,"duration":3000},
  "transform":{"anchorPoint":[0,0],"position":[80,80],"scale":[100,100],"rotation":0,"opacity":100},
  "rect":{"size":[400,160],"fillColor":[0.05,0.25,0.8,1]}}]' |
  Set-Content -Encoding utf8 actions.json

& "$env:LOCALAPPDATA\Tesseract\bin\tsrct.cmd" project apply -p smoke.tsrct --actions actions.json
& "$env:LOCALAPPDATA\Tesseract\bin\tsrct.cmd" preview -p smoke.tsrct -t 0.5 -o smoke-frame2.png
```

The second frame must contain the blue card (400×160 px at `(80,80)`, RGBA `[0.05,0.25,0.8,1]`). If it is still empty, the renderer is not executing content — read the CLI error and the [CLI installation reference](../skills/tesseract-video/references/installation.md).

---

## FAQ

**Does Tesseract work inside a DeepSeek Harness session?**  
Yes. DSH has local shell execution, file access, and GPU access, so `tsrct` runs locally with full hardware acceleration, and the skills are discovered from disk.

**Do I need a DSH plugin or manifest?**  
No. DSH reads skills from `~/.agents/skills`, `~/.dsh/skills`, or a project-local `.agents/skills` / `.dsh/skills`. Copying the four bundles is the complete integration.

**Do I need both the plugin and the skills?**  
No. Install the skills (or the plugin, for agents that support plugin listings); they provide the same creative guidance, and the agent then installs the matching runtime.

**Will it use my own footage?**  
Yes. Put your clips, audio, fonts, and images in the session workspace and tell the agent which files to use. Tesseract packages them into the project as editable assets.

**Why does the agent ask for approval during setup?**  
The CLI installs into `%LOCALAPPDATA%\Tesseract` (or the platform equivalent), which is outside the DSH session workspace. DSH asks before writing there; the skills themselves only need a skill root, which is a normal user-level directory.

**Where do I get runtime and setup help?**  
The [CLI installation reference](../skills/tesseract-video/references/installation.md) covers compatibility, checksums, and platform requirements. Report the exact CLI error if a download, install, or render fails.

**Can I switch rendering engines if the GPU is unavailable?**  
No. Do not substitute a hosted service or another renderer; report the failure. On Linux, a compatible Mesa lavapipe driver provides software rendering.

---

Documentation adapted for DeepSeek Harness. Tesseract is developed by NOCAP, Inc. d/b/a Mirage.
