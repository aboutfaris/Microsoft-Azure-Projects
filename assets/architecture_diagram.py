#!/usr/bin/env python3
"""Microsoft Azure Set: high-level lab architecture diagram.

Built from the 340 architecture diagram reference implementation
(.kiro/steering/aws-architecture-diagram-style.md), with these owner-approved deviations
for this portfolio repo: no company branding or footer, Azure icons only (official Azure
icons bundled in the `diagrams` package), and one Microsoft Azure boundary.

Set up once:  python3 -m venv /tmp/c340_diag_venv
              /tmp/c340_diag_venv/bin/pip install diagrams     (official icons)
              brew install librsvg                              (rsvg-convert)
Run:          /tmp/c340_diag_venv/bin/python architecture_diagram.py <out-prefix>
It writes <out-prefix>.svg and <out-prefix>.png (rendered at 2x). The checks must print
"layout problems: none".
"""
import base64
import os
import subprocess
import sys

import diagrams

R = os.path.join(os.path.dirname(os.path.dirname(diagrams.__file__)), "resources")
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/arch"
OUT_SVG, OUT_PNG = OUT + ".svg", OUT + ".png"

# ---------------- style: owner-approved, keep as is ----------------
FONT = "Helvetica Neue, Helvetica, Arial, sans-serif"
INK, TEXT2, LINE, GROUP, BADGE, ORANGE, RULE, ACCENT = (
    "#232F3E", "#545B64", "#3F4752", "#7D8998", "#146EB4", "#FF9900", "#E3E6EA", "#8C4FFF")
ICON, HALF = 52, 26
KINDS = {  # stroke, width, dash, arrowhead marker, legend label
    "service": (LINE, 1.6, None, "ah", "Connection inside Azure"),
    "external": (LINE, 1.6, "6 5", "ah", "To or from outside Azure"),
    "business": (ACCENT, 2.2, None, "ahb", "Business flow"),
}

# ---------------- EDIT: canvas text ----------------
W, H = 1600, 1060
TITLE = "Microsoft Azure Set | Lab Architecture"
SUBTITLE = ("A small Windows domain on Azure VMs (sections 01, 03, 04) plus a standalone "
            "two-VM traffic lab (section 02).")
REGION = "lab resource groups and virtual networks"

out, icons, SEGS, BADGES = [], [], [], []
N, BOX, USED = {}, {}, set()


def add(s):
    out.append(s)


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def est_w(s, size):
    return len(s) * size * 0.53


def text(x, y, s, size=13, weight=400, color=INK, anchor="middle", halo=False):
    h = (' stroke="#FFFFFF" stroke-width="5" stroke-linejoin="round" paint-order="stroke"'
         if halo else "")
    add(f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" '
        f'font-weight="{weight}" fill="{color}" text-anchor="{anchor}"{h}>{esc(s)}</text>')


_cache = {}


def data(rel):
    if rel not in _cache:
        with open(os.path.join(R, rel), "rb") as fh:
            _cache[rel] = "data:image/png;base64," + base64.b64encode(fh.read()).decode()
    return _cache[rel]


def node(key, rel, cx, cy, l1, l2=None):
    """Register an icon at slot (cx, cy) with a name and an optional role line."""
    assert key not in N, key
    N[key] = (cx, cy, 2 if l2 else 1)
    icons.append((rel, cx, cy, l1, l2))
    w = max(ICON, est_w(l1, 13), est_w(l2 or "", 12))
    BOX[key] = (cx - w / 2, cy - HALF, cx + w / 2, cy + HALF + (36 if l2 else 21))


def draw_nodes():
    for rel, cx, cy, l1, l2 in icons:
        add(f'<image x="{cx-HALF}" y="{cy-HALF}" width="{ICON}" height="{ICON}" '
            f'xlink:href="{data(rel)}"/>')
        text(cx, cy + HALF + 17, l1, 13, 400, INK)
        if l2:
            text(cx, cy + HALF + 32, l2, 12, 400, TEXT2)


def port(key, side, gap=5):
    """Connection point: l, r, t (top edge of icon), b (below the label block)."""
    cx, cy, n = N[key]
    return {"l": (cx - HALF - gap, cy), "r": (cx + HALF + gap, cy),
            "t": (cx, cy - HALF - gap),
            "b": (cx, cy + HALF + (36 if n == 2 else 21) + gap)}[side]


def path(pts, a, b, kind="service"):
    color, width, dash, marker, _ = KINDS[kind]
    USED.add(kind)
    for p, q in zip(pts, pts[1:]):
        assert p[0] == q[0] or p[1] == q[1], ("diagonal segment", a, b, p, q)
        SEGS.append((p, q, a, b))
    d = "M " + " L ".join(f"{x},{y}" for x, y in pts)
    da = f' stroke-dasharray="{dash}"' if dash else ""
    add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}"{da} '
        f'marker-end="url(#{marker})"/>')


def link(a, sa, b, sb, kind="service", via=None):
    """Connect two nodes. via = elbow points; every segment must be horizontal or vertical."""
    path([port(a, sa)] + (via or []) + [port(b, sb)], a, b, kind)


def badge(cx, cy, n, record=True):
    if record:
        BADGES.append((cx, cy, n))
    add(f'<rect x="{cx-12}" y="{cy-12}" width="24" height="24" rx="3" fill="{BADGE}"/>')
    text(cx, cy + 4.6, str(n), 13, 700, "#FFFFFF")


def group(x0, y0, x1, y1, title):
    add(f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="none" '
        f'stroke="{GROUP}" stroke-width="1.3" stroke-dasharray="5 4"/>')
    text(x0 + 14, y0 + 25, title, 14.5, 700, INK, "start")


# ---------------- EDIT: grid ----------------
AX0, AX1, AY0, AY1 = 190, 1410, 110, 846              # Microsoft Azure boundary
COLS = [(220, 582), (618, 980), (1016, 1378)]         # group columns
SL = [[round(x0 + (x1 - x0) * f) for f in (0.2, 0.5, 0.8)] for x0, x1 in COLS]  # icon slots
ROWS = [(160, 470), (506, 816)]                       # group rows
A1, B1, A2, B2 = 255, 395, 601, 731                   # icon lanes (center y)
XL, XR = 95, 1505                                     # external columns
GY, GX1, GX2 = 488, 600, 998                          # row gutter y, column gutters x

# ---------------- canvas and Azure boundary ----------------
add(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
    f'width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
add('<defs>'
    '<marker id="ah" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="6.5" '
    f'markerHeight="6.5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{LINE}"/></marker>'
    '<marker id="ahb" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="5" '
    f'markerHeight="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{ACCENT}"/></marker>'
    '</defs>')
add(f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>')
text(40, 56, TITLE, 26, 700, INK, "start")
text(40, 82, SUBTITLE, 14, 400, TEXT2, "start")
add(f'<rect x="{AX0}" y="{AY0}" width="{AX1-AX0}" height="{AY1-AY0}" fill="none" '
    f'stroke="{INK}" stroke-width="1.6"/>')
# official Azure icon from the diagrams package as the boundary tile
add(f'<image x="{AX0+4}" y="{AY0+4}" width="26" height="26" '
    f'xlink:href="{data("azure/azure.png")}"/>')
add(f'<text x="{AX0+40}" y="{AY0+23}" font-family="{FONT}" font-size="14.5" '
    f'font-weight="700" fill="{INK}">Microsoft Azure<tspan dx="10" font-weight="400" '
    f'fill="{TEXT2}">{esc(REGION)}</tspan></text>')

# ---------------- EDIT: groups ----------------
(c0, c1, c2), (r0, r1) = COLS, ROWS
group(c0[0], r0[0], c0[1], r1[1], "02 NSGs and network protocols")       # standalone lab
group(c1[0], r0[0], c2[1], r0[1], "01 Active Directory in Azure VMs")
group(c1[0], r1[0], c1[1], r1[1], "03 Network file shares and permissions")
group(c2[0], r1[0], c2[1], r1[1], "04 Building intuition for DNS")

# ---------------- EDIT: nodes ----------------
VMW = "azure/compute/vm-windows.png"
DNS = "azure/networking/dns-zones.png"

# outside Azure
node("you", "onprem/client/client.png", XL, A1, "Your computer", "Remote Desktop")
node("web", "onprem/network/internet.png", XR, 760, "Internet", "www.google.com")

# 02 NSGs and network protocols
node("winvm", VMW, SL[0][0], A1, "Windows 10 VM", "runs Wireshark")
node("ubuntu", "azure/compute/vm-linux.png", SL[0][2], A1, "Ubuntu Server VM", "SSH target")
node("nsg", "azure/networking/network-security-groups.png", SL[0][1], B1,
     "Network security groups", "one per VM")
node("azdns", DNS, SL[0][0], A2, "Azure-provided DNS", "and DHCP")

# 01 Active Directory in Azure VMs
node("client1", VMW, SL[1][0], A1, "Client-1", "Windows 10 client")
node("dc1", VMW, SL[2][0], A1, "DC-1", "domain controller")
node("users", "azure/identity/users.png", SL[2][2], A1, "AD users and OUs", "_EMPLOYEES, _ADMINS")
node("ps", "azure/general/powershell.png", SL[2][2], B1, "PowerShell script", "bulk-creates users")
node("vnet", "azure/networking/virtual-networks.png", SL[1][1], B1,
     "Virtual network", "static private IP on DC-1")

# 03 Network file shares and permissions
node("shares", "azure/general/folder-blank.png", SL[1][1], A2, "SMB shares on DC-1",
     "4 folders, group permissions")
node("acct", "azure/identity/groups.png", SL[1][1], B2, "ACCOUNTANTS", "security group")

# 04 Building intuition for DNS
node("cache", "azure/general/cache.png", SL[2][0], A2, "Client-1 DNS cache", "ipconfig /flushdns")
node("zone", DNS, SL[2][2], A2, "DNS on DC-1", "A and CNAME records")

# ---------------- EDIT: connections (kind: service, external) ----------------
link("you", "r", "winvm", "l", "external")
link("winvm", "r", "ubuntu", "l")
link("winvm", "b", "azdns", "t")
link("client1", "r", "dc1", "l")
link("dc1", "r", "users", "l")
link("ps", "t", "users", "b")
link("client1", "l", "shares", "l", via=[(GX1, A1), (GX1, A2)])
link("dc1", "b", "shares", "r", via=[(SL[2][0], GY), (GX2, GY), (GX2, A2)])
link("acct", "t", "shares", "b")
link("cache", "r", "zone", "l")
link("zone", "b", "web", "l", "external", via=[(SL[2][2], 760)])

# ---------------- EDIT: line labels (white halo keeps them readable over lines) ----------------
text(SL[0][1], A1 - 9, "ICMP, SSH", 11.5, 400, TEXT2, "middle", halo=True)
text(SL[0][0] + 10, 480, "DHCP, DNS", 11.5, 400, TEXT2, "start", halo=True)
text((SL[1][0] + SL[2][0]) / 2, A1 - 9, "joins the domain, uses DC-1 for DNS",
     11.5, 400, TEXT2, "middle", halo=True)
text((SL[2][0] + SL[2][2]) / 2, A1 - 9, "ADUC", 11.5, 400, TEXT2, "middle", halo=True)
text(c1[0] + 10, A2 + 22, "opens \\\\dc-1", 11.5, 400, TEXT2, "start", halo=True)
text(GX2 - 66, A2 - 9, "hosts", 11.5, 400, TEXT2, "middle", halo=True)
text(SL[1][1] + 10, 690, "Read/Write", 11.5, 400, TEXT2, "start", halo=True)
text(SL[2][1], A2 - 9, "ping, nslookup", 11.5, 400, TEXT2, "middle", halo=True)
text(SL[2][2] + 10, 700, "CNAME search", 11.5, 400, TEXT2, "start", halo=True)

draw_nodes()

# ---------------- EDIT: step badges (x, y, number), in a gutter beside their line ----------------
for cx, cy, n in [(158, 228, 1), (SL[1][1], 282, 2), (1280, 340, 3), (SL[0][1], 282, 4),
                  (650, 578, 5), (SL[2][1], 630, 6)]:
    badge(cx, cy, n)

# ---------------- EDIT: legend steps, one short sentence each, same order as the badges ----------------
LY = 890
STEPS = [
    "You reach every lab VM from your own computer over Remote Desktop.",
    "01: DC-1 runs AD DS with a static private IP; Client-1 uses it for DNS and joins the domain.",
    "01, Part 7: a PowerShell script on DC-1 bulk-creates domain users in the _EMPLOYEES OU.",
    "02: Wireshark on the Windows VM captures ICMP, SSH, DHCP, DNS, and RDP; an NSG guards each VM.",
    "03: DC-1 shares four folders; Client-1 tests access, and ACCOUNTANTS gets the accounting share.",
    "04: Client-1 resolves A and CNAME records from DNS on DC-1 and caches answers until flushed.",
]

text(40, LY, "How it works", 16, 700, INK, "start")
per_col = (len(STEPS) + 1) // 2
for i, s in enumerate(STEPS):
    col, row = divmod(i, per_col)
    bx, by = 52 + col * 770, LY + 34 + row * 32
    badge(bx, by, i + 1, record=False)
    text(bx + 22, by + 4.6, s, 13.5, 400, INK, "start")

# line-style key, one entry per line kind actually used
KEY_Y = LY + 40 + per_col * 32
lx = 40
for k, (color, width, dash, marker, label) in KINDS.items():
    if k not in USED:
        continue
    da = f' stroke-dasharray="{dash}"' if dash else ""
    add(f'<path d="M {lx},{KEY_Y} L {lx+52},{KEY_Y}" stroke="{color}" stroke-width="{width}"'
        f'{da} marker-end="url(#{marker})"/>')
    text(lx + 62, KEY_Y + 4.5, label, 12.5, 400, TEXT2, "start")
    lx += 62 + est_w(label, 12.5) + 48

add("</svg>")
assert KEY_Y + 30 <= H, "canvas too short for the legend: raise H"


# ---------------- checks: keep all of them ----------------
def seg_hits_box(p, q, box, pad=2):
    x0, y0, x1, y1 = box
    (ax, ay), (bx, by) = p, q
    if ay == by:
        lo, hi = sorted((ax, bx))
        return y0 - pad < ay < y1 + pad and lo < x1 + pad and hi > x0 - pad
    lo, hi = sorted((ay, by))
    return x0 - pad < ax < x1 + pad and lo < y1 + pad and hi > y0 - pad


def boxes_overlap(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def crossings():
    hs = [s for s in SEGS if s[0][1] == s[1][1]]
    vs = [s for s in SEGS if s[0][0] == s[1][0]]
    found = []
    for hp, hq, ha, hb in hs:
        y = hp[1]
        x0, x1 = sorted((hp[0], hq[0]))
        for vp, vq, va, vb in vs:
            if (ha, hb) == (va, vb):
                continue
            x = vp[0]
            y0, y1 = sorted((vp[1], vq[1]))
            if x0 < x < x1 and y0 < y < y1:
                found.append(f"{ha}->{hb} x {va}->{vb}")
    return found


def shared_segments():
    found = []
    for i in range(len(SEGS)):
        for j in range(i + 1, len(SEGS)):
            (p, q, a, b), (r, s, c, d) = SEGS[i], SEGS[j]
            if (a, b) == (c, d):
                continue
            if p[1] == q[1] == r[1] == s[1]:
                lo1, hi1 = sorted((p[0], q[0]))
                lo2, hi2 = sorted((r[0], s[0]))
            elif p[0] == q[0] == r[0] == s[0]:
                lo1, hi1 = sorted((p[1], q[1]))
                lo2, hi2 = sorted((r[1], s[1]))
            else:
                continue
            if min(hi1, hi2) - max(lo1, lo2) > 0:
                found.append(f"{a}->{b} shares a segment with {c}->{d}")
    return found


problems = []
for p, q, a, b in SEGS:
    for k, box in BOX.items():
        if k not in (a, b) and seg_hits_box(p, q, box):
            problems.append(f"line {a}->{b} crosses {k}")
keys = list(BOX)
for i in range(len(keys)):
    for j in range(i + 1, len(keys)):
        if boxes_overlap(BOX[keys[i]], BOX[keys[j]]):
            problems.append(f"label overlap {keys[i]} / {keys[j]}")
for cx, cy, n in BADGES:
    bb = (cx - 12, cy - 12, cx + 12, cy + 12)
    for p, q, a, b in SEGS:
        if seg_hits_box(p, q, bb, pad=1):
            problems.append(f"badge {n} sits on line {a}->{b}")
    for k, box in BOX.items():
        if boxes_overlap(bb, box):
            problems.append(f"badge {n} overlaps {k}")
for k, (x0, y0, x1, y1) in BOX.items():
    for (c0, c1) in COLS:
        if c0 < (x0 + x1) / 2 < c1 and (x0 < c0 + 4 or x1 > c1 - 4):
            problems.append(f"label of {k} touches its group border")
problems += shared_segments()
X = crossings()
if len(X) > 2:
    problems.append(f"{len(X)} line crossings (2 at most, only where unavoidable)")

svg = "\n".join(out)
assert "\u2014" not in svg and "\u2013" not in svg, "em or en dash found"
with open(OUT_SVG, "w") as fh:
    fh.write(svg)
subprocess.run(["rsvg-convert", "-z", "2", "-o", OUT_PNG, OUT_SVG], check=True)
print("nodes:", len(N), "segments:", len(SEGS), "badges:", len(BADGES))
print("crossings:", len(X), *X)
print("layout problems:", problems if problems else "none")
print("wrote", OUT_SVG, "and", OUT_PNG)
