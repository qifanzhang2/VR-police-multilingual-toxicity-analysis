# VR-POLICE — Multilingual Toxicity Analysis for Social-VR Voice Chat

**VR-POLICE** is a research/analytics pipeline that turns **voice-to-text transcripts from social VR** into **actionable safety insights**: toxicity rates, cross-language comparisons, and visuals that help designers and moderation teams make better decisions.

> 🎯 Goal: *automate detection, measurement, and visual reporting of toxic behavior in social‑VR voice chat so designers can make data‑driven safety decisions.*


---

## What you get

- **Cross-lingual toxicity analytics** (per-language counts/rates + comparisons)
- **Sentiment + keyword signals** to triangulate “what’s happening” beyond a single score
- **Plots / summaries** suitable for quick stakeholder review
- A workflow designed for **messy, real-world transcripts** (noise, accents, code-switching, short utterances)

---

## Repo structure

```text
.
├── Open_transcript.py        # load / parse transcript exports into analysis-ready text segments
├── Text_calculation.py       # compute toxicity/sentiment + aggregate metrics (by language, etc.)
├── Analysis_response.py      # post-process results into visuals / summaries
└── README.md
```

---

## Quickstart

### 1) Create an environment
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install -U pip
```

### 2) Install dependencies
This project uses common Python NLP + data tooling (e.g., `pandas`, `numpy`, `matplotlib`, `transformers`, `torch`, and optionally `spacy`).

If you already have a working ML/NLP environment, start with:
```bash
pip install pandas numpy matplotlib scikit-learn transformers torch
```

> If a script errors due to a missing library, install it and re-run.  
> (A future improvement is adding a pinned `requirements.txt` for one-command installs.)

### 3) Run the pipeline
This repo is organized around three scripts. A typical workflow looks like:

1) **Parse transcripts → clean segments**
```bash
python Open_transcript.py
```

2) **Compute metrics (toxicity/sentiment) + aggregates**
```bash
python Text_calculation.py
```

3) **Generate visuals / summaries**
```bash
python Analysis_response.py
```

If any script supports CLI flags, you can discover them via:
```bash
python <script>.py --help
```

If a script uses hard-coded file paths (common for research prototypes), open it and update the input/output paths at the top.

---

## Inputs & outputs (recommended conventions)

Because transcript export formats vary by platform, VR-POLICE works best when you normalize into a simple table of text segments.

### Suggested input schema (segments)
| field | description |
|------|-------------|
| `segment_id` | unique id |
| `timestamp` | event time (or start time) |
| `speaker_id` | anonymized speaker identifier |
| `text` | transcript text for the segment |
| `language` | language code (e.g., `en`, `pt`, `fa`, `ar`) |

### Typical outputs
- **Per-language summary**: total segments, toxic segments, toxicity rate
- **Top toxic / sentiment-bearing words** (optional, language-dependent)
- **Plots**: bar charts for toxicity rate by language, frequency charts, etc.
- **JSON artifacts**: structured results suitable for downstream reporting

---

## Method notes (how to interpret results)

Toxicity detection is a *measurement problem*, not a truth oracle.

- Short utterances can be ambiguous (sarcasm, reclaimed slurs, friendly banter).
- Cross-cultural language can be especially tricky: direct translation ≠ equivalent harm.
- Always treat outputs as **signals for investigation**, not automatic judgments about people.

A practical way to use this tool:
1. Look at **language-level shifts** (spikes, drift, hotspots).
2. Drill into **examples** for context and labeling errors.
3. Use insights to refine **policy, prompts, training data, or moderation UX**.

---

## Privacy & safety

Voice-to-text transcripts can contain sensitive personal data.

- Prefer **anonymized speaker IDs**
- Avoid committing raw transcripts to GitHub
- Store outputs securely and limit access
- If you use LLMs for summarization, assume the text may be sensitive and follow your org’s data policy

---

## Roadmap (good next upgrades)

- Add `requirements.txt` + `Makefile` for one-command setup
- Standardize I/O with a `data/` and `outputs/` folder convention
- Add unit tests for transcript parsing (the messiest part of the pipeline)
- Add calibration / abstention options to reduce false positives
- Add a small sample dataset + expected output to enable quick verification

---
