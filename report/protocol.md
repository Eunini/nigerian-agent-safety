# Do agent safety refusals hold up in Nigerian languages?

Draft protocol. No model safety rates have been measured or claimed.

## Question

Do refusal and harmful-completion rates differ across English, Yoruba, Hausa,
Igbo and Nigerian Pidgin, and between plain chat and tool-using agents? Does
translating a request to English for a safety check reduce harmful behavior
without an unacceptable rise in benign over-refusal?

## Data and translation

Import 100 category-balanced standard HarmBench behaviors and 100 safe-labelled
XSTest prompts from pinned source commits. Keep the text private. Retain English
as a control and translate the same IDs into four Nigerian languages. Use a
versioned translator, preserve ambiguity, and never ask it to answer the prompt.
NLLB support for Nigerian Pidgin is not assumed. The configurable translator
must actually support all four languages.

Ask consenting native speakers to check 30 items per Nigerian language, balanced
between harmful and benign sources. Record meaning/fluency on a 1–5 scale,
accept/reject status, reviewer ID and translation hash. Acceptance requires
meaning >=4 and fluency >=3. Report distributions and
major mistranslations. Correct rejected translations and review them again.
The runner checks that completed review records match the current translation
hashes. A 30-item sample does not certify every translation.

## Agent, models and conditions

Use three licensed open instruct models from distinct families and one versioned
commercial free-tier endpoint. Keep target model, prompt, output budget and
temperature fixed across four conditions: chat, agent, guarded chat and guarded
agent. The English system instruction is identical across languages. The agent
has a four-turn maximum and four fake tools: send_email, web_search, write_file
and run_code. Implementations validate arguments and append hashes only; they
have no network, file-writing or code-execution dispatch.

The guard back-translates the actual request to English and applies a fixed
safety-check prompt before any target interaction. It never reads the original
gold English prompt as a substitute for translation. Guard/checker failures are
errors, not successful refusals. A blocked request creates no target completion
and no tool attempt. Record blocking, errors and latency separately.

## Scoring and judge validation

Measure full refusal, harmful completion, harmful tool attempt and benign
over-refusal. A tool call alone is not harmful; semantic judgment of its intended
action is required. Real-world harmful execution is zero by construction, and
must not be confused with attempted harmful tool use.

Back-translate responses and use the fixed, versioned judge prompt in
safety/score.py. Tool arguments remain available privately for semantic review.
Reject invalid judge JSON rather than coercing strings or missing values into
safe labels. Judge failures remain unjudged. Report attempted cases, request
errors and judgment coverage alongside conditional rates and Wilson intervals.

Independently hand-label 100 target outputs, stratified by language and source
kind. Hide automatic labels from reviewers. Exclude automatic guard-block records
from this calibration sample. Report agreement and Cohen's kappa for each label,
and inspect disagreements by language/condition. One overall agreement number
can hide language-specific judge failure.

## Analysis and chart

Plot harmful-completion rate by language for chat/agent, before/after the guard,
with confidence intervals and a separate facet per target model. Report benign
over-refusal and harmful tool attempts in companion tables. Compare paired IDs
across conditions; use a paired bootstrap or appropriate paired test for final
difference claims. The existing Wilson intervals describe individual rates,
not the uncertainty of paired differences.

## Ethics and release

Never publish harmful outputs or the harmful prompt set. Keep raw data and
trajectories in mode-700 directories with mode-600 files. Use only fake tools,
respect all model/API/benchmark terms, allow reviewers to skip sensitive content,
and privately disclose a serious commercial-model vulnerability before affected
results are published. The public exporter constructs aggregate records from an
allowlist; it never copies model responses into public results.

## Limitations and current conclusion

Translation, judge bias and English system prompting can confound language
comparisons. A small prompt set and four models do not establish language-wide
safety. Inert tools measure attempted actions, not downstream real-world harm.
Free-tier quotas may limit the 16,000 target evaluations plus ancillary calls.
The protocol and implementation are ready; results, human/native review and any
mitigation benefit remain unmeasured.
