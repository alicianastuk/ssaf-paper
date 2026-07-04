"""
NS1 rate-independence test, protocol schematic for Section XI.
Top: protocol flow in canon vocabulary (varied preparations, fixed
certified context E with a disjoint witness channel, fitted rates).
Bottom: the two outcome patterns, NS1-consistent flat rates versus a
falsifying state-dependent pattern. Illustrative schematic, no data.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams.update({
    "mathtext.fontset": "cm",
    "font.family": "serif",
    "font.serif": ["DejaVu Serif"],
})
DARK = "#2b2b2b"
rng = np.random.default_rng(20260709)

fig = plt.figure(figsize=(12.6, 9.0), dpi=200)
gs = fig.add_gridspec(2, 1, height_ratios=[0.85, 1.15], hspace=0.30)

# ---------------- top: protocol flow ----------------
axf = fig.add_subplot(gs[0])
axf.set_xlim(0, 12.6)
axf.set_ylim(0, 3.6)
axf.set_aspect("equal")
axf.axis("off")


def box(ax, cx, cy, w, h, title, sub, tfs=12.5, sfs=9.5):
    b = FancyBboxPatch((cx - w/2, cy - h/2), w, h,
                       boxstyle="round,pad=0.06,rounding_size=0.10",
                       facecolor="white", edgecolor="#9a9a9a", lw=1.1,
                       zorder=3)
    ax.add_patch(b)
    ax.text(cx, cy + 0.22, title, fontsize=tfs, color=DARK,
            ha="center", va="center", zorder=4)
    ax.text(cx, cy - 0.28, sub, fontsize=sfs, color="#6f6f6f",
            ha="center", va="center", zorder=4, linespacing=1.35)


def arrow(ax, p, q, faint=False):
    ar = FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=12,
                         lw=1.1 if not faint else 0.9,
                         color=DARK if not faint else "#9a9a9a",
                         shrinkA=4, shrinkB=4, zorder=2,
                         linestyle="solid" if not faint else (0, (3, 3)))
    ax.add_patch(ar)


box(axf, 2.15, 2.45, 3.5, 1.35, r"preparations $\rho_1,\dots,\rho_n$",
    "quantum state varied\nacross runs")
box(axf, 6.45, 2.45, 3.9, 1.35, r"fixed classical context $E$",
    "apparatus, coupling geometry,\ntemperature, calibration certified")
box(axf, 10.75, 2.45, 3.3, 1.35, r"fitted rates $\hat\lambda_\alpha$",
    "reduced-dynamics fits\nper preparation")
box(axf, 6.45, 0.65, 3.9, 0.95, "witness channel",
    r"monitors $E$, disjoint from the fitted rates", sfs=9.0)

arrow(axf, (3.95, 2.45), (4.45, 2.45))
arrow(axf, (8.45, 2.45), (9.05, 2.45))
arrow(axf, (6.45, 1.15), (6.45, 1.75), faint=True)

# ---------------- bottom: outcome patterns ----------------
axp = fig.add_subplot(gs[1])
n = 8
x = np.arange(1, n + 1)
lam_E = 1.00
err = 0.030
flat = lam_E + rng.normal(0, 0.011, n)
assert np.abs(flat - lam_E).max() < 2 * err, "flat series exceeds errors"
viol = 0.90 + 0.031 * x + rng.normal(0, 0.008, n)

axp.axhline(lam_E, color="#9a9a9a", lw=1.0, linestyle=(0, (5, 4)))
axp.text(0.62, lam_E + 0.012, r"$\Lambda_\alpha(E)$", fontsize=12,
         color="#777777", va="bottom")
axp.errorbar(x, flat, yerr=err, fmt="o", ms=6, color=DARK,
             ecolor="#8a8a8a", elinewidth=1.0, capsize=3,
             label="NS1-consistent: rates statistically"
                   " indistinguishable")
axp.errorbar(x, viol, yerr=err, fmt="s", ms=6, mfc="white",
             mec="#6f6f6f", ecolor="#b5b5b5", elinewidth=1.0, capsize=3,
             color="#6f6f6f",
             label="falsifying pattern: reproducible state dependence")
axp.set_xticks(x)
axp.set_xticklabels([f"$\\rho_{i}$" for i in x], fontsize=11)
axp.set_xlabel("state preparation, under witness-confirmed fixed $E$",
               fontsize=12.5)
axp.set_ylabel(r"fitted rate $\hat\lambda_\alpha$", fontsize=12.5)
axp.set_xlim(0.4, n + 0.6)
axp.legend(frameon=False, fontsize=10.5, loc="upper left")
axp.text(0.985, 0.035, "illustrative schematic, not data",
         transform=axp.transAxes, fontsize=11, color="#8a8a8a",
         ha="right", va="bottom", style="italic")
axp.tick_params(colors="#8a8a8a", labelsize=10)
for s in ("top", "right"):
    axp.spines[s].set_visible(False)
for s in ("left", "bottom"):
    axp.spines[s].set_color("#b5b5b5")

fig.savefig("../figures/fig_ns1_protocol_schematic.png",
            bbox_inches="tight", facecolor="white", pad_inches=0.12)
print("saved")
