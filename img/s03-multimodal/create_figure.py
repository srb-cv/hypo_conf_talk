"""Extend the supplied vector fusion diagram: uv run python img/s03-multimodal/create_figure.py."""

from copy import deepcopy
import math
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
SVG = "http://www.w3.org/2000/svg"
INK = "http://www.inkscape.org/namespaces/inkscape"
ET.register_namespace("", SVG)
ET.register_namespace("inkscape", INK)
BLUE, RED, TEXT, GRAY = "#326ba8", "#cf574f", "#24344b", "#68788d"


def add(parent, tag, **attrs):
    return ET.SubElement(parent, f"{{{SVG}}}{tag}", {k.replace("_", "-"): str(v) for k, v in attrs.items()})


def layer(root, name):
    g = add(root, "g", id=name.lower().replace(" ", "-"))
    g.set(f"{{{INK}}}groupmode", "layer")
    g.set(f"{{{INK}}}label", name)
    return g


def text(parent, x, y, content, size=24, fill=TEXT, weight="normal", anchor="middle"):
    node = add(parent, "text", x=x, y=y, fill=fill, font_family="DejaVu Sans, sans-serif",
               font_size=size, font_weight=weight, text_anchor=anchor)
    node.text = content


source = ET.parse(ROOT / "input/fusion.svg").getroot()
root = ET.Element(f"{{{SVG}}}svg", width="1500", height="560", viewBox="0 0 1500 560")
add(root, "title").text = "Multimodal Deep SVDD learns a hypersphere over fused representations"
add(root, "desc").text = (
    "Modalities A, B, and C are fused into a combined representation z. Deep SVDD maps "
    "that combined representation into a space where normal samples lie in a compact "
    "hypersphere centered at c. Red diamonds illustrate anomalous test representations. "
    "The sphere is drawn as a two-dimensional cross-section."
)
add(layer(root, "Background"), "rect", width=1500, height=560, fill="white")
defs = source.find(f"{{{SVG}}}defs")
if defs is not None:
    root.append(deepcopy(defs))

# Preserve the supplied fusion drawing as vector objects, replacing its empty output circle.
fusion = layer(root, "Original modality fusion")
placement = add(fusion, "g", transform="translate(35,120) scale(5.3)")
drawing = deepcopy(source.find(f"{{{SVG}}}g"))
for child in list(drawing):
    if child.get("id") == "g5":
        drawing.remove(child)
placement.append(drawing)

labels = layer(root, "Headings and labels")
text(labels, 355, 48, "Fuse multiple modalities", 31, weight="bold")
text(labels, 1170, 48, "Learn a compact hypersphere", 31, weight="bold")
text(labels, 355, 87, "One combined representation per sample", 23, GRAY)
text(labels, 1170, 87, "Normality in the fused representation space", 23, GRAY)
text(labels, 660, 503, "Fused representation z", 24, TEXT)

mapping = layer(root, "Deep SVDD mapping")
add(mapping, "path", d="M735,301 H958 M943,289 L958,301 L943,313", fill="none",
    stroke=BLUE, stroke_width=4, stroke_linecap="round", stroke_linejoin="round")
text(mapping, 846, 258, "Deep SVDD", 29, BLUE, "bold")
text(mapping, 846, 345, "φ(z; W)", 26, BLUE)

sphere = layer(root, "Hypersphere in combined representation space")
cx, cy, radius = 1180, 295, 127
add(sphere, "circle", cx=cx, cy=cy, r=radius, fill="#edf4fb", stroke=BLUE, stroke_width=3)
points = layer(root, "Normal fused representations")
for i in range(32):
    angle = i*math.pi*(3-math.sqrt(5))
    r = 79*math.sqrt((i+0.5)/32)
    add(points, "circle", cx=f"{cx+r*math.cos(angle):.2f}",
        cy=f"{cy+r*math.sin(angle):.2f}", r=5.7, fill=BLUE)

center = layer(root, "Center and radius")
add(center, "circle", cx=cx, cy=cy, r=5.5, fill=TEXT, stroke="white", stroke_width=1.5)
text(center, cx-15, cy+27, "c", 26)
angle = -0.36
add(center, "line", x1=cx, y1=cy, x2=cx+radius*math.cos(angle),
    y2=cy+radius*math.sin(angle), stroke=TEXT, stroke_width=2, stroke_dasharray="5 5")
text(center, cx+75, cy-35, "R", 25)

anomalies = layer(root, "Anomalous test representations")
for x, y in [(1018, 228), (1233, 135), (1353, 259), (1280, 445)]:
    add(anomalies, "path", d=f"M{x},{y-8} L{x+8},{y} L{x},{y+8} L{x-8},{y} Z",
        fill=RED, stroke="white", stroke_width=1.5)
text(labels, 1180, 476, "Normal samples cluster near c", 24, BLUE)
text(labels, 1180, 512, "Anomalous samples lie farther away", 23, RED)

ET.indent(root)
ET.ElementTree(root).write(ROOT / "multimodal-deep-svdd.svg", encoding="utf-8", xml_declaration=True)
print("Created multimodal-deep-svdd.svg")
