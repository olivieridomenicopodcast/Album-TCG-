from PIL import Image, ImageDraw, ImageFilter
import math

def rounded_rect(draw, box, radius, fill):
    draw.rounded_rectangle(box, radius=radius, fill=fill)

def make_icon(size, path):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    pad = int(size * 0.06)
    box = [pad, pad, size - pad, size - pad]
    r = int(size * 0.14)

    # Leather cover background with subtle vertical gradient
    grad = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grad)
    top = (42, 29, 20, 255)     # #2a1d14
    bottom = (24, 16, 11, 255)  # darker
    for y in range(size):
        t = y / size
        c = tuple(int(top[i] + (bottom[i]-top[i])*t) for i in range(4))
        gd.line([(0, y), (size, y)], fill=c)

    mask = Image.new("L", (size, size), 0)
    md = ImageDraw.Draw(mask)
    rounded_rect(md, box, r, 255)
    img.paste(grad, (0, 0), mask)

    d = ImageDraw.Draw(img)

    # subtle border
    d.rounded_rectangle(box, radius=r, outline=(15, 10, 7, 255), width=max(2, size//128))

    # Binder rings on the left (3 brass rings)
    ring_x = int(size * 0.235)
    ring_positions = [0.32, 0.5, 0.68]
    ring_r = int(size * 0.052)
    brass = (201, 162, 75, 255)
    brass_dark = (140, 108, 45, 255)
    for py in ring_positions:
        cy = int(size * py)
        d.ellipse([ring_x - ring_r, cy - ring_r, ring_x + ring_r, cy + ring_r],
                   fill=brass_dark)
        inner = int(ring_r * 0.62)
        d.ellipse([ring_x - inner, cy - inner, ring_x + inner, cy + inner],
                   fill=(24, 16, 11, 255))
        d.ellipse([ring_x - inner + 2, cy - inner + 2, ring_x + inner - 2, cy + inner - 2],
                   outline=brass, width=max(1, size//180))

    # Card/sleeve on the right side, slightly tilted feel via offset rect + highlight
    card_left = int(size * 0.42)
    card_right = int(size * 0.86)
    card_top = int(size * 0.28)
    card_bottom = int(size * 0.82)
    card_r = int(size * 0.05)

    d.rounded_rectangle([card_left, card_top, card_right, card_bottom],
                         radius=card_r, fill=(232, 220, 192, 255),
                         outline=(15, 10, 7, 255), width=max(2, size//160))

    # inner card frame (like a TCG card border)
    inset = int(size * 0.035)
    d.rounded_rectangle(
        [card_left + inset, card_top + inset, card_right - inset, card_bottom - inset],
        radius=int(card_r*0.6), outline=brass, width=max(2, size//140)
    )

    # star / gem centered in the card
    cx = (card_left + card_right) // 2
    cy = (card_top + card_bottom) // 2 + int(size*0.01)
    star_r_out = int(size * 0.11)
    star_r_in = int(star_r_out * 0.45)
    points = []
    for i in range(10):
        ang = -math.pi/2 + i * math.pi / 5
        rr = star_r_out if i % 2 == 0 else star_r_in
        points.append((cx + rr*math.cos(ang), cy + rr*math.sin(ang)))
    d.polygon(points, fill=(140, 30, 30, 255), outline=(90, 18, 18, 255))

    # plastic sleeve gloss diagonal highlight over whole card
    gloss = Image.new("RGBA", (size, size), (0,0,0,0))
    gd = ImageDraw.Draw(gloss)
    gd.polygon([
        (card_left, card_top),
        (card_left + int((card_right-card_left)*0.45), card_top),
        (card_left, card_top + int((card_bottom-card_top)*0.55)),
    ], fill=(255,255,255,40))
    img = Image.alpha_composite(img, gloss)

    img.save(path, "PNG")

make_icon(192, "/home/claude/binder/icon-192.png")
make_icon(512, "/home/claude/binder/icon-512.png")
print("done")
