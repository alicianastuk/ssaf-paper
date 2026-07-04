"""
Sequencing record vs temporal reconstruction, single-panel redesign.
The record (black ink) is a strict partial order drawn as a Hasse
diagram: one vertical chain plus one dead-end branch. One monotone
labeling tau hovers beside the nodes in gray. The pair 3, 4 is
comparable as labels but incomparable in the record.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch

plt.rcParams.update({
    "mathtext.fontset": "cm",
    "font.family": "serif",
    "font.serif": ["DejaVu Serif"],
})

DARK = "#2b2b2b"
FILL = "#e9e9e9"
GRAY = "#8a8a8a"
FAINT = "#aaaaaa"

# the record: chain a -> b -> d -> e -> f, branch a -> c
nodes = {
    "a": (3.0, 6.15),
    "b": (2.0, 4.95),
    "c": (4.4, 4.95),
    "d": (2.0, 3.70),
    "e": (2.0, 2.45),
    "f": (2.0, 1.20),
}
edges = [("a", "b"), ("a", "c"), ("b", "d"), ("d", "e"), ("e", "f")]

# one monotone labeling tau, in gray beside each node
tau = {"a": "1", "b": "2", "c": "3", "d": "4", "e": "5", "f": "6"}
# label offsets: chain labels sit left, branch label sits right
off = {
    "a": (-0.62, 0.10),
    "b": (-0.62, 0.00),
    "c": (0.62, 0.00),
    "d": (-0.62, 0.00),
    "e": (-0.62, 0.00),
    "f": (-0.62, 0.00),
}

R = 0.30

fig, ax = plt.subplots(figsize=(10.5, 7.0), dpi=200)
ax.set_xlim(0, 10.5)
ax.set_ylim(0, 7.0)
ax.set_aspect("equal")
ax.axis("off")

# arrows first (under nodes)
for u, v in edges:
    ar = FancyArrowPatch(nodes[u], nodes[v], arrowstyle="-|>",
                         mutation_scale=13, lw=1.4, color=DARK,
                         shrinkA=24, shrinkB=24, zorder=2)
    ax.add_patch(ar)

# nodes and gray tau labels
for name, (x, y) in nodes.items():
    ax.add_patch(Circle((x, y), R, facecolor=FILL,
                        edgecolor=DARK, lw=1.2, zorder=3))
    dx, dy = off[name]
    ax.text(x + dx, y + dy, tau[name], fontsize=16, color=GRAY,
            ha="center", va="center", zorder=4, style="italic")

# annotation: the incomparable pair
note_x, note_y = 6.35, 3.55
ax.plot([note_x - 0.10, nodes["c"][0] + 0.24],
        [note_y + 0.55, nodes["c"][1] - 0.26],
        lw=0.9, color=FAINT, linestyle=(0, (2, 3)), zorder=1)
ax.plot([note_x - 0.10, nodes["d"][0] + 0.34],
        [note_y - 0.10, nodes["d"][1] + 0.02],
        lw=0.9, color=FAINT, linestyle=(0, (2, 3)), zorder=1)
ax.text(note_x, note_y,
        "labels 3 and 4 compare as numbers,\n"
        "but no path joins these nodes:\n"
        "the record does not order them.\n"
        "Exchanging 3 and 4 gives an\n"
        "equally valid labeling $\\tau$.",
        fontsize=12.5, color="#777777", ha="left", va="center",
        linespacing=1.45)

# legend: ink vs pencil
ax.text(5.25, 0.30,
        "black: realized sequencing record (prerequisite arrows)"
        "        gray: one monotone labeling $\\tau$ (bookkeeping only)",
        fontsize=11.5, color="#666666", ha="center", va="center")

fig.savefig("../figures/fig_sequencing_partial_order.png",
            bbox_inches="tight", facecolor="white")
print("saved")
