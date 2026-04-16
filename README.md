# Obsidian Scholar Network

[中文说明](README_CN.md)

> Build an interactive coauthorship network inside Obsidian — see who defines a topic, who collaborates with whom, and which scholars bridge separate research communities.

![Scholar Network Screenshot](screenshots/network-graph.png)

This is **not** a plugin. It is a methodology plus a starter kit — templates, an AI prompt, Dataview queries, and a Python visualization script — that you can adapt to any academic field.

---

## Why You Need This

If you only manage papers, you are missing half the picture. Papers tell you *what* has been studied; a scholar network tells you *who* is doing the studying and how they relate to each other.

Concretely, a scholar network helps you answer questions like:

- **Who is the gatekeeper of a topic?** If you are writing a paper on return predictability, whose work *must* you cite, and who will likely referee your submission?
- **Is a research community tight-knit or fragmented?** A tight cluster (few scholars, many co-authorships) means high entry barriers but strong collaboration opportunities. A loose cluster means easier entry but less collegial review.
- **Who bridges separate communities?** Some scholars publish across topics — they connect clusters that would otherwise be invisible to each other. These bridges are often the most valuable people to talk to at conferences.
- **What does a scholar's coauthor map look like before you meet them?** Knowing someone's top collaborators and recent direction makes conference conversations far more productive.

A literature database answers "what papers exist." A scholar network answers "who are the people, and how do they connect." This is especially useful for junior level scholars who are exploring a new field or topic. By starting from a well-known scholar, the scholar network under similar topics easily expands.

---

## How It Works (4 Steps)

```
Google Scholar page ──► Web Clipper ──► Clippings/scholarname.md
                                              │
                                              ▼
                        Any LLM + Scholar-profiler.md prompt
                                              │
                                              ▼
                                     Scholars/Full Name.md
                                              │
                                              ▼
                      python scholar_network.py ──► interactive HTML
```

1. **Clip** a scholar's Google Scholar, ORCID, or personal page using [Obsidian Web Clipper](https://obsidian.md/clipper). The raw markdown lands in your `Clippings/` folder.
2. **Process** the clipping with any LLM. Paste the clipping together with `Scholar-profiler.md` (included in this repo) and ask the AI to generate a structured scholar note. The AI will parse papers, deduplicate entries, rank coauthors, assign topics from your vocabulary, and output a complete note.
3. **Save** the generated note into your vault's `Scholars/` folder. Review it — especially the Notes section, where your own judgment matters most.
4. **Visualize** by running the Python script. It reads all scholar notes, builds a coauthorship graph, and outputs a self-contained HTML file you can open in any browser.

Repeat steps 1–3 for each scholar. After 5–10 scholars you will start seeing clusters emerge in the network graph.

---

## Quick Start (≈ 30 minutes)

### Prerequisites

| Tool | Purpose | Required? |
|------|---------|-----------|
| [Obsidian](https://obsidian.md/) | Note-taking environment | Yes |
| [Dataview](https://github.com/blacksmithgu/obsidian-dataview) plugin | Powers the Dashboard queries | Yes |
| [Obsidian Web Clipper](https://obsidian.md/clipper) | Captures scholar pages as Markdown | Yes |
| [Python 3.10+](https://www.python.org/) | Runs the visualization script | Yes |
| Any LLM (ChatGPT, Claude, Gemini, etc.) | Processes clippings into structured notes | Yes |
| [Templater](https://github.com/SilasKnobel/Templater) plugin | Auto-fills dates in the scholar template | Optional |

### Step 1: Copy the starter files into your vault

Copy these three folders from `vault-starter/` into your Obsidian vault:

```
vault-starter/Scholars/     →  YourVault/Scholars/
vault-starter/Templates/    →  YourVault/Templates/
vault-starter/Agent Prompt/ →  YourVault/Agent Prompt/
```

After copying, your vault should contain:
- `Scholars/_Scholar Network.md` — the Dataview dashboard (works automatically)
- `Scholars/_Scholar Topic Vocabulary.md` — the topic vocabulary (you will customize this)
- `Scholars/_Topic Maps/` — empty folder for future topic-level index notes
- `Templates/Scholar Template.md` — Templater version of the note template
- `Templates/Scholar Template (plain).md` — plain Markdown version (no Templater needed)
- `Agent Prompt/Scholar-profiler.md` — the AI processing prompt

### Step 2: Customize the topic vocabulary

Open `Scholars/_Scholar Topic Vocabulary.md`. It ships with a **financial economics** vocabulary as a working example. If you work in a different field, replace the topics — but **keep the structure**:

- `###` headings define **broad families** (e.g., `### Pricing & Returns`)
- Each table row defines a valid topic within that family
- The visualization script reads these families to derive colors and cluster layout

> **Important:** The vocabulary is not just a tag checklist. It is the semantic layer that drives the entire visualization. Topics in the same family get related colors and stay visually closer in the graph. See [Why the vocabulary matters](#vocabulary-as-semantic-infrastructure) below.

### Step 3: Create your first scholar note

This is where the system comes alive.

1. **Clip a scholar page.** Go to any scholar's Google Scholar profile (or ORCID, or personal website) and use the Obsidian Web Clipper to save it. The raw markdown will land in your `Clippings/` folder.

2. **Feed it to an LLM.** Open the clipping and `Agent Prompt/Scholar-profiler.md` in your AI tool of choice. Ask the AI something like:

   > "Use Scholar-profiler.md to create a scholar profile from this clipping."

   The AI will:
   - Parse all papers and coauthors from the clipping
   - Deduplicate repeated entries (Google Scholar often lists the same paper multiple times)
   - Rank coauthors by number of joint papers and keep the top 20
   - Assign 1–3 `primary_topics` from your vocabulary
   - Assign a `role` (gatekeeper, active, emerging, or peripheral)
   - Choose 5 representative papers
   - Write a brief profile and notes section

3. **Save the output** as `Scholars/Full Name.md` in your vault. Review the result — the AI handles the tedious extraction work, but your expert judgment on topics, role, and the Notes section is what makes the note truly valuable.

4. **Check the dashboard.** Open `Scholars/_Scholar Network.md` in Obsidian. The Dataview queries update automatically — you should see your new scholar appear in the tables.

> **Tip:** You do not need to fill every field perfectly on the first pass. Many scholar notes start as stubs — a name, one or two topics, a few coauthors. As you read more papers and attend more conferences, you will naturally fill in the details. The beauty of wikilinks is that even a stub note creates a visible node in the graph.

### Step 4: Grow the network and visualize

Repeat Step 3 for more scholars. Once you have 5 or more, generate the interactive network:

```bash
# Install dependencies (first time only)
pip install -r scripts/requirements.txt

# Generate the visualization
python scripts/scholar_network.py --vault-root /path/to/your/vault
```

This produces `Scholars/scholar_network.html` — open it in a browser to explore.

This repository does **not** ship with a ready-made demo dataset. You are expected to create scholar notes in your own vault's `Scholars/` folder. The `examples/` folder is reference material only.

You can also specify a custom output path:

```bash
python scripts/scholar_network.py --vault-root /path/to/your/vault --output ~/Desktop/network.html
```

Re-run the script whenever you add or update scholar notes to refresh the graph.

---

## Repository Layout

```text
obsidian-scholar-network/
├── README.md                        # This file
├── README_CN.md                     # Chinese documentation
├── LICENSE                          # MIT
│
├── vault-starter/                   # Copy into your vault
│   ├── Scholars/
│   │   ├── _Scholar Network.md      # Dataview dashboard
│   │   ├── _Scholar Topic Vocabulary.md  # Topic vocabulary (customize!)
│   │   └── _Topic Maps/             # Per-topic index notes (start empty)
│   ├── Templates/
│   │   ├── Scholar Template.md      # Templater version
│   │   └── Scholar Template (plain).md  # Plain Markdown version
│   └── Agent Prompt/
│       └── Scholar-profiler.md      # AI processing prompt
│
├── scripts/
│   ├── scholar_network.py           # Visualization generator
│   └── requirements.txt             # networkx, pyvis, pyyaml
│
├── examples/                        # Real scholar notes for reference
│   ├── Eugene Fama.md               # Gatekeeper — the canonical example
│   ├── Kenneth French.md            # Stub-style note — minimal but functional
│   ├── Kumar Venkataraman.md        # Active scholar — rich coauthor network
│   └── Stacey Jacobsen.md          # Cross-topic bridge — spans two communities
│
├── screenshots/                     # Publication screenshots
└── docs/
    └── customization.md             # Adapting to other fields
```

---

## Key Design Decisions

### Topic first, field second

`asset pricing` is too broad to map a real academic community. Saying a scholar works on "asset pricing" tells you almost nothing — asset pricing contains factor models, anomalies, liquidity, demand-based pricing, and dozens of other directions, each with its own distinct group of researchers.

This project uses **topics** (fine-grained) as the primary axis and keeps **fields** (coarse-grained) as optional metadata for cross-referencing with a literature database.

### Coauthorship over citation

Citations are easy to collect but weak as community signals — you can cite someone you have never spoken to. Coauthorship is a much stronger indicator of genuine research proximity: if two people are willing to put their names on the same paper, they are in the same circle.

### Vocabulary as semantic infrastructure

The vocabulary file (`_Scholar Topic Vocabulary.md`) does three jobs simultaneously:

1. **Constrains** which topics are valid in `primary_topics` — preventing tag explosion
2. **Groups** topics into broad families via `###` headings
3. **Drives** the visualization: topics in the same family get related colors and are pulled closer together in the layout

Here is a concrete example. These three topics all belong to the family `Pricing & Returns`:

- `factor models`
- `return predictability`
- `demand-based pricing`

In the network graph:
- They share a **blue color family** — different shades, but visually related
- They are connected by **weak hidden layout links** that keep them in the same region
- But **coauthorship edges still dominate** — the layout reflects real collaboration, not just category labels

This means you can adapt the entire system to a new field by replacing the vocabulary while keeping the same structure. The script does not hard-code any topic or color — it derives everything from the vocabulary file.

If you want to override a family's color, add a `{color=#HEX}` tag to the heading:

```md
### Pricing & Returns {color=#1F77B4}
```

---

## Included Examples

The `examples/` folder contains real scholar notes illustrating different use cases:

| Example | What it demonstrates |
|---------|---------------------|
| [Eugene Fama](examples/Eugene%20Fama.md) | A **gatekeeper** — the most cited finance scholar, with detailed profile and extensive notes |
| [Kenneth French](examples/Kenneth%20French.md) | A **stub** — minimal note with just one coauthor, but still a valid and useful node in the network |
| [Kumar Venkataraman](examples/Kumar%20Venkataraman.md) | An **active scholar** — rich coauthor structure showing a real research cluster |
| [Stacey Jacobsen](examples/Stacey%20Jacobsen.md) | A **cross-topic bridge** — genuinely spans market microstructure and corporate finance |

These examples are documentation only. They are not used by the visualization script unless you copy them into your vault's `Scholars/` folder.

---

## What the Dashboard Shows

Once your vault has a few scholar notes, `_Scholar Network.md` automatically generates these views via Dataview:

- **Topic Landscape** — how many scholars per topic, how many gatekeepers, and whether the community is tight-knit or fragmented
- **Gatekeeper Directory** — every scholar marked as gatekeeper, with their topics and affiliations
- **Most Connected Scholars** — ranked by number of tracked coauthors
- **Cross-Topic Bridges** — scholars whose `primary_topics` span two or more areas
- **Coauthorship Links** — a flat list of who links to whom
- **Stub Scholars** — notes that need profiling
- **Recently Updated** — the last 10 scholar notes you touched

No manual maintenance needed — the queries update every time you open the note.

---

## Customization

See [docs/customization.md](docs/customization.md) for detailed guidance on:

- Replacing the finance vocabulary with your own field
- Choosing the right topic granularity
- Controlling family colors (automatic or manual override)
- Adjusting topic and family clustering strength
- Adapting the Scholar Profiler prompt to a new discipline
- Changing node sizing and tooltip content

---

## Screenshots

> **Note:** The `screenshots/` folder currently uses a single published image:
> - `network-graph.png` — the interactive network visualization

---

## License

MIT
