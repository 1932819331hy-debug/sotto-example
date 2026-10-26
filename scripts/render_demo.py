"""Render an illustrated, secret-free terminal walkthrough for the README."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
WIDTH, HEIGHT = 1120, 560
BACKGROUND = "#10191d"
TEXT = "#e4ebed"
MUTED = "#a0b0b8"
ACCENT = "#8cdeb7"


def font(size):
    for path in [
        "/System/Library/Fonts/Menlo.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "C:/Windows/Fonts/consola.ttf",
    ]:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size=size)


BODY, SMALL, TITLE = font(21), font(17), font(26)
SCENES = [
    ("01 / Try the program", "Without a secret, the demo explains what is missing.", [
        ("$ python3 python/main.py", TEXT),
        ("DEMO_SECRET is missing or empty.", "#f0b497"),
        ("Set it with `sotto set DEMO_SECRET`, then run this demo", MUTED),
        ("with `sotto run -- <command>`.", MUTED),
    ]),
    ("02 / Initialise locally", "No account. No server. One setup for all nine languages.", [
        ("$ sotto init", TEXT),
        ("[First run: choose and confirm a master password]", MUTED),
        ("[Save your Emergency Kit privately]", MUTED),
        ("initialised `sotto-example` (dev)", ACCENT),
    ]),
    ("03 / Store a demo secret", "Sotto encrypts the value into your local vault.", [
        ("$ sotto set DEMO_SECRET", TEXT),
        ("Value: [hidden input]", MUTED),
        ("set DEMO_SECRET (sotto-example/dev)", ACCENT),
    ]),
    ("04 / Run with Sotto", "The program receives the secret. Its value stays off screen.", [
        ("$ sotto run -- python3 python/main.py", TEXT),
        ("Sotto demo: secret loaded successfully.", ACCENT),
        ("", TEXT),
        ("Same setup. Python + eight more languages.", MUTED),
    ]),
]


def render(index, visible):
    title, caption, lines = SCENES[index]
    canvas = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(canvas)
    draw.text((38, 25), "sotto / local secret demo", font=SMALL, fill=MUTED)
    draw.text((38, 83), title, font=TITLE, fill=TEXT)
    draw.text((38, 130), caption, font=SMALL, fill=MUTED)
    draw.rounded_rectangle((28, 185, WIDTH - 28, 443), radius=12, fill="#18262c", outline="#30434c")
    for row, (line, color) in enumerate(lines[:visible]):
        draw.text((48, 214 + row * 42), line, font=BODY, fill=color)
    for step in range(4):
        x = 38 + step * 264
        draw.rounded_rectangle((x, 477, x + 244, 481), radius=2, fill=ACCENT if step <= index else "#30434c")
    draw.text((38, 510), "Illustrated walkthrough / setup prompts summarised", font=SMALL, fill=MUTED)
    return canvas


def main():
    frames, durations = [], []
    for index, (_, _, lines) in enumerate(SCENES):
        for visible in range(1, len(lines) + 1):
            frames.append(render(index, visible))
            durations.append(700 if visible < len(lines) else 3800)
    output = ROOT / "docs/demo.gif"
    output.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(output, save_all=True, append_images=frames[1:], duration=durations, loop=0, optimize=True)
    print(f"Wrote {output.relative_to(ROOT)} ({output.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
