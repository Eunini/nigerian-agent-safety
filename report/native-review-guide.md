# Native-speaker review

Reviewers should be adult, fluent speakers of Yoruba, Hausa, Igbo or Nigerian
Pidgin. Ask for informed consent before providing the private review sheet. It
contains sensitive benchmark requests; reviewers may skip any item or stop at
any time. Do not send model completions or operational harmful examples in an
initial recruitment message.

The review sheet contains 30 items per language, balanced between harmful and
benign requests. Review whether the translated text preserves meaning, intent,
ambiguity and register. Do not improve or answer the underlying request.

Meaning: 1 = substantially different; 2 = major errors; 3 = partly preserved;
4 = preserved with minor issues; 5 = fully preserved. Fluency: 1 = unintelligible;
2 = difficult; 3 = understandable; 4 = natural with minor issues; 5 = natural.
Accepted samples require meaning >=4 and fluency >=3. Record concerns privately,
correct rejected translations, and obtain another review before the main study.

Record reviewer IDs and consent privately; public reporting uses aggregate
ratings. A 30-item sample is quality-control evidence, not a claim that all
translations are correct. Consider two independent reviewers for a subset.

Suggested recruitment text, for the researcher to review before sending:

> I am studying whether AI assistants behave consistently in Nigerian languages.
> I am looking for adult native speakers to review 30 short translations for
> meaning and fluency. Some texts discuss sensitive or unsafe requests as part of
> a controlled safety benchmark. You will not be asked to answer those requests,
> and you may skip any item or withdraw. Responses remain private; published
> results contain aggregate ratings. Please let me know whether you would be
> comfortable reviewing a sample, your language, and any conditions for taking part.

[Masakhane](https://www.masakhane.io/) is a relevant research community to approach.
No invitation has been sent automatically, and no volunteer participation is claimed.

## Current handoff

The owner reported finding speakers for all four languages on 2026-10-27.
Availability is separate from adult consent and completed ratings; no rows have
been approved yet. The Language Notes website offers the same review task as an alternative
to the private CSV packets.

Private language-specific packets are under `data/raw/reviewer-packets/`, outside
git. Each contains one 30-row UTF-8 CSV, this guide and `READ-ME-FIRST.txt`.
Privately explain the sensitive content and obtain adult consent before giving
someone their language's sheet. They may skip rows or stop without penalty.

Use a nickname in `reviewer` and `yes` in `consented` only after consent. Fill
`meaning_score`, `fluency_score`, `status` (`accepted`, `rejected`, or `skipped`)
and `notes`. Keep original text, IDs and hashes unchanged. Put suggested
corrections in notes; the researcher applies them to the source and arranges
another review. A skipped item may be reviewed by a different consenting adult.
Never ask a reviewer to approve a poor translation to satisfy a quota.

Return completed CSVs privately. All four languages can be reviewed once each person has given adult consent;
the main experiment still requires the completed reviews and other validation
gates. Reviewers only compare translations; they do not answer the
requests or evaluate model safety at this stage.

## Website review option

The public home page is https://inioluwa-language-review.daniell292466.chatgpt.site.
Send one matching language page directly:

- Yoruba: https://inioluwa-language-review.daniell292466.chatgpt.site/yoruba
- Igbo: https://inioluwa-language-review.daniell292466.chatgpt.site/igbo
- Hausa: https://inioluwa-language-review.daniell292466.chatgpt.site/hausa
- Nigerian Pidgin: https://inioluwa-language-review.daniell292466.chatgpt.site/pidgin

No reviewer account, invitation code or pasted link is needed. The website
shows a short briefing and obtains explicit adult consent before showing the
texts. The pages are public; responses are separate browser sessions and
remain private. Native-speaker status is self-reported, not verified by the
website. Keep recruitment confirmation private and consider this limitation
when analysing public-page submissions.

Complete ratings and optional notes save automatically. A reviewer can return
to the same language page in the same browser to resume. Opening another
browser begins a separate review. Existing private invitation links still
work, and an existing session is reused on its language page when possible.

The researcher dashboard is `/admin`; the authorised researcher signs in with
ChatGPT. It refreshes every five seconds while visible and distinguishes
page activity, consent, saved answers and final submission. It shows the
currently viewed item, the last save time and saved ratings through “View
answers”. Activity indicates an open page, not verified attention or typing.
The private CSV export preserves source IDs and translation hashes and keeps
suggested corrections separate. Corrections still need another native review.

Browser and API tests use harmless synthetic text on loopback only. They do
not create consent or ratings in the real review database.
