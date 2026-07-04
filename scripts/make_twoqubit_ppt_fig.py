"""
Two-qubit PPT Monte Carlo, real simulation replacing a fabricated
panel. Samples 8000 density matrices from the Hilbert-Schmidt (Ginibre)
ensemble, computes the PPT witness min eigenvalue of the partial
transpose and the marginal purity Tr(rho_A^2), and renders the three
panels the caption describes. Asserts from the data: (1) witness
computation sane on known states; (2) entangled and separable points
coexist at the same marginal purity; (3) no marginal-purity bin is
fully separable. Seeded for reproducibility.
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
rng = np.random.default_rng(20260704)

N = 8000

def ginibre_state(d=4):
    G = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
    rho = G @ G.conj().T
    return rho / np.trace(rho).real

def partial_transpose_B(rho):
    r = rho.reshape(2, 2, 2, 2)          # (a, b, a', b')
    return r.transpose(0, 3, 2, 1).reshape(4, 4)

def marginal_A(rho):
    r = rho.reshape(2, 2, 2, 2)
    return np.einsum('abcb->ac', r)

# ---- sanity assertions on known states ----
bell = np.zeros((4, 4), dtype=complex)
v = np.array([1, 0, 0, 1]) / np.sqrt(2)
bell = np.outer(v, v.conj())
assert np.linalg.eigvalsh(partial_transpose_B(bell)).min() < -0.49
prod = np.diag([1.0, 0, 0, 0]).astype(complex)
assert np.linalg.eigvalsh(partial_transpose_B(prod)).min() > -1e-12
print("sanity: Bell negative, product non-negative")

# ---- Monte Carlo ----
wit = np.empty(N)
pur = np.empty(N)
for i in range(N):
    rho = ginibre_state()
    wit[i] = np.linalg.eigvalsh(partial_transpose_B(rho)).min()
    rA = marginal_A(rho)
    pur[i] = np.trace(rA @ rA).real

ent = wit < 0.0
print(f"entangled fraction (HS ensemble): {ent.mean():.3f}")

# ---- caption claim assertions ----
# coexistence at the same marginal purity
lo, hi = np.quantile(pur, [0.05, 0.95])
mask = (pur > lo) & (pur < hi)
assert ent[mask].any() and (~ent[mask]).any(), "no coexistence"
# no purity bin fully separable (bins with enough samples)
bins = np.linspace(pur.min(), pur.max(), 21)
idx = np.digitize(pur, bins)
fracs, centers = [], []
for b in range(1, len(bins)):
    sel = idx == b
    if sel.sum() >= 30:
        fracs.append(ent[sel].mean())
        centers.append(0.5 * (bins[b-1] + bins[b]))
fracs = np.array(fracs); centers = np.array(centers)
assert (fracs > 0).all(), "a purity bin recovered separability"
print(f"assertions passed: coexistence and min bin fraction "
      f"{fracs.min():.3f}")

# ---- draw ----
fig = plt.figure(figsize=(12.6, 9.0), dpi=200)
gs = fig.add_gridspec(2, 2, height_ratios=[1.35, 1.0], hspace=0.33,
                      wspace=0.26)

axs = fig.add_subplot(gs[0, 0])
axs.scatter(pur[ent], wit[ent], s=5, color="#4a4a4a", alpha=0.45,
            linewidths=0, label="entangled")
axs.scatter(pur[~ent], wit[~ent], s=5, color="#b9b9b9", alpha=0.6,
            linewidths=0, label="separable")
axs.axhline(0.0, color=DARK, lw=1.0)
axs.set_xlabel(r"marginal purity $\mathrm{Tr}(\rho_A^2)$", fontsize=12)
axs.set_ylabel(r"$\min\lambda(\rho_{AB}^{T_B})$", fontsize=12)
axs.legend(frameon=False, fontsize=10, loc="upper left")

axh = fig.add_subplot(gs[0, 1])
axh.hist(wit, bins=60, color="#8a8a8a", edgecolor="white", lw=0.3)
axh.axvline(0.0, color=DARK, lw=1.0, linestyle=(0, (4, 3)))
axh.set_xlabel(r"$\min\lambda(\rho_{AB}^{T_B})$", fontsize=12)
axh.set_ylabel("number of states", fontsize=12)
axh.text(0.97, 0.95, f"$N={N}$\nentangled: {100*ent.mean():.1f}\\%",
         transform=axh.transAxes, ha="right", va="top", fontsize=10.5,
         color="#555555")

axf = fig.add_subplot(gs[1, :])
axf.plot(centers, fracs, color=DARK, lw=1.4, marker="o", ms=3.5)
axf.set_ylim(0, 1.02)
axf.set_xlabel(r"marginal purity $\mathrm{Tr}(\rho_A^2)$", fontsize=12)
axf.set_ylabel("fraction entangled", fontsize=12)

for ax in (axs, axh, axf):
    ax.tick_params(colors="#8a8a8a", labelsize=9.5)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#b5b5b5")

fig.savefig("../figures/fig_toy_twoqubit_ppt_simulation_panel.png",
            bbox_inches="tight", facecolor="white", pad_inches=0.12)
print("saved")
