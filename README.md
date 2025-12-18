VR-POLICE: Cross-Cultural Toxicity Detection & Insight Platform
Objective
Automate the detection, measurement, and visual reporting of toxic behaviour in social‑VR voice chat so designers can make data‑driven safety decisions.
My Contribution
Designed and coded the entire analytics workflow—from raw voice‑to‑text output to executive‑ready dashboards—using modern NLP and data‑engineering practices.
Key Outcomes
- 90 % reduction in manual transcript review time.
- Multilingual coverage (English, Portuguese, Dari, Arabic) with pluggable language models.
- Actionable dashboards adopted by the game‑design team for the next release cycle.
Technical Snapshot
Stack
Highlights
Python 3.11
pandas, spaCy, matplotlib, transformers
Machine Learning
DistilBERT sentiment fine‑tune, custom toxicity lexicons
Data Engineering
CLI‑driven modules, timestamped output pipeline, CSV/JSON interchange
Visualization
Matplotlib‑based bar plots & frequency charts
Collaboration
Git, README‑driven docs, requirements.txt
Repository Layout
vr‑police/
├── data_ingest.py             # parses *.pkl transcripts → clean CSV
├── crosslingual_toxicity.py   # sentiment + toxic‑word analytics, JSON prompt builder
├── llm_visualizer.py          # ingests LLM response, produces plots & reports ├── requirements.txt           # project dependencies
└── README.md                  
Skills Demonstrated
- Full‑stack data science – ingestion → NLP → visual analytics.
- Cross‑cultural NLP – lemmatization & sentiment across four languages.
- Prompt engineering – dynamic generation of LLM prompts tailored to detected language mix.
- Clean code & documentation – PEP‑8, type hints, CLI flags, and README‑first approach.
Future Roadmap
1. Real‑time processing via WebSockets.
2. Expand to additional languages with a multilingual transformer.
3. Containerise and deploy on AWS ECS for horizontal scalability.
<img width="468" height="620" alt="image" src="https://github.com/user-attachments/assets/918c7663-4c07-4cf0-b7d7-959b6d66c457" />
