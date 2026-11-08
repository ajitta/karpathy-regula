# Karpathy Regula

Karpathy's coding guidelines rewritten to keep each instruction's conditions,
actions, and reasons together, packaged for Claude Code and Codex. Both hosts load
one shared English skill.

The four principles are: think before coding, keep implementations simple, make
scoped changes, and define verifiable goals. This is an unofficial adaptation;
see [attribution](plugins/karpathy-regula/NOTICE.md).

## What changed, and why?

The revision used **dia-regula 2.2.0**, a skill for reviewing and writing model
instructions from [ajitta/dialectic-skills](https://github.com/ajitta/dialectic-skills).
Its four rules concern keeping conditions and actions together, bounding editing
permissions precisely, reducing instructions while retaining reasons, and using
consistent names. The [exact standard used](docs/research/karpathy-regula-2026-11-08/inputs/dia-regula-2.2.0.md)
also distinguishes required rules from optional writing advice. It is an authoring
method; you do not need to install dia-regula to use this plugin.

| Area | Original | This revision |
|---|---|---|
| Conditions | Headings such as "Before implementing:" gate several separate bullets. | The condition sits in the paragraph containing the actions it gates. |
| Reasons | Some requirements are short commands without a local explanation. | Related requirements share an explicit reason, such as avoiding complexity that does not serve the request. |
| Repetition | Bold slogans repeat requirements stated below them. | Repeated slogans are folded into the operative paragraphs. |
| Core requirements | Four coding principles, scope restrictions, examples, and trivial-task discretion. | These are retained; paragraph layout and explanatory wording change. |

For example, the original separates "When editing existing code:" from "Match
existing style, even if you'd do it differently." The revision places that scope
and action in the same paragraph and explains that unrelated edits and style
changes obscure the requested change. This is intended to make applicability and
purpose easier to use together; a causal benefit has not been established.

The [original snapshot](docs/research/karpathy-regula-2026-11-08/inputs/original-SKILL.md),
[evaluated revision](docs/research/karpathy-regula-2026-11-08/inputs/revised-SKILL.md),
and [review and adjudication record](docs/research/karpathy-regula-2026-11-08/review-and-adjudication.md)
let you inspect the changes. The revision has fewer lines but more body text;
it is not a compression claim. Added reasons are editorial interpretation, and
their effects remain unmeasured separately from the layout change.

## Names

| Item | Name |
|---|---|
| Repository | `ajitta/karpathy-regula` |
| Plugin and marketplace | `karpathy-regula` |
| Skill | `coding-guidelines` |
| Claude Code invocation | `/karpathy-regula:coding-guidelines` |
| Codex invocation | `$karpathy-regula:coding-guidelines` |

`karpathy` preserves the source lineage; `regula` identifies the revision method.
The name does not imply endorsement or a proven performance gain.

## Claude Code

In Claude Code:

```text
/plugin marketplace add ajitta/karpathy-regula
/plugin install karpathy-regula@karpathy-regula
```

Start a new session and invoke:

```text
/karpathy-regula:coding-guidelines Fix this bug while preserving unrelated code.
```

For a local checkout, validate and inspect it before installing:

```sh
claude plugin validate --strict plugins/karpathy-regula
claude plugin validate --strict .
```

## Codex

From a terminal:

```sh
codex plugin marketplace add ajitta/karpathy-regula
codex plugin add karpathy-regula@karpathy-regula
```

Start a new chat and invoke `$karpathy-regula:coding-guidelines` with the coding
task. In the desktop app, the registered marketplace can also be opened in the
Plugins directory. Installation availability depends on the host version and
workspace settings.

## Repository layout

```text
.claude-plugin/marketplace.json       Claude catalog
.agents/plugins/marketplace.json      Codex catalog
plugins/karpathy-regula/
  plugin.json                         Portable Agent Plugins manifest
  .claude-plugin/plugin.json           Claude compatibility manifest
  .codex-plugin/plugin.json            Codex compatibility manifest
  skills/coding-guidelines/
    SKILL.md                          Single shared instruction body
    agents/openai.yaml                Codex UI metadata
  LICENSE
  NOTICE.md
```

The host-specific manifests identify the same package and skill directory.
There are no servers, hooks, or runtime dependencies. The repository includes a
development-only YAML parser for validation.

## Validate and package

Python 3.11 or later:

```sh
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python tools/package.py --check
python tools/package.py
```

The archive is written to `dist/karpathy-regula-0.1.0.zip`. It contains just the
plugin, including hidden compatibility manifests, license, and attribution.
The marketplace catalogs stay in the repository rather than inside the plugin
archive. Both native Claude validation and the repository checks run in CI.
The local discovery/installation check and its limits are recorded in
[validation](docs/validation.md).

## Evidence and limits

The [research archive in this repository](docs/research/karpathy-regula-2026-11-08/README.md)
contains the input texts, review history, exact task fixtures, all 60 attempted-run
results, public process observations, selected execution excerpts, and unadopted
proposals for improving dia-regula. It mirrors the earlier
[session record](https://github.com/ajitta/dialectic-skills/tree/562369929331854a95a5415e94790d5eb68d9b85/docs/research/karpathy-regula-2026-11-08).
The full native event archive and private local paths are not published.

A pilot requested `gpt-6.1-sol` at high reasoning effort through Codex CLI 0.167.0:
six small Python tasks, three repetitions per version, 36 completed runs.

| Observation | Original | Revision |
|---|---|---|
| Functional and scope checks | 18/18 | 18/18 |
| Specific intermediate policy message after file inspection and before source edits | 4/15 editing runs | 12/15 editing runs |
| Mean-denominator task: failing assertion against the correct expected value before the fix | 1/3 | 0/3 |

The last row matters: all three revised mean-task runs checked the current wrong
value before editing, but that diagnostic check was not a failing regression
assertion. More explanation does not automatically mean stricter compliance with
the requested procedure. See [process analysis](docs/research/karpathy-regula-2026-11-08/process-analysis.md)
for command order and case-level differences.

The process analysis is post-hoc. Visible messages and tool actions do not reveal
private internal reasoning. The study had no no-skill control or layout/reason
ablation, and its follow-up was incomplete: 24 attempts yielded 11 completed runs
and 13 account-limit interruptions. These observations establish neither improved
internal judgment nor a general coding-performance gain. Intended benefits remain
unmeasured as causal effects; the renamed plugin invocation has not had a new
behavioral evaluation. See [evaluation methods and results](docs/research/karpathy-regula-2026-11-08/behavioral-evaluation.md).

No untested additions proposed in that discussion are included here. The source
and evaluated-body hash are recorded in [provenance](docs/provenance.json).
Changing the plugin identity or UI metadata is distinct from changing its coding
instructions.

## Releases

Download the plugin ZIP from [GitHub Releases](https://github.com/ajitta/karpathy-regula/releases).
Each release includes a SHA-256 checksum file. The ZIP contains the plugin; the
research archive and marketplace catalogs are in the repository and GitHub's
automatically generated source archives. Use the marketplace commands above for
host installation.

Format references: [Claude manifest](https://code.claude.com/docs/en/plugins-reference),
[Claude marketplaces](https://code.claude.com/docs/en/plugin-marketplaces),
and [OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins).

## License

MIT. The license and attribution ship with the plugin.
