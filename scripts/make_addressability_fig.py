"""
Addressability quotient figure for SSAF.
Phi (configuration space) -> projection pi_E -> addressability quotient Q_E.
Minimalist grayscale, Computer Modern math, print resolution.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, FancyArrowPatch
from matplotlib.path import Path

plt.rcParams.update({
    "mathtext.fontset": "cm",
    "font.family": "serif",
    "font.serif": ["DejaVu Serif"],
})

DARK = "#2b2b2b"
MID = "#666666"
LIGHT = "#b9b9b9"
FAINT = "#d9d9d9"

fig, ax = plt.subplots(figsize=(14.0, 6.4), dpi=200)
ax.set_xlim(0, 14)
ax.set_ylim(0, 6.4)
ax.set_aspect("equal")
ax.axis("off")

# ---------------- left: configuration space ----------------
ax.text(1.9, 3.4, r"$\Phi$", fontsize=150, color=DARK,
        ha="center", va="center")
ax.text(1.9, 1.15, "Configuration Space", fontsize=17, color=DARK,
        ha="center", va="center")

# ---------------- right: isometric lattice (quotient) ----------------
cx, cy, R = 10.6, 3.55, 1.95
angles = np.deg2rad(np.arange(30, 391, 60))
hex_pts = np.array([[cx + R * np.cos(a), cy + R * np.sin(a)] for a in angles[:6]])
hex_path = Path(hex_pts)

# lattice lines in three isometric directions, clipped to the hexagon
hex_poly_clip = Polygon(hex_pts, closed=True, facecolor="none", edgecolor="none")
ax.add_patch(hex_poly_clip)
n = 8
for theta in (0, 60, 120):
    t = np.deg2rad(theta)
    d = np.array([np.cos(t), np.sin(t)])       # line direction
    p = np.array([-np.sin(t), np.cos(t)])      # perpendicular
    for k in np.linspace(-R, R, n):
        a0 = np.array([cx, cy]) + p * k - d * 2.6 * R
        a1 = np.array([cx, cy]) + p * k + d * 2.6 * R
        (ln,) = ax.plot([a0[0], a1[0]], [a0[1], a1[1]],
                        lw=0.55, color=FAINT, zorder=1)
        ln.set_clip_path(hex_poly_clip)

# hexagon outline and vertex dots
outline = Polygon(hex_pts, closed=True, facecolor="none",
                  edgecolor=LIGHT, lw=1.1, zorder=2)
ax.add_patch(outline)
for x, y in hex_pts:
    ax.plot(x, y, "o", ms=4.5, color="#9a9a9a", zorder=3)

# the addressable class: single dot where both arrows terminate
class_pt = (cx - 0.62 * R, cy)
ax.plot(*class_pt, "o", ms=7, color=DARK, zorder=5)
ax.text(class_pt[0] + 0.28, class_pt[1] + 0.62,
        r"$[g_a]_E = [g_b]_E$", fontsize=16, color=DARK,
        ha="left", va="center", zorder=6,
        bbox=dict(facecolor="white", edgecolor="none", pad=2.0, alpha=0.85))

# ---------------- arrows: two configurations, one class ----------------
tail_top = (3.35, 3.95)
tail_bot = (3.35, 3.15)
ax.plot(*tail_top, "o", ms=5.5, color=DARK, zorder=4)
ax.plot(*tail_bot, "o", ms=5.5, color=DARK, zorder=4)
ax.text(tail_top[0] - 0.22, tail_top[1] + 0.02, r"$g_a$", fontsize=17,
        color=DARK, ha="right", va="center")
ax.text(tail_bot[0] - 0.22, tail_bot[1] + 0.02, r"$g_b$", fontsize=17,
        color=DARK, ha="right", va="center")

for tail in (tail_top, tail_bot):
    ar = FancyArrowPatch(tail, class_pt, arrowstyle="-|>",
                         mutation_scale=16, lw=1.5, color=DARK,
                         shrinkA=4, shrinkB=5, zorder=4)
    ax.add_patch(ar)

# projection label above the arrows
ax.text(6.05, 4.35, r"$\pi_E$", fontsize=20, color=DARK,
        ha="center", va="center")

# annotation below the arrows
ax.text(6.05, 2.45, "operational equivalence under $E$", fontsize=13.5,
        color=MID, ha="center", va="center")

# ---------------- quotient labels ----------------
ax.text(cx, 1.15, "Addressability quotient", fontsize=17, color=DARK,
        ha="center", va="center")
ax.text(cx, 0.55, r"$Q_E := \Phi/\!\sim_E$", fontsize=18, color=DARK,
        ha="center", va="center")

fig.savefig("../figures/addressibility.png",
            bbox_inches="tight", facecolor="white")
print("saved")
