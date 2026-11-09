# Karpathy Regula

Karpathy's coding guidelines for Claude Code and Codex, rewritten so that each
instruction keeps its condition, its action and its reason together. Both hosts
load one shared English skill, `coding-guidelines`, with four principles: think
before coding, keep implementations simple, make scoped changes, and define
verifiable goals.

This is an unofficial adaptation of the Karpathy Guidelines skill by
[forrestchang](https://github.com/forrestchang); see
[attribution](plugins/karpathy-regula/NOTICE.md). It has not been shown to produce
better code than the original; see [Evidence and limits](#evidence-and-limits).

## Install

### Claude Code

1. In Claude Code, add the marketplace:

   ```text
   /plugin marketplace add ajitta/karpathy-regula
   ```

2. Install the plugin:

   ```text
   /plugin install karpathy-regula@karpathy-regula
   ```

3. Start a new session.
4. Put the skill's name in front of a coding task:

   ```text
   /karpathy-regula:coding-guidelines Fix the discount bug in cart.py without touching anything else.
   ```

From a terminal, steps 1 and 2 are `claude plugin marketplace add ajitta/karpathy-regula`
and `claude plugin install karpathy-regula@karpathy-regula`. The plugin is also listed
in the [ajitta catalog](https://github.com/ajitta/claude-plugins) as
`karpathy-regula@ajitta`. Install it through one route only; two routes give you
two copies of the skill.

### Codex

1. In a terminal, add the marketplace:

   ```sh
   codex plugin marketplace add ajitta/karpathy-regula
   ```

2. Install the plugin:

   ```sh
   codex plugin add karpathy-regula@karpathy-regula
   ```

3. Start a new Codex session.
4. Put the skill's name in front of a coding task:

   ```text
   $karpathy-regula:coding-guidelines Fix the discount bug in cart.py without touching anything else.
   ```

In the desktop app, the registered marketplace can also be opened in the Plugins
directory. Availability depends on the host version and workspace settings.

### Does it load without being named?

Both hosts list the skill with its description, so a model may load it when a
coding task matches that description. In a small check (one coding request that did
not name the skill, two runs per host), Codex CLI 0.166.0 with `gpt-6.1-sol` read
the skill on its own in both runs, while Claude Code 2.1.314 with its default model
listed it but did not load it in either run. In Claude Code,
name the skill as in step 4 when you want it applied.

### Update or remove

Claude Code, from a terminal:

```sh
claude plugin marketplace update karpathy-regula
claude plugin update karpathy-regula@karpathy-regula
claude plugin uninstall karpathy-regula@karpathy-regula
```

Codex:

```sh
codex plugin marketplace upgrade karpathy-regula
codex plugin add karpathy-regula@karpathy-regula
codex plugin remove karpathy-regula@karpathy-regula
```

The first two lines of each block update; the last line removes the plugin.
Start a new session after either.

## What you will notice

The clearest observed difference is a short statement of the planned edit, and of
what will be left alone, before the first edit. One task from the research runs
(Codex, gpt-6.1-sol, the skill file read before the task):

> Change label in labels.py to return name.strip().lower() directly instead of
> calling wrap_label.

`labels.py` also imports `legacy_helper`, which nothing uses. The original
guidelines' run (`pilot-cleanup-02-original`) posted:

> I’ll read the requested karpathy-guidelines skill, then make the change in
> `labels.py` and verify it locally.
>
> Updated `labels.py` so `label` returns `name.strip().lower()` directly. Removed
> the unused `wrap_label` import.
>
> Verified whitespace trimming, lowercasing, and empty inputs with local Python.

This revision's run (`pilot-cleanup-02-revised`) posted:

> I’ll read the requested karpathy-guidelines skill, then make the change in
> `labels.py`.
>
> I’ll change the return expression and remove `wrap_label` from the import. I’ll
> leave the existing unused `legacy_helper` import in place and check that `label`
> strips whitespace and lowercases the name.
>
> Updated `labels.py` so `label` returns `name.strip().lower()` directly. Removed
> the unused `wrap_label` import.
>
> Syntax and behavior checks passed.

Both runs changed the return, removed only `wrap_label` from the import and kept
`legacy_helper`. The difference is the middle message, posted before any file
changed. On this task it appeared in every
revision run and in no original run (pilot 3/3 against 0/3, later re-run 4/4
against 0/4).

## What changed, and why

The revision used **dia-regula 2.2.0**, a skill for writing and reviewing model
instructions from [ajitta/dialectic-skills](https://github.com/ajitta/dialectic-skills).
Its four rules concern keeping conditions and actions together, bounding editing
permissions precisely, reducing instructions while keeping their reasons, and using
one name per thing. The [exact standard used](docs/research/karpathy-regula-2026-11-08/inputs/dia-regula-2.2.0.md)
also separates required rules from optional writing advice. It is an authoring
method; you do not need to install dia-regula to use this plugin.

| Area | Original | This revision |
|---|---|---|
| Conditions | Headings such as "Before implementing:" gate several separate bullets. | Each condition sits in the paragraph with the actions it gates. |
| Reasons | Most requirements are short commands without a local explanation. | Related requirements share an explicit reason, such as avoiding complexity that does not serve the request. The reasons are the editor's, not the original author's. |
| Slogans | A bold slogan heads each section. | Slogans that repeat a requirement below them are folded in. One, "Surface tradeoffs" in section 1, was not repeated below; it became a step: "Before implementing, surface tradeoffs and say if a simpler approach exists, pushing back when warranted, because the user needs to see these choices before implementation commits to an approach." |
| Core requirements | Four coding principles, scope restrictions, examples, and trivial-task discretion. | Retained. |

The added reasons and the new section 1 step change what a model may do, so they
are meaning changes, not rewording: dia-regula 2.3.0 counts an added reason as one,
because a reason lets the model generalize a rule to cases it does not name. The
[original snapshot](docs/research/karpathy-regula-2026-11-08/inputs/original-SKILL.md),
[evaluated revision](docs/research/karpathy-regula-2026-11-08/inputs/revised-SKILL.md)
and [review and adjudication record](docs/research/karpathy-regula-2026-11-08/review-and-adjudication.md)
let you compare them. The revision has fewer lines but 17.7% more body text.

## Evidence and limits

### The pilot

A pilot requested `gpt-6.1-sol` at high reasoning effort through Codex CLI 0.167.0:
six small Python tasks, three runs per version, 36 completed runs. The harness told
the model to read the skill file before the task.

| Observation | Original | Revision |
|---|---|---|
| Functional and scope checks | 18/18 | 18/18 |
| A message between reading the task files and the first edit (editing tasks) | 4/15 | 12/15 |
| Mean-denominator task: failing assertion against the correct expected value before the fix | 1/3 | 0/3 |

The message category was defined after the runs; in all 47 completed runs it
equals "the run posted a third public message". All three revised mean-task runs
checked the current wrong value before editing, but not with a failing assertion
against the correct value: more explanation did not mean stricter compliance with
the requested procedure. See the [process analysis](docs/research/karpathy-regula-2026-11-08/process-analysis.md).

### Re-run and section swap

A later review re-ran two of the tasks with the record's prompts and fixtures
(Codex CLI 0.166.0, `gpt-6.1-sol`, high effort, 28 runs), adding two mixed versions
that swap section 1 between the texts:

| Task | Original | Revision | Original with revised section 1 | Revision with original section 1 |
|---|---|---|---|---|
| cleanup | 0/4 | 4/4 | 4/4 | 1/4 |
| verification | 4/4 | 4/4 | 2/2 | 2/2 |

The cleanup difference recurred and follows section 1, the section whose meaning
changed. Which part of that section brings the message (the new step, its two
added reasons or the layout) was not isolated. The verification difference did not
recur: the original posted the message too, so the pilot's message difference on
that task (0/3 against 3/3) is an observation of one build and day. See [review.md](docs/research/karpathy-regula-2026-11-08/review.md)
and the [probe record](https://github.com/ajitta/dialectic-skills/blob/6db2b90c6e7e19bea5cf3dd7c11bd72a2a757a40/docs/probes.md#L826).

### What this does not show

There was no no-skill control, most tasks were small enough for both versions to
pass every functional check, and the pilot's follow-up was incomplete: 24 attempts
yielded 11 completed runs and 13 account-limit interruptions. Visible messages and
tool actions do not reveal private reasoning. None of this shows better judgment or
better code. See [evaluation methods and results](docs/research/karpathy-regula-2026-11-08/behavioral-evaluation.md).

### Known limits of the text

These come from the original and are kept, because a change to the skill body needs
its own comparison runs (see [AGENTS.md](AGENTS.md)):

- "For trivial tasks, use judgment." sits in a separate paragraph and relaxes all
  four sections without saying which steps it relaxes.
- "loop until they are verified" does not say what to do when no check can run.
- Section 4 turns "Fix the bug" into writing a test that reproduces it, but does not
  say whether to keep that test. On the verification task no completed run of
  either version kept one (0/17).

### Research archive

The [research archive](docs/research/karpathy-regula-2026-11-08/README.md) mirrors
the session record in ajitta/dialectic-skills at
[v2.9.0](https://github.com/ajitta/dialectic-skills/tree/6db2b90c6e7e19bea5cf3dd7c11bd72a2a757a40/docs/research/karpathy-regula-2026-11-08),
including `review.md`, which corrects the record where they differ. Paths inside it
such as `docs/spec.md`, `docs/probes.md` and `AGENTS.md` refer to that repository.
It holds the input texts, review history, exact task fixtures, all 60 attempted-run
results, process observations, selected execution excerpts, and unadopted proposals
for dia-regula. The full native event archive and private local paths are not
published. The source and the evaluated body's hash are recorded in
[provenance](docs/provenance.json).

## Names

| Item | Name |
|---|---|
| Repository | `ajitta/karpathy-regula` |
| Plugin and marketplace | `karpathy-regula` |
| Display name | Karpathy Regula |
| Skill | `coding-guidelines` |
| Claude Code invocation | `/karpathy-regula:coding-guidelines` |
| Codex invocation | `$karpathy-regula:coding-guidelines` |

`karpathy` preserves the source lineage; `regula` identifies the revision method.
The name does not imply endorsement or a proven performance gain. The skill body
keeps the original heading, "Karpathy Guidelines".

## Repository layout

```text
.claude-plugin/marketplace.json       Claude catalog
.agents/plugins/marketplace.json      Codex catalog
plugins/karpathy-regula/
  plugin.json                         Portable Agent Plugins manifest
  .claude-plugin/plugin.json          Claude compatibility manifest
  .codex-plugin/plugin.json           Codex compatibility manifest
  skills/coding-guidelines/
    SKILL.md                          Single shared instruction body
    agents/openai.yaml                Codex UI metadata
  LICENSE
  NOTICE.md
```

The host-specific manifests identify the same package and skill directory. There
are no servers, hooks, or runtime dependencies. The repository includes a
development-only YAML parser for validation.

## Validate and package

Python 3.11 or later:

```sh
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python tools/package.py --check
python tools/package.py
```

The archive is written to `dist/karpathy-regula-<version>.zip`. It contains only the
plugin, including hidden compatibility manifests, license, and attribution; the
marketplace catalogs stay in the repository. Entries are stored with fixed
timestamps and file modes, so rebuilding a release tag from 0.1.1 on gives the
SHA-256 in that release's `SHA256SUMS.txt`. Both native Claude validation and the
repository checks run in CI. Install and loading checks are recorded in
[validation](docs/validation.md).

For a local checkout, validate before installing:

```sh
claude plugin validate --strict plugins/karpathy-regula
claude plugin validate --strict .
```

## Releases

Download the plugin ZIP from [GitHub Releases](https://github.com/ajitta/karpathy-regula/releases).
Each release includes a SHA-256 checksum file. The research archive and marketplace
catalogs are in the repository and GitHub's generated source archives. Use the
marketplace commands above to install.

Format references: [Claude manifest](https://code.claude.com/docs/en/plugins-reference),
[Claude marketplaces](https://code.claude.com/docs/en/plugin-marketplaces),
and [OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins).

## License

MIT. The license and attribution ship with the plugin.
