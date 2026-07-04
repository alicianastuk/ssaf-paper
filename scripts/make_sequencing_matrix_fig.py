"""
The sequencing record as a pairwise comparison matrix, beside the
matrix the timeline claims. The record's matrix has genuinely empty
cells (incomparable pairs). A monotone reconstruction fills every
cell by fiat. Highlighted cells are the invented entries.
Poset: 1<2,4,5,6 (chain), 1<3 (branch); 3 incomparable to 2,4,5,6.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

plt.rcParams.update({
    "mathtext.fontset": "cm",
    "font.family": "serif",
    "font.serif": ["DejaVu Serif"],
})

DARK = "#2b2b2b"
GRAY = "#8a8a8a"
DIAG = "#efefef"
HOLE = "#f7f4ea"      # warm blank: a genuinely empty cell
INVENT = "#e8dfc8"    # invented entry in the completion

# strict order of the record (row precedes column)
prec = {(1,2),(1,3),(1,4),(1,5),(1,6),
        (2,4),(2,5),(2,6),
        (4,5),(4,6),
        (5,6)}
incomp = {(2,3),(3,2),(3,4),(4,3),(3,5),(5,3),(3,6),(6,3)}

n = 6
cs = 0.78   # cell size

fig, ax = plt.subplots(figsize=(12.6, 7.0), dpi=200)
ax.set_xlim(0, 12.6)
ax.set_ylim(0, 7.0)
ax.set_aspect("equal")
ax.axis("off")


def draw_matrix(ox, oy, completed, title):
    ax.text(ox + n*cs/2, oy + n*cs + 0.62, title, fontsize=15,
            color=DARK, ha="center", va="center")
    for i in range(1, n+1):        # row (top to bottom)
        for j in range(1, n+1):    # column
            x = ox + (j-1)*cs
            y = oy + (n-i)*cs
            if i == j:
                face = DIAG
            elif (i, j) in incomp and not completed:
                face = HOLE
            elif (i, j) in incomp and completed:
                face = INVENT
            else:
                face = "white"
            ax.add_patch(Rectangle((x, y), cs, cs, facecolor=face,
                                   edgecolor="#c9c9c9", lw=0.8))
            if i == j:
                continue
            if (i, j) in prec:
                sym = r"$\prec$"
            elif (j, i) in prec:
                sym = r"$\succ$"
            elif completed:
                sym = r"$\prec$" if i < j else r"$\succ$"
            else:
                sym = ""
            if sym:
                col = GRAY if ((i, j) in incomp and completed) else DARK
                ax.text(x + cs/2, y + cs/2, sym, fontsize=13,
                        color=col, ha="center", va="center")
    # row and column labels
    for k in range(1, n+1):
        ax.text(ox - 0.30, oy + (n-k)*cs + cs/2, str(k), fontsize=12.5,
                color=GRAY, ha="center", va="center", style="italic")
        ax.text(ox + (k-1)*cs + cs/2, oy + n*cs + 0.24, str(k),
                fontsize=12.5, color=GRAY, ha="center", va="center",
                style="italic")


oy = 1.35
draw_matrix(1.0, oy, completed=False,
            title=r"Sequencing record $S_E$: pairwise verdicts")
draw_matrix(7.2, oy, completed=True,
            title=r"Completion under a monotone labeling $\tau$")

# legend
ax.add_patch(Rectangle((1.0, 0.42), 0.30, 0.30, facecolor=HOLE,
                       edgecolor="#c9c9c9", lw=0.8))
ax.text(1.42, 0.57, "no verdict in the record: structural incomparability",
        fontsize=11.5, color="#777777", ha="left", va="center")
ax.add_patch(Rectangle((7.2, 0.42), 0.30, 0.30, facecolor=INVENT,
                       edgecolor="#c9c9c9", lw=0.8))
ax.text(7.62, 0.57, "entries supplied by the reconstruction only",
        fontsize=11.5, color="#777777", ha="left", va="center")

fig.savefig("../figures/fig_sequencing_matrix.png",
            bbox_inches="tight", facecolor="white")
print("saved")
