#!/usr/bin/env python3
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ICON_DIR = HERE / "icons"
LOGO_DIR = HERE / "logos"
GLYPH_DIR = HERE / "glyphs"

WIDTH = 900
MARGIN = 12
PANEL_RADIUS = 32
HERO_RADIUS = 40
TILE_RADIUS = 16

FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

PANEL = "#141417"
TILE = "#1E1E23"
DIVIDER = "#25252A"
STRONG = "#F4F4F5"
BODY = "#A1A1AA"
MUTED = "#71717A"
FAINT = "#52525B"
ACCENT = "#818CF8"

ICON_FILL = {"nextjs": "#09090B"}
ICON_RECOLOR = {
    "lua": [("#000080", "#7B86E8")],
    "pnpm": [("#4c4c4c", "#A1A1AA")],
    "mysql": [("#00618A", "#5AA9D6")],
    "debian": [("#A80030", "#E01B5A")],
}

TOOLS = [
    ("angular", "Angular"),
    ("nextjs", "Next.js"),
    ("html5", "HTML"),
    ("css3", "CSS"),
    ("javascript", "JavaScript"),
    ("typescript", "TypeScript"),
    ("tailwindcss", "Tailwind CSS"),
    ("nestjs", "NestJS"),
    ("nodejs", "Node.js"),
    ("laravel", "Laravel"),
    ("lua", "Lua"),
    ("discordjs", "Discord.js"),
    ("mysql", "MySQL"),
    ("postgresql", "PostgreSQL"),
    ("mongodb", "MongoDB"),
    ("redis", "Redis"),
    ("docker", "Docker"),
    ("kubernetes", "Kubernetes"),
    ("git", "Git"),
    ("npm", "npm"),
    ("pnpm", "pnpm"),
    ("vscode", "VS Code"),
    ("azure", "Azure"),
    ("debian", "Debian"),
    ("ubuntu", "Ubuntu"),
    ("python", "Python"),
    ("cloudflare", "Cloudflare"),
    ("figma", "Figma"),
]

COMPANIES = {
    "paddlewheel": ("Paddlewheel Inc.", "paddlewheel"),
    "sleepy-lab": ("Sleepy Lab Innovations Inc.", "sleepy-lab"),
}

OPEN_SOURCE = [
    {
        "file": "open-source-usercue.svg",
        "name": "UserCue",
        "color": "#FF2B87",
        "kind": "Feedback board",
        "logo": "usercue",
        "tile": TILE,
        "lines": [
            "A self-hosted feedback home: people post",
            "suggestions, vote, and follow the roadmap,",
            "while your team ships and writes the changelog.",
        ],
        "stack": [("nextjs", "Next.js"), ("typescript", "TypeScript"), ("postgresql", "PostgreSQL"), ("docker", "Docker")],
        "company": "paddlewheel",
    },
    {
        "file": "open-source-orbit.svg",
        "name": "Orbit",
        "color": "#FF0099",
        "kind": "HRM for communities",
        "logo": "orbit",
        "tile": "#FF0099",
        "lines": [
            "An HRM for virtual communities to manage",
            "members and track activity, with Discord and",
            "Roblox integrations and a full admin dashboard.",
        ],
        "stack": [("nextjs", "Next.js"), ("typescript", "TypeScript"), ("supabase", "Supabase"), ("tailwindcss", "Tailwind CSS")],
        "company": "sleepy-lab",
    },
]

LINKS = [
    ("link-portfolio.svg", "brennanpeters.ca", "globe"),
    ("link-github.svg", "GitHub", "github"),
    ("link-discord.svg", "Discord", "discord"),
    ("link-email.svg", "Email", "mail"),
]

EXPERIENCE = [
    ("paddlewheel", "Chief Executive Officer", "June 2026 to Present"),
    ("sleepy-lab", "Vice President", "January 2026 to Present"),
]


def esc(value):
    return value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, value, fill=BODY, size=16, weight=400, tracking=0, anchor=None, family=None):
    attrs = [f'x="{x}"', f'y="{y}"', f'fill="{fill}"', f'font-size="{size}"', f'font-weight="{weight}"']
    if tracking:
        attrs.append(f'letter-spacing="{round(tracking * size, 2)}"')
    if anchor:
        attrs.append(f'text-anchor="{anchor}"')
    if family:
        attrs.append(f'font-family="{family}"')
    return f"  <text {' '.join(attrs)}>{esc(value)}</text>"


def eyebrow(x, y, value):
    return text(x, y, value, ACCENT, 14, 500, 0.025)


def heading(x, y, value, size=30):
    return text(x, y, value, STRONG, size, 500, -0.025)


def divider(x1, x2, y):
    return f'  <line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{DIVIDER}"/>'


def panel(width, height, radius=PANEL_RADIUS, fill=PANEL):
    return (
        f'  <rect x="{MARGIN}" y="{MARGIN}" width="{width - 2 * MARGIN}" '
        f'height="{height - 2 * MARGIN}" rx="{radius}" fill="{fill}"/>'
    )


def document(width, height, title, body, defs=""):
    defs_block = f"  <defs>\n{defs}  </defs>\n" if defs else ""
    return (
        f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" '
        f'xmlns="http://www.w3.org/2000/svg" font-family="{FONT}" role="img" aria-labelledby="title">\n'
        f'  <title id="title">{esc(title)}</title>\n'
        f"{defs_block}{chr(10).join(body)}\n</svg>\n"
    )


def load_svg(directory, name):
    source = (directory / f"{name}.svg").read_text(encoding="utf-8")
    viewbox = re.search(r'viewBox="([^"]+)"', source).group(1)
    inner = re.search(r"<svg[^>]*>(.*)</svg>", source, re.DOTALL).group(1)
    for old, new in ICON_RECOLOR.get(name, []):
        inner = inner.replace(old, new)
    for identifier in re.findall(r'id="([^"]+)"', inner):
        scoped = f"{name}-{identifier}"
        inner = inner.replace(f'id="{identifier}"', f'id="{scoped}"')
        inner = inner.replace(f"url(#{identifier})", f"url(#{scoped})")
        inner = inner.replace(f'href="#{identifier}"', f'href="#{scoped}"')
    return viewbox, inner


def load_icon(name):
    return load_svg(ICON_DIR, name)


def logo(x, y, width, height, name):
    viewbox, inner = load_svg(LOGO_DIR, name)
    return (
        f'  <svg x="{x}" y="{y}" width="{width}" height="{height}" viewBox="{viewbox}" '
        f'preserveAspectRatio="xMinYMid meet" fill="#000">{inner}</svg>'
    )


def icon_tile(x, y, size, name, label, radius=TILE_RADIUS):
    viewbox, inner = load_icon(name)
    padding = round(size * 0.22, 1)
    icon_size = round(size - 2 * padding, 1)
    fill = ICON_FILL.get(name, "#000")
    return [
        f'  <g><title>{esc(label)}</title>',
        f'    <rect x="{x}" y="{y}" width="{size}" height="{size}" rx="{radius}" fill="{TILE}"/>',
        f'    <svg x="{x + padding}" y="{y + padding}" width="{icon_size}" height="{icon_size}" '
        f'viewBox="{viewbox}" fill="{fill}">{inner}</svg>',
        "  </g>",
    ]


def hero():
    width, height = WIDTH, 432
    stage_x, stage_y, stage_w, stage_h = 560, 24, 316, 384
    center_x = stage_x + stage_w // 2
    center_y = stage_y + stage_h // 2

    defs = (
        '    <linearGradient id="stage" x1="0" y1="0" x2="1" y2="1">\n'
        '      <stop offset="0" stop-color="#17172B"/>\n'
        '      <stop offset="0.5" stop-color="#131316"/>\n'
        '      <stop offset="1" stop-color="#1B1428"/>\n'
        "    </linearGradient>\n"
        "    <style>\n"
        "      .wave { transform-box: fill-box; transform-origin: 70% 70%; animation: wave 3s ease-in-out infinite; }\n"
        "      @keyframes wave {\n"
        "        0%, 55%, 100% { transform: rotate(0deg); }\n"
        "        10% { transform: rotate(14deg); }\n"
        "        20% { transform: rotate(-8deg); }\n"
        "        30% { transform: rotate(14deg); }\n"
        "        40% { transform: rotate(-4deg); }\n"
        "        50% { transform: rotate(10deg); }\n"
        "      }\n"
        "      @media (prefers-reduced-motion: reduce) { .wave { animation: none; } }\n"
        "    </style>\n"
    )

    body = [
        panel(width, height, HERO_RADIUS),
        f'  <rect x="{stage_x}" y="{stage_y}" width="{stage_w}" height="{stage_h}" rx="36" fill="url(#stage)"/>',
        f'  <text class="wave" fill="#F4F4F5" x="{center_x}" y="{center_y + 54}" font-size="160" text-anchor="middle">👋</text>',
        heading(60, 150, "Hi, I'm", 60),
        heading(60, 218, "Brennan Peters", 60),
        text(62, 272, "a software developer and entrepreneur.", BODY, 22, 300),
        text(62, 322, "I design and ship products end to end. Interfaces,", MUTED, 15),
        text(62, 346, "APIs, and infrastructure, with a focus on clarity", MUTED, 15),
        text(62, 370, "and speed.", MUTED, 15),
    ]
    return "hero.svg", document(width, height, "Hi, I'm Brennan Peters, a software developer and entrepreneur", body, defs)


def tools():
    per_row, tile, gap = 7, 56, 14
    grid_w = per_row * tile + (per_row - 1) * gap
    left = WIDTH - 60 - grid_w
    top = 66
    rows = -(-len(TOOLS) // per_row)
    height = top + rows * tile + (rows - 1) * gap + 66
    body = [
        panel(WIDTH, height),
        eyebrow(60, top + 14, "Tools"),
        heading(60, top + 56, "These are the"),
        heading(60, top + 94, "tools I work with."),
        text(60, top + 130, "From interfaces to APIs", BODY, 15, 300),
        text(60, top + 152, "and infrastructure.", BODY, 15, 300),
    ]
    for index, (name, label) in enumerate(TOOLS):
        x = left + (index % per_row) * (tile + gap)
        y = top + (index // per_row) * (tile + gap)
        body += icon_tile(x, y, tile, name, label)
    return "tools.svg", document(WIDTH, height, "Tools Brennan works with", body)


def open_source():
    height = 232
    body = [
        panel(WIDTH, height),
        eyebrow(60, 76, "Open source"),
        heading(60, 122, "I love working on and creating"),
        heading(60, 162, "open source projects. Take a peek."),
    ]
    return "open-source.svg", document(WIDTH, height, "Open source projects by Brennan", body)


def project_card(project):
    width, height = 450, 420
    left = 40
    tile = 56
    body = [panel(width, height)]
    body.append(f'  <rect x="{left}" y="48" width="{tile}" height="{tile}" rx="{TILE_RADIUS}" fill="{project["tile"]}"/>')
    inset = 14 if project["tile"] == TILE else 12
    body.append(logo(left + inset, 48 + inset, tile - 2 * inset, tile - 2 * inset, project["logo"]))
    body.append(text(left, 142, project["kind"], MUTED, 13))
    body.append(text(left, 180, project["name"], project["color"], 32, 500, -0.025))
    for index, line in enumerate(project["lines"]):
        body.append(text(left, 214 + index * 22, line, BODY, 14, 300))
    for index, (name, label) in enumerate(project["stack"]):
        body += icon_tile(left + index * 46, 278, 38, name, label, 11)
    company_name, company_logo = COMPANIES[project["company"]]
    body.append(text(left, 372, "by", MUTED, 13, 300))
    body.append(logo(left + 22, 356, 22, 22, company_logo))
    body.append(text(left + 52, 372, company_name, BODY, 13))
    body.append(text(width - left, 372, "GitHub  →", ACCENT, 13, 500, anchor="end"))
    return project["file"], document(width, height, f"{project['name']}, an open source project by {company_name}", body)


def experience():
    top, offset = 176, 24
    height = top + offset + 176 + 52
    columns = [60, 480]
    body = [
        panel(WIDTH, height),
        eyebrow(60, 76, "Experience"),
        heading(60, 122, "Where I show up."),
    ]
    for index, (company, role, period) in enumerate(EXPERIENCE):
        x = columns[index]
        y = top + index * offset
        company_name, _ = COMPANIES[company]
        body.append(logo(x, y, 72, 64, company))
        body.append(text(x, y + 118, role, STRONG, 28, 500, -0.025))
        body.append(text(x, y + 148, company_name, BODY, 16, 300))
        body.append(text(x, y + 176, period, MUTED, 13))
    return "experience.svg", document(WIDTH, height, "Where Brennan works", body)


def contact():
    height = 300
    body = [
        panel(WIDTH, height),
        eyebrow(60, 76, "Contact"),
        heading(60, 132, "Got a project in mind?", 38),
        text(62, 176, "I'm always happy to chat about interesting ideas, collaborations,", BODY, 15, 300),
        text(62, 200, "or products worth building.", BODY, 15, 300),
        text(60, 246, "hello@brennanpeters.ca  →", ACCENT, 18, 500),
    ]
    return "contact.svg", document(WIDTH, height, "Get in touch with Brennan", body)


def glyph(x, y, size, name, color):
    source = (GLYPH_DIR / f"{name}.svg").read_text(encoding="utf-8")
    inner = re.search(r"<svg[^>]*>(.*)</svg>", source, re.DOTALL).group(1)
    inner = re.sub(r"<title>.*?</title>", "", inner)
    if 'stroke="currentColor"' in source:
        style = f'fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'
    else:
        style = f'fill="{color}"'
    return f'  <svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="0 0 24 24" {style}>{inner}</svg>'


def link_tab(file, label, icon):
    height, gap, pad, icon_size = 32, 4, 16, 15
    text_x = gap + pad + icon_size + 9
    text_w = round(len(label) * 7.1)
    pill_w = pad + icon_size + 9 + text_w + 8 + 10 + pad
    width = pill_w + 2 * gap
    body = [
        f'  <rect x="{gap}" width="{pill_w}" height="{height}" rx="{height // 2}" fill="{TILE}"/>',
        glyph(gap + pad, (height - icon_size) / 2, icon_size, icon, BODY),
        f'  <text x="{text_x}" y="20.5" fill="{STRONG}" font-size="13" font-weight="500">{esc(label)}'
        f'<tspan fill="{MUTED}" dx="8" font-size="12">↗</tspan></text>',
    ]
    return file, document(width, height, label, body)


def main():
    outputs = [hero(), tools(), open_source(), experience(), contact()]
    outputs += [project_card(project) for project in OPEN_SOURCE]
    outputs += [link_tab(file, label, icon) for file, label, icon in LINKS]
    for name, content in outputs:
        path = HERE / name
        path.write_text(content, encoding="utf-8")
        print(f"wrote assets/{name} ({max(path.stat().st_size // 1024, 1)} KB)")


if __name__ == "__main__":
    main()
