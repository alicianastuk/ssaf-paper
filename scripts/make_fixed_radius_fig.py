"""
Trajectory witness on the fixed-radius sphere, rebuilt from the toy's
own 3D surrogate (eq:toy_basin_flow):

    dx/dtau = -k(E) x + Omega(E) x  (cross product),  k > 0.

The direction x-hat precesses on a cone of fixed inclination about
Omega(E): a circle on the unit sphere. The script integrates the ODE
numerically (RK4) and asserts the caption's invariance claim before
saving. A faint band shows the same witness under slow context
re-indexing of Omega, the only licensed source of apparent axis drift.
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

# ---- fixed-context parameters ----
k = 0.15
Omega = 2.2 * np.array([0.30, 0.22, 0.93])
Omega_hat = Omega / np.linalg.norm(Omega)

def rhs(x, Om):
    return -k * x + np.cross(Om, x)

def integrate(x0, Om_of_t, T=14.0, dt=0.002):
    n = int(T / dt)
    xs = np.empty((n, 3))
    x = x0.astype(float)
    for i in range(n):
        Om = Om_of_t(i * dt)
        k1 = rhs(x, Om)
        k2 = rhs(x + 0.5*dt*k1, Om)
        k3 = rhs(x + 0.5*dt*k2, Om)
        k4 = rhs(x + dt*k3, Om)
        x = x + (dt/6.0)*(k1 + 2*k2 + 2*k3 + k4)
        xs[i] = x
    return xs

# initial condition at ~40 degrees from Omega
perp = np.cross(Omega_hat, [0.0, 0.0, 1.0])
perp /= np.linalg.norm(perp)
alpha0 = np.deg2rad(40.0)
x0 = np.cos(alpha0)*Omega_hat + np.sin(alpha0)*perp

# ---- fixed E: the invariance case ----
xs = integrate(x0, lambda t: Omega)
dirs = xs / np.linalg.norm(xs, axis=1)[:, None]
incl = np.degrees(np.arccos(dirs @ Omega_hat))
dev = incl.max() - incl.min()
assert dev < 1e-3, f"inclination drifted by {dev} degrees"
print(f"assertion passed: inclination invariant to {dev:.2e} degrees "
      f"(mean {incl.mean():.3f} deg)")

# ---- slow re-indexing of Omega: the licensed drift case ----
def Om_drift(t):
    ang = 0.16 * t
    c, s = np.cos(ang), np.sin(ang)
    R = np.array([[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]])
    return R @ Omega

xs2 = integrate(x0, Om_drift, T=40.0)
dirs2 = xs2 / np.linalg.norm(xs2, axis=1)[:, None]

# ---- draw ----
fig = plt.figure(figsize=(9.6, 8.8), dpi=200)
ax = fig.add_subplot(111, projection="3d")

u = np.linspace(0, 2*np.pi, 36)
v = np.linspace(0, np.pi, 19)
U, V = np.meshgrid(u, v)
ax.plot_wireframe(np.cos(U)*np.sin(V), np.sin(U)*np.sin(V), np.cos(V),
                  color="#dedede", lw=0.4, rstride=1, cstride=1)

# re-indexing band, faint, drawn first
ax.plot(dirs2[:, 0], dirs2[:, 1], dirs2[:, 2], color="#c4c4c4", lw=0.55)

# fixed-E circle, dark
ax.plot(dirs[:, 0], dirs[:, 1], dirs[:, 2], color="#000000", lw=1.7)
ax.scatter(*dirs[0], color=DARK, s=34, depthshade=False)

# the generator axis
ax.plot([-1.30*Omega_hat[0], 1.30*Omega_hat[0]],
        [-1.30*Omega_hat[1], 1.30*Omega_hat[1]],
        [-1.30*Omega_hat[2], 1.30*Omega_hat[2]],
        color="#6f6f6f", lw=1.2)
ax.text(1.38*Omega_hat[0], 1.38*Omega_hat[1], 1.38*Omega_hat[2],
        r"$\Omega(E)$", fontsize=14, color=DARK)

# style
ax.set_box_aspect((1, 1, 1))
for pane in (ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane):
    pane.set_visible(False)
ax.grid(False)
ax.set_xticks([-1, 0, 1]); ax.set_yticks([-1, 0, 1]); ax.set_zticks([-1, 0, 1])
ax.tick_params(colors="#9a9a9a", labelsize=8, pad=-2)
ax.set_xlabel(r"$\hat x_1$", fontsize=12, color=DARK, labelpad=-6)
ax.set_ylabel(r"$\hat x_2$", fontsize=12, color=DARK, labelpad=-6)
ax.set_zlabel(r"$\hat x_3$", fontsize=12, color=DARK, labelpad=-6)
ax.xaxis.line.set_color("#b5b5b5")
ax.yaxis.line.set_color("#b5b5b5")
ax.zaxis.line.set_color("#b5b5b5")
ax.view_init(elev=20, azim=-55)

fig.text(0.5, 0.035,
         "dark: fixed $E$, inclination about $\\Omega(E)$ invariant"
         "        light: slow context re-indexing of $\\Omega$, the only"
         " licensed drift",
         fontsize=11.5, color="#666666", ha="center")

fig.subplots_adjust(left=0, right=1, bottom=0.05, top=1)
fig.savefig("../figures/fig_spin_proxy_trajectory_fixed_radius_sphere.png",
            bbox_inches="tight", facecolor="white", pad_inches=0.15)
print("saved")
