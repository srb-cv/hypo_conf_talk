"""Create the editable Deep SVDD diagram with uv run python img/s02-dsvdd/create_figure.py."""

import math
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
NS = "http://www.w3.org/2000/svg"
INK = "http://www.inkscape.org/namespaces/inkscape"
ET.register_namespace("", NS)
ET.register_namespace("inkscape", INK)
BLUE = "#326ba8"
RED = "#cf574f"
TEXT = "#24344b"
GRAY = "#68788d"


def add(parent, tag, **attrs):
    return ET.SubElement(parent, f"{{{NS}}}{tag}", {k.replace("_", "-"): str(v) for k, v in attrs.items()})


def label(parent, x, y, value, size=24, color=TEXT, weight="normal", anchor="middle"):
    node = add(parent, "text", x=x, y=y, font_family="DejaVu Sans, sans-serif",
               font_size=size, fill=color, font_weight=weight, text_anchor=anchor)
    node.text = value


def layer(root, name):
    g = add(root, "g", id=name.lower().replace(" ", "-"))
    g.set(f"{{{INK}}}groupmode", "layer")
    g.set(f"{{{INK}}}label", name)
    return g


def arrow(g, x1, x2, y):
    add(g, "path", d=f"M{x1},{y} H{x2} M{x2-12},{y-8} L{x2},{y} L{x2-12},{y+8}",
        fill="none", stroke=GRAY, stroke_width=3, stroke_linejoin="round", stroke_linecap="round")


def diamond(g, x, y):
    add(g, "path", d=f"M{x},{y-7} L{x+7},{y} L{x},{y+7} L{x-7},{y} Z",
        fill=RED, stroke="white", stroke_width=1.5)


root = ET.Element(f"{{{NS}}}svg", width="1400", height="550", viewBox="0 0 1400 550")
add(root, "title").text = "Deep SVDD learns compact normal representations"
add(root, "desc").text = (
    "Input samples are mapped through a neural network into a feature space. "
    "Normal representations cluster near a center c inside a compact hypersphere; "
    "illustrative anomalous test representations lie farther away. "
    "The hypersphere is illustrated as a two-dimensional cross-section."
)
add(layer(root, "Background"), "rect", width=1400, height=550, fill="white")
labels = layer(root, "Headings and explanations")
for x, title, subtitle in [
    (210, "Input data", "Normal training samples"),
    (690, "Neural network", "Learn the representation φ(x; W)"),
    (1165, "Representation space", "Compact hypersphere"),
]:
    label(labels, x, 48, title, 29, weight="bold")
    label(labels, x, 86, subtitle, 21, GRAY)

axes = layer(root, "Coordinate axes")
for x, width in [(65, 315), (975, 355)]:
    add(axes, "path", d=f"M{x},137 V418 H{x+width}", fill="none", stroke="#a6b3c2", stroke_width=1.6)
    add(axes, "path", d=f"M{x-5},147 L{x},137 L{x+5},147 M{x+width-10},413 L{x+width},418 L{x+width-10},423",
        fill="none", stroke="#a6b3c2", stroke_width=1.6)

samples = layer(root, "Normal input samples")
for i in range(32):
    u = i / 31
    x = 97 + 259*u + 8*math.sin(i*2.1)
    y = 204 + 161*math.sin(u*math.pi/2) + 14*math.sin(i*2.4)
    add(samples, "circle", cx=f"{x:.2f}", cy=f"{y:.2f}", r=5.5, fill=BLUE)
label(labels, 218, 461, "Normal patterns in the data", 21, BLUE)

flow = layer(root, "Mapping arrows")
arrow(flow, 413, 480, 273)
arrow(flow, 899, 948, 273)

network = layer(root, "Neural network connections")
columns = [(520, [207, 251, 295, 339]),
           (624, [163, 207, 251, 295, 339, 383]),
           (728, [185, 229, 273, 317, 361]),
           (832, [229, 273, 317])]
for (x1, ys1), (x2, ys2) in zip(columns, columns[1:]):
    for y1 in ys1:
        for y2 in ys2:
            add(network, "line", x1=x1, y1=y1, x2=x2, y2=y2, stroke="#b5c8dd", stroke_width=1.3)
nodes = layer(root, "Neural network nodes")
for x, ys in columns:
    for y in ys:
        add(nodes, "circle", cx=x, cy=y, r=11, fill="#e8f0fa", stroke=BLUE, stroke_width=2)
label(labels, 680, 461, "Bring normal representations together", 21, BLUE)

sphere = layer(root, "Compact hypersphere")
cx, cy, radius = 1151, 276, 102
add(sphere, "circle", cx=cx, cy=cy, r=radius, fill="#edf4fb", stroke=BLUE, stroke_width=2.5)
representations = layer(root, "Normal representations")
for i in range(28):
    angle = i*math.pi*(3-math.sqrt(5))
    r = 64*math.sqrt((i+0.5)/28)
    add(representations, "circle", cx=f"{cx+r*math.cos(angle):.2f}",
        cy=f"{cy+r*math.sin(angle):.2f}", r=4.5, fill=BLUE)
center = layer(root, "Center and radius")
add(center, "circle", cx=cx, cy=cy, r=5, fill=TEXT, stroke="white", stroke_width=1.5)
label(center, cx-13, cy+22, "c", 23)
angle = -0.37
ex, ey = cx+radius*math.cos(angle), cy+radius*math.sin(angle)
add(center, "line", x1=cx, y1=cy, x2=ex, y2=ey, stroke=TEXT, stroke_width=1.7, stroke_dasharray="4 4")
label(center, cx+62, cy-30, "R", 23)
anomalies = layer(root, "Anomalous test representations")
for x, y in [(1019, 204), (1194, 134), (1297, 240), (1224, 397)]:
    diamond(anomalies, x, y)
label(labels, 1195, 115, "Anomalous test sample", 19, RED)
label(labels, 1165, 461, "Farther from c → higher anomaly score", 20, TEXT)

legend = layer(root, "Legend and learning message")
add(legend, "circle", cx=71, cy=514, r=5.5, fill=BLUE)
label(legend, 87, 521, "Normal", 18, BLUE, anchor="start")
diamond(legend, 205, 514)
label(legend, 221, 521, "Anomalous", 18, RED, anchor="start")
label(legend, 1370, 521, "Learn from normal data · Score new samples by distance to c", 21,
      anchor="end")

ET.indent(root)
ET.ElementTree(root).write(ROOT / "deep-svdd.svg", encoding="utf-8", xml_declaration=True)
print("Created deep-svdd.svg")
