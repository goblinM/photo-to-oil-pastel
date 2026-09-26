# Portability Guide

This skill is designed as a portable instruction package, not as a plugin tied to one chat product. There is no universal skill installation format across agent products, so each host needs a small integration layer while the creative workflow remains unchanged.

## Portable core

Copy these files and keep their relative paths:

```text
SKILL.md
docs/
references/
scripts/
```

`agents/openai.yaml` is an optional OpenAI/Codex discovery adapter. Other hosts can ignore or replace the entire `agents/` directory without changing the core workflow.

## Integration patterns

### Native skill or instruction-directory host

Copy the whole folder into the host's supported skills or instructions directory and point the host to `SKILL.md`. Configure an image-editing tool that follows [`backend-contract.md`](backend-contract.md).

### Prompt-based agent

Provide `SKILL.md` as the system or task instruction, make `references/prompt-templates.md` available as a referenced resource, and expose file/artifact operations plus an image-editing backend. The agent should invoke `scripts/assemble_step_loop.py` only after all three stage images have passed inspection.

### Workflow engine

Map the process to these nodes:

```text
source inspection
  → finished image edit
  → human/model approval
  → early-stage edit + late-stage edit
  → visual consistency check
  → local assembly script
  → usage report
```

The two unfinished-stage nodes both use the accepted finished image as their reference. They may run in parallel after final-image approval.

### Application or backend service

Implement the operation in [`backend-contract.md`](backend-contract.md), then orchestrate the file names and stage order defined in `SKILL.md`. Keep provider-specific code, endpoints, and credentials outside this package.

## Capability fallback

- No image-editing backend: return the paintability analysis and three subject-adapted prompts only.
- Image backend but no visual inspection capability: require human approval after each generated stage.
- No FFmpeg or Python: deliver the three still images; do not claim a GIF or MP4 was created.
- No token metadata: report each token field as `unavailable` and state that the backend did not expose it.

## Porting checklist

- The host can read a user-provided reference image.
- The host can save or retain generated raster artifacts.
- The image backend accepts both a reference image and a text instruction.
- The host can preserve the three-stage file order and inspect visual consistency.
- Python 3.9+, FFmpeg, and FFprobe are available if GIF/MP4 output is required.
- Credentials are injected by the host and are absent from the copied package.
- Usage metadata is passed through exactly when available and never estimated.

## Generic invocation

```text
Use the photo-to-oil-pastel instructions on <source image>. First produce a paintability plan, then create the finished oil-pastel image and two genuine unfinished stages through the configured image-editing backend. After visual verification, assemble a 6-second looping GIF and report exact model usage when the backend exposes it.
```
