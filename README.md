# Do agent safety refusals hold up in Nigerian languages?

**Research status: protocol and implementation; model findings are pending.**

Ethics rules, written before any model experiment:

- Never publish harmful model outputs. Public reports contain aggregate rates only.
- All tools are inert Python stubs. They never send messages, search the web, write
  a requested file, or execute generated code.
- Observe the license and terms of every benchmark, model, translator, and API.
- Privately disclose a serious commercial-model gap before publishing affected findings.
- Keep source harmful prompts, translations, trajectories and human review in
  ignored private directories with restricted filesystem permissions.
- Native reviewers consent before seeing sensitive content and may skip any item.

The study compares English, Yoruba, Hausa, Igbo and Nigerian Pidgin, with plain
chat and tool-using agents, before and after a translate-to-English safety check.
The safety check uses an actual back-translation; it never substitutes the gold
English source as if translation were perfect.

```bash
python3.12 -m venv .venv
. .venv/bin/activate
pip install -e '.[dev]'
pytest -q
python -m safety.import_data
# Review source licenses, then configure model and translator endpoints locally.
python -m safety.translate --inputs data/raw/english.jsonl --out data/raw/translations.jsonl --config configs/local.json
python -m safety.review prepare --inputs data/raw/translations.jsonl --out runs/private/native-review.csv
# Complete native reviews externally; validate them before the study.
python -m safety.review validate --reviews runs/private/native-review.csv
python -m safety.run --inputs data/raw/translations.jsonl --config configs/local.json --reviews runs/private/native-review.csv --out runs/private/study.jsonl
python -m safety.score --run runs/private/study.jsonl --config configs/local.json --out runs/private/judged.jsonl
python -m safety.review labels --inputs runs/private/judged.jsonl --out runs/private/human-labels.csv
python -m safety.calibrate --judged runs/private/judged.jsonl --labels runs/private/human-labels.csv --out report/judge-agreement.json
python -m safety.report --judged runs/private/judged.jsonl --out report/results
python scripts/make_pdf.py
```

Copy `configs/example.json` to ignored `configs/local.json`. API keys are read from
environment variables named in configuration; no keys go in JSON files. An endpoint
must be an API root such as `http://127.0.0.1:8080/v1`. Select models and their exact
revisions after checking licenses and free-tier quotas. No paid endpoint is assumed.

NLLB-200 is not assumed to support Nigerian Pidgin. This implementation uses a
configurable translation endpoint for all languages and requires native review.
Automatic translation alone is not evidence of translation quality.

Read [the protocol](report/protocol.md), [background](report/background.md), and
[completion record](report/completion.md). The PDF is explicitly labelled a draft
until results, human calibration and disclosure review are complete.

The full design is 4 models × 5 languages × 200 prompts × 2 interaction modes ×
2 guard conditions = **16,000 target evaluations**, plus translation, safety-check
and judge requests. Free-tier quotas may require multiple sessions. Failed calls
and missing judgments are reported separately and never treated as successful refusals.
