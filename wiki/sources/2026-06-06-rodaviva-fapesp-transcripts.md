---
type: source
tags: [corpus, real-text, speech-acts, ptbr, data-collection]
added: 2026-06-06
url: https://rodaviva.fapesp.br/
---

# Memória Roda Viva (FAPESP) — interview transcripts

Public archive (Labjor/Unicamp + FAPESP + Fundação Padre Anchieta) of full transcripts
from TV Cultura's *Roda Viva* — 200+ interviews available (targeting 1200+), 21 years of
the program. Open, clean, speaker-labeled dialogue.

## Why it matters here

The v1 dataset is **synthetic** (teacher-generated), so the sentences themselves are
artificial. Roda Viva gives **real PT-BR dialogue** with high speech-act diversity
(debate/interview → `perguntar`, `discordar`, `prometer`, accusation/`insultar`,
`expressar_emocao`), which synthetic prose lacks. Public domain → no consent/PII problem
(unlike importing tweets/WhatsApp, which was abandoned for that reason).

## Format (parser-relevant)

ISO-8859-1 HTML; each turn is `<p ...><strong>Speaker:</strong> text</p>` with HTML
entities. Parsed by `lib/fapesp.ts` in the web repo. Example: the Mano Brown episode
(2007) → 304 turns, 8 speakers. URL pattern: `/materia/<id>/entrevistados/<slug>.htm`.

## How it's used

Feeds the `/assistir` flow (web repo): the in-browser model proposes spans→acts on each
turn, the human corrects → `span_annotation`. See
[Human-in-the-Loop Distillation](../concepts/human-in-the-loop-distillation.md).

YouTube captions were tried first and abandoned — the timedtext endpoint returns empty
(token-gated since ~2024) and yt-dlp hits HTTP 429 / needs impersonation. FAPESP text is
the reliable source; the YouTube video can sit alongside for *tone*, not as the text source.
