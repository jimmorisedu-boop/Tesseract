# Motion design: full scenes and overlays

## Design the motion before the syntax

State one visual idea in concrete terms: a number grows into a comparison; a line reveals the flow through a process; a label follows the subject's direction; typography is revealed by the product's silhouette. If the only idea is “things fade in,” reconsider the design.

Decide the focal element, its relationship to the footage, and how the composition changes over time. A full scene should have composition, progression, and a payoff, not just a centered heading above three rounded boxes.

For motion that opens a paid-social or YouTube ad, read [ad hooks](ad-hooks.md) for concept selection, placement context, music/SFX synchronization, and the early opening review.

## Overlays

- Start with the footage's actual safe area. Account for the face, hands, product, subtitles, and platform cropping. Check placement across the whole interval, not one still.
- Prefer a small label or shape that points to meaningful evidence. A large opaque panel is appropriate only if the brief calls for that treatment.
- Animate in, hold long enough to read, animate out. Entrance and exit should relate to the cut or the subject's movement.
- Use contrast from placement first, then a subtle scrim/stroke/shadow as needed. Do not blanket every shot in a heavy gradient.
- For graphics behind a person, use a person matte when its required local model/resource is available, and confirm its polarity. Verify support on an actual frame first; the skill does not install segmentation models. A person-white matte with **lumaInverted** reveals graphics outside the person; **luma** reveals them inside the person. Some engine recipe prose describes the latter without stating the intended visual relationship—pick and test the polarity for the actual design.
- For a tracked pointer, do not describe it as tracked unless there are actual time-varying positions aligned to observed footage. Static arrows are fine when appropriate.

## "Выезды" & Dynamic News Graphics (Slide-Ins, Pop-Ins, Callouts)

For news analysis, investigative videos, and documentary explainers (see [investigative news style](investigative-news-style.md)):

1. **Media Headline Cards (Выезды плашек со статьями и цитатами)**:
   - Use crisp white or slate cards with rounded corners (8–16px) and subtle drop shadow.
   - Include the **authentic publisher logo** in the upper-left (e.g. Reuters, CNN, The Atlantic, Сноб, РБК) and high-contrast bold typography.
   - Apply a subtle tilt angle (-2° to +3°) for editorial dynamism.
   - Animate the card sliding in from offscreen (300–400ms) using snappy cubic-bezier easing (`cubicBezier(0.16, 1.0, 0.3, 1.0)`). Hold for 2.5–4.0s so the viewer can read the quote, then slide out or cut cleanly.
   - Pair with an energetic, clean **whoosh / swish** sound accent on entry.
2. **Personality Cutout Portraits (Выезды фото-вырезок)**:
   - Use high-resolution cutout portraits with transparent alpha channels (PNG).
   - Position in the lower-right or right third, opposite the presenter.
   - Slide up or in over 250–350ms with a slight scale settle (from 93% to 100%).
   - Pair with a soft **pop**, **camera shutter**, or **click** sound.
3. **Telegram & Social Media Bubbles (Посты из соцсетей)**:
   - Mimic native Telegram/Twitter chat bubbles with channel avatar, verified badge, channel name, and timestamp.
   - Bold or highlight key phrases. Slide in from bottom-right with slight overshoot (`cubicBezier(0.34, 1.3, 0.64, 1)`).
   - Pair with an interface **pop** or **digital tap** SFX.
4. **Scanned Documents & Yellow Marker Highlights (Выезд документов с маркером)**:
   - Display scanned decrees, court documents, or press releases with a gentle drift / push-in (scale 100% -> 105%).
   - Animate a yellow semi-transparent highlight layer (`rgba(255, 235, 59, 0.45)`) drawing horizontally across the key sentence in sync with the spoken narration.
   - Pair with a soft **marker squeak** or **paper rustle** SFX.
5. **Interactive Flight Radar & Map Route Graphics (Карты и радарные треки)**:
   - Clean vector or satellite map with animated route paths (e.g. flight trajectories with plane icons and pulsing waypoints).
   - Animate the line drawing across waypoints with location labels popping in sequentially.
   - Pair with a subtle **data hum** and radar **ping** SFX.
6. **Framed Archival Video Windows & Split Screens (Видео в рамке)**:
   - Place archival footage or speeches inside a technical/editorial graphic border with timecodes, audio visualizer bars, and source tags.
   - Use split-screen layouts (presenter on left, archival insert on right) when contrasting claims with video proof.

## Full-frame scenes

Build a hierarchy: focal content, supporting context, environment. Use spatial and temporal relationships to explain meaning. Possibilities include a native vector schematic, dimensional arrangements of 2D layers, split-screen comparisons, mask-driven type reveals, data with accurate values, or footage integrated into a composited scene.

Reserve motion for changes that guide attention. Give the viewer a stable interval to understand the result. Avoid defaulting every scene to parallax, glow, particles, bouncing labels, and a camera push at once.

## Native mechanism map

| Design need | Tesseract mechanism | Look up |
|---|---|---|
| Type hierarchy / editable text | `Text.sourceText` and imported font files | [FX authoring](fx-authoring.md#text-with-an-available-font) and the document schema |
| Per-character reveals | Text Animator and selectors; drive fields with dynamics | [FX authoring](fx-authoring.md#text-with-an-available-font) and [motion](motion.md) |
| Coordinated movement | `Group` with child layers and stable parent IDs | [FX authoring](fx-authoring.md) |
| Drawn paths / linework | `Shape` paths, fills, strokes; animate supported path fields | the document schema's Shape definitions |
| A moving reveal | Track matte or path mask using a real layer reference | the document schema's mask and track-matte definitions |
| Treatment across several layers | Group effects or an Adjustment layer above the affected siblings | the document schema's effect definitions |
| Soft lighting, blur, grade | Ordered typed layer effects | the document schema's effect definitions |
| 3D-looking layer arrangement | Supported 3D transform properties and depth ordering | the document schema and [motion](motion.md) |
| Custom pixel treatment | Bounded premultiplied-alpha WGSL custom shader | [custom shader contract](custom-shader.md) |

This is not a Blender runtime. Distinguish transforming 2D layers in 3D from general meshes, physics, or a full 3D scene.

## Timing and motion character

Tesseract FX uses editable keyframe actions and `AnimationGraph` expressions, not CSS or AE keyframe-array JSON. Read [motion](motion.md) for the installed action workflow. Use `layerTimeJsCode` and the owning layer's clock. An expression returns its value; it is not a general browser script.

For a simple reveal, 200–450ms is a useful starting range, adjusted to the scale of movement and edit. Give secondary details a small deliberate offset. Choose easing based on mass and purpose; a restrained ease-out usually reads more deliberately than an automatic spring. Overshoot can fit playful material but should be intentional.

Use standard motion blur only where it improves fast transforms; enable both composition and layer switches. Long tails of blur can erase text or mask a timing error. Render the actual movement before committing to the treatment.

## Brand application

Use supplied fonts, palette, logo geometry, and references. Keep exact logo art separate from generated scenery. This plugin's Mirage icon is not a default asset for client work. With no supplied style, choose a restrained, legible direction appropriate to the footage and describe it briefly.

## Reusable examples

[FX authoring](fx-authoring.md) contains editable examples for footage, a card, grouped labels, and captions. [Motion](motion.md) shows keyframes and procedural animation. Adapt the composition and motion to the brief rather than copying the entire example look.
