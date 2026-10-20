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

The public briefing is at https://inioluwa-language-review.daniell292466.chatgpt.site.
Reviewers need an individual, private invitation for their assigned language.
The website obtains adult consent before showing any packet text. Do not post
invitation links publicly or reuse one link for several people. There is no
reviewer ChatGPT account requirement.

The researcher dashboard is `/admin`; the authorised researcher signs in with
ChatGPT to create more invitations, monitor consent and progress, and export
a private CSV. The export preserves source IDs and translation hashes and
keeps suggested corrections separate. Availability, consent, saved decisions
and final submission are different states. No automated test ratings enter
the real review database. Corrections still need another native review.
