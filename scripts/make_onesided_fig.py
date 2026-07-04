"""
One-sided local CPTP updating, hard mode made real.
Samples two-qubit states with negativity <= N_max, attacks each with
20 Haar-random local CPTP channels on B, and plots initial negativity
against the WORST CASE (maximum) post-channel negativity. Asserts
monotonicity for every (state, channel) pair and envelope preservation
before saving. Seeded.
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
rng = np.random.default_rng(20260707)

N_STATES, N_CHANNELS, N_MAX, K_ENV = 400, 20, 0.20, 3

def ginibre_state(d=4):
    G = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
    rho = G @ G.conj().T
    return rho / np.trace(rho).real

def negativity(rho):
    r = rho.reshape(2, 2, 2, 2).transpose(0, 3, 2, 1).reshape(4, 4)
    ev = np.linalg.eigvalsh(r)
    return float(-ev[ev < 0].sum())

def random_local_channel_kraus():
    M = rng.normal(size=(2 * K_ENV, 2)) + 1j * rng.normal(size=(2 * K_ENV, 2))
    Q, _ = np.linalg.qr(M)          # 2k x 2 isometry
    return [Q[2*i:2*i+2, :] for i in range(K_ENV)]

I2 = np.eye(2)

# ---- sample envelope states ----
states, before = [], []
while len(states) < N_STATES:
    rho = ginibre_state()
    n = negativity(rho)
    if n <= N_MAX:
        states.append(rho)
        before.append(n)
before = np.array(before)

# ---- adversarial channel attack ----
worst = np.empty(N_STATES)
violations = 0
for i, rho in enumerate(states):
    best = 0.0
    for _ in range(N_CHANNELS):
        kraus = random_local_channel_kraus()
        out = sum(np.kron(I2, K) @ rho @ np.kron(I2, K).conj().T
                  for K in kraus)
        n_after = negativity(out)
        if n_after > before[i] + 1e-9:
            violations += 1
        best = max(best, n_after)
    worst[i] = best

assert violations == 0, f"{violations} monotonicity violations"
assert worst.max() <= N_MAX + 1e-9, "envelope violated"
print(f"assertions passed: 0 violations over "
      f"{N_STATES * N_CHANNELS} channel applications; "
      f"max worst-case after = {worst.max():.3f} <= {N_MAX}")

# ---- draw ----
fig, ax = plt.subplots(figsize=(8.6, 6.8), dpi=200)
ax.scatter(before, worst, s=10, color="#4a4a4a", alpha=0.55,
           linewidths=0)
lim = N_MAX * 1.05
ax.plot([0, N_MAX], [0, N_MAX], color=DARK, lw=1.0)
ax.axhline(N_MAX, color="#8a8a8a", lw=1.0, linestyle=(0, (5, 4)))
ax.text(0.003, N_MAX + 0.004, r"declared envelope $N_{\max}$",
        fontsize=10.5, color="#777777", va="bottom")
ax.text(0.135, 0.152, "monotonicity bound", fontsize=10.5,
        color="#555555", rotation=38)
ax.set_xlim(-0.004, lim); ax.set_ylim(-0.004, lim + 0.012)
ax.set_xlabel(r"negativity before local CPTP on $B$", fontsize=12.5)
ax.set_ylabel("worst case negativity after\n"
              r"(max over 20 random local channels)", fontsize=12.5)
ax.tick_params(colors="#8a8a8a", labelsize=10)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_color("#b5b5b5")
ax.text(0.985, 0.03,
        f"$N={N_STATES}$ states, {N_CHANNELS} channels each",
        transform=ax.transAxes, fontsize=10, color="#777777",
        ha="right", va="bottom")

fig.savefig("../figures/Onesidedentanglement.png",
            bbox_inches="tight", facecolor="white", pad_inches=0.12)
print("saved")
