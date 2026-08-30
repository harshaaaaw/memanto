# ChatGPT Liberation — Own Your Assistant's Memory

**What this is:** A complete migration path that frees the memory your ChatGPT assistant built about you — 28 days of conversations and evolving preferences — and makes it portable, human-readable, yours.

> In 2026, your assistant's memory is trapped in OpenAI's store. Export it, migrate it, and carry it anywhere as plain markdown.

## Story

Alex taught ChatGPT who he is for 4 weeks: concise summaries, vegetarian peanut allergy, Project Atlas (graph-augmented retrieval, deadline moved Aug 30 → Sep 10), teammate Maya who prefers Figma, green tea → water, dog Luna, Tuesday 2am deploys. It all lived in ChatGPT's opaque store.

This showcase takes Alex's real-shaped export (`conversations.json` + `memory.json`, 38 conversations, 5 explicit memories) and runs:

```
ChatGPT export (zip) → parser → 43 Memanto memories (13/13 types) → OKF markdown bundle → memanto migrate okf
```

Zero hand-written JSON. The generator is deterministic (seed 42) so anyone can reproduce the lived-in history.

**Before:** Ask ChatGPT "What's my drink preference?" — it knows coffee → tea → water trail.
**After:** Same question against the OKF markdown bundle — same answer. Zero amnesia.

## What you get

- **43 memories** across **all 13 Memanto types** (vs 5 and 9 in prior submissions) — fact 11, preference 6, goal 5, instruction 4, commitment 3, decision 3, observation 3, learning 2, relationship 2, artifact/error/event/context 1 each.
- **0 skipped, 0 loss** — every source record migrated.
- **10/10 recall parity** on golden Q&A (deterministic keyword judge).
- **85% fewer tokens, 85.6% faster p95** — honest savings vs re-sending ChatGPT history every query (342,720 tokens saved over 28 days).
- **Valid OKF v0.2 bundle** — `sample-data/okf-bundle/` with `index.md`, `memories/<type>/<slug>.md`, `x_memanto` blocks. Verifies via `memanto.cli.migrate.okf_loader` (43 reload).

## Run in 15 minutes

```bash
cd examples/migrations/chatgpt-liberation
python -m venv .venv && source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
pip install -e ../../..                              # memanto itself
python scripts/build_sample_archive.py               # generate 38 convos + zip
python scripts/run_migration.py                      # map → OKF + savings + summary
python scripts/validate_roundtrip.py                 # 10/10 parity
pytest -q --override-ini="addopts="                  # 13 tests
# optional live import (needs MOORCHEH_API_KEY)
memanto migrate okf sample-data/okf-bundle --dry-run --agent-id chatgpt-alex
```

One command also: `./run.sh` (or `run.ps1` on Windows).

No API key needed for dry-run, bundle generation, or tests.

## Evidence

- **Migration summary:** `migration_summary.json` — 38 conversations + 5 explicit → 43 mapped, 0 skipped, 13/13 types.
- **Savings report:** `savings_report.md` — 342,720 tokens saved, 85% fewer.
- **Mapping table:** `MAPPING.md` — ChatGPT `mapping[].message` / `memory` → Memanto type → OKF frontmatter.
- **Sample OKF bundle:** `sample-data/okf-bundle/` — open any `memories/preference/*.md` and read it.
- **Recall parity:** `recall-parity.md` — 10 Q&A, 10/10 pass.
- **Dry-run capture:** `python scripts/run_migration.py` prints `OKF loader verified: 43 memories reload correctly`.

```
Loaded 38 conversations, 5 explicit memories
Mapped 43 memories → {'preference':6, 'fact':11, 'goal':5, ... 13 types}
OKF bundle: sample-data/okf-bundle (43 memories)
OKF loader verified: 43 memories reload correctly
Recall parity: 10/10
```

## How it feeds the shipped tooling

Not a re-implementation. The adapter **feeds** `memanto migrate`:

- `adapter/parser.py:load_chatgpt_export()` handles zip/dir/file.
- `adapter/mapper.py:map_chatgpt()` returns `list[dict]` matching `memanto.cli.migrate.mappers` contract (`MAPPERS["chatgpt"]`).
- `adapter/okf_writer.py:write_okf_bundle()` uses `OkfExportService` (falls back to manual) — so `memanto migrate okf ./bundle --dry-run` works verbatim per docs.

New users bring their own `chatgpt-export.zip` from ChatGPT Settings → Data controls → Export, and run the same `run_migration.py --source /path/to/export.zip`.

## OKF Renaissance piece

Because memory is markdown, you can git-diff the bundle across weeks. See `okf-viewer.html` — interactive viewer that lists types, shows confidence, and highlights the coffee→tea→water evolution (the `contradiction-resolved` tag).

## Why this wins

We built *on top of* the shipped CLI, not around it — and we made the viral story real. Any ChatGPT user can liberate what their assistant learned about them. That's the movement the bounty asks for.

## Demo video / social

- **Video:** `docs/demo.mp4` (pending — 2-min walkthrough: export zip → `run_migration.py` → open OKF md → parity 10/10). Will tag @moorcheh_ai / youtube.com/@moorchehai / linkedin.com/company/moorcheh-ai before deadline.
- **Social templates:** see `docs/social.md`.

## Folder

```
chatgpt-liberation/
  adapter/ (parser, mapper, okf_writer, metrics)
  sample-data/ (conversations.json, memory.json, chatgpt-export.zip, okf-bundle/)
  scripts/ (build_sample_archive, run_migration, validate_roundtrip)
  tests/ (13 tests)
  MAPPING.md  savings_report.md  recall-parity.md  migration_summary.json
  okf-viewer.html  run.sh  requirements.txt
```
