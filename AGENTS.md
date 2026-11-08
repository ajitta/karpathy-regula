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
Do not edit installed plugin caches or change user installation settings as part
of a repository edit.
