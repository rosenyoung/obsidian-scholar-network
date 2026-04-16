# Customization Guide

This repository ships with a **financial economics** vocabulary and example notes, but the structure is intentionally domain-agnostic. This guide walks you through adapting it to your own field.

---

## 1. Replace the Topic Vocabulary

The most important file to customize is:

```
vault-starter/Scholars/_Scholar Topic Vocabulary.md
```

Keep the structure, replace the content:

- `###` headings define **broad families** — these drive color grouping and layout proximity
- Each table row defines a valid topic within that family
- The visualization script reads these families directly — nothing is hard-coded

Example of what a family looks like:


### Pricing & Returns {color=#1F77B4}

| Topic | Describes a Scholar Known For... | Example Gatekeepers |
|-------|----------------------------------|---------------------|
| `factor models` | Building/testing cross-sectional pricing models | Eugene Fama |
| `return predictability` | Time-series and cross-sectional forecasting | John Cochrane |


### Why the `###` heading matters

The script uses each `###` heading as a family name to derive:

- A **base color** for the family (auto-assigned from a palette, or manually set with `{color=#HEX}`)
- **Related shades** for each topic within the family — so `factor models` and `return predictability` look like siblings, not strangers
- **Weak hidden layout links** between topic anchors in the same family, keeping related clusters visually close without overpowering the coauthorship structure

If you flatten the vocabulary into a single list with no `###` headings, the graph loses its semantic structure — every topic gets an independent color and drifts freely. The families are what make the visualization informative rather than just pretty.

---

## 2. Choose the Right Topic Granularity

Scholar topics should answer the question: **"What is this person known for?"**

**Good granularity:**
- `attention` — specific enough to identify a research circle
- `fund flows` — maps to a real community of researchers
- `climate finance` — a distinct and growing subfield

**Too broad (avoid):**
- `behavioral finance` — contains dozens of sub-communities
- `corporate finance` — way too many unrelated researchers would share this tag

**Too narrow (avoid):**
- `EDGAR download patterns` — this is a data source, not a research identity
- `SPAC lockup expiration` — this is a single paper topic, not what a scholar is "known for"

A practical test: if fewer than 2 scholars in your network would share a topic after 30+ profiles, the topic is probably too narrow — consider merging it into a broader one.

---

## 3. Adapt the Profiler Prompt

The AI processing prompt lives at:

```
vault-starter/Agent Prompt/Scholar-profiler.md
```

When moving to a new field, you will want to change:

| What to change                                   | Why                                                                                           |
| ------------------------------------------------ | --------------------------------------------------------------------------------------------- |
| Finance-specific journal names (JF, JFE, RFS...) | Replace with your field's top venues                                                          |
| Finance-specific field labels in `fields`        | Use your discipline's broad categories                                                        |
| Literature-note cross-reference paths            | Point to your own literature folder, or remove if you don't use one                           |
| Role language and career markers                 | Adjust if your field has different seniority conventions                                      |
| Gatekeeper judgment criteria                     | Calibrate to your field's norms — what counts as "defining a topic" varies across disciplines |

The profiler prompt is designed to work with **any** LLM. You do not need a specific AI service — ChatGPT, Claude, Gemini, or any model that can follow structured instructions will work.

---

## 4. Adjust Visual Clustering Strength

In `scripts/scholar_network.py`, two constants control how strongly the layout pulls related scholars together:

```python
TOPIC_GLUE_LENGTH = 300    # same topic → weak attraction
FAMILY_GLUE_LENGTH = 420   # same family, different topic → weaker attraction
```

**Lower values = stronger pull** (nodes cluster more tightly). **Higher values = looser layout** (nodes spread out more).

When to adjust:

| Symptom | Fix |
|---------|-----|
| Same-topic scholars are scattered across the graph | Lower `TOPIC_GLUE_LENGTH` (try 200) |
| Related topics from the same family drift too far apart | Lower `FAMILY_GLUE_LENGTH` (try 350) |
| Topic clusters are too tight, overlapping each other | Raise both values |
| Layout feels dominated by topic labels rather than coauthorship | Raise both values — coauthorship edges should be the primary layout driver |

The key principle: **coauthorship edges should always dominate the layout.** The glue links are there to prevent related clusters from randomly drifting to opposite corners of the graph, not to force an artificial grouping.

---

## 5. Override Family Colors

By default, the script auto-assigns family colors from a built-in palette. If you want a specific color for a family, set it directly in the vocabulary file:

```md
### Behavioral & Information {color=#8E24AA}
```

The script will use this as the base color and still generate related shades for each topic within the family. For example, if the family has 4 topics, they might get shades ranging from a lighter to a darker purple.

If no `{color=...}` tag is present, the script assigns colors automatically in the order the families appear in the file.

---

## 6. Change Node Semantics

The default visual encoding is:

| Visual property | Driven by |
|----------------|-----------|
| Node **color** | First entry in `primary_topics` (mapped through family → shade) |
| Node **size** | `role` — gatekeeper > active > emerging > peripheral |
| Gold **border** | `role == "gatekeeper"` |
| **Edge** visibility | Only coauthors who have their own scholar note in the vault |
| Edge **thickness** | Number of joint papers (`coauthor_papers`) |
| **Hidden edges** | Same-topic glue + same-family glue (layout only, not visible) |

If you want to change any of these, the relevant places in `scholar_network.py` are:

- `ROLE_SIZES` dict — maps role names to pixel sizes
- `build_graph()` function — constructs nodes, visible edges, and hidden glue edges
- Tooltip HTML construction inside `build_graph()` — controls what shows on hover

---

## 7. Keep Examples Separate from Your Data

The `examples/` folder is documentation — it shows what well-formed scholar notes look like. It is **not** the dataset your script reads.

Your actual scholar notes should live in:

```
<your vault>/Scholars/*.md
```

This separation means you can publish the repo without forcing users to inherit your example scholars as part of their own graph. If you want to try the examples, copy them into your vault's `Scholars/` folder manually.
