"""Rebuild the slide's editable SVGs: uv run python img/s01-ad/create_figures.py."""

import base64
import math
from pathlib import Path
import urllib.request
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
SVG = "http://www.w3.org/2000/svg"
INK = "http://www.inkscape.org/namespaces/inkscape"
ET.register_namespace("", SVG)
ET.register_namespace("inkscape", INK)
BLUE = "#326ba8"
TEXT = "#24344b"
GRAY = "#65758b"
MIRROR = "https://huggingface.co/datasets/Voxel51/mvtec-ad/resolve/30a183a3b96e3aef953f230784b123b719b09d97/"
SAMPLES = [
    ("normal-01.png", "data/data_24/348.png"),
    ("normal-02.png", "data/data_24/374.png"),
    ("normal-03.png", "data/data_24/360.png"),
    ("test-hole.png", "data/data_29/002-57.png"),
]


def element(parent, tag, **attrs):
    return ET.SubElement(parent, f"{{{SVG}}}{tag}", {k.replace("_", "-"): str(v) for k, v in attrs.items()})


def text(parent, x, y, content, size=26, color=TEXT, anchor="start", weight="normal"):
    e = element(parent, "text", x=x, y=y, fill=color, font_size=size,
                font_family="DejaVu Sans, sans-serif", text_anchor=anchor, font_weight=weight)
    e.text = content
    return e


def layer(root, name):
    g = element(root, "g", id=name.lower().replace(" ", "-"))
    g.set(f"{{{INK}}}groupmode", "layer")
    g.set(f"{{{INK}}}label", name)
    return g


def canvas(title, description):
    root = ET.Element(f"{{{SVG}}}svg", {"width": "1200", "height": "440", "viewBox": "0 0 1200 440"})
    element(root, "title").text = title
    element(root, "desc").text = description
    element(layer(root, "Background"), "rect", width=1200, height=440, fill="white")
    return root


def save(root, name):
    ET.indent(root)
    ET.ElementTree(root).write(ROOT / name, encoding="utf-8", xml_declaration=True)


def arrow(parent, x1, x2, y):
    element(parent, "path", d=f"M{x1},{y} H{x2} M{x2-12},{y-9} L{x2},{y} L{x2-12},{y+9}",
            fill="none", stroke=GRAY, stroke_width=3, stroke_linecap="round", stroke_linejoin="round")


def hazelnuts():
    assets = ROOT / "assets"
    assets.mkdir(exist_ok=True)
    for name, remote in SAMPLES:
        target = assets / name
        if not target.exists():
            print(f"Downloading {name}", flush=True)
            with urllib.request.urlopen(MIRROR + remote, timeout=45) as response:
                data = response.read()
            if not data.startswith(b"\x89PNG\r\n\x1a\n"):
                raise ValueError(f"Invalid PNG: {remote}")
            target.write_bytes(data)

    root = canvas("Finding anomalous patterns in images", "Three normal MVTec AD hazelnuts provide a reference. A test hazelnut with a hole asks: Is this normal?")
    labels = layer(root, "Labels and questions")
    text(labels, 40, 54, "Normal examples", 30, weight="bold")
    text(labels, 865, 54, "Test image", 30, weight="bold")
    images = layer(root, "Hazelnut photographs")
    for name, x, y, side in [
        ("normal-01.png", 40, 100, 205),
        ("normal-02.png", 265, 100, 205),
        ("normal-03.png", 490, 100, 205),
        ("test-hole.png", 865, 88, 230),
    ]:
        image = element(images, "image", x=x, y=y, width=side, height=side,
                        preserveAspectRatio="xMidYMid meet", id=name.removesuffix(".png"))
        image.set("href", "data:image/png;base64," + base64.b64encode((assets / name).read_bytes()).decode())
    arrow(layer(root, "Flow arrow"), 750, 815, 203)
    text(labels, 368, 357, "What does normal look like?", 25, GRAY, "middle")
    text(labels, 980, 357, "Is this normal?", 29, BLUE, "middle", "bold")
    text(labels, 40, 417, "Images: MVTec AD · © MVTec Software GmbH · CC BY-NC-SA 4.0", 16, GRAY)
    save(root, "hazelnuts.svg")


def signal(t):
    return 0.68 * math.sin(2 * math.pi * t) + 0.12 * math.sin(4 * math.pi * t + 0.4)


def curve(parent, x, width, cycles, spike=False):
    points = []
    for i in range(601):
        u = i / 600
        value = signal(cycles * u)
        if spike:
            value += 2.3 * math.exp(-((u - 0.76) / 0.012) ** 2)
        points.append(f"{x + width*u:.2f},{233 - 48*value:.2f}")
    element(parent, "polyline", points=" ".join(points), fill="none", stroke=BLUE,
            stroke_width=3.5, stroke_linecap="round", stroke_linejoin="round")


def timeseries():
    root = canvas("Finding anomalous patterns in a time series", "A repeating normal reference is followed by a test signal. One ordinary segment and one spike segment each ask: Is this normal? The signal is synthetic.")
    labels = layer(root, "Labels and questions")
    text(labels, 40, 54, "Normal pattern", 30, weight="bold")
    text(labels, 570, 54, "Test signal", 30, weight="bold")
    regions = layer(root, "Question regions")
    for x, width in [(608, 127), (959, 103)]:
        element(regions, "rect", x=x, y=99, width=width, height=217, rx=8,
                fill="#edf3fa", stroke="#a6b9ce", stroke_width=1.5, stroke_dasharray="6 5")
    axes = layer(root, "Axes")
    for x, width in [(70, 370), (590, 540)]:
        element(axes, "path", d=f"M{x},96 V316 H{x+width+12}", fill="none", stroke=GRAY, stroke_width=1.5)
        element(axes, "path", d=f"M{x},233 H{x+width}", fill="none", stroke="#d9e1eb", stroke_width=1)
        text(labels, x+width, 344, "Time", 18, GRAY, "end")
    text(labels, 40, 89, "Signal", 18, GRAY)
    text(labels, 570, 89, "Signal", 18, GRAY)
    waves = layer(root, "Signal curves")
    curve(waves, 70, 370, 4)
    curve(waves, 590, 540, 6, spike=True)
    arrow(layer(root, "Flow arrow"), 480, 530, 220)
    for center in (671.5, 1010.5):
        element(regions, "path", d=f"M{center},318 V355", fill="none", stroke="#a6b9ce", stroke_width=1.5)
        text(labels, center, 387, "Is this normal?", 24, BLUE, "middle", "bold")
    text(labels, 40, 417, "Illustrative synthetic signal", 16, GRAY)
    save(root, "time-series.svg")


if __name__ == "__main__":
    hazelnuts()
    timeseries()
    print("Created hazelnuts.svg and time-series.svg")
