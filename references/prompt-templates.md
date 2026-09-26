# Prompt Templates

Adapt these templates to the inspected photo. Keep only details that matter for the actual subject.

## Finished paintable artwork

```text
Use case: style-transfer
Asset type: a genuinely paintable oil-pastel artwork for a short process loop
Input image: edit target; preserve <identity/composition/perspective/main anchors>
Primary request: simplify this photograph into a handmade oil-pastel drawing that a beginner-to-intermediate artist could realistically complete on textured warm ivory paper
Subject hierarchy: <primary subject>; <secondary anchor>; turn the remaining background into quiet shapes
Style/medium: real oil pastel or oil stick, broad blunt strokes, limited layering, visible paper gaps, uneven pressure, broken edges, occasional overlapping colors
Composition: preserve <essential framing>; remove or simplify <clutter, signs, people, tiny objects>
Color palette: limit the drawing to <6–10 named practical colors>
Text: keep exact text only when explicitly required; otherwise convert lettering to non-readable marks or simple color rectangles
Constraints: recognizable and hand-drawable; preserve <identity-critical or structure-critical details>
Avoid: photorealism, hyper-detail, smooth airbrush gradients, glossy digital painting, perfect vector edges, cinematic glow, added objects, watermark, signature, frame
```

## Early block-in

```text
Edit the referenced finished oil-pastel artwork into an EARLY BLOCK-IN STAGE of the exact same drawing. Lock the crop, perspective, subject scale, main silhouettes, and the placement of <major anchors>. Show warm textured paper with broad incomplete color masses using the same limited palette. Leave substantial paper gaps. Use blunt uneven oil-pastel strokes with visible pressure changes. Keep only the simplest contour or facial marks. Remove tiny texture, lettering, jewelry or object detail, sharp highlights, and polish. This must look like a real halfway-finished oil-pastel block-in, not a blurred, faded, pixelated, or digitally filtered final image. No labels, grid, added objects, watermark, or tools outside the artwork.
```

## Late intermediate

```text
Edit the referenced finished oil-pastel artwork into a LATE INTERMEDIATE STAGE of the exact same drawing. Lock the crop, perspective, subject scale, main silhouettes, and the placement of <major anchors>. All broad colors are already filled. Add major shadows, second-layer colors, and the most important subject details, but omit the smallest texture marks, readable lettering, sharp highlights, and final edge cleanup. Preserve visible paper grain, uneven pressure, broken edges, and obvious oil-pastel layering. It must look like a real artwork about 75 percent complete, not a blurred, faded, pixelated, or digitally filtered final image. No labels, grid, added objects, watermark, or tools outside the artwork.
```

## Correction prompts

Use one focused correction only. Examples:

- Preserve the exact face, hand pose, subject scale, and crop; simplify only the background.
- Keep the accepted composition unchanged; replace smooth digital shading with broad broken oil-pastel strokes and visible paper gaps.
- Keep every major branch and building boundary fixed; reduce only the blossom detail and final highlights.
