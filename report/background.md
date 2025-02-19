# Background

**Yong, Menghini and Bach (2023/2024).** The authors show that translating unsafe
English inputs into low-resource languages can expose cross-lingual weaknesses
in GPT-4 safeguards. This is evidence about the tested model and attack setting,
not proof that every current model or Nigerian language behaves identically.
The present study tests a different interaction boundary: whether multilingual
requests cause tool attempts as well as unsafe text, and whether a translation
gate changes that behavior.
[Paper](https://arxiv.org/abs/2310.02446).

**HarmBench (Mazeika et al., 2024).** HarmBench standardizes automated red-team
evaluation, behavior sets and completion assessment. It motivates using fixed,
versioned harmful behaviors and a stable scoring policy rather than inventing
an attack set after seeing model failures. Here, a category-balanced sample of
standard text behaviors is imported privately. The implemented fixed-prompt
judge is a separate evaluator; it is not misrepresented as the released
HarmBench classifier, and requires human calibration.
[Paper](https://arxiv.org/abs/2402.04249),
[authors' repository](https://github.com/centerforaisafety/HarmBench).

**XSTest (Röttger et al., 2023/2024).** XSTest evaluates exaggerated refusals on
benign prompts that resemble sensitive or unsafe requests, alongside unsafe
contrasts. Its contribution is making helpfulness loss visible when evaluating
safety interventions. This study draws only its safe-labelled items for the
benign set and measures over-refusal separately; a guard that blocks everything
must not be presented as a successful safety intervention.
[Paper](https://arxiv.org/abs/2308.01263),
[authors' repository](https://github.com/paul-rottger/exaggerated-safety).
