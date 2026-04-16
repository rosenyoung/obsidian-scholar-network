# Scholar Topic Vocabulary

> **Rule:** Every topic used in a scholar note's `primary_topics` MUST come from this file. If a scholar genuinely works on a topic not listed here, add it first — that friction prevents topic explosion.

*Forked from [[_Tag Vocabulary]] (literature notes) on 2026-04-14. Maintained separately — scholar topics may diverge from paper-level topics as the network grows.*

---

## How Scholar Topics Differ from Literature Topics

Literature topics describe **what a single paper is about** (1–3 per paper, very specific).
Scholar topics describe **what a researcher is known for** (1–3 per scholar, broader).

A literature topic like `earnings announcements` may be too narrow for a scholar topic — the scholar might be known for `return predictability` more broadly. Conversely, a scholar might be the gatekeeper of a topic so specific it doesn't exist in the literature vocabulary (e.g., `corporate culture`).

---

## Topics (45 initial, will evolve)

### Pricing & Returns

| Topic | Describes a Scholar Known For... | Example Gatekeepers |
|-------|----------------------------------|---------------------|
| `factor models` | Building/testing cross-sectional pricing models, factor construction, factor zoo | Eugene Fama, Lu Zhang |
| `anomalies` | Return anomalies, mispricing, limits to arbitrage, anomaly robustness | Robert Stambaugh |
| `return predictability` | Time-series/cross-sectional return forecasting, price-scaled variables | John Cochrane |
| `momentum` | Cross-sectional/time-series/factor momentum, momentum crashes | Mark Carhart, Tobias Moskowitz |
| `demand-based pricing` | Demand systems, flow-driven pricing, inelastic markets, institutional demand effects | Ralph Koijen |
| `intermediary asset pricing` | Intermediaries as marginal investors, broker-dealer constraints | Zhiguo He |
| `earnings announcements` | PEAD, earnings surprises, market reactions to earnings news | |
| `bubbles` | Asset price bubbles, overvaluation episodes, crash dynamics | Robin Greenwood |

### Asset Management

| Topic | Describes a Scholar Known For... | Example Gatekeepers |
|-------|----------------------------------|---------------------|
| `fund performance` | Alpha measurement, skill vs luck, scale-performance, benchmark evaluation | |
| `fund flows` | Flow-performance relationship, fire sales, flow-induced trading | Joshua Coval |
| `fund manager incentives` | Manager compensation, risk-shifting, tournament behavior, career concerns | |
| `target-date funds` | TDF design, glide paths, lifecycle asset allocation, 401(k) defaults | |
| `benchmarking` | Benchmark effects on trading, index reconstitution, active share, tracking error | Martijn Cremers |
| `fund governance` | Fund proxy voting, securities lending, fiduciary duty, fund board oversight | |
| `fund fragility` | Run dynamics in open-end funds, swing pricing, liquidity transformation | |

### Corporate

| Topic | Describes a Scholar Known For... | Example Gatekeepers |
|-------|----------------------------------|---------------------|
| `executive compensation` | CEO pay, pay-for-performance, option grants, relative performance evaluation | |
| `board governance` | Board structure, independent directors, director incentives | |
| `shareholder activism` | Blockholder intervention, proxy fights, exit vs voice, shareholder voting | Alex Edmans |
| `capital structure` | Leverage decisions, trade-off theory, pecking order, dynamic capital structure | |
| `mergers acquisitions` | M&A deals, takeover dynamics, fairness opinions | |
| `corporate investment` | Investment decisions, Tobin's Q, investment-price sensitivity, real options | |
| `payout policy` | Dividends, share repurchases, payout flexibility | |
| `financial constraints` | Credit constraints, cash holdings, liquidity management | |
| `agency problems` | Principal-agent conflicts, moral hazard, managerial entrenchment | |
| `corporate culture` | Organizational culture, employee satisfaction, workplace norms, culture and performance | Kai Li |

### Behavioral & Information

| Topic | Describes a Scholar Known For... | Example Gatekeepers |
|-------|----------------------------------|---------------------|
| `overconfidence` | Managerial or investor overconfidence, miscalibration, overtrading | Ulrike Malmendier |
| `investor sentiment` | Aggregate sentiment measures, noise trading, sentiment-driven mispricing | Malcolm Baker |
| `attention` | Limited investor attention, inattention, salience, media effects on markets | Zhi Da |
| `extrapolation` | Belief formation, over/underreaction, experience effects, diagnostic expectations | Nicola Gennaioli |
| `investor disagreement` | Heterogeneous beliefs, opinion divergence, echo chambers | |
| `disclosure` | Voluntary/mandatory disclosure, transparency, information production | |
| `information asymmetry` | Adverse selection, insider information, informed trading | Albert Kyle |

### Market Structure

| Topic | Describes a Scholar Known For... | Example Gatekeepers |
|-------|----------------------------------|---------------------|
| `liquidity` | Market liquidity, liquidity risk, bid-ask spreads, illiquidity premium | Yakov Amihud |
| `price discovery` | Price efficiency, information in prices, feedback to real economy | Philip Bond |
| `short selling` | Short constraints, short interest, lending fees, manipulative shorting | |
| `market design` | Exchange competition, HFT, algorithmic trading, market fragmentation | Albert Menkveld |

### Institutions & Policy

| Topic | Describes a Scholar Known For... | Example Gatekeepers |
|-------|----------------------------------|---------------------|
| `monetary policy` | Central banks, interest rate effects, QE, yield curve | |
| `financial regulation` | Securities regulation, banking regulation, systemic risk, macroprudential | |
| `political connections` | Political economy of finance, lobbying, government intervention | |

### Special Topics

| Topic | Describes a Scholar Known For... | Example Gatekeepers |
|-------|----------------------------------|---------------------|
| `climate finance` | ESG investing, carbon pricing, green bonds, stranded assets | Stefano Giglio |
| `cryptocurrency` | Crypto markets, DeFi, stablecoins, blockchain, CBDCs | |
| `machine learning` | ML/AI in finance, NLP, textual analysis, LLMs, alternative data | Shihao Gu |
| `ipo` | IPOs, SPACs, going public, underpricing | Jay Ritter |
| `retirement saving` | 401(k), pensions, lifecycle portfolio choice, financial literacy | |
| `china` | Chinese financial markets, Chinese firms, Chinese regulation | |
| `real effects` | Feedback from financial markets to real economic decisions | Itay Goldstein |

---

## How to Use

### In scholar note frontmatter:
```yaml
primary_topics:
  - attention
  - investor sentiment
  - return predictability
role: gatekeeper
```

### Rules:
1. **`primary_topics`** — 1 to 3 topics this scholar is **known for**. These define their identity in the network.
2. **`role`** — one of: `gatekeeper` (defines the topic), `active` (publishes regularly), `emerging` (junior/rising), `peripheral` (occasional contributor).
3. **Adding a new topic** — Add it to this file first with a clear description and at least one example gatekeeper. Then use it.
4. **Tag naming** — all lowercase, no hyphens, natural English phrases (1–3 words).
5. **Divergence from literature vocabulary** — This is expected. Scholar topics can be broader (e.g., combining `fund flows` + `fund fragility` into `delegated asset management`) or narrower (e.g., splitting out `corporate culture` from `agency problems`).

### Retirement criteria:
If a topic has fewer than 2 scholars after you've profiled 30+ scholars, consider merging it.

---

## Changelog

| Date | Change | Reason |
|------|--------|--------|
| 2026-04-14 | Initial version (46 topics) | Forked from literature _Tag Vocabulary (45 topics). Added `corporate culture`. |
