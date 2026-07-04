"""
Sequencing as a tapering admissible band.
The band's angular coordinate is a schematic phase descriptor; its
width is the remaining admissible window; monotone contraction tapers
the band, and a tapering band laid flat winds into a spiral. The
winding is the embedding, not motion. Black dots and arrows: realized
ordering record. Gray numerals: monotone labels tau. Crossed stubs:
continuations falling outside the narrowed window, non-addressable
relative to the record.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Polygon

plt.rcParams.update({
    "mathtext.fontset": "cm",
    "font.family": "serif",
    "font.serif": ["DejaVu Serif"],
})

DARK = "#2b2b2b"
GRAY = "#8a8a8a"

CX, CY = 4.15, 3.85          # spiral center
R0, K = 3.05, 0.285          # center-curve radius r = R0 - K*theta
W0 = 0.52                    # initial half-width of the band
TH_MAX = 3.2 * np.pi         # 1.6 turns, radius stays positive

def r_center(th):
    return R0 - K * th

def half_width(th):
    return W0 * (1.0 - 0.92 * th / TH_MAX)

def xy(th, r):
    return CX + r * np.cos(th), CY + r * np.sin(th)

fig, ax = plt.subplots(figsize=(12.4, 7.6), dpi=200)
ax.set_xlim(0, 12.4)
ax.set_ylim(0, 7.6)
ax.set_aspect("equal")
ax.axis("off")

# ---------- the band ----------
th = np.linspace(0, TH_MAX, 600)
outer = np.array([xy(t, r_center(t) + half_width(t)) for t in th])
inner = np.array([xy(t, r_center(t) - half_width(t)) for t in th])
band = np.vstack([outer, inner[::-1]])
ax.add_patch(Polygon(band, closed=True, facecolor="#ececec",
                     edgecolor="#b0b0b0", lw=1.0, zorder=1))

# faint center line of the band
cline = np.array([xy(t, r_center(t)) for t in th])
ax.plot(cline[:, 0], cline[:, 1], lw=0.7, color="#cfcfcf",
        linestyle=(0, (4, 4)), zorder=2)

# ---------- the realized record ----------
chain_th = [0.55, 1.75, 2.95, 4.15, 5.35, 6.55, 7.75]
chain = [xy(t, r_center(t)) for t in chain_th]
for p, q in zip(chain[:-1], chain[1:]):
    ar = FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=11,
                         lw=1.3, color=DARK, shrinkA=7, shrinkB=7,
                         zorder=4)
    ax.add_patch(ar)
for x, y in chain:
    ax.add_patch(Circle((x, y), 0.085, facecolor=DARK, edgecolor=DARK,
                        zorder=5))
# gray bookkeeping numerals, offset outward from the band
for i, t in enumerate(chain_th, start=1):
    lx, ly = xy(t, r_center(t) + half_width(t) + 0.34)
    ax.text(lx, ly, str(i), fontsize=12.5, color=GRAY,
            ha="center", va="center", style="italic", zorder=5)

# ---------- non-addressable continuations ----------
def cross_stub(t_from, ang_off=0.0):
    x0, y0 = xy(t_from, r_center(t_from))
    x1, y1 = xy(t_from + ang_off, r_center(t_from) + half_width(t_from) + 0.62)
    ax.plot([x0, x1], [y0, y1], lw=1.0, color="#9a9a9a",
            linestyle=(0, (4, 3)), zorder=3)
    c = Circle((x1, y1), 0.13, facecolor="white", edgecolor="#9a9a9a",
               lw=1.1, zorder=4)
    ax.add_patch(c)
    d = 0.07
    ax.plot([x1-d, x1+d], [y1-d, y1+d], lw=1.1, color="#9a9a9a", zorder=5)
    ax.plot([x1-d, x1+d], [y1+d, y1-d], lw=1.1, color="#9a9a9a", zorder=5)

cross_stub(2.35, 0.18)
cross_stub(5.90, 0.16)
cross_stub(8.60, 0.20)

# ---------- annotations ----------
ax.text(8.55, 6.35,
        "the admissible window: band width is the\n"
        "remaining admissible range in the descriptor;\n"
        "the taper is monotone contraction under\n"
        "successive registered restrictions",
        fontsize=12, color="#555555", ha="left", va="center",
        linespacing=1.5)
lx, ly = xy(0.9, r_center(0.9) + half_width(0.9))
ax.plot([8.45, lx + 0.12], [6.35, ly + 0.10], lw=0.9, color="#bbbbbb",
        linestyle=(0, (2, 3)), zorder=2)

ax.text(8.55, 2.15,
        "a band that lengthens while narrowing\n"
        "winds when laid flat: the winding is the\n"
        "embedding of the taper, not motion",
        fontsize=12, color="#555555", ha="left", va="center",
        linespacing=1.5)

# ---------- legend ----------
ax.add_patch(Circle((1.05, 0.62), 0.085, facecolor=DARK, edgecolor=DARK))
ax.text(1.30, 0.62, "configuration realized along the ordering record",
        fontsize=11, color="#555555", ha="left", va="center")
cx2, cy2 = 6.55, 0.62
c = Circle((cx2, cy2), 0.115, facecolor="white", edgecolor="#9a9a9a",
           lw=1.1)
ax.add_patch(c)
d = 0.062
ax.plot([cx2-d, cx2+d], [cy2-d, cy2+d], lw=1.1, color="#9a9a9a")
ax.plot([cx2-d, cx2+d], [cy2+d, cy2-d], lw=1.1, color="#9a9a9a")
ax.text(6.80, 0.62, "continuation outside the narrowed window:"
        " non-addressable",
        fontsize=11, color="#555555", ha="left", va="center")
ax.text(6.2, 0.16,
        "gray numerals: monotone labels $\\tau$ (bookkeeping only)"
        "        angular coordinate: schematic descriptor, no metric"
        " content",
        fontsize=10.5, color="#777777", ha="center", va="center")

fig.savefig("../figures/admissible_ribbon.png",
            bbox_inches="tight", facecolor="white")
print("saved")
