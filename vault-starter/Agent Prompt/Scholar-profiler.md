# Scholar Profiler — Web Clipping to Scholar Note

## Purpose

This prompt converts a raw web clipping of a scholar page into a structured scholar note in `Scholars/`.

The goal is not to write a biography. The goal is to build a node in a research network:

- connect the scholar to a controlled set of topics
- connect the scholar to their main coauthors
- connect the scholar to representative papers

The final note should help answer:

- who defines a topic
- who works near whom
- who bridges otherwise separate communities

## Accepted Inputs

The source file is usually a Markdown clipping in `Clippings/`, captured from:

- Google Scholar
- ORCID
- a personal website
- SSRN author page
- IDEAS / RePEc

The clipping may be messy. Duplicates, malformed tables, incomplete metadata, and mixed published / working-paper lists are normal.

## Core Rules

### 1. Read the whole clipping first

Extract what is actually available:

- scholar name
- affiliation
- homepage if visible
- research interests
- paper titles, years, venues, coauthors

If the clipping is partial, work with what is present and explicitly note the gaps.

### 2. Identify papers and coauthors

For papers:

- deduplicate repeated titles or repeated DOI records
- distinguish published papers from working papers when possible
- choose 5 representative papers

Representative papers should prioritize:

1. top-journal placement
2. citation prominence if visible
3. fit with the scholar’s core identity

For coauthors:

- count joint appearances across the clipping
- rank by joint paper count
- keep the top 20

### 3. Assign topics from the controlled vocabulary

Always read:

`Scholars/_Scholar Topic Vocabulary.md`

before assigning `primary_topics`.

Rules:

- choose 1 to 3 topics
- choose topics the scholar is known for, not every topic they have touched
- do not invent a new topic silently
- if the vocabulary is missing something important, flag that gap in the note instead of forcing a bad fit

Also assign 1 to 2 broad `fields` if your vault uses them.

### 4. Assign a role conservatively

- `gatekeeper`: defines a topic area
- `active`: regular, well-known contributor
- `emerging`: junior or rising scholar
- `peripheral`: occasional contributor whose main identity lies elsewhere

Default to `active` unless the clipping clearly supports something else.

### 5. Cross-reference existing vault data

Before creating a note:

- check whether the scholar already has a note in `Scholars/`
- if yes, update it rather than creating a duplicate
- check whether major coauthors already have scholar notes
- use wikilinks in `top_coauthors` either way

### 6. Literature-note cross-reference is optional

If the user keeps literature notes in the vault, you may also search them and link matching papers in the representative-paper table.

Examples:

- `Zotero Literature Note/`
- any other literature-note folder the user uses

If no literature-note system exists, leave `vault_note` blank. This workflow should still work.

### 7. Optional stub creation

If the user explicitly asks for stubs, create minimal stub scholar notes for major coauthors who do not yet have notes.

Do not create stubs by default.

### 8. Write `recent_focus`

This should describe the scholar’s current direction based on the last few years of work, not their entire career.

Good:

- "Retail investor attention measurement using search and platform data"

Bad:

- "Studies finance"
- "Published in JF in 2011"

## Output Format

Create or update:

`Scholars/<Full Name>.md`

with this structure:

```yaml
---
type: scholar
name: "<Full Name>"
affiliation: "<Institution>"
country: "<Country or code>"
homepage: "<URL>"
google_scholar: "<URL>"
orcid: "<ORCID>"
primary_topics:
  - <topic1>
  - <topic2>
role: <gatekeeper|active|emerging|peripheral>
fields:
  - <field1>
top_coauthors:
  - "[[Coauthor 1]]"
  - "[[Coauthor 2]]"
coauthor_papers:
  - <count1>
  - <count2>
representative_papers:
  - title: "<Paper Title>"
    year: YYYY
    journal: "<Journal Abbreviation>"
    vault_note: ""
recent_focus: "<One sentence on current research direction>"
status: active
last_updated: YYYY-MM-DD
source_clipping: "[[Clippings/<clipping filename>.md]]"
---
```

Body structure:

```markdown
# <Full Name>

## Profile

2 to 4 factual sentences on who this scholar is, where they are, and what they are known for.

## Representative Papers

| Paper | Year | Journal | In Vault? |
|-------|------|---------|-----------|
| <Title> | YYYY | <Journal> | - |

## Recent Work

- Paper title - with [[Coauthor]], [[Coauthor]] (Year, Venue or WP)

## Top Coauthors

| Rank | Coauthor | Joint Papers | Their Topics |
|------|----------|-------------|--------------|
| 1 | [[Name]] | N | topic1, topic2 |

## Notes

Add observations about:
- research cluster
- institutional ties
- relevance to the user’s own map
- vocabulary gaps
- likely bridge position in the network
```

## Quality Checklist

- scholar name and affiliation are correct
- `primary_topics` come from the vocabulary file
- `top_coauthors` and `coauthor_papers` have matching lengths
- representative papers define the scholar well
- `recent_focus` is genuinely recent
- role assignment is honest and conservative
- literature-note links are added only if the user actually has such notes
- no duplicate scholar note was created
- `source_clipping` points back to the raw clipping

## Mindset

Think like a network builder, not a biographer.

Every scholar note should make the eventual map better by improving:

1. topic identity
2. coauthor completeness
3. cross-note connectivity
4. field structure
