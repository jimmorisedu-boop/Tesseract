<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/images/wordmark-dark.svg" />
    <source media="(prefers-color-scheme: light)" srcset="docs/images/wordmark-light.svg" />
    <img src="docs/images/wordmark-light.svg" alt="Tesseract by Mirage" width="478" />
  </picture>
</p>

<p align="center">
  <strong>The creative suite built for your AI agent.</strong><br />
  Editing, motion, and sound. Connected in one local project.
</p>

<p align="center">
  <a href="#get-started">Get started</a> ·
  <a href="#what-you-can-make">What you can make</a> ·
  <a href="#example-projects">Examples</a> ·
  <a href="#manual-downloads">Downloads</a> ·
  <a href="https://mirage.app">Mirage</a>
</p>

<img src="docs/images/hero.png" alt="An illustration of video layers, keyframes, and audio, with the direction: Apply heat refraction. Ease it in with the music." width="912" />

Tesseract brings professional creative tools into your agent workflow. Work with video layers, compositions, keyframes, and audio in one connected project. Preview the result, direct a revision, and render the finished video locally.

## Get started

**macOS, Windows, or Linux x86_64**, including compatible cloud-agent environments.
Your agent needs file and command access.
See the [installation guide](skills/tesseract-video/references/installation.md) for platform requirements.

### Install with one command

```sh
npx skills add mirage-hq/Tesseract
```

Choose the Tesseract skills you need. Requires Node.js/npm for this installer; the Tesseract CLI itself does not require Node.

Then [ask it to make a video](#what-you-can-make). The skills guide your agent through CLI setup when needed.

### Or let your agent install it

```text
Install the Tesseract skills from https://github.com/mirage-hq/Tesseract.
Follow their installation guide to set up the matching CLI for my
computer, verify its checksum, and confirm it runs.
Then ask me for my footage or the video I want to make.
```

### Plugins & Agent Integrations

- [Antigravity Guide & Plugin →](docs/antigravity.md)
- [DeepSeek Harness Guide →](docs/deepseek.md)
- [News-review house style skill →](skills/news-review-video/SKILL.md)
- [ChatGPT/Codex plugin →](https://chatgpt.com/plugins/plugins_6ab148f4986c819198f6a08c7fb30f3e?open_in_app)
- Claude Code plugin coming soon

### Manual downloads

**[Download a release →](https://github.com/mirage-hq/Tesseract/releases)** · **[Installation guide →](skills/tesseract-video/references/installation.md)**

| Download | Choose this for |
| --- | --- |
| CLI ZIP — `linux-x86_64` | Linux PCs and compatible cloud-agent environments |
| CLI ZIP — `darwin-arm64` | Apple Silicon Mac |
| CLI ZIP — `darwin-x86_64` | Intel Mac |
| CLI ZIP — `windows-x86_64` | 64-bit Windows PC |
| Web runtime ZIP — `web` | Build browser-based Tesseract editors and previews |
| Matching `.sha256` | Verify your ZIP before installing |

Use the CLI version required by your skills. Install either the plugin or the skills; you don't need both.

## Global Installation & Cross-Project Setup (Запуск из любой папки)

To make Tesseract and its AI skills available across **any project or folder** on your machine:

### 1. Add Tesseract CLI to PATH
The CLI executable installs to:
- **Windows**: `$env:LOCALAPPDATA\Tesseract\bin\tsrct.cmd`
- **macOS**: `~/Library/Application Support/Tesseract/bin/tsrct`
- **Linux**: `~/.local/share/Tesseract/bin/tsrct`

To run `tsrct` from any terminal directory:
```powershell
# Windows PowerShell (User PATH)
[Environment]::SetEnvironmentVariable(
    "Path",
    [Environment]::GetEnvironmentVariable("Path", "User") + ";$env:LOCALAPPDATA\Tesseract\bin",
    "User"
)
```
```bash
# macOS / Linux (add to ~/.zshrc or ~/.bashrc)
export PATH="$HOME/.local/share/Tesseract/bin:$PATH"
```

### 2. Install Skills Globally for AI Agents
To allow Antigravity, DeepSeek, or other AI agents to discover Tesseract skills in **any workspace**:
```powershell
# Option A: Global shared agents directory (Antigravity & DeepSeek)
$dst = "$HOME\.agents\skills"
New-Item -ItemType Directory -Force $dst | Out-Null
Copy-Item -Recurse -Force "skills\*" $dst

# Option B: Global Antigravity plugin directory
$pluginDst = "$HOME\.gemini\config\plugins\tesseract"
New-Item -ItemType Directory -Force $pluginDst | Out-Null
Copy-Item -Recurse -Force "*" $pluginDst
```

### 3. Running in a New Project Folder
In any directory on your computer:
1. Open the folder in your AI harness (Antigravity, DSH).
2. Place your raw host footage in the folder.
3. Prompt your agent to edit the video — it will autonomously source authentic B-roll, assemble the dynamic edit, animate slide-ins ("выезды"), duck sound, and export:
   - **Master MP4**: Finished 1080p video.
   - **Tesseract Project**: `.tsrct` non-destructive bundle.
   - **Adobe Premiere Pro**: Final Cut Pro / Premiere XML (`<project>_premiere.xml`).
   - **Adobe After Effects**: ExtendScript (`<project>_aftereffects.jsx`) or transparent ProRes 4444 MOV overlays.

## What you can make

| Skill | Use it for |
| --- | --- |
| **Tesseract: Edit Video** | Cut footage, adjust framing, combine dialogue, duck music, and export to MP4 + Adobe Premiere/AE. |
| **Tesseract: Motion Graphics** | Animate titles, typography, diagrams, news slide-ins ("выезды"), and overlays. |
| **News-review house style** | Journalistic news explainers (Sobchak archetype): 2.5–5s pacing, punch-ins, authentic inserts, marker highlights. |
| **Tesseract: Editor** | Build a custom browser editor for previewing, editing, and saving Tesseract projects. |
| **Tesseract: Design** | Create static visuals, including posters, social graphics, and UI mockups. |

Attach your material, then copy a prompt:

```text
Use Tesseract to turn these clips into a 30-second product video.
Keep the opening quick, add a clean title, and finish on the logo.
```

```text
Use Tesseract to animate a diagram of these three steps.
Use our brand colors and keep the text editable.
```

```text
Use Tesseract to design a promotional graphic to accompany this video.
Match its typography and colors. Deliver the PNG and editable project.
```

Preview, then direct a revision:

```text
Make the title arrive earlier and soften the motion.
Render a preview before exporting the finished video.
```

Keep the editable `.tsrct` project for your next revision.

## Example projects

Finished projects to open, take apart, and remix — each one an editable `.tsrct` document with the video it renders to.

**[Browse the examples →](https://github.com/mirage-hq/Tesseract-Projects)**

Grouped by scope: a single feature shown on its own, a small finished piece, or a full production. Point your agent at any `.tsrct` and describe the change you want.

## Terms

[Product terms](TERMS.md) · [Tesseract terms](https://mirage.app/legal/tesseract-terms) · [Privacy policy](https://mirage.app/legal/privacy-policy) · [Third-party notices](THIRD_PARTY_NOTICES.md)

Each CLI ZIP includes third-party notices, licenses, and matching dependency sources.
