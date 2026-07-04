# State Space Admissibility Framework (SSAF)

Source repository for the SSAF manuscript, v1.0 (December 2025, revised
July 2026).

Author: Alicia Nastuk
ORCID: [0009-0004-8124-8653](https://orcid.org/0009-0004-8124-8653)

## Contents

`main.tex` and `refs.bib` are the complete manuscript source (RevTeX
4.2, single author, approximately 345 pages compiled). `figures/`
contains the fifteen figures the manuscript includes. `scripts/`
contains the fourteen Python generators that produce them; run any
script from inside `scripts/` and it writes its figure into
`figures/`.

## Reproducibility

Several generators are verifying figures: they assert the claims made
in their corresponding captions before saving, and refuse to produce
output otherwise. These include strict radial contraction
(`make_basin_flow_fig.py`), inclination invariance under fixed context
via direct numerical integration (`make_fixed_radius_fig.py`),
positivity, marginal invariance to machine precision and
negativity-shift stress bounds for the Bell-diagonal pair
(`make_bell_pair_figs.py`), coexistence and no-separable-bin claims for
the two-qubit PPT Monte Carlo (`make_twoqubit_ppt_fig.py`,
`make_ppt_scatter_fig.py`), negativity monotonicity over 8000
adversarial local-channel applications (`make_onesided_fig.py`), and
Gibbs passivity over 5000 Haar-random cyclic protocols
(`make_activity_fig.py`). All randomized generators use fixed seeds.

The executable verification suite for the manuscript's finite toy
constructions lives in a companion repository:
[ssaf-verification](https://github.com/alicianastuk/ssaf-verification).

## Building

Requires a TeX Live installation with RevTeX 4.2 (package
`texlive-publishers` on Debian/Ubuntu). From the repository root:

```
latexmk -pdf main.tex
```

Figure regeneration requires Python 3 with numpy and matplotlib.

## Provenance

Mathematical formalization, structural auditing, LaTeX engineering,
figure generation and the verification suites were carried out with
substantial assistance from Anthropic's Claude, directed by the author;
the framework, its concepts and final responsibility for the content
are the author's. Full disclosure appears in the manuscript's
acknowledgments.

## Citation

Please cite the versioned Zenodo record for this manuscript (DOI to be
added upon deposit).
