#!/usr/bin/env python3
"""Assemble three oil-pastel stages into a short MP4 or looping GIF."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Assemble early, middle, and final drawing stages without digital reveal effects."
    )
    parser.add_argument("--early", type=Path, required=True)
    parser.add_argument("--middle", type=Path, required=True)
    parser.add_argument("--final", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True, help="Output .gif or .mp4")
    parser.add_argument("--keep-master", type=Path, help="Optional MP4 copy when output is GIF")
    parser.add_argument("--duration", type=float, default=6.0, help="Total duration, 5–10 seconds")
    parser.add_argument("--fps", type=int, default=10, help="6–20 FPS")
    parser.add_argument("--width", type=int, default=540, help="Output width, 240–1080")
    parser.add_argument("--force", action="store_true", help="Overwrite existing outputs")
    return parser.parse_args()


def require_program(name: str) -> None:
    if shutil.which(name) is None:
        raise SystemExit(f"Required program not found: {name}")


def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def image_size(path: Path) -> tuple[int, int]:
    result = subprocess.run(
        [
            "ffprobe", "-v", "error", "-select_streams", "v:0",
            "-show_entries", "stream=width,height", "-of", "json", str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    stream = json.loads(result.stdout)["streams"][0]
    return int(stream["width"]), int(stream["height"])


def build_master(
    early: Path,
    middle: Path,
    final: Path,
    output: Path,
    duration: float,
    fps: int,
    width: int,
    height: int,
) -> None:
    early_seconds = duration * 0.27
    middle_seconds = duration * 0.27
    final_seconds = duration - early_seconds - middle_seconds
    scale_pad = (
        f"scale={width}:{height}:force_original_aspect_ratio=decrease:flags=lanczos,"
        f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=0xf3e8d2,setsar=1"
    )
    filter_graph = (
        f"[0:v]{scale_pad}[v0];"
        f"[1:v]{scale_pad}[v1];"
        f"[2:v]{scale_pad}[v2];"
        f"[v0][v1][v2]concat=n=3:v=1:a=0,fps={fps},format=yuv420p[out]"
    )
    run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-loop", "1", "-framerate", str(fps), "-t", f"{early_seconds:.3f}", "-i", str(early),
            "-loop", "1", "-framerate", str(fps), "-t", f"{middle_seconds:.3f}", "-i", str(middle),
            "-loop", "1", "-framerate", str(fps), "-t", f"{final_seconds:.3f}", "-i", str(final),
            "-filter_complex", filter_graph,
            "-map", "[out]", "-an", "-c:v", "libx264", "-crf", "18",
            "-preset", "medium", "-movflags", "+faststart", str(output),
        ]
    )


def make_gif(master: Path, output: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="oil-pastel-loop-") as temp_dir:
        palette = Path(temp_dir) / "palette.png"
        run(
            [
                "ffmpeg", "-y", "-v", "error", "-i", str(master),
                "-vf", "palettegen=stats_mode=diff", str(palette),
            ]
        )
        run(
            [
                "ffmpeg", "-y", "-v", "error", "-i", str(master), "-i", str(palette),
                "-lavfi", "paletteuse=dither=sierra2_4a", "-loop", "0", str(output),
            ]
        )


def main() -> None:
    args = parse_args()
    require_program("ffmpeg")
    require_program("ffprobe")

    for path in (args.early, args.middle, args.final):
        if not path.is_file():
            raise SystemExit(f"Input image not found: {path}")
    if not 5.0 <= args.duration <= 10.0:
        raise SystemExit("--duration must be between 5 and 10 seconds")
    if not 6 <= args.fps <= 20:
        raise SystemExit("--fps must be between 6 and 20")
    if not 240 <= args.width <= 1080:
        raise SystemExit("--width must be between 240 and 1080")
    if args.output.suffix.lower() not in {".gif", ".mp4"}:
        raise SystemExit("--output must end in .gif or .mp4")

    targets = [args.output] + ([args.keep_master] if args.keep_master else [])
    for target in targets:
        if target and target.exists() and not args.force:
            raise SystemExit(f"Output already exists; pass --force to replace it: {target}")
        if target:
            target.parent.mkdir(parents=True, exist_ok=True)

    source_width, source_height = image_size(args.final)
    height = round(args.width * source_height / source_width)
    height += height % 2

    if args.output.suffix.lower() == ".mp4":
        build_master(
            args.early, args.middle, args.final, args.output,
            args.duration, args.fps, args.width, height,
        )
        master_path = args.output
    else:
        with tempfile.TemporaryDirectory(prefix="oil-pastel-master-") as temp_dir:
            master_path = Path(temp_dir) / "master.mp4"
            build_master(
                args.early, args.middle, args.final, master_path,
                args.duration, args.fps, args.width, height,
            )
            make_gif(master_path, args.output)
            if args.keep_master:
                shutil.copy2(master_path, args.keep_master)

    report = {
        "output": str(args.output.resolve()),
        "master": str(args.keep_master.resolve()) if args.keep_master else (
            str(master_path.resolve()) if args.output.suffix.lower() == ".mp4" else None
        ),
        "duration_seconds": args.duration,
        "fps": args.fps,
        "width": args.width,
        "height": height,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        print(f"Media command failed with exit code {exc.returncode}", file=sys.stderr)
        raise SystemExit(1) from exc
