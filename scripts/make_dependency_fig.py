"""
Dependency diagram for SSAF: primitives (Phi, E) feed the
context-indexed structural layer, which supports the derived
organization (envelopes, sequencing record, addressability quotient),
which is constrained by NS1, whose consequences include no-signalling,
exclusion of state-conditioned generator selection and the
rate-independence test. Arrows denote definitional or constraint
dependence only. Family style: grayscale, CM math.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

plt.rcParams.update({
    "mathtext.fontset": "cm",
    "font.family": "serif",
    "font.serif": ["DejaVu Serif"],
})
DARK = "#2b2b2b"

fig, ax = plt.subplots(figsize=(13.0, 9.2), dpi=200)
ax.set_xlim(0, 13.0)
ax.set_ylim(0, 9.2)
ax.set_aspect("equal")
ax.axis("off")


def box(cx, cy, w, h, title, sub=None, fill="white", edge="#9a9a9a",
        tfs=12, sfs=9.5):
    b = FancyBboxPatch((cx - w/2, cy - h/2), w, h,
                       boxstyle="round,pad=0.06,rounding_size=0.10",
                       facecolor=fill, edgecolor=edge, lw=1.1, zorder=3)
    ax.add_patch(b)
    if sub:
        ax.text(cx, cy + 0.16, title, fontsize=tfs, color=DARK,
                ha="center", va="center", zorder=4)
        ax.text(cx, cy - 0.22, sub, fontsize=sfs, color="#6f6f6f",
                ha="center", va="center", zorder=4)
    else:
        ax.text(cx, cy, title, fontsize=tfs, color=DARK,
                ha="center", va="center", zorder=4)


def arrow(p, q, faint=False):
    ar = FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=11,
                         lw=1.0 if not faint else 0.8,
                         color=DARK if not faint else "#b5b5b5",
                         shrinkA=3, shrinkB=3, zorder=2,
                         linestyle="solid" if not faint else (0, (3, 3)))
    ax.add_patch(ar)


# ---- tier 1: primitives ----
box(4.4, 8.55, 3.3, 0.85, r"$\Phi \equiv \mathcal{D}(\mathcal{H})$",
    "configuration space")
box(8.6, 8.55, 3.3, 0.85, r"classical context $E$",
    "fixed operational context")

# ---- tier 2: context-indexed structural layer ----
cont = Rectangle((0.55, 5.95), 11.9, 1.55, facecolor="#f4f4f4",
                 edgecolor="#c9c9c9", lw=1.0, zorder=1)
ax.add_patch(cont)
ax.text(0.75, 7.32, "context-indexed structural layer", fontsize=10,
        color="#8a8a8a", ha="left", va="center", style="italic")

y2 = 6.62
box(1.85, y2, 2.05, 0.95, r"$\mathcal{A}(E)$", "admissible set")
box(4.05, y2, 2.05, 0.95, r"$\mathrm{Compat}_E$", "compatibility")
box(6.25, y2, 2.05, 0.95, r"$\sim_E,\ \mathcal{O}(E)$", "addressability")
box(8.45, y2, 2.05, 0.95, r"$\Gamma_E,\ \mathcal{N}_E$", "connectivity")
box(10.65, y2, 2.05, 0.95, r"$\mu_E$", "admissibility measure")

arrow((4.4, 8.10), (5.4, 7.50))
arrow((8.6, 8.10), (7.6, 7.50))

# ---- tier 3: derived organization ----
y3 = 4.55
box(2.7, y3, 3.05, 1.0, r"envelopes $B_E$",
    "compatibility closure")
box(6.5, y3, 3.35, 1.0, r"sequencing record $S_E$",
    "strict partial order of restrictions")
box(10.3, y3, 3.05, 1.0, r"quotient $Q_E=\Phi/\!\sim_E$",
    "addressable classes")

arrow((1.85, 6.12), (2.35, 5.08))
arrow((4.05, 6.12), (3.15, 5.08))
arrow((1.85, 6.12), (5.35, 5.08))
arrow((6.25, 6.12), (6.5, 5.08))
arrow((8.45, 6.12), (7.35, 5.08), faint=True)
arrow((10.65, 6.12), (7.75, 5.08), faint=True)
arrow((6.25, 6.12), (9.7, 5.08))

# ---- tier 4: NS1 ----
y4 = 2.75
box(6.5, y4, 7.0, 1.05,
    r"NS1 dependency constraint",
    r"resolution-rate parameters indexed by $E$ alone, never by"
    r" $\rho$; updating remains linear CPTP")
arrow((2.7, 4.03), (4.6, 3.30))
arrow((6.5, 4.03), (6.5, 3.30))
arrow((10.3, 4.03), (8.4, 3.30))

# ---- tier 5: consequences ----
y5 = 0.95
box(2.6, y5, 3.2, 1.0, "no-signalling",
    "marginal invariance under local maps")
box(6.5, y5, 3.35, 1.0, "no state-conditioned",
    "generator selection under fixed context")
box(10.4, y5, 3.2, 1.0, "rate-independence test",
    "the experimental protocol")

arrow((5.0, 2.20), (3.3, 1.48))
arrow((6.5, 2.20), (6.5, 1.48))
arrow((8.0, 2.20), (9.7, 1.48))

fig.savefig("../figures/fig_dependency_diagram.png",
            bbox_inches="tight", facecolor="white", pad_inches=0.12)
print("saved")
