# Repository guidance

Reply to the owner in Korean. Keep the shared skill and package metadata in English.

The canonical skill is `plugins/karpathy-regula/skills/coding-guidelines/SKILL.md`.
Claude and Codex load this same file. Keep the portable, Claude, and Codex plugin
manifests aligned on identity and version, and keep both marketplace paths pointed
at that plugin directory.

The skill body is the reviewed Regula revision. A body change needs an explicit
request and an updated provenance record; do not imply an unmeasured improvement.
The name, frontmatter, and host metadata may change without rewriting its body.

Checks:

```sh
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python tools/package.py --check
claude plugin validate --strict plugins/karpathy-regula
claude plugin validate --strict .
```

Package with `python tools/package.py`; inspect the archive before publishing.
The archive is reproducible: rebuilding a release tag must give the SHA-256 in
that release's `SHA256SUMS.txt`. Do not edit installed plugin caches or change user
installation settings as part of a repository edit.

`docs/research/karpathy-regula-2026-11-08/` mirrors the research record in
`ajitta/dialectic-skills` at the commit named in `docs/provenance.json`; keep it
byte-identical to that commit. Paths inside it such as `docs/spec.md`,
`docs/probes.md` and `AGENTS.md` refer to that repository, while the probe rules
below also apply here.

## Probes and evals (owner, 2026-11-04)

- Before a probe or eval batch, write the plan: cells × runs × engines = total, and
  the decision it informs. Ask the owner first when the total is over 30 runs.
- Runs per cell: 1 to confirm unchanged or expected behaviour, 2 for a changed
  behaviour. Raise to 5 only when results disagree with the expectation or between
  arms or engines; use 10 or more only for an arm-against-arm figure the release
  notes will quote.
- Read results while the batch runs and stop it once the answer is clear.
- Form-only edits are checked by one independent review instead of runs.
