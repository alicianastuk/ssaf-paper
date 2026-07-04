"""
Toy basin flow surrogate, regenerated from the paper's own equation
(eq:toy_basin_flow_multifactor):

    dx/dtau = -k(E) x + omega(E) J x,   k > 0,  J skew.

Two-dimensional chart, closed-form solution
    r(tau) = r0 exp(-k tau),  theta(tau) = theta0 + omega tau.

The script asserts the caption's claim (strict radial contraction)
before saving. Family style: grayscale, CM math, no in-image titles.
Parameters: k = 0.18, omega = 2.4, r0 = 0.72, tau in [0, 28].
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({
    "mathtext.fontset": "cm",
    "font.family": "serif",
    "font.serif": ["DejaVu Serif"],
})

DARK = "#2b2b2b"

# ---- surrogate parameters (indexed by fixed E) ----
k = 0.18           # contraction strength, k(E) > 0
omega = 2.4        # circulation weight, omega(E)
r0, th0 = 0.72, 0.35
tau = np.linspace(0.0, 28.0, 6000)

# ---- closed-form solution of the linear surrogate ----
r = r0 * np.exp(-k * tau)
th = th0 + omega * tau
x1 = r * np.cos(th)
x2 = r * np.sin(th)

# ---- verify the caption's claim before drawing ----
radii = np.hypot(x1, x2)
assert np.all(np.diff(radii) < 0), "radial contraction is not strict"
print(f"assertion passed: ||x(tau)|| strictly decreasing "
      f"({radii[0]:.3f} -> {radii[-1]:.2e})")

# ---- draw ----
fig, ax = plt.subplots(figsize=(7.6, 7.2), dpi=200)
ax.plot(x1, x2, color=DARK, lw=1.0)
ax.plot(x1[0], x2[0], "o", ms=7, markerfacecolor="white",
        markeredgecolor=DARK, markeredgewidth=1.3, zorder=5)

ax.set_aspect("equal")
ax.set_xlim(-0.85, 0.85)
ax.set_ylim(-0.85, 0.85)
ax.set_xlabel(r"$x_1$", fontsize=14, color=DARK)
ax.set_ylabel(r"$x_2$", fontsize=14, color=DARK, rotation=0, labelpad=10)
ax.tick_params(colors="#8a8a8a", labelsize=10)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_color("#b5b5b5")

ax.text(0.985, 0.02,
        "$k(E)=0.18$,  $\\omega(E)=2.4$,  $\\tau\\in[0,28]$",
        transform=ax.transAxes, fontsize=10.5, color="#777777",
        ha="right", va="bottom")

fig.savefig("../figures/fig_toy_basin_flow_spiral.png",
            bbox_inches="tight", facecolor="white", pad_inches=0.12)
print("saved")
