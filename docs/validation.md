# Packaging validation

These are package, install and loading checks, not behavioral evaluations of the
coding guidelines.

## 0.1.1 (2026-11-09)

| Check | Result |
|---|---|
| Python package tests | 9 passed: one shared skill with hidden manifests, archive entries in POSIX path order, reproducible archive, version drift rejection, the same rejection under `python -O`, an error line for a missing manifest key, rejection of an unexpected plugin file, catalog path escape rejection, and unreviewed body-edit rejection |
| `python tools/package.py --check` | Passed |
| Reproducible ZIP | The same SHA-256 from Python 3.12 and 3.14, and after changing every file's modification time; entries are ordered by POSIX path so a Windows build uses the same order |
| Claude Code 2.1.314 | Plugin and marketplace validation passed with `--strict` (missing-icon advisory only). Installed from `ajitta/karpathy-regula` in an isolated config directory and listed as enabled |
| Codex CLI 0.166.0 | Installed from `ajitta/karpathy-regula` in an isolated state directory and listed as installed and enabled |
| Named invocation | Claude Code: `/karpathy-regula:coding-guidelines` with `--plugin-dir` loaded the body in 2 of 2 runs (Haiku; one run quoted a sentence that exists only in the revision). Codex: `$karpathy-regula:coding-guidelines` read the installed plugin's `SKILL.md` in 1 of 1 run (`gpt-6.1-sol`, medium effort) |
| Loading without the name | One coding request that did not name the skill: Codex read the skill in 2 of 2 runs (`gpt-6.1-sol`, medium effort); Claude Code with its default model listed it but loaded it in 0 of 2 runs |

Install and loading rows used 0.1.0 (from `main` and a `--plugin-dir` copy); its
skill body and description are identical to 0.1.1. The 0.1.1 install is rechecked
from GitHub after merge.

The isolated directories were deleted afterward, and the credentials copied into
the Codex probe were removed after its runs. The owner's installed plugins and
settings were not changed.

The skill body is byte-identical to the reviewed revision's body; 0.1.1 changes the
skill's display name in `agents/openai.yaml`, `NOTICE.md`, version fields,
documentation, and the packaging tool.

## 0.1.0 (2026-11-08)

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

The historical study is available in the
[local research archive](research/karpathy-regula-2026-11-08/README.md) and linked
from provenance and NOTICE.
