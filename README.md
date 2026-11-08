# Karpathy Regula

Karpathy's coding guidelines, revised with dia-regula and packaged for Claude Code
and Codex. Both hosts load one shared English skill.

The four principles are: think before coding, keep implementations simple, make
scoped changes, and define verifiable goals. This is an unofficial adaptation;
see [attribution](plugins/karpathy-regula/NOTICE.md).

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

The packaged body matches the reviewed revision from the
[2026-11-08 research session](https://github.com/ajitta/dialectic-skills/tree/main/docs/research/karpathy-regula-2026-11-08).
The original and revised instructions tied on the pilot's functional/scope checks.
The revision more often disclosed conditions and edit boundaries before acting.
These observations do not establish improved internal judgment or general coding
performance. Follow-up runs were incomplete because of an account usage limit.

No untested additions proposed in that discussion are included here. The source
and evaluated-body hash are recorded in [provenance](docs/provenance.json).
Changing the plugin identity or UI metadata is distinct from changing its coding
instructions.

Format references: [Claude manifest](https://code.claude.com/docs/en/plugins-reference),
[Claude marketplaces](https://code.claude.com/docs/en/plugin-marketplaces),
and [OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins).

## License

MIT. The license and attribution ship with the plugin.
