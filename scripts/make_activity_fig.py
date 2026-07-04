"""
Activity without leverage, rebuilt as a verified qubit experiment.
Left: persistent Heisenberg correlation C(n) = Re Tr[X T^n(X) omega]
under a fixed unitary step, no decay. Right: extracted work
W_ext = Tr[(omega - U omega U^dag) H] over Haar-random cyclic
unitaries; Gibbs passivity forces W_ext <= 0. Assertions: positive
variance (activity), persistence (no decay), passivity across the
whole sample. Seeded.
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
rng = np.random.default_rng(20260708)

sx = np.array([[0, 1], [1, 0]], dtype=complex)
sz = np.array([[1, 0], [0, -1]], dtype=complex)

# ---- fixed context: Hamiltonian and Gibbs reference state ----
beta = 1.70
H = sz
w = np.diag(np.exp(-beta * np.diag(H).real))
omega = w / np.trace(w).real

# activity: variance of sigma_x in omega
var_x = np.real(np.trace(omega @ sx @ sx) - np.trace(omega @ sx)**2)
assert var_x > 0.5, "no activity present"

# ---- left panel: persistent correlation ----
theta = 0.233
U0 = np.array([[np.exp(-1j * theta), 0], [0, np.exp(1j * theta)]])
steps = np.arange(60)
X = sx.copy()
C = []
Xn = sx.copy()
for n in steps:
    C.append(np.real(np.trace(sx @ Xn @ omega)))
    Xn = U0.conj().T @ Xn @ U0
C = np.array(C)
# persistence: amplitude in the final quarter matches the global one
assert np.abs(C[45:]).max() > 0.9 * np.abs(C).max(), "correlation decayed"

# ---- right panel: cyclic unitary protocols ----
N_U = 5000
W = np.empty(N_U)
E0 = np.real(np.trace(omega @ H))
for i in range(N_U):
    M = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
    Q, R = np.linalg.qr(M)
    Q = Q @ np.diag(np.diag(R) / np.abs(np.diag(R)))
    W[i] = E0 - np.real(np.trace(Q @ omega @ Q.conj().T @ H))

assert W.max() <= 1e-12, f"passivity violated: max W = {W.max()}"
print(f"assertions passed: Var = {var_x:.3f} > 0, persistence holds, "
      f"passivity over {N_U} protocols (max W = {W.max():.2e}, "
      f"min W = {W.min():.3f})")

# ---- draw ----
fig, (axl, axr) = plt.subplots(1, 2, figsize=(13.2, 5.6), dpi=200)

axl.plot(steps, C, color=DARK, lw=1.1, marker="o", ms=3.2)
axl.axhline(0, color="#c9c9c9", lw=0.8)
axl.set_xlabel(r"step $n$", fontsize=12.5)
axl.set_ylabel(r"$C(n)=\mathrm{Re}\,\mathrm{Tr}"
               r"[X\,T^{n}(X)\,\omega_E]$", fontsize=12.5)

axr.hist(W, bins=60, color="#8a8a8a", edgecolor="white", lw=0.3)
axr.axvline(0, color=DARK, lw=1.0, linestyle=(0, (4, 3)))
axr.set_xlabel(r"$W_{\mathrm{ext}}(U;\omega_E)$", fontsize=12.5)
axr.set_ylabel("count", fontsize=12.5)
axr.text(0.03, 0.96,
         f"qubit, $\\beta={beta}$\n"
         f"$\\mathrm{{Var}}_\\omega(\\sigma_x)={var_x:.3f}$\n"
         f"$\\max W_{{\\mathrm{{ext}}}}={W.max():.1e}$\n"
         f"$N={N_U}$ Haar unitaries",
         transform=axr.transAxes, fontsize=10.5, color="#555555",
         ha="left", va="top", linespacing=1.5)

for ax in (axl, axr):
    ax.tick_params(colors="#8a8a8a", labelsize=10)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#b5b5b5")

fig.subplots_adjust(wspace=0.26)
fig.savefig("../figures/activity_without_leverage.png",
            bbox_inches="tight", facecolor="white", pad_inches=0.12)
print("saved")
