# Image Backend Contract

This contract keeps the skill independent of any image-model vendor. A host adapter may call a local model, a remote API, a native agent tool, or a workflow node, provided it exposes the behavior below.

## Required operation

Conceptual interface:

```text
edit_image(reference_image, prompt, output_path, options?) -> result
```

Required inputs:

- `reference_image`: readable local path, uploaded asset, or resolvable artifact URI.
- `prompt`: the subject-adapted instruction from `references/prompt-templates.md`.
- `output_path`: requested raster output location or artifact name.

Optional inputs:

- target width and height;
- output format, preferably PNG;
- seed or consistency controls;
- protected-region mask, identity-reference crop, or regional reference-strength controls;
- negative prompt or provider-specific safety options.

Required result:

- one raster image as a file path or resolvable artifact URI;
- explicit success or failure state;
- an error message on failure.

Optional result metadata:

- provider and model name;
- request ID;
- exact input, output/image, and total token usage;
- generation time and seed.

## Stage sequence

The adapter must run three separate edits in this order:

1. source photo → finished oil-pastel artwork;
2. accepted finished artwork → early block-in;
3. accepted finished artwork → late intermediate.

Do not derive the unfinished stages from the source photograph, and do not request all stages as a contact sheet. The host must inspect and accept the finished image before using it as the reference for stages 2 and 3.

## Conceptual request

```json
{
  "operation": "edit_image",
  "reference_image": "01-source.png",
  "prompt": "<adapted finished-art prompt>",
  "output_path": "02-final-oil-pastel.png",
  "options": {
    "format": "png",
    "preserve_composition": true
  }
}
```

## Conceptual response

```json
{
  "status": "success",
  "image": "02-final-oil-pastel.png",
  "usage": {
    "input_tokens": null,
    "output_tokens": null,
    "total_tokens": null,
    "reason_unavailable": "Provider did not expose token usage"
  }
}
```

`null` means unavailable, never zero. Do not estimate missing usage.

## Adapter responsibilities

- Resolve authentication outside the skill directory.
- Normalize provider output into a readable raster artifact.
- Preserve the requested crop and composition when the provider supports controls for them.
- Pass the feature-lock card unchanged to every relevant stage request; use regional protection controls for small identity-critical faces when available.
- Record failed and cancelled attempts for the final usage report.
- Never silently substitute text-to-image generation when reference-image editing is required.
