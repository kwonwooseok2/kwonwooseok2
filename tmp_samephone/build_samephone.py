#!/usr/bin/env python3
"""Build ONE black iPhone 17 Pro Max shell, paste 2 screens into identical rect.

Method:
  1) Draw upright chassis once (fixed screen_rect)
  2) Paste each UI into that same rect (pixel-aligned)
  3) Apply identical 3D perspective (좌상→우하 vibe)
  4) Transparent nukki PNG — no rembg
"""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ASSETS = Path("/home/ubuntu/.cursor/projects/workspace/assets")
OUT_DIR = Path("/opt/cursor/artifacts/assets")
WORK = Path("/workspace/tmp_samephone")

DARK_UI = ASSETS / "ba56e623-3716-4610-8a6b-962a6a12c7e0.png"
LIGHT_UI = ASSETS / "eff52c26-ddf6-4acf-a998-df07fdc7d056.png"

# High-res upright build (then perspective). Screen content native ~471x1024.
SCREEN_W = 942  # 2× UI width for sharp output
BEZEL = 22
SIDE_THICK = 28  # left metallic edge for 3D depth
PAD = 40


def rounded_mask(size: tuple[int, int], radius: int) -> Image.Image:
    w, h = size
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], radius=radius, fill=255)
    return m


def vertical_metal_gradient(h: int, w: int) -> Image.Image:
    """Subtle brushed metal strip for left side edge."""
    arr = np.zeros((h, w, 4), dtype=np.uint8)
    for x in range(w):
        t = x / max(1, w - 1)
        # darker near body, highlight near outer edge
        base = int(18 + 42 * (1 - t) + 28 * abs(0.55 - t))
        hi = int(min(255, base + 55 * (1 - abs(0.25 - t) * 2)))
        arr[:, x, 0] = hi
        arr[:, x, 1] = hi
        arr[:, x, 2] = min(255, hi + 4)
        arr[:, x, 3] = 255
    # soft horizontal brush noise
    noise = np.random.default_rng(7).integers(-6, 7, size=(h, 1, 1), dtype=np.int16)
    rgb = arr[:, :, :3].astype(np.int16) + noise
    arr[:, :, :3] = np.clip(rgb, 0, 255).astype(np.uint8)
    return Image.fromarray(arr, "RGBA")


def build_shell(screen_size: tuple[int, int]) -> tuple[Image.Image, tuple[int, int, int, int]]:
    """Return upright phone chassis (blank black screen) + screen_rect (l,t,r,b)."""
    sw, sh = screen_size
    outer_r = max(64, sw // 10)
    screen_r = max(48, sw // 14)

    canvas_w = SIDE_THICK + BEZEL * 2 + sw + BEZEL + PAD * 2
    canvas_h = BEZEL * 2 + sh + PAD * 2

    phone = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(phone)

    # Outer body rect (front face)
    ox0 = PAD + SIDE_THICK
    oy0 = PAD
    ox1 = PAD + SIDE_THICK + BEZEL * 2 + sw
    oy1 = PAD + BEZEL * 2 + sh

    body = (14, 14, 16, 255)
    rim = (62, 62, 68, 255)
    rim_hi = (110, 110, 118, 255)
    btn = (38, 38, 42, 255)

    # Left side thickness (3D edge) — parallelogram-ish strip before front face
    side = vertical_metal_gradient(oy1 - oy0 + 1, SIDE_THICK + 2)
    # taper top/bottom of side with rounded mask aligned to body
    side_mask = Image.new("L", side.size, 0)
    sd = ImageDraw.Draw(side_mask)
    # slightly inset so side sits behind front curve
    sd.rounded_rectangle(
        [0, 6, side.size[0] - 1, side.size[1] - 7],
        radius=outer_r // 3,
        fill=255,
    )
    phone.paste(side, (ox0 - SIDE_THICK + 2, oy0), side_mask)

    # Front chassis
    draw.rounded_rectangle([ox0, oy0, ox1, oy1], radius=outer_r, fill=body)
    # Metallic rim highlight (inset stroke)
    draw.rounded_rectangle(
        [ox0 + 1, oy0 + 1, ox1 - 1, oy1 - 1],
        radius=max(1, outer_r - 1),
        outline=rim_hi,
        width=2,
    )
    draw.rounded_rectangle(
        [ox0 + 3, oy0 + 3, ox1 - 3, oy1 - 3],
        radius=max(1, outer_r - 3),
        outline=rim,
        width=1,
    )

    # Side buttons on left thickness / front junction
    btn_x0 = ox0 - SIDE_THICK + 6
    btn_x1 = ox0 + 1
    ay0 = oy0 + int((oy1 - oy0) * 0.17)
    ah = max(22, int(sh * 0.032))
    draw.rounded_rectangle([btn_x0, ay0, btn_x1, ay0 + ah], radius=4, fill=btn)
    vy0 = oy0 + int((oy1 - oy0) * 0.24)
    vh = int(sh * 0.065)
    gap = int(sh * 0.018)
    draw.rounded_rectangle([btn_x0, vy0, btn_x1, vy0 + vh], radius=4, fill=btn)
    draw.rounded_rectangle(
        [btn_x0, vy0 + vh + gap, btn_x1, vy0 + 2 * vh + gap], radius=4, fill=btn
    )
    # Power button right
    rx0 = ox1 - 1
    rx1 = ox1 + 12
    py0 = oy0 + int((oy1 - oy0) * 0.28)
    ph = int(sh * 0.095)
    draw.rounded_rectangle([rx0, py0, rx1, py0 + ph], radius=4, fill=btn)

    # Screen well (black)
    sx0 = ox0 + BEZEL
    sy0 = oy0 + BEZEL
    sx1 = sx0 + sw
    sy1 = sy0 + sh
    draw.rounded_rectangle(
        [sx0 - 1, sy0 - 1, sx1, sy1], radius=screen_r, fill=(0, 0, 0, 255)
    )

    screen_rect = (sx0, sy0, sx1, sy1)

    # Soft specular on left rim of front face
    gloss = Image.new("RGBA", phone.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(gloss)
    gd.rounded_rectangle(
        [ox0 + 2, oy0 + 8, ox0 + 7, oy1 - 8],
        radius=3,
        fill=(180, 180, 190, 55),
    )
    phone = Image.alpha_composite(phone, gloss)

    # Store chassis alpha for clean nukki (body + side + buttons)
    # Keep as drawn; transparent outside already.

    # Attach metadata as custom attrs via return
    shell_meta = {
        "outer": (ox0, oy0, ox1, oy1),
        "outer_r": outer_r,
        "screen_r": screen_r,
        "di": None,  # filled by paste
    }
    phone.info["meta"] = shell_meta  # type: ignore[assignment]
    return phone, screen_rect


def paste_screen(
    shell: Image.Image,
    screen_rect: tuple[int, int, int, int],
    ui: Image.Image,
    screen_r: int,
) -> Image.Image:
    """Paste UI into fixed screen_rect (pixel-aligned). Same geometry every time."""
    out = shell.copy()
    sx0, sy0, sx1, sy1 = screen_rect
    sw, sh = sx1 - sx0, sy1 - sy0

    ui = ui.convert("RGBA").resize((sw, sh), Image.Resampling.LANCZOS)
    # Flatten onto black so any UI transparency becomes bezel-safe black
    flat = Image.new("RGBA", (sw, sh), (0, 0, 0, 255))
    flat = Image.alpha_composite(flat, ui)

    mask = rounded_mask((sw, sh), max(8, screen_r - 6))
    # Slight inset so UI never spills onto bezel
    inset = 2
    if inset > 0:
        inner = rounded_mask((sw - inset * 2, sh - inset * 2), max(6, screen_r - 8))
        mask2 = Image.new("L", (sw, sh), 0)
        mask2.paste(inner, (inset, inset))
        mask = mask2

    out.paste(flat, (sx0, sy0), mask)

    # Dynamic Island on top of UI (same position both variants)
    draw = ImageDraw.Draw(out)
    di_w = int(sw * 0.30)
    di_h = max(30, int(sw * 0.072))
    di_x = sx0 + (sw - di_w) // 2
    di_y = sy0 + max(16, int(sh * 0.016))
    draw.rounded_rectangle(
        [di_x, di_y, di_x + di_w, di_y + di_h],
        radius=di_h // 2,
        fill=(0, 0, 0, 255),
    )
    return out


def apply_perspective(im: Image.Image) -> Image.Image:
    """좌상→우하 3D angle: top-left closer, left edge visible, mild foreshortening."""
    arr = np.array(im)
    h, w = arr.shape[:2]

    # Source corners of content bbox
    a = arr[:, :, 3]
    ys, xs = np.where(a > 8)
    if len(xs) == 0:
        return im
    l, t, r, b = int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())
    src = np.float32(
        [
            [l, t],  # TL
            [r, t],  # TR
            [r, b],  # BR
            [l, b],  # BL
        ]
    )

    bw, bh = r - l, b - t
    # Destination: tilt clockwise-ish (~-12° vibe) with perspective
    # TL pulled up-left (closer), BR pushed down-right (farther)
    # Slight horizontal shear so left edge reads in depth
    out_w = int(bw * 1.18)
    out_h = int(bh * 1.06)
    margin = 48
    canvas_w = out_w + margin * 2
    canvas_h = out_h + margin * 2

    # Match style-ref proportions: top narrower than bottom, shifted right as y increases
    top_inset_l = int(bw * 0.02)
    top_inset_r = int(bw * 0.18)
    bot_inset_l = int(bw * 0.10)
    bot_inset_r = int(bw * 0.02)
    top_y = margin + int(bh * 0.01)
    bot_y = margin + out_h - int(bh * 0.01)
    # Shift top to the left relative to bottom (좌상→우하 diagonal)
    x_shift = int(bw * 0.12)

    dst = np.float32(
        [
            [margin + top_inset_l + x_shift * 0.15, top_y],  # TL
            [margin + out_w - top_inset_r + x_shift * 0.15, top_y + int(bh * 0.045)],  # TR lower
            [margin + out_w - bot_inset_r + x_shift, bot_y],  # BR
            [margin + bot_inset_l + x_shift, bot_y - int(bh * 0.01)],  # BL
        ]
    )

    M = cv2.getPerspectiveTransform(src, dst)
    warped = cv2.warpPerspective(
        arr,
        M,
        (canvas_w, canvas_h),
        flags=cv2.INTER_LANCZOS4,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(0, 0, 0, 0),
    )
    # Clean near-zero alpha dust (keep AA, no rembg)
    a2 = warped[:, :, 3]
    warped[a2 < 6] = 0
    return Image.fromarray(warped, "RGBA")


def trim_transparent(im: Image.Image, pad: int = 10) -> Image.Image:
    arr = np.array(im)
    ys, xs = np.where(arr[:, :, 3] > 0)
    if len(xs) == 0:
        return im
    l, t, r, b = int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())
    l = max(0, l - pad)
    t = max(0, t - pad)
    r = min(im.width - 1, r + pad)
    b = min(im.height - 1, b + pad)
    return im.crop((l, t, r + 1, b + 1))


def soft_shadow(im: Image.Image) -> Image.Image:
    """Very subtle contact shadow under phone — still nukki-friendly (no hard plate)."""
    # Skip separate shadow plate; keep pure transparent nukki per request.
    return im


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    dark_ui = Image.open(DARK_UI)
    light_ui = Image.open(LIGHT_UI)
    assert dark_ui.size == light_ui.size

    sw = SCREEN_W
    sh = int(round(dark_ui.height * (sw / dark_ui.width)))
    screen_size = (sw, sh)

    shell, screen_rect = build_shell(screen_size)
    screen_r = max(48, sw // 14)

    # Persist shell once for debug / reuse
    shell.save(WORK / "shell_upright_blank.png", "PNG")
    print("shell", shell.size, "screen_rect", screen_rect)

    outputs = [
        ("dark", dark_ui, OUT_DIR / "pair-samephone-dark.png"),
        ("light", light_ui, OUT_DIR / "pair-samephone-light.png"),
    ]

    sizes = []
    alphas = []
    for name, ui, dest in outputs:
        composed = paste_screen(shell, screen_rect, ui, screen_r)
        composed.save(WORK / f"upright_{name}.png", "PNG")
        angled = apply_perspective(composed)
        angled = trim_transparent(angled, pad=12)
        angled = soft_shadow(angled)
        angled.save(dest, "PNG", optimize=True)
        arr = np.array(angled)
        sizes.append(angled.size)
        alphas.append(arr[:, :, 3].copy())
        corners = [
            int(arr[0, 0, 3]),
            int(arr[0, -1, 3]),
            int(arr[-1, 0, 3]),
            int(arr[-1, -1, 3]),
        ]
        print(
            name,
            dest,
            angled.size,
            "bytes",
            dest.stat().st_size,
            "corners_a",
            corners,
        )

    # Identity checks: same silhouette / frame
    assert sizes[0] == sizes[1], sizes
    assert np.array_equal(alphas[0] > 0, alphas[1] > 0) or (
        np.mean((alphas[0] > 0) != (alphas[1] > 0)) < 0.002
    ), "silhouette mismatch"
    # Alpha should be nearly identical (same shell + same warp)
    a_diff = np.abs(alphas[0].astype(np.int16) - alphas[1].astype(np.int16))
    print("alpha mean abs diff", float(a_diff.mean()), "max", int(a_diff.max()))
    assert a_diff.mean() < 2.0, "frame/lighting alpha diverged"

    # Diff should concentrate in screen RGB only
    d = np.array(Image.open(OUT_DIR / "pair-samephone-dark.png"))
    l = np.array(Image.open(OUT_DIR / "pair-samephone-light.png"))
    rgb_diff = np.abs(d[:, :, :3].astype(int) - l[:, :, :3].astype(int)).sum(axis=2)
    print(
        "rgb diff mean (opaque)",
        float(rgb_diff[d[:, :, 3] > 200].mean()),
    )


if __name__ == "__main__":
    main()
