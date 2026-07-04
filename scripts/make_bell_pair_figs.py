"""
Bell-diagonal pair, both subfigures from one shared ensemble.
(1) bell_diagonal_before_after.png: correlation-plane projection
    before and after a local Pauli channel on B.
(2) entanglement_band_negativity.png: same projection, before-states
    colored by negativity.
Assertions: sampled and post-channel states PSD; A's marginal invariant
under the local channel to machine precision. Seeded.
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
rng = np.random.default_rng(20260706)

I2 = np.eye(2)
sx = np.array([[0, 1], [1, 0]], dtype=complex)
sy = np.array([[0, -1j], [1j, 0]])
sz = np.array([[1, 0], [0, -1]], dtype=complex)
paulis = [sx, sy, sz]

def bell_diag(c):
    rho = np.eye(4, dtype=complex)
    for ci, s in zip(c, paulis):
        rho = rho + ci * np.kron(s, s)
    return rho / 4.0

# ---- rejection-sample valid Bell-diagonal states ----
N = 800
cs = []
while len(cs) < N:
    c = rng.uniform(-1, 1, 3)
    if np.linalg.eigvalsh(bell_diag(c)).min() >= 0:
        cs.append(c)
cs = np.array(cs)
states = [bell_diag(c) for c in cs]

# ---- local Pauli channel on B, Kraus form ----
p = np.array([0.60, 0.20, 0.10, 0.10])
kraus = [np.sqrt(p[0]) * np.kron(I2, I2)] + \
        [np.sqrt(pk) * np.kron(I2, s) for pk, s in zip(p[1:], paulis)]

def apply_channel(rho):
    return sum(K @ rho @ K.conj().T for K in kraus)

def marginal_A(rho):
    r = rho.reshape(2, 2, 2, 2)
    return np.einsum('abcb->ac', r)

def corr(rho, s):
    return np.real(np.trace(rho @ np.kron(s, s)))

def negativity(rho):
    r = rho.reshape(2, 2, 2, 2).transpose(0, 3, 2, 1).reshape(4, 4)
    ev = np.linalg.eigvalsh(r)
    return float(-ev[ev < 0].sum())

after = [apply_channel(r) for r in states]

# ---- assertions ----
for r in states + after:
    assert np.linalg.eigvalsh(r).min() > -1e-12, "state not PSD"
dev = max(np.abs(marginal_A(a) - marginal_A(b)).max()
          for a, b in zip(after, states))
assert dev < 1e-12, f"marginal of A moved by {dev}"
print(f"assertions passed: all states PSD, marginal A invariant "
      f"to {dev:.1e}")

zz_b = np.array([corr(r, sz) for r in states])
xx_b = np.array([corr(r, sx) for r in states])
zz_a = np.array([corr(r, sz) for r in after])
xx_a = np.array([corr(r, sx) for r in after])
neg = np.array([negativity(r) for r in states])
print(f"entangled (negativity > 0): {(neg > 1e-12).mean():.3f}")

def style(ax):
    ax.set_xlabel(r"$\langle Z\otimes Z\rangle$", fontsize=13)
    ax.set_ylabel(r"$\langle X\otimes X\rangle$", fontsize=13)
    ax.set_xlim(-1.05, 1.05); ax.set_ylim(-1.05, 1.05)
    ax.set_aspect("equal")
    ax.tick_params(colors="#8a8a8a", labelsize=10)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#b5b5b5")

# ---- figure 1: before/after ----
fig, ax = plt.subplots(figsize=(7.4, 7.0), dpi=200)
ax.scatter(zz_b, xx_b, s=9, color="#b9b9b9", linewidths=0,
           label="admissible states, before")
ax.scatter(zz_a, xx_a, s=12, color=DARK, marker="x", linewidths=0.9,
           label="after local Pauli channel on $B$")
style(ax)
ax.legend(frameon=False, fontsize=10.5, loc="lower right")
fig.savefig("../figures/bell_diagonal_before_after.png",
            bbox_inches="tight", facecolor="white", pad_inches=0.1)

# ---- stress test: joint diagnostic moves, marginal does not ----
neg_after = np.array([negativity(r) for r in after])
dneg = np.abs(neg_after - neg)
print(f"stress test: max |Delta negativity| = {dneg.max():.3f}, "
      f"mean = {dneg.mean():.3f}, vs marginal deviation {dev:.1e}")
assert dneg.max() > 0.05, "channel barely moves the joint diagnostic"

# ---- figure 2: negativity coloring, before and after ----
fig2, ax2 = plt.subplots(figsize=(7.9, 7.0), dpi=200)
vmax = max(neg.max(), neg_after.max(), 1e-9)
sc = ax2.scatter(zz_b, xx_b, s=12, c=neg, cmap="Greys", vmin=0,
                 vmax=vmax, linewidths=0.2, edgecolors="#999999",
                 label="before")
ax2.scatter(zz_a, xx_a, s=16, c=neg_after, cmap="Greys", vmin=0,
            vmax=vmax, marker="x", linewidths=0.9,
            label="after local channel on $B$")
ax2.legend(frameon=False, fontsize=10.5, loc="lower right")
style(ax2)
cb = fig2.colorbar(sc, ax=ax2, fraction=0.046, pad=0.03)
cb.set_label("negativity", fontsize=12, color=DARK)
cb.ax.tick_params(colors="#8a8a8a", labelsize=9)
cb.outline.set_edgecolor("#b5b5b5")
fig2.savefig("../figures/entanglement_band_negativity.png",
             bbox_inches="tight", facecolor="white", pad_inches=0.1)
print("saved both")
