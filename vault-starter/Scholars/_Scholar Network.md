# Scholar Network

> A topic-centric map of researchers, their coauthorship links, and the cooperative structure of each research topic.
> See [[_Scholar Topic Vocabulary]] for the controlled topic list.

---

## Topic Landscape

How many scholars are active in each topic, and how cooperative are they?

```dataview
TABLE WITHOUT ID
  topic AS "Topic",
  length(rows) AS "Scholars",
  length(filter(rows, (r) => r.role = "gatekeeper")) AS "Gatekeepers",
  round(sum(map(rows, (r) => length(r.top_coauthors))) / length(rows), 1) AS "Avg Coauth Links",
  choice(
    length(rows) <= 5 AND sum(map(rows, (r) => length(r.top_coauthors))) / length(rows) >= 3,
    "tight-knit",
    choice(
      length(rows) <= 5 AND sum(map(rows, (r) => length(r.top_coauthors))) / length(rows) < 1.5,
      "siloed",
      choice(
        length(rows) > 10,
        "large field",
        "moderate"
      )
    )
  ) AS "Character"
FROM "Scholars"
WHERE type = "scholar"
FLATTEN primary_topics AS topic
GROUP BY topic
SORT length(rows) DESC
```

---

## Gatekeepers Directory

```dataview
TABLE
  name AS "Scholar",
  primary_topics AS "Topics",
  affiliation AS "Affiliation",
  recent_focus AS "Recent Focus"
FROM "Scholars"
WHERE type = "scholar" AND role = "gatekeeper"
SORT file.name
```

---

## Most Connected Scholars

```dataview
TABLE
  name AS "Scholar",
  primary_topics AS "Topics",
  length(top_coauthors) AS "Coauthors Tracked",
  role AS "Role",
  affiliation AS "Affiliation"
FROM "Scholars"
WHERE type = "scholar"
SORT length(top_coauthors) DESC
LIMIT 20
```

---

## Cross-Topic Bridges

Scholars who span multiple topics — bridge-builders connecting research communities.

```dataview
TABLE
  name AS "Scholar",
  primary_topics AS "Topics",
  affiliation AS "Affiliation"
FROM "Scholars"
WHERE type = "scholar" AND length(primary_topics) >= 2
SORT length(primary_topics) DESC
```

---

## Coauthorship Links

```dataview
TABLE WITHOUT ID
  file.link AS "Scholar",
  top_coauthors AS "Coauthors (in vault)"
FROM "Scholars"
WHERE type = "scholar" AND top_coauthors
SORT file.name
```

---

## Stub Scholars (Need Profiling)

```dataview
TABLE name AS "Scholar", primary_topics AS "Topics"
FROM "Scholars"
WHERE type = "scholar" AND status = "stub"
SORT file.name
```

---

## Recently Updated

```dataview
TABLE name AS "Scholar", primary_topics AS "Topics", last_updated AS "Updated"
FROM "Scholars"
WHERE type = "scholar"
SORT last_updated DESC
LIMIT 10
```

---

## Interactive Network Map

Open the interactive visualization: [Scholar Network Map](scholar_network.html)

Regenerate after adding/updating scholar notes:
```bash
python /path/to/obsidian-scholar-network/scripts/scholar_network.py --vault-root /path/to/your/vault
```
