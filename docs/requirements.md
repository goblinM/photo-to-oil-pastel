# Photo to Oil Pastel Requirements

This document records the runtime, capability, input/output, and quality requirements for the skill. The canonical execution instructions remain in `../SKILL.md`.

## Runtime requirements

| Requirement | Status | Purpose |
| --- | --- | --- |
| Instruction-capable host | Required | Run the workflow from `SKILL.md`; this may be an agent, application, CLI, or workflow engine. |
| File system or artifact store | Required | Read the source photo and retain generated artifacts without modifying the original. |
| Compatible image-editing backend | Required for artwork generation | Create the finished artwork and two drawing stages from reference images. |
| `python3` 3.9+ | Required for loop assembly | Run `scripts/assemble_step_loop.py`; only the standard library is used. |
| `ffmpeg` | Required | Convert HEIC working copies and encode MP4/GIF outputs. |
| `ffprobe` | Required | Read image dimensions and verify output media. |

No Pillow, OpenCV, NumPy, or other third-party Python packages are required at runtime.

Codex's `imagegen` skill is one optional backend adapter, not a dependency of the portable core. Other hosts may use any local or remote image-to-image implementation that satisfies [`backend-contract.md`](backend-contract.md).

The official `skill-creator/scripts/quick_validate.py` utility additionally needs `PyYAML`, but that package is a development-time validation dependency, not a runtime dependency of this skill.

## Capability requirements

- The image backend must accept a reference image plus a text instruction and return a raster image file or resolvable artifact URI.
- The backend should preserve composition and identity closely enough for controlled image-to-image editing.
- The host must support visual inspection by a human or a vision-capable model before accepting each stage.
- The host must be able to place generated images in a user-visible output directory or artifact store.
- Exact token accounting is optional because some built-in image tools do not expose usage metadata. The final report must mark unavailable fields instead of estimating them.

## Input requirements

- One user-provided photo in a format readable by the image viewer or FFmpeg.
- Supported practical inputs include PNG, JPEG, WebP, and HEIC when the local FFmpeg build can decode it.
- The original file is read-only input. Always create a non-destructive working copy.
- Best results come from a clear focal subject, a recognizable silhouette, and no more than one strong secondary anchor.

## Functional requirements

1. Analyze the photo before generation and identify the main subject, secondary anchor, removable clutter, and a 6–10 color palette.
2. Create a finished oil-pastel artwork that looks realistically paintable by a beginner-to-intermediate artist.
3. Use the accepted finished artwork as the reference for the early and late drawing stages.
4. Generate stages separately at full resolution; do not use a contact sheet as the animation source.
5. Assemble a 5–10 second step loop using direct stage changes.
6. Preserve major anchors across stages and reject obvious geometry or identity drift.
7. Report image-generation call counts and exact token usage when exposed; otherwise report `unavailable` with the reason.

## Visual quality requirements

- Prefer broad blunt strokes, visible paper tooth, uneven pressure, broken edges, paper gaps, and limited layering.
- Simplify clutter, tiny objects, signage, complex backgrounds, and photographic micro-detail.
- Preserve identity-critical features for people, pets, and keepsakes.
- Preserve structure-critical geometry for landscapes, street scenes, buildings, horizons, and trees.
- Avoid photorealism, glossy digital rendering, smooth airbrush gradients, perfect vector edges, excessive bloom, and invented readable text.
- The early and middle frames must each look like believable unfinished drawings, not degraded versions of the final image.
- Do not use blur-to-sharp, pixel reveals, strip masks, or geometry-dissolving transitions.

## Output requirements

Default artifact names:

```text
01-source.png
02-final-oil-pastel.png
03-early-block-in.png
04-late-intermediate.png
05-process-master.mp4
06-oil-pastel-process.gif
```

Default loop profile:

- Duration: 6 seconds, configurable from 5 through 10 seconds.
- Frame rate: 10 FPS, configurable from 6 through 20 FPS.
- Portrait GIF: 540 pixels wide; height derived from the final artwork.
- The final stage receives approximately 46% of the total duration.
- GIF loops continuously; MP4 uses H.264 with `yuv420p` for compatibility.

## Permissions and side effects

- Reading a user-selected photo and writing results to the requested output directory are in scope.
- Do not overwrite existing outputs unless the user explicitly permits replacement or the script is called with `--force` for a known test target.
- Do not install missing programs or Python packages without user approval.
- Do not embed API keys, access tokens, provider endpoints, or account identifiers in this skill package.
- Do not modify or delete the source photo.

## Token reporting schema

Use this structure in the final response:

```text
Usage
- Successful image-generation calls: <number>
- Failed/cancelled image-generation calls: <number>
- Input tokens: <exact number | unavailable>
- Output/image tokens: <exact number | unavailable>
- Total tokens: <exact number | unavailable>
- Note: <why unavailable, if applicable; local FFmpeg does not call the image model>
```
