"""Draws every image the site ships: logo files, favicon set, team photos,
background texture and the 1200x630 link-preview cards.

Needs Pillow (cloud workspace). Run AFTER editing data.py:
    python3 _build/assets.py && python3 _build/build.py
Sources live in _build/src/ (pulled from the client's deck).
"""
import io, json, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(HERE, "src")
sys.path.insert(0, HERE)
import data as D

OUT = os.path.join(ROOT, "assets")
INK = (12, 12, 11)          # brand near-black (never pure #000)
OFF = (245, 244, 240)       # brand off-white (never pure #fff)

def out(*p):
    path = os.path.join(OUT, *p)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path

def font(name, size):
    return ImageFont.truetype(os.path.join(SRC, f"archivo-{name}.ttf"), size)

# ------------------------------------------------------------------ logo
logo = Image.open(os.path.join(SRC, "logo-white.png")).convert("RGBA")
# the deck logo carries a soft outer glow; cut it so edges are crisp on any ground
_a = logo.split()[3].point(lambda v: 0 if v < 120 else min(255, (v - 120) * 255 // 100))
logo.putalpha(_a)
# rows measured on the deck file: mark 55-823, wordmark 850-1086
mark = logo.crop((0, 55, logo.width, 824))
mark = mark.crop(mark.getbbox())
word = logo.crop((0, 850, logo.width, 1091))
word = word.crop(word.getbbox())
stack = logo.crop(logo.getbbox())

def recolor(img, rgb):
    a = img.split()[3]
    solid = Image.new("RGBA", img.size, rgb + (255,))
    solid.putalpha(a)
    return solid

def fit_w(img, w):
    h = round(img.height * w / img.width)
    return img.resize((w, h), Image.LANCZOS)

# horizontal lockup: mark + wordmark side by side (header / footer)
mh = 400
m2 = mark.resize((round(mark.width * mh / mark.height), mh), Image.LANCZOS)
wh = round(mh * 0.62)
w2 = word.resize((round(word.width * wh / word.height), wh), Image.LANCZOS)
gap = round(mh * 0.16)
horiz = Image.new("RGBA", (m2.width + gap + w2.width, mh), (0, 0, 0, 0))
horiz.alpha_composite(m2, (0, 0))
horiz.alpha_composite(w2, (m2.width + gap, (mh - wh) // 2))

for name, img in [("logo-horizontal", horiz), ("logo-stacked", stack), ("logo-mark", mark)]:
    for tone, rgb in [("light", OFF), ("dark", INK)]:
        im = fit_w(recolor(img, rgb), 1200 if name != "logo-mark" else 800)
        im.save(out("brand", f"{name}-{tone}.png"), optimize=True)
# schema logo: solid background, >=512 wide
sl = Image.new("RGB", (1024, 1024), INK)
s2 = recolor(stack, OFF); s2.thumbnail((760, 760), Image.LANCZOS)
sl.paste(s2, ((1024 - s2.width) // 2, (1024 - s2.height) // 2), s2)
sl.save(out("brand", "logo-schema.png"), optimize=True)

# ------------------------------------------------------------------ favicons
def icon(size, pad=0.16, bg=INK, radius=0.0):
    c = Image.new("RGBA", (size, size), bg + (255,))
    if radius:
        mask = Image.new("L", (size, size), 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, size - 1, size - 1), round(size * radius), fill=255)
        c.putalpha(mask)
    m = recolor(mark, OFF)
    inner = round(size * (1 - 2 * pad))
    m.thumbnail((inner, inner), Image.LANCZOS)
    c.alpha_composite(m, ((size - m.width) // 2, (size - m.height) // 2))
    return c

icon(180, pad=0.18).convert("RGB").save(out("icons", "apple-touch-icon.png"))
icon(192, pad=0.14).save(out("icons", "icon-192.png"))
icon(512, pad=0.14).save(out("icons", "icon-512.png"))
icon(512, pad=0.24).save(out("icons", "maskable-512.png"))      # mark inside the 80% safe zone
icon(32, pad=0.08).save(out("icons", "favicon-32.png"))
icon(16, pad=0.04).save(out("icons", "favicon-16.png"))
big = icon(256, pad=0.08)
big.save(os.path.join(ROOT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])

# vector favicon from the logo geometry (same shapes as the inline SVG mark)
svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="-60 -150 1120 1030">'
       '<rect x="-60" y="-150" width="1120" height="1030" rx="120" fill="#0c0c0b"/>'
       '<g fill="#f5f4f0"><path d="M345 0 L515 0 L170 460 L0 460 Z"/><rect x="0" y="460" width="515" height="145"/>'
       '<path d="M385 0 H515 V718 Q515 730 503 730 H397 Q385 730 385 718 Z"/>'
       '<rect x="555" y="0" width="175" height="110"/><rect x="555" y="165" width="255" height="110"/>'
       '<rect x="555" y="330" width="345" height="110"/><rect x="555" y="495" width="445" height="110"/></g></svg>')
open(out("icons", "favicon.svg"), "w").write(svg)

manifest = {
    "name": D.NAME, "short_name": D.SHORT, "start_url": "/", "display": "standalone",
    "background_color": "#0c0c0b", "theme_color": "#0c0c0b",
    "icons": [
        {"src": "/assets/icons/icon-192.png", "sizes": "192x192", "type": "image/png"},
        {"src": "/assets/icons/icon-512.png", "sizes": "512x512", "type": "image/png"},
        {"src": "/assets/icons/maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
    ],
}
json.dump(manifest, open(os.path.join(ROOT, "site.webmanifest"), "w"), indent=2)

# ------------------------------------------------------------------ texture
stone = Image.open(os.path.join(SRC, "stone.png")).convert("RGB")
for w, q in [(1920, 62), (900, 60)]:
    s = fit_w(stone, w)
    s.save(out("img", f"stone-{w}.jpg"), quality=q, optimize=True, progressive=True)

# ------------------------------------------------------------------ team photos
# Black and white so photos taken in different places look like one set.
FOCUS_Y = {"justin-brown": 0.12, "david-cline": 0.18, "romell-witherspoon": 0.2, "matt-mccall": 0.15, "sophie-siegel": 0.3}
for p in D.TEAM:
    im = Image.open(os.path.join(SRC, f"head-{p['slug']}.png")).convert("RGB")
    im = ImageOps.grayscale(im).convert("RGB")
    W, H = im.size
    tw, th = (W, round(W * 5 / 4)) if W * 5 / 4 <= H else (round(H * 4 / 5), H)
    x = (W - tw) // 2
    y = round((H - th) * FOCUS_Y.get(p["slug"], 0.2))
    im = im.crop((x, y, x + tw, y + th))
    for w in (800, 480):
        fit_w(im, w).save(out("img", "team", f"{p['slug']}-{w}.jpg"), quality=80, optimize=True, progressive=True)

# ------------------------------------------------------------------ share cards (1200x630)
def card(slug, kicker, title):
    W, H = 1200, 630
    bg = fit_w(stone, W).crop((0, 0, W, H))
    bg = Image.blend(bg, Image.new("RGB", (W, H), INK), 0.35)
    c = bg.convert("RGBA")
    d = ImageDraw.Draw(c)
    lm = recolor(horiz, OFF); lm.thumbnail((360, 90), Image.LANCZOS)
    c.alpha_composite(lm, (90, 80))
    d.text((90, 250), kicker.upper(), font=font("cond-800", 30), fill=(170, 170, 165))
    size = 100
    f = font("cond-900", size)
    words = title.upper().split(); lines = []; cur = ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) > 1020 and cur:
            lines.append(cur); cur = w
        else:
            cur = t
    lines.append(cur)
    y = 300
    for ln in lines[:3]:
        d.text((86, y), ln, font=f, fill=OFF)
        y += size * 0.98
    # four rising bars, bottom right — the "levels"
    for i, w in enumerate((44, 66, 88, 110)):
        d.rectangle((W - 90 - 110, 84 + i * 22, W - 90 - 110 + w, 84 + i * 22 + 13), fill=OFF)
    c.convert("RGB").save(out("og", f"{slug}.jpg"), quality=84, optimize=True)

card("home", "Basketball sports advisory", "Enhance. Elevate. Enlighten. Empower.")
card("services", "The four levels", "Foundation. Visibility. Perspective. Legacy.")
card("team", "4Levels Sports Advisory", "Meet the team")
card("clients", "4Levels Sports Advisory", "Our clients")
card("contact", "4Levels Sports Advisory", "Start the conversation")
card("404", "4Levels Sports Advisory", "Page not found")
print("assets ok")
