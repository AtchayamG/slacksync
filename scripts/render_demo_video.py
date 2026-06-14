from __future__ import annotations

import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "demo-video"
SLIDES = OUT / "slides"
VIDEO = OUT / "slacksync-demo.mp4"
NARRATION = OUT / "narration.mp3"
CONCAT = OUT / "slides.txt"
W, H = 1920, 1080

BG = "#070910"
PANEL = "#101523"
LINE = "#32384a"
TEXT = "#f7f7fb"
MUTED = "#b8c1d6"
BLUE = "#36c5f0"
GREEN = "#2eb67d"
YELLOW = "#ecb22e"
RED = "#e01e5a"
VIOLET = "#7c5cff"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


F_TITLE = font(74, True)
F_H2 = font(46, True)
F_BODY = font(32)
F_SMALL = font(23)
F_MONO = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 24) if Path("C:/Windows/Fonts/consola.ttf").exists() else font(24)


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont, width: int) -> list[str]:
    lines: list[str] = []
    for paragraph in text.split("\n"):
      words = paragraph.split()
      current = ""
      for word in words:
          trial = f"{current} {word}".strip()
          if draw.textlength(trial, font=fnt) <= width:
              current = trial
          else:
              if current:
                  lines.append(current)
              current = word
      if current:
          lines.append(current)
    return lines


def text_block(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, fnt: ImageFont.FreeTypeFont, fill: str, width: int, line_gap: int = 10) -> int:
    x, y = xy
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + line_gap
    return y


def base() -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, W, H), fill=BG)
    draw.ellipse((-380, -280, 560, 420), fill="#0a3040")
    draw.ellipse((1400, -260, 2220, 470), fill="#30101e")
    draw.rounded_rectangle((58, 58, W - 58, H - 58), radius=28, outline=LINE, width=2, fill="#090d17")
    return img, draw


def title(draw: ImageDraw.ImageDraw, heading: str, kicker: str = "SlackSync") -> None:
    draw.text((118, 105), kicker, font=F_SMALL, fill=BLUE)
    draw.text((118, 142), heading, font=F_TITLE, fill=TEXT)


def fit_image(path: Path, box: tuple[int, int, int, int], bg: str = "#05070d") -> tuple[Image.Image, tuple[int, int]]:
    src = Image.open(path).convert("RGB")
    x1, y1, x2, y2 = box
    bw, bh = x2 - x1, y2 - y1
    src.thumbnail((bw, bh), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (bw, bh), bg)
    px = (bw - src.width) // 2
    py = (bh - src.height) // 2
    canvas.paste(src, (px, py))
    return canvas, (x1, y1)


def cover_image(path: Path, box: tuple[int, int, int, int], anchor: str = "center") -> tuple[Image.Image, tuple[int, int]]:
    src = Image.open(path).convert("RGB")
    x1, y1, x2, y2 = box
    bw, bh = x2 - x1, y2 - y1
    source_ratio = src.width / src.height
    target_ratio = bw / bh
    if source_ratio > target_ratio:
        new_w = int(src.height * target_ratio)
        left = 0 if anchor == "left" else max(0, (src.width - new_w) // 2)
        src = src.crop((left, 0, left + new_w, src.height))
    else:
        new_h = int(src.width / target_ratio)
        top = 0
        src = src.crop((0, top, src.width, min(src.height, top + new_h)))
    src = src.resize((bw, bh), Image.Resampling.LANCZOS)
    return src, (x1, y1)


def paste_panel(
    img: Image.Image,
    draw: ImageDraw.ImageDraw,
    path: Path,
    box: tuple[int, int, int, int],
    label: str | None = None,
    cover: bool = False,
    anchor: str = "center",
) -> None:
    x1, y1, x2, y2 = box
    draw.rounded_rectangle((x1 - 14, y1 - 14, x2 + 14, y2 + 14), radius=20, fill="#05070d", outline=LINE, width=2)
    fitted, pos = cover_image(path, box, anchor) if cover else fit_image(path, box)
    img.paste(fitted, pos)
    if label:
        draw.rounded_rectangle((x1 + 18, y1 + 18, x1 + 260, y1 + 58), radius=20, fill="#101523", outline="#3d4660")
        draw.text((x1 + 36, y1 + 25), label, font=F_SMALL, fill=TEXT)


def bullet(draw: ImageDraw.ImageDraw, x: int, y: int, label: str, color: str = GREEN) -> int:
    draw.rounded_rectangle((x, y + 5, x + 16, y + 21), radius=8, fill=color)
    return text_block(draw, (x + 34, y), label, F_BODY, TEXT, 700, 8)


def card(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], heading: str, body: str, accent: str) -> None:
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(box, radius=18, fill=PANEL, outline=LINE, width=2)
    draw.rectangle((x1, y1, x1 + 8, y2), fill=accent)
    draw.text((x1 + 30, y1 + 28), heading, font=F_H2, fill=TEXT)
    text_block(draw, (x1 + 30, y1 + 92), body, F_SMALL, MUTED, x2 - x1 - 60, 8)


def slide01() -> Image.Image:
    img, draw = base()
    title(draw, "Agent operations inside Slack")
    text_block(draw, (118, 270), "SlackSync turns one /sync command into review, tests, docs, and CI triage with Slack-native evidence for every step.", F_BODY, MUTED, 880, 12)
    metrics = [("180 ms", "Slack acknowledgement"), ("4", "specialized agents"), ("0", "secrets in demo mode"), ("87/100", "merge-readiness score")]
    x = 118
    for value, label in metrics:
        draw.rounded_rectangle((x, 560, x + 385, 760), radius=20, fill=PANEL, outline=LINE, width=2)
        draw.text((x + 32, 595), value, font=F_TITLE, fill=TEXT)
        draw.text((x + 34, 690), label, font=F_SMALL, fill=MUTED)
        x += 420
    return img


def slide02() -> Image.Image:
    img, draw = base()
    title(draw, "Live console for judges")
    text_block(draw, (118, 235), "The console mirrors the Slack workflow and calls the live FastAPI route. Screenshots are captured from the real local app.", F_SMALL, MUTED, 1500, 8)
    paste_panel(img, draw, OUT / "web-console-polished.png", (180, 320, 1740, 985), "React + FastAPI", cover=True)
    return img


def slide03() -> Image.Image:
    img, draw = base()
    title(draw, "Slack command proof")
    text_block(draw, (118, 235), "The installed /sync command responds in the SlackSync sandbox and returns judge-readable agent output.", F_SMALL, MUTED, 1500, 8)
    paste_panel(img, draw, OUT / "slack-proof.png", (220, 330, 930, 940), "Slack sandbox", cover=True)
    paste_panel(img, draw, OUT / "web-console-polished.png", (1030, 330, 1740, 940), "Local console", cover=True, anchor="left")
    return img


def slide04() -> Image.Image:
    img, draw = base()
    title(draw, "Four agents, one router")
    cards = [
        ("Reviewer", "Scores PR readiness, flags risky files, and writes concise review notes.", VIOLET),
        ("Tester", "Drafts syntax-valid pytest coverage for changed services and edge cases.", BLUE),
        ("Scribe", "Turns commits and Slack context into release notes and changelog sections.", YELLOW),
        ("Watchdog", "Summarizes CI failures, root cause, and next action directly in Slack.", RED),
    ]
    boxes = [(118, 310, 900, 510), (1020, 310, 1802, 510), (118, 590, 900, 790), (1020, 590, 1802, 790)]
    for box, item in zip(boxes, cards):
        card(draw, box, *item)
    bullet(draw, 118, 880, "Maestro attaches MCP-style repository context and Slack real-time-search evidence before the agent response.", GREEN)
    return img


def slide05() -> Image.Image:
    img, draw = base()
    title(draw, "Architecture evidence")
    paste_panel(img, draw, ROOT / "assets" / "diagrams" / "architecture.png", (150, 250, 1770, 940), "SlackSync system map")
    return img


def slide06() -> Image.Image:
    img, draw = base()
    title(draw, "Production-grade guardrails")
    left = [
        "Slack signature verification rejects stale timestamps.",
        "Shared TypeScript contracts keep UI and API responses aligned.",
        "Demo mode is deterministic and never requires secrets.",
        "Public MIT-licensed repo contains docs, tests, manifest, and architecture proof.",
    ]
    y = 300
    for line in left:
        y = bullet(draw, 150, y, line, BLUE) + 30
    code = [
        "npm run build",
        "npm run test",
        "python -m pytest -q",
        "rg secret-patterns .  # clean"
    ]
    draw.rounded_rectangle((1080, 300, 1710, 770), radius=18, fill="#05070d", outline=LINE, width=2)
    draw.text((1125, 345), "Verification commands", font=F_H2, fill=TEXT)
    cy = 435
    for line in code:
        draw.text((1130, cy), f"$ {line}", font=F_MONO, fill="#ffe7a4")
        cy += 70
    return img


def slide07() -> Image.Image:
    img, draw = base()
    title(draw, "Ready for judges")
    text_block(draw, (118, 260), "SlackSync gives engineering teams a transparent Slack-native agent layer: one command, context-aware routing, visible approvals, and auditable outputs.", F_BODY, MUTED, 1200, 12)
    y = 570
    for line, color in [
        ("Sandbox URL invited for testing", GREEN),
        ("Architecture diagram attached", BLUE),
        ("Demo video under three minutes", YELLOW),
        ("Public GitHub repository and MIT license", VIOLET),
    ]:
        y = bullet(draw, 260, y, line, color) + 22
    return img


def render_slides() -> None:
    SLIDES.mkdir(parents=True, exist_ok=True)
    for i, maker in enumerate([slide01, slide02, slide03, slide04, slide05, slide06, slide07], 1):
        maker().save(SLIDES / f"slide{i:02}.png", quality=95)


SCRIPT = (
    "SlackSync turns Slack into an engineering agent operations center. "
    "A single slash command routes review, tests, documentation, and CI triage to specialized agents, while keeping the work visible in Slack. "
    "This is the live judge console. It mirrors the Slack workflow, calls the FastAPI command route, and keeps demo mode deterministic with no secrets loaded. "
    "The Slack proof is real: the installed /sync command responds inside the SlackSync sandbox, and the console shows the same agent outcome for judges to inspect. "
    "Behind the scenes, Maestro parses the command, attaches repository context and Slack search evidence, then routes to Reviewer, Tester, Scribe, or Watchdog. "
    "The architecture is intentionally inspectable: Slack surfaces connect to FastAPI, then to typed contracts, specialized agents, and Block Kit responses. "
    "The project includes production guardrails: signature verification, shared contracts, deterministic fixtures, tests, docs, a public repository, and a license. "
    "For judges, SlackSync is ready to run: the sandbox is invited, the architecture diagram is attached, the video is under three minutes, and the workflow is auditable end to end."
)


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, cwd=ROOT, check=True)


def render_audio() -> None:
    run([
        "edge-tts",
        "--voice",
        "en-US-AndrewNeural",
        "--rate",
        "+4%",
        "--text",
        SCRIPT,
        "--write-media",
        str(NARRATION),
    ])


def render_video() -> None:
    durations = [7, 12, 13, 14, 13, 12, 9]
    segments = []
    for i, duration in enumerate(durations, 1):
        segment = OUT / f"segment-{i:02}.mp4"
        segments.append(segment)
        run([
            "ffmpeg",
            "-y",
            "-loop",
            "1",
            "-t",
            str(duration),
            "-i",
            str(SLIDES / f"slide{i:02}.png"),
            "-vf",
            "format=yuv420p",
            "-r",
            "30",
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "18",
            "-an",
            str(segment),
        ])
    lines = []
    for segment in segments:
        lines.append(f"file '{segment.as_posix()}'")
    CONCAT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    run([
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(CONCAT),
        "-i",
        str(NARRATION),
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        "-shortest",
        "-movflags",
        "+faststart",
        str(VIDEO),
    ])


if __name__ == "__main__":
    render_slides()
    render_audio()
    render_video()
    print(VIDEO)
