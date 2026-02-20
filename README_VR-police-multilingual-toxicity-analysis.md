# VR‑POLICE — Multilingual Toxicity Analytics for Social‑VR Voice Chat

Turn messy voice‑to‑text transcript exports from social VR into **language‑aware safety signals**: toxicity proxies, per‑language rates, and “what words are driving it” summaries — with optional visualization that’s easy to paste into a deck.

This repo is intentionally a **research prototype / work sample**: it favors readability and end‑to‑end reproducibility over perfect packaging.

---

## What this pipeline actually does (end‑to‑end)

### 1) Ingest transcript exports (`.pkl`) → normalized segments (`.csv`)
`Open_transcript.py` reads pickle files that contain a transcript “content” object with a `segments` list and a top‑level `language`. It extracts:

- `text`
- `voice_file_address` (source filename)
- `start_time`, `end_time`
- `language`

…and writes one merged table: `all_text_segments.csv`.

### 2) Clean + score each segment (sentiment model used as a toxicity proxy)
`Text_calculation.py`:

- preprocesses text with **spaCy** (lowercasing, removing symbols, lemmatizing, keeping content POS: ADJ/ADV/VERB/NOUN, removing duplicates)
- runs `transformers.pipeline("sentiment-analysis")` using  
  `distilbert-base-uncased-finetuned-sst-2-english`
- stores the label as `Sentiment_Type` (`POSITIVE` / `NEGATIVE`)

> Important: **the current code uses sentiment as a stand‑in for toxicity** (i.e., “NEGATIVE ≈ toxic”).  
> That is a reasonable *screening signal* for quick analysis, but it is not a ground‑truth toxicity classifier.

### 3) Aggregate cross‑lingual “toxicity” rates
Still in `Text_calculation.py`, the pipeline aggregates by `language`:

- Total texts
- “Toxic” texts (currently counted as `NEGATIVE`)
- Toxicity rate (%)

It writes `toxicity_analysis.json`.

### 4) Generate per‑language keyword evidence
Also in `Text_calculation.py`:

- writes a per‑language word frequency file (positive vs. negative buckets)  
  e.g., `en_word_frequencies.txt`, `pt_word_frequencies.txt`, etc.

### 5) (Optional) LLM‑assisted structured summary + visualization
The repo also supports a workflow where you copy an LLM’s JSON‑ish output back into a script:

- `Text_calculation.py` writes a **prompt template** to `prompt.txt` to guide structured summarization.
- `Analysis_response.py` reads the (often messy) model output, **cleans / fixes** it into JSON, and plots the **relative frequency** of top toxic words by language.

This is useful when you want a clean “executive summary” artifact but the raw LLM output isn’t perfectly valid JSON.

---

## Repo structure

```text
.
├── Open_transcript.py       # .pkl transcripts → all_text_segments.csv
├── Text_calculation.py      # preprocess + score + aggregate + keywords + prompt.txt
├── Analysis_response.py     # parse messy JSON-like model output → visualization
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

```bash
pip install pandas numpy matplotlib scikit-learn transformers torch spacy
python -m spacy download en_core_web_sm
```

> GPU is optional. The pipeline will use it automatically if PyTorch sees one.

### 3) Point the scripts at your data (important)

Right now, both `Open_transcript.py` and `Text_calculation.py` contain **hard‑coded Windows paths**.  
For your run, open each file and change the path variables near the bottom:

- In `Open_transcript.py`: `input_directory_path = "..."`  
  (folder containing transcript `.pkl` files)

- In `Text_calculation.py`: `file_path = "..."`  
  (path to `all_text_segments.csv`)

Suggested convention:

```text
project/
  data/
    transcripts_pkl/
  outputs/
    run_YYYYMMDD_HHMMSS/
```

---

## Run the pipeline

### Step A — Parse transcripts → CSV

```bash
python Open_transcript.py
```

Expected output (auto‑timestamped folder):

- `output_YYYYMMDD_HHMMSS/all_text_segments.csv`
- `output_YYYYMMDD_HHMMSS/<filename>_content.txt` (debug dumps)

### Step B — Compute metrics + export artifacts

Edit `Text_calculation.py` to point to your `all_text_segments.csv`, then:

```bash
python Text_calculation.py
```

Outputs (default folder `word_frequencies_by_language/`):

- `toxicity_analysis.json`
- `<lang>_word_frequencies.txt` for each language present
- `prompt.txt` (for optional LLM structured analysis)

### Step C (Optional) — Visualize “top toxic words by language”

If you have a structured JSON output from an LLM (or any tool), run:

```bash
python Analysis_response.py
```

Then paste the model output when prompted and type `END`.

The script will:
1) clean/repair mixed content into valid JSON
2) plot relative frequencies of top toxic words (default top 5)

---

## Input formats

### Expected `.pkl` schema (what `Open_transcript.py` expects)

Each `.pkl` file should deserialize into a dict‑like object containing:

- `language` (string)
- `segments` (list of dicts), each with keys like:
  - `id`
  - `start`, `end`
  - `text`

If your export differs, adapt the extraction logic in `print_all_pickle_files_content()`.

### Expected CSV schema (what `Text_calculation.py` expects)

`all_text_segments.csv` must contain:

- `text`
- `language`

(The parser also writes `voice_file_address`, `start_time`, `end_time`, which are useful for drilling into examples.)

---

## How to interpret results (don’t let metrics cosplay as truth)

This repo produces **safety signals**, not final judgments.

- Voice transcripts are noisy (ASR errors, accents, code‑switching, short fragments).
- “Negative sentiment” is not the same as “harmful toxicity.”
- Some communities reclaim slurs or use profanities affectionately.

Best practice:
1) Use the aggregate rates to detect **spikes / drift / hotspots** by language.
2) Drill into examples (use `voice_file_address` + timestamps).
3) Improve measurement: replace the sentiment proxy with a true toxicity model + calibration.

---

## Swapping in a real toxicity detector (recommended)

`Text_calculation.py` currently calls:

```python
pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
```

To upgrade:
- switch the pipeline task/model (e.g., a multilingual toxicity classifier)
- rename `Sentiment_Type` to something like `Toxic_Label`
- re‑define what counts as “toxic” during aggregation

If you care about precision (you usually should), add:
- a confidence threshold
- an “abstain/unknown” bucket
- manual review sampling for calibration

---

## Privacy & safety

Transcripts can contain personal data.

- Don’t commit raw transcripts to GitHub.
- Prefer anonymized speaker IDs.
- Store outputs securely.
- If you use an external LLM for summarization, follow your org’s data policy.

---

## Roadmap (easy upgrades that make this repo feel “production-ready”)

- Add `requirements.txt` (pinned versions)
- Standardize `data/` + `outputs/` directories + CLI flags
- Add a small sample dataset + expected outputs for verification
- Add toxicity calibration + abstention to reduce false positives
- Add slice reports for low‑resource languages (variance is the story)

---

## About

Automate the detection, measurement, and visual reporting of toxic behaviour in social‑VR voice chat so designers can make data‑driven safety decisions.
