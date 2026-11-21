#!/usr/bin/env python3
"""Generate animated tech-stack cards (icon + label tiles) from assets/tech/*.svg.

Each source pill in assets/tech embeds its logo as a data-URI <image> and its brand
colour in the "gl" gradient. This script reuses both to build one animated SVG per
category in assets/stack/, so the README needs no external icon service.

Run:  python3 scripts/gen_stack.py
"""
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "tech"
OUT = ROOT / "assets" / "stack"

CATEGORIES = [
    ("mobile", "Android & Multiplatform", "#3DDC84",
     ["kotlin", "android", "compose", "kmp", "cmp", "coroutines", "ktor", "hilt",
      "room", "retrofit", "swiftui", "gradle", "androidstudio"]),
    ("backend", "Backend & Microservices", "#6DB33F",
     ["springboot", "springcloud", "springsecurity", "microservices", "kafka",
      "rabbitmq", "java", "hibernate", "maven", "swagger", "nodejs", "express"]),
    ("data", "Databases & Caching", "#4169E1",
     ["postgresql", "mysql", "mariadb", "mongodb", "cassandra", "cockroachdb",
      "redis", "elasticsearch", "firebase"]),
    ("devops", "DevOps, Cloud & Observability", "#2496ED",
     ["docker", "kubernetes", "aws", "jenkins", "githubactions", "nginx",
      "prometheus", "grafana", "kibana", "linux", "git"]),
    ("web", "Web, Languages & Design", "#F7DF1E",
     ["javascript", "typescript", "react", "nextjs", "vue", "tailwind", "python",
      "cpp", "figma"]),
]

COLS = 7
TILE_W, TILE_H = 104, 112
GAP = 14
PAD_X, PAD_TOP, PAD_BOTTOM = 24, 66, 24
ICON = 46


def load(name):
    text = (SRC / f"{name}.svg").read_text(encoding="utf-8")
    label = html.unescape(re.search(r'aria-label="([^"]*)"', text).group(1))
    href = re.search(r'<image[^>]*href="([^"]+)"', text, re.S).group(1)
    m = re.search(r'id="gl".*?stop-color="(#[0-9A-Fa-f]{6})"', text, re.S)
    color = m.group(1) if m else "#7F52FF"
    return label, href, color


def shorten(label):
    return {"Coroutines & Flow": "Coroutines", "Compose Multiplatform": "Compose MP",
            "Kotlin Multiplatform": "KMP", "Jetpack Compose": "Compose",
            "Spring Security": "Spring Sec", "Android Studio": "Android Studio",
            "GitHub Actions": "GH Actions", "Elasticsearch": "Elastic",
            "Hilt / Dagger": "Hilt", "Tailwind CSS": "Tailwind",
            "Microservices": "Microservices", "Apache Kafka": "Kafka"}.get(label, label)


def build(slug, title, accent, names):
    items = [load(n) for n in names]
    rows = (len(items) + COLS - 1) // COLS
    cols = min(COLS, len(items))
    grid_w = cols * TILE_W + (cols - 1) * GAP
    width = max(grid_w + 2 * PAD_X, COLS * TILE_W + (COLS - 1) * GAP + 2 * PAD_X)
    height = PAD_TOP + rows * TILE_H + (rows - 1) * GAP + PAD_BOTTOM

    tiles = []
    for i, (label, href, color) in enumerate(items):
        r, c = divmod(i, COLS)
        in_row = min(COLS, len(items) - r * COLS)
        row_w = in_row * TILE_W + (in_row - 1) * GAP
        x0 = (width - row_w) / 2 + c * (TILE_W + GAP)
        y0 = PAD_TOP + r * (TILE_H + GAP)
        delay = 0.08 * i
        float_delay = (i % 5) * 0.6
        text = html.escape(shorten(label))
        fs = 12.5 if len(text) <= 11 else 11
        tiles.append(f'''
  <g class="t" style="animation-delay:{delay:.2f}s">
   <g class="f" style="animation-delay:{float_delay:.1f}s">
    <rect x="{x0}" y="{y0}" width="{TILE_W}" height="{TILE_H}" rx="18" fill="url(#tile)"/>
    <rect x="{x0}" y="{y0}" width="{TILE_W}" height="{TILE_H}" rx="18" fill="none" stroke="{color}" stroke-opacity=".55" stroke-width="1.3"/>
    <circle class="g" cx="{x0 + TILE_W / 2}" cy="{y0 + 42}" r="30" fill="{color}" style="animation-delay:{float_delay:.1f}s"/>
    <image x="{x0 + (TILE_W - ICON) / 2}" y="{y0 + 19}" width="{ICON}" height="{ICON}" href="{href}"/>
    <text x="{x0 + TILE_W / 2}" y="{y0 + 92}" font-size="{fs}" text-anchor="middle">{text}</text>
   </g>
  </g>''')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{html.escape(title)}">
 <title>{html.escape(title)}</title>
 <defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#140d24"/><stop offset="1" stop-color="#0a0713"/></linearGradient>
  <linearGradient id="tile" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#21183a"/><stop offset="1" stop-color="#120c20"/></linearGradient>
  <linearGradient id="edge" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{accent}"/><stop offset=".5" stop-color="#7F52FF"/><stop offset="1" stop-color="{accent}"/></linearGradient>
  <linearGradient id="shine" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".09"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
  <filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="12"/></filter>
  <clipPath id="clip"><rect width="{width}" height="{height}" rx="22"/></clipPath>
 </defs>
 <style>
  text{{font-family:'Segoe UI',Ubuntu,'Helvetica Neue',Arial,sans-serif;fill:#ECE8FF;font-weight:600}}
  .h{{font-size:19px;font-weight:700;letter-spacing:.3px}}
  .t{{opacity:0;animation:in .7s cubic-bezier(.2,.8,.2,1) forwards}}
  .f{{animation:fl 4s ease-in-out infinite}}
  .g{{opacity:.18;filter:url(#blur);animation:gl 3s ease-in-out infinite}}
  .s{{animation:sh 6s linear infinite}}
  .d{{animation:dt 2s ease-in-out infinite}}
  @keyframes in{{from{{opacity:0;transform:translateY(14px)}}to{{opacity:1;transform:none}}}}
  @keyframes fl{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-4px)}}}}
  @keyframes gl{{0%,100%{{opacity:.12}}50%{{opacity:.42}}}}
  @keyframes sh{{from{{transform:translateX(-{width}px)}}to{{transform:translateX({width}px)}}}}
  @keyframes dt{{0%,100%{{opacity:.35}}50%{{opacity:1}}}}
 </style>
 <g clip-path="url(#clip)">
  <rect width="{width}" height="{height}" fill="url(#bg)"/>
  <rect class="s" width="{width * 0.45}" height="{height}" fill="url(#shine)"/>
 </g>
 <rect x=".75" y=".75" width="{width - 1.5}" height="{height - 1.5}" rx="21.5" fill="none" stroke="url(#edge)" stroke-opacity=".7" stroke-width="1.5"/>
 <circle class="d" cx="{PAD_X + 6}" cy="33" r="6" fill="{accent}"/>
 <text class="h" x="{PAD_X + 22}" y="40">{html.escape(title)}</text>
 <text x="{width - PAD_X}" y="40" font-size="12" text-anchor="end" fill-opacity=".55" style="fill:#a79fc9">{len(items)} tools</text>
{"".join(tiles)}
</svg>
'''


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for slug, title, accent, names in CATEGORIES:
        (OUT / f"{slug}.svg").write_text(build(slug, title, accent, names), encoding="utf-8")
        print("wrote", OUT / f"{slug}.svg")


if __name__ == "__main__":
    main()
