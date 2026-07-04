"""
Spin-axis proxy, two panels.
(a) Bounded tip-path family on the representation sphere: persistence.
(b) Under the declared antipodal identification a ~ -a the
representation space is RP^2; a path joining an axis to its antipode
closes into a genuinely non-contractible loop. Its double traversal is
contractible: the Z/2 loop structure.
Family style: grayscale, CM math, no in-image titles.
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

fig = plt.figure(figsize=(15.0, 7.6), dpi=200)


def style_axes(ax):
    ax.set_box_aspect((1, 1, 1))
    for pane in (ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane):
        pane.set_visible(False)
    ax.grid(False)
    ax.set_xticks([-1, 0, 1]); ax.set_yticks([-1, 0, 1]); ax.set_zticks([-1, 0, 1])
    ax.tick_params(colors="#9a9a9a", labelsize=8, pad=-2)
    ax.set_xlabel(r"$\hat a_x$", fontsize=12, color=DARK, labelpad=-6)
    ax.set_ylabel(r"$\hat a_y$", fontsize=12, color=DARK, labelpad=-6)
    ax.set_zlabel(r"$\hat a_z$", fontsize=12, color=DARK, labelpad=-6)
    ax.xaxis.line.set_color("#b5b5b5")
    ax.yaxis.line.set_color("#b5b5b5")
    ax.zaxis.line.set_color("#b5b5b5")
    ax.view_init(elev=16, azim=-58)


def wire_sphere(ax):
    u = np.linspace(0, 2*np.pi, 36)
    v = np.linspace(0, np.pi, 19)
    U, V = np.meshgrid(u, v)
    ax.plot_wireframe(np.cos(U)*np.sin(V), np.sin(U)*np.sin(V), np.cos(V),
                      color="#dcdcdc", lw=0.4, rstride=1, cstride=1)


# ---------------- panel (a): bounded wobble family ----------------
ax1 = fig.add_subplot(121, projection="3d")
wire_sphere(ax1)
t = np.linspace(0, 14*np.pi, 4000)
theta = 0.62 + 0.20*np.cos(6.31*t + 0.4)
phi = t
ax1.plot(np.sin(theta)*np.cos(phi), np.sin(theta)*np.sin(phi),
         np.cos(theta), color=DARK, lw=0.85)
mask = (t >= 2*np.pi) & (t <= 4*np.pi)
ax1.plot(np.sin(theta[mask])*np.cos(phi[mask]),
         np.sin(theta[mask])*np.sin(phi[mask]),
         np.cos(theta[mask]), color="#000000", lw=1.6)
style_axes(ax1)

# ---------------- panel (b): antipodal loop in RP^2 ----------------
ax2 = fig.add_subplot(122, projection="3d")
wire_sphere(ax2)

# endpoints: an axis and its antipode
th0, ph0 = 0.55, 0.85
a0 = np.array([np.sin(th0)*np.cos(ph0), np.sin(th0)*np.sin(ph0),
               np.cos(th0)])
# orthonormal companions
n = np.cross(a0, [0.0, 0.0, 1.0]); n /= np.linalg.norm(n)
m = np.cross(a0, n)

s = np.linspace(0, np.pi, 500)
wig = 0.10*np.sin(3*s)
path = (np.outer(np.cos(s), a0) + np.outer(np.sin(s), n)
        + np.outer(wig, m))
path /= np.linalg.norm(path, axis=1)[:, None]
ax2.plot(path[:, 0], path[:, 1], path[:, 2], color="#000000", lw=1.7)

# endpoint markers
ax2.scatter(*a0, color=DARK, s=42, depthshade=False)
ax2.scatter(*(-a0), facecolors="white", edgecolors=DARK, s=46,
            linewidths=1.3, depthshade=False)
ax2.text(a0[0]+0.10, a0[1]+0.05, a0[2]+0.12, r"$\hat{a}$",
         fontsize=14, color=DARK)
ax2.text(-a0[0]-0.05, -a0[1]-0.05, -a0[2]-0.30,
         r"$-\hat{a}\;(\equiv\hat{a})$",
         fontsize=14, color=DARK)
style_axes(ax2)

# ---------------- panel tags and note ----------------
fig.text(0.27, 0.045, "(a) bounded circulation family", fontsize=13,
         color="#555555", ha="center")
fig.text(0.76, 0.045,
         "(b) endpoints identified under $\\hat{a}\\sim-\\hat{a}$:"
         " the loop closes and is non-contractible",
         fontsize=13, color="#555555", ha="center")

fig.subplots_adjust(left=0.0, right=1.0, bottom=0.06, top=1.0,
                    wspace=0.02)
fig.savefig("../figures/fig_spin_axis_proxy_noncontractible.png",
            bbox_inches="tight", facecolor="white", pad_inches=0.15)
print("saved")
