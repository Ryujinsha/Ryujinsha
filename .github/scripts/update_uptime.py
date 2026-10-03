"""
Generates profile.svg with terminal colors from the hardcoded art + dynamic info.
Also regenerates README.md to embed the SVG.
Run directly or via GitHub Actions.
"""

import re
import html
import calendar
from datetime import date
from pathlib import Path

BIRTHDATE = date(2006, 1, 3)

ART_LINES = [
    "                                                                ",
    "                                                                  ",
    "         ..--.......                            .....             ",
    "     --+##################+.       .+##################.#.        ",
    "  .#-#####-......-#########+       ############-....+####+#-      ",
    "  ..##-.    .##########+              .-++++++---.     .+##.      ",
    "          -##########+-.-#          .#..+#########+-              ",
    "        +##.+#######-#+. #+         #+ ++#.#######.+##.           ",
    "      #++-.+#######.--. #.         #-  -  #######  -+#-          ",
    "         -##########++.               +############-             ",
    "                                                                ",
    "                                                                ",
    "                                                                 ",
    "                                                                 ",
    "                                                      +#        ",
    "                                                     ##         ",
    "                                                   .#+          ",
    "                                              -   .#+           ",
    "                                           .-##   #+            ",
    "                                        .###.    -#             ",
    "              .#....      ....--+#######-.       #.             ",
    "               ##-------+++------...            .#              ",
    "               ..                               +#              ",
    "                   ................             ..                  ",
]

BG        = "#0d1117"
ART_CLR   = "#3fb950"   
HEAD_CLR  = "#f0f6fc"   
SEP_CLR   = "#30363d"  
SECT_CLR  = "#58a6ff"  
LABEL_CLR = "#8b949e" 
DOT_CLR   = "#484f58"   
VAL_CLR   = "#e6edf3"   

FONT = "'Courier New', Courier, monospace"
FS   = 13      
LH   = 19     
CW   = 7.82    
PX   = 14      
PY   = 14    
GAP  = 2


def calc_uptime() -> str:
    birth, today = BIRTHDATE, date.today()
    y = today.year  - birth.year
    m = today.month - birth.month
    d = today.day   - birth.day
    if d < 0:
        m -= 1
        d += calendar.monthrange(today.year, today.month - 1 if today.month > 1 else 12)[1]
    if m < 0:
        y -= 1
        m += 12
    return f"{y} years, {m} months, {d} days"


def build_info_lines(uptime: str) -> list[str]:
    sep64 = "\u2500" * 64
    sep53 = "\u2500" * 53
    sep49 = "\u2500" * 49
    return [
        "Github@Ryujinsha",
        sep64,
        f"  OS:         ........ Windows 11, iOS, Linux",
        f"  Uptime:     ........ {uptime}",
        f"  Host:       ........ Self-hosted",
        f"  IDE:        ........ Antigravity IDE, VSCode 1.96.0",
        "",
        "  Languages.Programming: .. Java, Python, JavaScript, PHP, C++",
        "  Languages.Computer:    .. HTML, CSS, JSON, YAML",
        "  Languages.Real:        .. English, Indonesian",
        "",
        "  Hobbies: .... Anime, Gaming, Designing, Coding, PC Building",
        "",
        f"- Contact {sep53}",
        "  GitHub:    .............................. Ryujinsha",
        "  Discord:   .............................. ryujinsha",
        "",
        f"- GitHub Stats {sep49}",
        "  Repos: .............. 13 | Stars: ..................... 4",
        "  Followers: .......... 4  | Following: ................. 5",
        "  Contributions (Last Year): .................... 100",
        "",
        "",
        "",
    ]


def color_info_spans(s: str) -> list[tuple[str, str]]:
    """Parse an info line into [(text, color)] spans."""
    if not s.strip():
        return [("", VAL_CLR)]
    if "Github@" in s:
        return [(s, HEAD_CLR)]
    if re.match(r"^[\u2500 ]+$", s):
        return [(s, SEP_CLR)]
    if re.match(r"^- (Contact|GitHub)", s):
        m = re.match(r"(^- \S.*? )([\u2500]+)$", s)
        if m:
            return [(m.group(1), SECT_CLR), (m.group(2), SEP_CLR)]
        return [(s, SECT_CLR)]
    m = re.match(r"(\s+[A-Za-z][^:]+:\s+)(\.+\s*)(.*)", s)
    if m:
        return [(m.group(1), LABEL_CLR), (m.group(2), DOT_CLR), (m.group(3), VAL_CLR)]
    return [(s, VAL_CLR)]


def generate_svg(art: list[str], info: list[str]) -> str:
    art_w = max(len(l) for l in art)
    merged = []
    total = max(len(art), len(info))
    for i in range(total):
        a = art[i]  if i < len(art)  else ""
        b = info[i] if i < len(info) else ""
        merged.append((a.ljust(art_w) + " " * GAP, b))

    max_len = max(len(a) + len(b) for a, b in merged)
    W = int(max_len * CW) + PX * 2
    H = len(merged) * LH + PY * 2

    rows = []
    for i, (art_part, info_part) in enumerate(merged):
        y = PY + (i + 1) * LH
        art_span = f'<tspan fill="{ART_CLR}">{html.escape(art_part)}</tspan>'
        info_span = "".join(
            f'<tspan fill="{clr}">{html.escape(seg)}</tspan>'
            for seg, clr in color_info_spans(info_part)
        )
        rows.append(
            f'  <text x="{PX}" y="{y}" xml:space="preserve"'
            f' font-family={FONT!r} font-size="{FS}">'
            f'{art_span}{info_span}</text>'
        )

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">\n'
        f'  <rect width="{W}" height="{H}" fill="{BG}" rx="8"/>\n'
        + "\n".join(rows) + "\n"
        f"</svg>\n"
    )


def update_readme_to_svg():
    readme = Path("README.md").read_text(encoding="utf-8")
    updated = re.sub(
        r"<pre>.*?</pre>",
        '<img src="profile.svg" alt="Github@Ryujinsha profile" />',
        readme,
        flags=re.DOTALL,
    )
    if updated != readme:
        Path("README.md").write_text(updated, encoding="utf-8")
        print("README.md updated to embed profile.svg")


def main():
    uptime = calc_uptime()
    info   = build_info_lines(uptime)
    svg    = generate_svg(ART_LINES, info)
    Path("profile.svg").write_text(svg, encoding="utf-8")
    print(f"profile.svg generated (uptime: {uptime})")
    update_readme_to_svg()


if __name__ == "__main__":
    main()
