"""
Standalone two-qubit PPT scatter, regenerated from the same seeded
Hilbert-Schmidt Monte Carlo machinery as the simulation panel figure.
Asserts the caption's coexistence claim from the data before saving.
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
rng = np.random.default_rng(20260705)

N = 6000

def ginibre_state(d=4):
    G = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
    rho = G @ G.conj().T
    return rho / np.trace(rho).real

def partial_transpose_B(rho):
    r = rho.reshape(2, 2, 2, 2)
    return r.transpose(0, 3, 2, 1).reshape(4, 4)

def marginal_A(rho):
    r = rho.reshape(2, 2, 2, 2)
    return np.einsum('abcb->ac', r)

wit = np.empty(N); pur = np.empty(N)
for i in range(N):
    rho = ginibre_state()
    wit[i] = np.linalg.eigvalsh(partial_transpose_B(rho)).min()
    rA = marginal_A(rho)
    pur[i] = np.trace(rA @ rA).real

ent = wit < 0.0
lo, hi = np.quantile(pur, [0.05, 0.95])
mask = (pur > lo) & (pur < hi)
assert ent[mask].any() and (~ent[mask]).any(), "no coexistence"
print(f"assertion passed: coexistence holds, entangled fraction "
      f"{ent.mean():.3f}")

fig, ax = plt.subplots(figsize=(9.4, 6.6), dpi=200)
ax.scatter(pur[ent], wit[ent], s=5, color="#4a4a4a", alpha=0.45,
           linewidths=0, label="entangled")
ax.scatter(pur[~ent], wit[~ent], s=5, color="#b9b9b9", alpha=0.6,
           linewidths=0, label="separable")
ax.axhline(0.0, color=DARK, lw=1.0)
ax.set_xlabel(r"marginal purity $\mathrm{Tr}(\rho_A^2)$", fontsize=13)
ax.set_ylabel(r"$\min\lambda(\rho_{AB}^{T_B})$", fontsize=13)
ax.legend(frameon=False, fontsize=11, loc="upper right")
ax.text(0.985, 0.03, f"$N={N}$, Hilbert--Schmidt ensemble",
        transform=ax.transAxes, fontsize=10, color="#777777",
        ha="right", va="bottom")
ax.tick_params(colors="#8a8a8a", labelsize=10)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_color("#b5b5b5")

fig.savefig("../figures/fig_toy_entanglement_ppt_vs_marginal_purity.png",
            bbox_inches="tight", facecolor="white", pad_inches=0.12)
print("saved")
