"""
Scholar Network Visualization Generator

Read scholar notes from an Obsidian vault, build a coauthorship network, and
generate a self-contained interactive HTML visualization.

Examples:
    python scripts/scholar_network.py --vault-root /path/to/your/vault
    python scripts/scholar_network.py --vault-root /path/to/your/vault --output /tmp/network.html

If no --vault-root is supplied, the script defaults to the repository root and
falls back to ./vault-starter when present. That makes the starter kit usable
out of the box while still supporting real vaults.
"""

from __future__ import annotations

import argparse
import colorsys
import io
import re
import sys
from collections import Counter
from pathlib import Path

import networkx as nx
from pyvis.network import Network
import yaml

# Windows consoles may still default to a non-UTF-8 codepage.
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DEFAULT_REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_COLOR = "#9E9E9E"
OTHER_FAMILY = "Other"

AUTO_FAMILY_BASE_PALETTE = [
    "#1F77B4",
    "#43A047",
    "#EF6C00",
    "#8E24AA",
    "#00897B",
    "#6D4C41",
    "#D81B60",
    "#546E7A",
    "#C0CA33",
    "#5E35B1",
]

TOPIC_GLUE_LENGTH = 300
FAMILY_GLUE_LENGTH = 420

ROLE_SIZES = {
    "gatekeeper": 40,
    "active": 25,
    "emerging": 18,
    "peripheral": 14,
    "stub": 10,
}

DEFAULT_SIZE = 20


VAULT_ROOT = DEFAULT_REPO_ROOT
SCHOLARS_DIR = VAULT_ROOT / "Scholars"
VOCAB_FILE = SCHOLARS_DIR / "_Scholar Topic Vocabulary.md"
OUTPUT_FILE = SCHOLARS_DIR / "scholar_network.html"

TOPIC_FAMILY_ORDER: list[str] = []
TOPIC_TO_FAMILY: dict[str, str] = {}
FAMILY_TO_TOPICS: dict[str, list[str]] = {}
FAMILY_COLOR_OVERRIDES: dict[str, str] = {}
FAMILY_BASE_COLORS: dict[str, str] = {OTHER_FAMILY: DEFAULT_COLOR}
TOPIC_COLORS: dict[str, str] = {}


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate an interactive scholar-network HTML file from Scholars/*.md notes."
    )
    parser.add_argument(
        "--vault-root",
        type=Path,
        default=DEFAULT_REPO_ROOT,
        help=(
            "Path to the vault root. Defaults to the repository root. "
            "If that root contains no Scholars/ folder but does contain "
            "vault-starter/Scholars/, the script will use vault-starter automatically."
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional output HTML path. Defaults to <vault-root>/Scholars/scholar_network.html",
    )
    return parser


def resolve_vault_root(candidate: Path) -> Path:
    candidate = candidate.resolve()

    if (candidate / "Scholars").exists():
        return candidate

    starter_candidate = candidate / "vault-starter"
    if (starter_candidate / "Scholars").exists():
        return starter_candidate

    return candidate


def configure_runtime(vault_root_arg: Path, output_arg: Path | None) -> None:
    global VAULT_ROOT, SCHOLARS_DIR, VOCAB_FILE, OUTPUT_FILE
    global TOPIC_FAMILY_ORDER, TOPIC_TO_FAMILY, FAMILY_TO_TOPICS
    global FAMILY_COLOR_OVERRIDES, FAMILY_BASE_COLORS, TOPIC_COLORS

    VAULT_ROOT = resolve_vault_root(vault_root_arg)
    SCHOLARS_DIR = VAULT_ROOT / "Scholars"
    VOCAB_FILE = SCHOLARS_DIR / "_Scholar Topic Vocabulary.md"
    OUTPUT_FILE = output_arg.resolve() if output_arg else (SCHOLARS_DIR / "scholar_network.html")

    (
        TOPIC_FAMILY_ORDER,
        TOPIC_TO_FAMILY,
        FAMILY_TO_TOPICS,
        FAMILY_COLOR_OVERRIDES,
    ) = parse_topic_vocabulary(VOCAB_FILE)
    FAMILY_BASE_COLORS = generate_family_base_colors(TOPIC_FAMILY_ORDER, FAMILY_COLOR_OVERRIDES)
    TOPIC_COLORS = generate_topic_colors(FAMILY_TO_TOPICS)


def parse_topic_vocabulary(
    filepath: Path,
) -> tuple[list[str], dict[str, str], dict[str, list[str]], dict[str, str]]:
    family_order: list[str] = []
    topic_to_family: dict[str, str] = {}
    family_to_topics: dict[str, list[str]] = {}
    family_color_overrides: dict[str, str] = {}

    try:
        lines = filepath.read_text(encoding="utf-8").splitlines()
    except OSError:
        return family_order, topic_to_family, family_to_topics, family_color_overrides

    current_family: str | None = None
    in_topics_section = False

    for line in lines:
        section_heading = re.match(r"^##\s+(.+?)\s*$", line)
        if section_heading:
            section_name = section_heading.group(1).strip()
            in_topics_section = section_name.startswith("Topics")
            if not in_topics_section:
                current_family = None
            continue

        if not in_topics_section:
            continue

        heading = re.match(r"^###\s+(.+?)(?:\s+\{color=(#[0-9A-Fa-f]{6})\})?\s*$", line)
        if heading:
            current_family = heading.group(1).strip()
            override_color = heading.group(2)
            if current_family not in family_to_topics:
                family_order.append(current_family)
                family_to_topics[current_family] = []
            if override_color:
                family_color_overrides[current_family] = override_color.upper()
            continue

        if not current_family:
            continue

        topic_match = re.match(r"^\|\s*`([^`]+)`\s*\|", line)
        if topic_match:
            topic = topic_match.group(1).strip()
            topic_to_family[topic] = current_family
            family_to_topics[current_family].append(topic)

    return family_order, topic_to_family, family_to_topics, family_color_overrides


def hex_to_hls(hex_color: str) -> tuple[float, float, float]:
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16) / 255
    g = int(hex_color[2:4], 16) / 255
    b = int(hex_color[4:6], 16) / 255
    return colorsys.rgb_to_hls(r, g, b)


def hls_to_hex(h: float, l: float, s: float) -> str:
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return "#{:02X}{:02X}{:02X}".format(
        round(r * 255),
        round(g * 255),
        round(b * 255),
    )


def generate_family_base_colors(
    family_order: list[str],
    family_color_overrides: dict[str, str],
) -> dict[str, str]:
    family_base_colors: dict[str, str] = {OTHER_FAMILY: DEFAULT_COLOR}
    known_families = [family for family in family_order if family != OTHER_FAMILY]
    n_families = len(known_families)

    for idx, family in enumerate(known_families):
        if family in family_color_overrides:
            family_base_colors[family] = family_color_overrides[family]
            continue

        if idx < len(AUTO_FAMILY_BASE_PALETTE):
            family_base_colors[family] = AUTO_FAMILY_BASE_PALETTE[idx]
            continue

        hue = (0.58 + (idx - len(AUTO_FAMILY_BASE_PALETTE)) / max(1, n_families)) % 1.0
        family_base_colors[family] = hls_to_hex(hue, 0.42, 0.62)

    return family_base_colors


def generate_topic_colors(family_to_topics: dict[str, list[str]]) -> dict[str, str]:
    topic_colors: dict[str, str] = {}

    for family, topics in family_to_topics.items():
        if not topics:
            continue

        base_hex = FAMILY_BASE_COLORS.get(family, DEFAULT_COLOR)
        hue, lightness, saturation = hex_to_hls(base_hex)
        count = len(topics)

        for idx, topic in enumerate(topics):
            if count == 1:
                topic_colors[topic] = base_hex
                continue

            position = idx / (count - 1)
            shade_lightness = min(0.72, max(0.28, lightness + (position - 0.5) * 0.26))
            shade_saturation = min(0.82, max(0.38, saturation + (0.5 - abs(position - 0.5)) * 0.08))
            topic_colors[topic] = hls_to_hex(hue, shade_lightness, shade_saturation)

    return topic_colors


def topic_family(topic: str) -> str:
    return TOPIC_TO_FAMILY.get(topic, OTHER_FAMILY)


def ordered_families_in_use(scholars: list[dict]) -> list[str]:
    family_counts = Counter(s["topic_family"] for s in scholars)
    ordered = [family for family in TOPIC_FAMILY_ORDER if family in family_counts]
    extras = sorted(family for family in family_counts if family not in TOPIC_FAMILY_ORDER)
    return ordered + extras


def choose_anchor(scholars: list[dict]) -> dict:
    return max(
        scholars,
        key=lambda s: (
            1 if s["role"] == "gatekeeper" else 0,
            len(s["coauthors"]),
            s["name"],
        ),
    )


def parse_frontmatter(filepath: Path) -> dict | None:
    try:
        text = filepath.read_text(encoding="utf-8")
    except OSError:
        return None

    match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return None

    try:
        frontmatter = yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return None

    return frontmatter if isinstance(frontmatter, dict) else None


def strip_wikilink(value: str) -> str:
    match = re.match(r"\[\[([^\]|]+?)(?:\|[^\]]+)?\]\]", value.strip())
    return match.group(1) if match else value.strip()


def load_scholars() -> list[dict]:
    scholars: list[dict] = []

    for md_file in SCHOLARS_DIR.glob("*.md"):
        if md_file.name.startswith("_"):
            continue

        fm = parse_frontmatter(md_file)
        if fm is None or fm.get("type") != "scholar":
            continue

        topics = fm.get("primary_topics", []) or []
        coauthors_raw = fm.get("top_coauthors", []) or []
        coauthor_papers = fm.get("coauthor_papers", []) or []
        representative_papers = fm.get("representative_papers", []) or []

        papers_str = ""
        if isinstance(representative_papers, list):
            lines = []
            for paper in representative_papers[:5]:
                if isinstance(paper, dict):
                    title = paper.get("title", "")
                    year = paper.get("year", "")
                    journal = paper.get("journal", "")
                    lines.append(f"  {title} ({journal}, {year})")
            papers_str = "\n".join(lines)

        scholars.append(
            {
                "name": fm.get("name", md_file.stem),
                "topics": topics,
                "primary_topic": topics[0] if topics else "unclassified",
                "topic_family": topic_family(topics[0] if topics else "unclassified"),
                "coauthors": [strip_wikilink(coauthor) for coauthor in coauthors_raw],
                "coauthor_papers": coauthor_papers,
                "role": fm.get("role", "active"),
                "affiliation": fm.get("affiliation", ""),
                "status": fm.get("status", "active"),
                "fields": fm.get("fields", []) or [],
                "recent_focus": fm.get("recent_focus", ""),
                "papers_str": papers_str,
            }
        )

    return scholars


def build_graph(scholars: list[dict]) -> nx.Graph:
    graph = nx.Graph()
    scholar_names = {scholar["name"] for scholar in scholars}

    for scholar in scholars:
        tooltip = (
            f"<b>{scholar['name']}</b><br>"
            f"<i>{scholar['affiliation']}</i><br>"
            f"Role: {scholar['role']}<br>"
            f"Field: {scholar['topic_family']}<br>"
            f"Topics: {', '.join(scholar['topics'])}<br>"
        )
        if scholar["recent_focus"]:
            tooltip += f"Recent: {scholar['recent_focus']}<br>"
        if scholar["papers_str"]:
            tooltip += f"<br>Key papers:<br>{scholar['papers_str'].replace(chr(10), '<br>')}"

        color = TOPIC_COLORS.get(scholar["primary_topic"], DEFAULT_COLOR)
        size = ROLE_SIZES.get(scholar["role"], DEFAULT_SIZE)
        is_gatekeeper = scholar["role"] == "gatekeeper"
        border_width = 6 if is_gatekeeper else 1
        border_color = "#FFD700" if is_gatekeeper else color

        shadow = (
            {"enabled": True, "color": "rgba(255,215,0,0.6)", "size": 14, "x": 0, "y": 0}
            if is_gatekeeper
            else {"enabled": True, "color": "rgba(0,0,0,0.15)", "size": 8, "x": 2, "y": 2}
        )

        graph.add_node(
            scholar["name"],
            label=scholar["name"],
            title=tooltip,
            color={
                "background": color,
                "border": border_color,
                "highlight": {"background": color, "border": "#FFD700"},
            },
            size=size,
            borderWidth=border_width,
            shadow=shadow,
            font={"size": 14, "color": "#333333"},
        )

    for scholar in scholars:
        for idx, coauthor in enumerate(scholar["coauthors"]):
            if coauthor not in scholar_names:
                continue

            weight = scholar["coauthor_papers"][idx] if idx < len(scholar["coauthor_papers"]) else 1
            if graph.has_edge(scholar["name"], coauthor):
                existing = graph[scholar["name"]][coauthor].get("weight", 1)
                merged_weight = max(existing, weight)
                graph[scholar["name"]][coauthor]["weight"] = merged_weight
                graph[scholar["name"]][coauthor]["title"] = f"{merged_weight} joint papers"
                graph[scholar["name"]][coauthor]["width"] = max(1, min(merged_weight, 10))
            else:
                graph.add_edge(
                    scholar["name"],
                    coauthor,
                    weight=weight,
                    title=f"{weight} joint papers",
                    width=max(1, min(weight, 10)),
                    color={"color": "#888888", "opacity": 0.6},
                    kind="coauthorship",
                )

    scholars_by_topic: dict[str, list[dict]] = {}
    for scholar in scholars:
        scholars_by_topic.setdefault(scholar["primary_topic"], []).append(scholar)

    topic_anchors: dict[str, dict] = {}
    for topic, topic_scholars in scholars_by_topic.items():
        anchor = choose_anchor(topic_scholars)
        topic_anchors[topic] = anchor

        if len(topic_scholars) < 2:
            continue

        for scholar in topic_scholars:
            if scholar["name"] == anchor["name"] or graph.has_edge(scholar["name"], anchor["name"]):
                continue

            graph.add_edge(
                scholar["name"],
                anchor["name"],
                hidden=True,
                physics=True,
                length=TOPIC_GLUE_LENGTH,
                kind="topic_glue",
            )

    topics_by_family: dict[str, list[str]] = {}
    for topic in scholars_by_topic:
        topics_by_family.setdefault(topic_family(topic), []).append(topic)

    for family, topics in topics_by_family.items():
        family_anchor_candidates = [topic_anchors[topic] for topic in topics if topic in topic_anchors]
        unique_family_anchors = list({anchor["name"]: anchor for anchor in family_anchor_candidates}.values())

        if len(unique_family_anchors) < 2:
            continue

        family_anchor = choose_anchor(unique_family_anchors)
        for anchor in unique_family_anchors:
            if anchor["name"] == family_anchor["name"] or graph.has_edge(anchor["name"], family_anchor["name"]):
                continue

            graph.add_edge(
                anchor["name"],
                family_anchor["name"],
                hidden=True,
                physics=True,
                length=FAMILY_GLUE_LENGTH,
                kind="family_glue",
            )

    return graph


def count_visible_edges(graph: nx.Graph) -> int:
    return sum(1 for _, _, data in graph.edges(data=True) if data.get("kind") == "coauthorship")


def build_legend_html(scholars: list[dict]) -> str:
    topics_in_use = {scholar["primary_topic"] for scholar in scholars}
    family_order = ordered_families_in_use(scholars)

    legend_sections: list[str] = []
    for family in family_order:
        family_topics = [topic for topic in FAMILY_TO_TOPICS.get(family, []) if topic in topics_in_use]
        if family == OTHER_FAMILY:
            family_topics.extend(
                sorted(
                    topic
                    for topic in topics_in_use
                    if topic_family(topic) == OTHER_FAMILY and topic not in family_topics
                )
            )

        if not family_topics:
            continue

        family_count = sum(1 for scholar in scholars if scholar["topic_family"] == family)
        family_header_color = FAMILY_BASE_COLORS.get(family, DEFAULT_COLOR)

        topic_rows = []
        for topic in family_topics:
            topic_rows.append(
                (
                    '<div style="display:flex;align-items:center;margin:3px 0;">'
                    f'<span style="display:inline-block;width:14px;height:14px;border-radius:50%;'
                    f'background:{TOPIC_COLORS.get(topic, DEFAULT_COLOR)};margin-right:8px;flex-shrink:0;"></span>'
                    f'<span style="font-size:13px;">{topic} '
                    f'({sum(1 for scholar in scholars if scholar["primary_topic"] == topic)})</span></div>'
                )
            )

        legend_sections.append(
            (
                '<div style="margin:8px 0 10px 0;">'
                '<div style="display:flex;align-items:center;font-weight:600;font-size:13px;'
                'margin-bottom:4px;color:#333;">'
                f'<span style="display:inline-block;width:10px;height:10px;border-radius:50%;'
                f'background:{family_header_color};margin-right:6px;flex-shrink:0;"></span>'
                f"{family} ({family_count})</div>"
                f'{"".join(topic_rows)}</div>'
            )
        )

    return "\n".join(legend_sections)


def generate_html(graph: nx.Graph, scholars: list[dict]) -> None:
    network = Network(
        height="900px",
        width="100%",
        bgcolor="#fafafa",
        font_color="#333333",
        directed=False,
        notebook=False,
        cdn_resources="in_line",
    )

    network.set_options(
        """
        {
          "physics": {
            "enabled": true,
            "solver": "forceAtlas2Based",
            "forceAtlas2Based": {
              "gravitationalConstant": -80,
              "centralGravity": 0.008,
              "springLength": 180,
              "springConstant": 0.06,
              "damping": 0.4,
              "avoidOverlap": 0.3
            },
            "stabilization": {
              "enabled": true,
              "iterations": 300
            }
          },
          "interaction": {
            "hover": true,
            "tooltipDelay": 200,
            "zoomView": true,
            "dragView": true,
            "navigationButtons": true
          },
          "nodes": {
            "shape": "dot",
            "shadow": {
              "enabled": true,
              "color": "rgba(0,0,0,0.15)",
              "size": 8,
              "x": 2,
              "y": 2
            }
          },
          "edges": {
            "smooth": {
              "type": "continuous"
            },
            "color": {
              "inherit": false
            }
          }
        }
        """
    )

    network.from_nx(graph)

    legend_html = build_legend_html(scholars)
    n_scholars = len(scholars)
    n_edges = count_visible_edges(graph)
    n_topics = len({scholar["primary_topic"] for scholar in scholars})

    stats_html = (
        '<div style="margin-bottom:12px;padding-bottom:8px;border-bottom:1px solid #ddd;'
        'font-size:13px;color:#555;">'
        f"<b>{n_scholars}</b> scholars &middot; "
        f"<b>{n_edges}</b> coauthorship links &middot; "
        f"<b>{n_topics}</b> topics</div>"
    )

    role_legend = (
        '<div style="margin-top:12px;padding-top:8px;border-top:1px solid #ddd;">'
        '<div style="font-weight:bold;font-size:13px;margin-bottom:4px;">Node size = Role</div>'
        '<div style="font-size:12px;color:#666;">'
        '<span style="border:3px solid #FFD700;border-radius:50%;'
        'display:inline-block;width:10px;height:10px;margin-right:4px;"></span>'
        "Gold border = Gatekeeper<br>"
        "Large = Gatekeeper &gt; Active &gt; Emerging &gt; Peripheral = Small"
        "</div></div>"
    )

    custom_html = f"""
    <div id="legend" style="
        position: fixed;
        top: 15px;
        right: 15px;
        background: white;
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 14px 18px;
        max-height: 85vh;
        overflow-y: auto;
        z-index: 1000;
        box-shadow: 0 2px 12px rgba(0,0,0,0.1);
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    ">
        <div style="font-weight:bold;font-size:15px;margin-bottom:8px;">Scholar Network</div>
        {stats_html}
        <div style="font-weight:bold;font-size:13px;margin-bottom:6px;">Topic families (related colors)</div>
        {legend_html}
        {role_legend}
    </div>

    <div style="
        position: fixed;
        bottom: 15px;
        left: 15px;
        background: white;
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 10px 14px;
        z-index: 1000;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        font-size: 12px;
        color: #888;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    ">
        Drag to move &middot; Scroll to zoom &middot; Hover for details &middot;
        Edge width = joint papers
    </div>
    """

    html = network.generate_html()
    html = html.replace("</body>", f"{custom_html}\n</body>")
    html = html.replace("<head>", "<head>\n<title>Scholar Network Map</title>")

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(html, encoding="utf-8")


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()
    configure_runtime(args.vault_root, args.output)

    print(f"Vault root: {VAULT_ROOT}")
    print(f"Reading scholar notes from: {SCHOLARS_DIR}")

    if not SCHOLARS_DIR.exists():
        print(
            "No Scholars/ directory found. Pass --vault-root /path/to/your/vault "
            "or run from the repository root where vault-starter/ exists."
        )
        raise SystemExit(1)

    scholars = load_scholars()
    if not scholars:
        print("No scholar notes found. Create notes in Scholars/ with type: scholar frontmatter.")
        raise SystemExit(0)

    print(f"Found {len(scholars)} scholars")

    topic_counts = Counter()
    for scholar in scholars:
        for topic in scholar["topics"]:
            topic_counts[topic] += 1

    print("\nTopic distribution:")
    for topic, count in topic_counts.most_common():
        print(f"  {topic}: {count} scholars")

    print("\nBuilding network graph...")
    graph = build_graph(scholars)
    print(f"  Nodes: {graph.number_of_nodes()}, Visible coauthorship edges: {count_visible_edges(graph)}")

    print(f"\nGenerating visualization -> {OUTPUT_FILE}")
    generate_html(graph, scholars)
    print("Done! Open the generated HTML file in a browser.")


if __name__ == "__main__":
    main()
