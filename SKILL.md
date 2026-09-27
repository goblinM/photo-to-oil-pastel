---
name: photo-to-oil-pastel
description: Transform a user-provided photo into a simplified, realistically paintable oil-pastel artwork and optionally create a 5–10 second looping GIF or MP4 from genuine block-in, refinement, and finished stages. Use for 照片转油画棒, 油彩笔画, 可绘制化简化, or oil-pastel process GIF requests. Do not use for ordinary photo filters, photorealistic repainting, or claims of recording a real human drawing session.
---

# Photo to Oil Pastel

Turn a meaningful photo into an oil-pastel drawing that looks achievable by hand, then optionally re-stage its creation as a short loop. Favor believable materials and paintable simplification over photographic fidelity.

This file is the platform-neutral execution entrypoint. For review and maintenance, see the [Chinese version](docs/skill-zh.md), [Chinese user guide](docs/user-guide-zh.md), [style-selection guide](references/style-selection.md), [runtime and functional requirements](docs/requirements.md), [portability guide](docs/portability.md), and [image-backend contract](docs/backend-contract.md). Keep the English and Chinese instructions synchronized when changing behavior. Files under `agents/` are optional host adapters and are not required by the portable core.

## User guidance and intake

Do not require users to understand style-family names, prompt syntax, paper exposure, or generation parameters. Guide them in plain language.

When invoked without a usable photo, respond with this concise direction, adapted to the host:

> Please upload one photo. I will first identify what should be preserved, recommend the most suitable oil-pastel treatment, and then create the finished still. If you also want the drawing process, say “add a 6-second GIF” or specify 5–10 seconds.

When a photo is present but the request is brief, do not return a questionnaire. Inspect it, state the recommended style and the most important preserve/simplify choices in 2–4 short lines, then proceed with a still image by default. Treat “you choose,” “直接做,” or no style preference as permission to select the best-fit style family using this skill—not as permission to change the story, identity, or subject.

Ask one concise question only when the answer would materially change the result, such as:

- two equally suitable styles would create clearly different moods;
- the user has not made clear which of several people or objects is the memory-critical subject;
- the requested output could reasonably mean either a still only or an animation and their wording does not establish a default.

Do not ask about technical settings that the defaults already resolve. If the user says “GIF,” “过程,” “从 0 到 1,” or “视频,” use the default 6-second staged loop unless another duration is specified.

Before generation, provide a compact **creation brief**:

- `Keep:` identity, pose, composition, or memory anchors;
- `Simplify:` clutter, micro-detail, and text treatment;
- `Style:` the recommended family described in ordinary visual language;
- `Deliver:` still, GIF, or still plus MP4/GIF.

After delivery, explain the main transformation in one short paragraph, disclose any rejected retry or unresolved limitation, provide the required usage block, and offer only relevant next choices such as “make it softer,” “change to another style family,” or “add a process GIF.” Do not overwhelm the user with the internal style card unless they ask to inspect it.

## Default deliverables

- `01-source.png`: non-destructive working copy of the source.
- `02-final-oil-pastel.png`: finished simplified artwork.
- `03-early-block-in.png`: broad-color stage.
- `04-late-intermediate.png`: layered, roughly 75%-complete stage.
- `05-process-master.mp4`: local animation master.
- `06-oil-pastel-process.gif`: 5–10 second loop, default 6 seconds at 10 FPS.

When the user requests only a still image, stop after the final artwork. Prefer GIF when the user asks for a loop, drawing steps, or 从铺色到完成; add MP4 only when requested or useful as a clean master.

## Workflow

### 1. Prepare and inspect the source

Create a dedicated output directory. Never modify the original photo.

If the source is HEIC and the image viewer cannot read it, convert only a working copy:

```bash
ffmpeg -y -v error -i SOURCE.HEIC -frames:v 1 OUTPUT_DIR/01-source.png
```

Inspect the converted image before generating anything. Identify:

- the primary subject or structural anchor;
- a secondary visual anchor worth preserving;
- clutter that can be removed without changing the memory or story;
- 6–10 practical oil-pastel colors;
- text, signs, tiny objects, and photographic details that should become abstract marks.

When the subject has a face or character-like features, write a **feature-lock card** before generation. Record only visible, identity-critical facts: eye count and shape, open/closed direction, pupil or highlight arrangement, nose geometry and fill, mouth presence and geometry, ear placement, face patches, and fixed accessories. Separate these hard invariants from texture that may be omitted. For example, “two narrow downward-curved eyes with two highlights; solid triangular nose; separate small mouth” is a lock, not optional styling.

For portraits, people, pets, or keepsakes, preserve identity-critical silhouette, pose, expression, and color blocks. For landscapes or street scenes, preserve the dominant perspective, main trunks/buildings/horizon, and light placement.

### 2. Plan for paintability

Do not directly imitate every photograph detail. Translate the source into a drawing plan:

- reduce background objects;
- merge similar colors into large shapes;
- retain one main focal subject and at most one strong secondary anchor;
- replace readable background text with non-readable marks or simple color rectangles;
- keep visible paper gaps, broken edges, uneven pressure, and limited layering;
- make the result plausible for a beginner-to-intermediate artist using real oil pastels.

Simplification may remove texture and secondary marks, but it must not redesign a locked facial feature. In an unfinished stage, either preserve the locked feature's geometry or omit a detail that has not been drawn yet; never replace it with a different symbol.

Reject directions that produce glossy digital illustration, smooth airbrush gradients, hyper-detailed fur or flowers, perfect vector edges, cinematic glow, or a generic AI-painting finish.
Retain visible oil-pastel granulation, wax crumbs, and paper tooth. A shared fine grain may run across multiple surfaces and is not a defect by itself. Do not smooth or airbrush the image merely to remove repeated grain; instead ensure that the larger structural strokes, shape simplification, and thickness hierarchy remain legible above this common material texture.

### 3. Select a style family

Read [references/style-selection.md](references/style-selection.md). Choose one primary style family from the photo's structure, subject scale, emotional tone, and amount of removable detail; do not default every photo to the same generic oil-pastel finish.

Write a short **style card** before prompting:

- selected family and why it fits this photo;
- stroke scale and direction;
- edge behavior and amount of paper exposure;
- layering density and value contrast;
- palette size and temperature;
- details that must be simplified or retained.

Use one primary family. Add at most one secondary influence only when it solves a specific need, and state that need. Never identify a style solely by a living artist, social-media creator, or copyrighted work; translate references into observable medium, stroke, edge, palette, and simplification properties.

### 4. Generate the finished artwork

Resolve an image-editing backend in this order:

1. use the host's native image-to-image or reference-image editing capability;
2. in Codex, load and follow the available `imagegen` skill;
3. in an API, CLI, agent framework, or workflow system, call an adapter that implements [docs/backend-contract.md](docs/backend-contract.md).

Treat the photo as the edit target. Do not depend on a particular model vendor, tool name, SDK, or credential layout. If no compatible image-editing backend is available, stop after producing the paintability analysis and the three adapted prompts. State clearly that no images were generated; do not pretend success or install a provider without permission.

Read [references/prompt-templates.md](references/prompt-templates.md) and adapt the finished-art prompt to the actual subject. Paste the style card into the prompt and express it through concrete marks rather than a style label alone. Preserve the source composition while simplifying it; do not introduce unrelated objects or narrative changes.

Inspect the result against both the source and the feature-lock card. Retry once only when there is a material failure such as changed identity, changed locked facial geometry, broken anatomy, lost focal subject, unreadable composition, excessive photographic detail, or obvious digital polish. Make the retry narrowly corrective.

Copy the accepted image into the output directory as `02-final-oil-pastel.png`.

### 5. Generate two real drawing stages

Use the accepted final artwork—not the original photograph—as the reference for both stage edits. Generate each stage as its own full-resolution image; do not ask for a multi-panel contact sheet.

1. **Early block-in:** large background and subject color masses, substantial paper gaps, minimal facial or object details, no polish.
2. **Late intermediate:** the same composition about 75% complete, with shadows and major details but without the smallest texture marks, sharp highlights, lettering, or final cleanup.

Use the corresponding templates in [references/prompt-templates.md](references/prompt-templates.md). Lock the crop, perspective, main silhouettes, branch/horizon/building placement, subject scale, and hand or face geometry in every stage.

Keep the same style card across all stages. Progress should come from coverage and layering, not from changing the drawing language between frames.

Paste the same feature-lock card verbatim into both stage prompts. If the face is small in the full frame, use a protected-region mask, crop/reference control, or a focused local correction when the backend supports it. Lack of tiny texture is acceptable; different eye, nose, or mouth topology is not.

Retry a stage once if a major anchor jumps or any locked feature changes. If the corrected stage still violates the feature lock, reject it and do not assemble the GIF. Report the rejected stage instead of treating identity drift as handmade variation.

### 6. Assemble the loop

Use the included script; it requires `ffmpeg` and `ffprobe` but no third-party Python packages:

```bash
python3 scripts/assemble_step_loop.py \
  --early OUTPUT_DIR/03-early-block-in.png \
  --middle OUTPUT_DIR/04-late-intermediate.png \
  --final OUTPUT_DIR/02-final-oil-pastel.png \
  --output OUTPUT_DIR/06-oil-pastel-process.gif \
  --keep-master OUTPUT_DIR/05-process-master.mp4 \
  --duration 6 \
  --fps 10
```

The loop uses direct stage changes, not blur-to-sharp, pixel reveals, horizontal strip masks, dissolving geometry, or other effects that make the result look like an AI filter. The final stage receives the longest hold.

### 7. Verify

- Compare the source and final artwork: the memory, main subject, and composition must remain recognizable.
- Compare the final artwork with the style card: stroke scale, paper exposure, edge treatment, palette, and detail density must match the selected family. Reject a result that falls back to generic detailed illustration.
- Confirm that the result retains visible granular wax, pigment crumbs, and paper tooth. Fine shared grain across surfaces is acceptable and often desirable; reject an over-smoothed result that loses the oil-pastel surface. Evaluate the direction and scale of the larger form-building strokes separately from the shared material grain.
- Compare all three generated stages side by side: major anchors should not move or change scale.
- Inspect every identity-critical face or character region at useful zoom. Compare eye geometry and highlight pattern, nose geometry, mouth presence/shape, ears, patches, and fixed accessories against the feature-lock card.
- An unfinished stage may contain fewer marks, but every visible locked mark must have the same topology and relative placement as the accepted final. Reject substitutions such as round eyes for curved eyes, a Y-shaped nose for a triangle, or a missing mouth after the mouth has already been established.
- Confirm the early and middle frames are believable standalone unfinished drawings.
- Confirm GIF duration is 5–10 seconds and the final artwork is held long enough to read.
- Inspect the first, middle, and final frames. Reject morphing anatomy, extra limbs, moving buildings, shifting trunks, readable invented text, or digital reveal artifacts.
- Prefer 540×720 at 10 FPS for a compact portrait GIF. Reduce GIF width or FPS before reducing its duration.

## Token and usage reporting

Every final response must include a usage block:

- successful image-generation calls;
- failed or cancelled image-generation calls, if any;
- exact input, output/image, and total tokens when the selected tool returns them;
- `unavailable` for each token field the tool does not expose, with a short reason;
- never estimate or invent token counts;
- note that local FFmpeg assembly does not itself call the image-generation model.

## Boundaries

- Describe the GIF as a staged reconstruction from generated drawing phases, not the model's hidden generation history or a recording of a real artist.
- A visible hand physically drawing every stroke is a different video-generation or compositing workflow. Do not promise it unless the required capability or user-provided footage is available.
- Do not preserve or invent readable signage unless the user explicitly requires exact text and the result has been verified.
- Do not remove another artist's signature or watermark without clear authorization.

## Portability

- Preserve the directory structure when copying this skill so relative links and the assembly script continue to work.
- Keep provider credentials and model selection outside this package. Supply them through the host platform or an adapter.
- A host may ignore `agents/openai.yaml`; it contains optional OpenAI/Codex discovery metadata only.
- If FFmpeg is unavailable, deliver the three still stages and explain that local GIF/MP4 assembly was skipped.
- See [docs/portability.md](docs/portability.md) for installation patterns on other hosts.
