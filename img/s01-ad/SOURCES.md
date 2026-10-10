# Figure sources and editing

Open `hazelnuts.svg` or `time-series.svg` in Inkscape. Text, arrows, axes,
question regions, and signal curves are editable vector elements in named layers.
The hazelnut photographs are embedded PNGs, making the SVG self-contained;
original downloaded PNGs are also retained in `assets/`.

## Hazelnut photographs

Source: MVTec AD, copyright MVTec Software GmbH.
Official dataset: https://www.mvtec.com/research-teaching/datasets/mvtec-ad
License: CC BY-NC-SA 4.0, https://creativecommons.org/licenses/by-nc-sa/4.0/
The hazelnut composition is distributed under the same license.

Downloaded from the Voxel51 mirror of MVTec AD, revision
`30a183a3b96e3aef953f230784b123b719b09d97`:
https://huggingface.co/datasets/Voxel51/mvtec-ad

| Local asset | Mirror path | Dataset annotation |
| --- | --- | --- |
| assets/normal-01.png | data/data_24/348.png | hazelnut, train, good |
| assets/normal-02.png | data/data_24/374.png | hazelnut, train, good |
| assets/normal-03.png | data/data_24/360.png | hazelnut, train, good |
| assets/test-hole.png | data/data_29/002-57.png | hazelnut, test, hole |

Citation: Paul Bergmann, Michael Fauser, David Sattlegger, and Carsten Steger.
MVTec AD — A Comprehensive Real-World Dataset for Unsupervised Anomaly Detection.
CVPR, 2019.

## Time series

Synthetic repeating signal with a narrow added spike in the test signal.
Both queried regions have the same styling to leave the audience's answer open.
No empirical data or measured anomaly detection results are implied.

## Rebuild

Run from the project root:

```sh
uv run python img/s01-ad/create_figures.py
```

Rebuilding replaces the generated SVGs, so preserve any manual Inkscape edits
before rerunning. Existing PNG assets are reused.
