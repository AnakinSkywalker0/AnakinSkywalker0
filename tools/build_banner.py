"""Build the profile header banners (assets/header-dark.svg and assets/header-light.svg).

Each banner is one self-contained SVG: the dusk photo embedded as JPEG, film grain,
three drifting birds, and the lettering converted to outlines so GitHub needs no fonts.

Setup (once):
    pip install fonttools pillow
    curl -L -o tools/Outfit.ttf "https://github.com/google/fonts/raw/main/ofl/outfit/Outfit%5Bwght%5D.ttf"

Run from the repo root:
    python tools/build_banner.py --font tools/Outfit.ttf

Edit the text below, rebuild, and commit the two SVGs. Outfit.ttf is git-ignored.
"""
import argparse, base64, io, os
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from PIL import Image, ImageEnhance

# ── text ──
NAME = "Abhishek Mishra"
TAGLINE = "Games, tools & strange little systems"
LABELS = ["Game development", "Systems design", "Real-time control"]
HANDLE = "anakinskywalker0"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1200, 560


def load(font_path, weight):
    f = TTFont(font_path)
    return instancer.instantiateVariableFont(f, {"wght": weight})


def kern_table(font):
    """Pair kerning from GPOS (format 1 and 2 PairPos), as {(left, right): xAdvance}."""
    pairs = {}
    if "GPOS" not in font:
        return pairs
    gpos = font["GPOS"].table
    for lookup in gpos.LookupList.Lookup:
        subs = lookup.SubTable
        if lookup.LookupType == 9:
            subs = [s.ExtSubTable for s in subs]
        elif lookup.LookupType != 2:
            continue
        for st in subs:
            if getattr(st, "LookupType", 2) != 2:
                continue
            cov = st.Coverage.glyphs
            if st.Format == 1:
                for i, left in enumerate(cov):
                    for pvr in st.PairSet[i].PairValueRecord:
                        v = getattr(pvr.Value1, "XAdvance", 0) if pvr.Value1 else 0
                        if v:
                            pairs.setdefault((left, pvr.SecondGlyph), v)
            elif st.Format == 2:
                c1 = st.ClassDef1.classDefs if st.ClassDef1 else {}
                c2 = st.ClassDef2.classDefs if st.ClassDef2 else {}
                rights = {}
                for g, c in c2.items():
                    rights.setdefault(c, []).append(g)
                for left in cov:
                    rec = st.Class1Record[c1.get(left, 0)]
                    for k, r2 in enumerate(rec.Class2Record):
                        v = getattr(r2.Value1, "XAdvance", 0) if r2.Value1 else 0
                        if v and k in rights:
                            for right in rights[k]:
                                pairs.setdefault((left, right), v)
    return pairs


class Typeset:
    def __init__(self, font_path, weight):
        self.font = load(font_path, weight)
        self.upm = self.font["head"].unitsPerEm
        self.cmap = self.font.getBestCmap()
        self.gs = self.font.getGlyphSet()
        self.hmtx = self.font["hmtx"]
        self.kern = kern_table(self.font)

    def run(self, text, size, tracking=0.0):
        """Return (path_d, width) for text set at `size`, baseline at y=0, starting at x=0."""
        s = size / self.upm
        names = [self.cmap[ord(ch)] for ch in text]
        x, parts = 0.0, []
        for i, g in enumerate(names):
            pen = SVGPathPen(self.gs, ntos=lambda v: ("%.2f" % v).rstrip("0").rstrip("."))
            self.gs[g].draw(TransformPen(pen, (s, 0, 0, -s, x, 0)))
            d = pen.getCommands()
            if d:
                parts.append(d)
            adv = self.hmtx[g][0]
            if i + 1 < len(names):
                adv += self.kern.get((g, names[i + 1]), 0)
            x += adv * s + tracking * size
        width = x - tracking * size
        return " ".join(parts), width


def text_el(ts, text, size, x, y, anchor="middle", tracking=0.0, **attrs):
    d, w = ts.run(text, size, tracking)
    if anchor == "middle":
        x -= w / 2
    elif anchor == "end":
        x -= w
    extra = " ".join('%s="%s"' % (k.replace("_", "-"), v) for k, v in attrs.items())
    return '<path transform="translate(%.1f %.1f)" d="%s" %s/>' % (x, y, d, extra)


def photo_uri(photo):
    im = Image.open(photo).convert("RGB")
    iw, ih = im.size
    ch = round(iw * H / W)
    y0 = round((ih - ch) * 0.80)
    im = im.crop((0, y0, iw, y0 + ch)).resize((1600, round(1600 * H / W)), Image.LANCZOS)
    im = ImageEnhance.Color(im).enhance(0.85)
    im = ImageEnhance.Brightness(im).enhance(0.86)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=74, optimize=True, progressive=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


WING = "M0 0C-2 -2 -5 -2.7 -7.5 -2.3C-9.5 -2 -11.5 -1.4 -13.5 -.4C-9 -.2 -4 .6 0 1.4Z"
BODY = "M6 0C4.5 -1.1 1 -1.4 -2 -1.1C-4 -.9 -5.5 -.5 -8.6 -1.1L-8.6 1.1C-5.5 .5 -4 .9 -2 1.1C1 1.4 4.5 1.1 6 0Z"
# y, scale, tilt, squash, drift-phase, flap period, flap offset, bob period
BIRDS = [(112, 1.05, 4, 1, -.547, 2.6, 0, 3.1),
         (98, .9, 24, .8, -.531, 3.1, -1.1, 2.6),
         (124, .75, -10, .9, -.515, 2.8, -1.9, 3.6)]


def bird(y, sc, tilt, sx, k, f, p, b):
    return ('<g class="drift" style="--k:%s"><g transform="translate(0 %s) scale(%s)">'
            '<g class="bob" style="--b:%ss"><g transform="rotate(%s) scale(%s 1)">'
            '<g transform="translate(-.4 -.6)" opacity=".55"><path class="wing" style="--f:%ss;--p:%ss" d="%s"/></g>'
            '<path d="%s"/>'
            '<g transform="translate(1 -.3)"><path class="wing" style="--f:%ss;--p:%ss" d="%s"/></g>'
            '</g></g></g></g>') % (k, y, sc, b, tilt, sx, f, p + .06, WING, BODY, f, p, WING)


def build(theme, light, regular, photo):
    label = NAME + ". " + TAGLINE.replace("&", "and") + "."
    name = text_el(light, NAME, 96, W / 2, 268, fill="#eeece8")
    tag = text_el(light, TAGLINE, 27, W / 2, 322, fill="#eeece8", fill_opacity=".78")
    nav = "".join(text_el(light, t, 19, 44, 58 + i * 27, anchor="start", fill="#eeece8", fill_opacity=".82")
                  for i, t in enumerate(LABELS))
    handle = text_el(regular, HANDLE, 21, W / 2, 64, fill="#eeece8")
    dot = text_el(regular, ".", 21, W / 2 + regular.run(HANDLE, 21)[1] / 2, 64, anchor="start", fill="#eeece8", fill_opacity=".56")

    bottom, mask = ('.55', ' mask="url(#fade)"') if theme == 'dark' else ('.35', '')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{label}">
<style>
.drift{{animation:drift 70s linear infinite;animation-delay:calc(70s * var(--k))}}
.bob{{animation:bob var(--b) ease-in-out infinite}}
.wing{{transform-box:fill-box;transform-origin:100% 55%;animation:flap var(--f) ease-in-out infinite;animation-delay:var(--p)}}
.rise{{opacity:0;animation:rise 1.8s cubic-bezier(.2,.7,.15,1) forwards}}
.cue{{animation:fall 2.6s cubic-bezier(.2,.7,.15,1) infinite}}
@keyframes drift{{0%{{transform:translate(-40px,0)}}25%{{transform:translate(270px,-6px)}}50%{{transform:translate(600px,3px)}}75%{{transform:translate(930px,-4px)}}100%{{transform:translate(1240px,0)}}}}
@keyframes bob{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-2px)}}}}
@keyframes flap{{0%,58%,100%{{transform:rotate(8deg)}}10%,34%{{transform:rotate(46deg)}}22%,46%{{transform:rotate(-34deg)}}}}
@keyframes rise{{from{{opacity:0;transform:translateY(14px)}}to{{opacity:1;transform:none}}}}
@keyframes fall{{from{{transform:translateY(-40px)}}to{{transform:translateY(120px)}}}}
@media (prefers-reduced-motion:reduce){{.drift,.bob,.wing,.cue{{animation:none}}.rise{{animation:none;opacity:1}}}}
</style>
<defs>
<linearGradient id="shade" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#0e1016" stop-opacity=".45"/><stop offset=".28" stop-color="#0e1016" stop-opacity=".12"/>
<stop offset=".6" stop-color="#0e1016" stop-opacity=".12"/><stop offset="1" stop-color="#0d1117" stop-opacity="{bottom}"/>
</linearGradient>
<linearGradient id="fadeG" x1="0" y1="0" x2="0" y2="1">
<stop offset=".72" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
</linearGradient>
<mask id="fade" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="url(#fadeG)"/></mask>
<clipPath id="card"><rect width="{W}" height="{H}" rx="14"/></clipPath>
<filter id="noise" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">
<feTurbulence type="fractalNoise" baseFrequency=".7" numOctaves="4" stitchTiles="stitch"/>
<feColorMatrix values=".33 .33 .33 0 0 .33 .33 .33 0 0 .33 .33 .33 0 0 0 0 0 0 1"/>
<feComponentTransfer><feFuncR type="linear" slope="2.6" intercept="-.8"/><feFuncG type="linear" slope="2.6" intercept="-.8"/><feFuncB type="linear" slope="2.6" intercept="-.8"/></feComponentTransfer>
</filter>
<linearGradient id="cueG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#eeece8" stop-opacity="0"/><stop offset="1" stop-color="#eeece8" stop-opacity=".85"/></linearGradient>
<clipPath id="cueClip"><rect x="599.5" y="470" width="1" height="90"/></clipPath>
</defs>
<g clip-path="url(#card)"{mask}>
<image href="{photo}" width="{W}" height="{H}" preserveAspectRatio="xMidYMid slice"/>
<g fill="#181c24" opacity=".7">{"".join(bird(*b) for b in BIRDS)}</g>
<rect width="{W}" height="{H}" fill="url(#shade)"/>
<rect width="{W}" height="{H}" filter="url(#noise)" opacity=".2" style="mix-blend-mode:overlay"/>
<g class="rise" style="animation-delay:.3s">{nav}{handle}{dot}</g>
<g class="rise" style="animation-delay:.6s">{name}</g>
<g class="rise" style="animation-delay:1s">{tag}</g>
<rect x="599.5" y="470" width="1" height="90" fill="#eeece8" fill-opacity=".14"/>
<g clip-path="url(#cueClip)"><rect class="cue" x="599.5" y="470" width="1" height="40" fill="url(#cueG)"/></g>
</g>
</svg>
'''
    return svg


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--font", required=True, help="Outfit variable font (.ttf)")
    ap.add_argument("--photo", default=os.path.join(ROOT, "tools", "dusk.webp"))
    ap.add_argument("--out", default=os.path.join(ROOT, "assets"))
    a = ap.parse_args()
    light, regular = Typeset(a.font, 300), Typeset(a.font, 400)
    photo = photo_uri(a.photo)
    for theme in ("dark", "light"):
        path = os.path.join(a.out, "header-%s.svg" % theme)
        svg = build(theme, light, regular, photo)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(svg)
        print("wrote", os.path.relpath(path, ROOT), len(svg) // 1024, "KB")


if __name__ == "__main__":
    main()
