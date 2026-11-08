# Packaging validation

Recorded on 2026-11-08. These are package/discovery checks, not new behavioral evals.

| Check | Result |
|---|---|
| Python package tests | 4 passed: single shared skill/hidden manifests, version drift rejection, path escape rejection, and unreviewed body-edit rejection |
| `python tools/package.py --check` | Passed JSON/YAML, identity/version, catalog path, body hash, license, and attribution checks |
| ZIP inspection | One plugin, one skill, hidden manifests, LICENSE and NOTICE; no marketplace catalog inside the archive |
| Claude Code 2.1.319 | Plugin, marketplace, and skill-component validation passed with `--strict` |
| Codex CLI 0.167.0 | In a temporary isolated state directory, registered the local marketplace, discovered 0.1.0, installed it, and listed it as installed/enabled |

The Codex probe used no user credentials and removed its temporary installation
state afterward. It did not alter the owner's actual installed plugins.

Claude's optional directory-listing checks reported a missing icon. That advisory
did not change the native validation result. This repository/ZIP distribution
does not claim submission to either vendor's public plugin directory.

The coding instruction body is byte-identical to the reviewed revision's body;
only skill identity and frontmatter metadata changed. The historical study is
linked from provenance and NOTICE. No new model turn was run to evaluate the
renamed plugin invocation or to establish a behavioral improvement.
